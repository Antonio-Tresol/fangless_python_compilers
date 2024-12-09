#ifndef DICT_HPP
#define DICT_HPP

#include <map>

#include "Iterable.hpp"
#include "List.hpp"
#include "Object.hpp"
#include "None.hpp"

class Dictionary : public Object {
 private:
  std::map<std::shared_ptr<Object>, std::shared_ptr<Object>, ObjectComparator>
      elements_;

 public:
  Dictionary() = default;

  std::string type() const override { return "dict"; }

  static std::shared_ptr<Dictionary> spawn() {
    return std::make_shared<Dictionary>();
  }

  static std::shared_ptr<Dictionary> spawn(
      std::initializer_list<
          std::pair<std::shared_ptr<Object>, std::shared_ptr<Object>>>
          init) {
    auto result = std::make_shared<Dictionary>();
    for (const auto& [key, value] : init) {
      result->elements_[key] = value;
    }
    return result;
  }

  std::string toString() const override {
    std::string result = "{";
    bool first = true;
    for (const auto& [key, value] : elements_) {
      if (!first) result += ", ";
      result += key->toString() + ": " + value->toString();
      first = false;
    }
    return result + "}";
  }

  template<TIterable TType>
  std::shared_ptr<Dictionary> fromkeys(const std::shared_ptr<TType>& elements,
    const std::shared_ptr<Object>& value = None::spawn()) {
    std::shared_ptr<Dictionary> result = Dictionary::spawn();
    for (auto element : *elements) {
      result->set(element, value);
    }

    return result;
  }

  template<TIterable TType>
  std::shared_ptr<None> update(const std::shared_ptr<TType>& iterable) {
    for (auto& placeholder : *iterable) {
      auto tuple = placeholder->asTuple();
      set((*tuple)[Number::spawn(0)], (*tuple)[Number::spawn(1)]);
    }

    return None::spawn();
  }

  std::shared_ptr<None> update(
    const std::shared_ptr<Dictionary>& updateElements) {
    for (auto& [key, value] : *updateElements) {
      set(key, value);
    }

    return None::spawn();
  }

  std::shared_ptr<None> update() {
    return None::spawn();
  }

  bool equals(const Object& other) const override {
    if (auto* mapObj = dynamic_cast<const Dictionary*>(&other)) {
      return elements_ == mapObj->elements_;
    }
    return false;
  }

  bool equals(const std::shared_ptr<Object>& other) const {
    return equals(*other);
  }

  friend bool operator==(const Dictionary& lhs, const Dictionary& rhs) {
    return lhs.equals(rhs);
  }

  friend bool operator==(const Dictionary& lhs, const Object& rhs) {
    return lhs.equals(rhs);
  }

  friend bool operator==(const Object& lhs, const Dictionary& rhs) {
    return rhs.equals(lhs);
  }

  friend bool operator==(const std::shared_ptr<Dictionary>& lhs,
                         const std::shared_ptr<Dictionary>& rhs) {
    return lhs->equals(*rhs);
  }

  friend bool operator==(const std::shared_ptr<Dictionary>& lhs,
                         const std::shared_ptr<Object>& rhs) {
    return lhs->equals(*rhs);
  }

  friend bool operator==(const std::shared_ptr<Object>& lhs,
                         const std::shared_ptr<Dictionary>& rhs) {
    return rhs->equals(lhs);
  }

  std::strong_ordering compare(const Object& other) const override {
    if (type() != other.type()) {
      return Object::compare(other);
    }

    const auto* other_dict = static_cast<const Dictionary*>(&other);

    if (auto cmp = elements_.size() <=> other_dict->elements_.size();
        cmp != std::strong_ordering::equal) {
      return cmp;
    }

    auto it1 = elements_.begin();
    auto it2 = other_dict->elements_.begin();

    while (it1 != elements_.end()) {
      if (auto key_cmp = (*it1->first) <=> (*it2->first);
          key_cmp != std::strong_ordering::equal) {
        return key_cmp;
      }
      if (auto value_cmp = (*it1->second) <=> (*it2->second);
          value_cmp != std::strong_ordering::equal) {
        return value_cmp;
      }
      ++it1;
      ++it2;
    }
    return std::strong_ordering::equal;
  }

  size_t hash() const override {
    throw std::runtime_error("unhashable type: 'dict'");
  }

  bool toBool() const override { return !elements_.empty(); }

  bool operator!() const { return elements_.empty(); }
  friend bool operator!(const std::shared_ptr<Dictionary>& obj) {
    return obj->operator!();
  }

  bool isInstance(const std::string& type) const override {
    return type == "dict" || type == "object";
  }

  void set(std::shared_ptr<Object> key, std::shared_ptr<Object> value) {
    if (!key->hash()) {
      throw std::runtime_error("unhashable type: '" + key->type() + "'");
    }
    elements_[key] = value;
  }

  std::shared_ptr<Object> get(std::shared_ptr<Object> key,
    std::shared_ptr<Object> defaultVal = None::spawn()) const {
    auto it = elements_.find(key);

    if (it == elements_.end()) {
      return defaultVal;
    }

    return it->second;
  }

  std::shared_ptr<Object> getDefault(
      std::shared_ptr<Object> key, std::shared_ptr<Object> defaultValue) const {
    auto it = elements_.find(key);
    return it != elements_.end() ? it->second : defaultValue;
  }

  void remove(std::shared_ptr<Object> key) {
    if (elements_.erase(key) == 0) {
      throw std::runtime_error("KeyError: " + key->toString());
    }
  }

  bool contains(std::shared_ptr<Object> key) const {
    return elements_.find(key) != elements_.end();
  }

  void clear() { elements_.clear(); }

  std::shared_ptr<Dictionary> copy() {
    auto copyElement = std::make_shared<Dictionary>();
    for (auto [key, val] : elements_) {
      copyElement->set(key, val);
    }
    return copyElement;
  }

  std::shared_ptr<Object> pop (const std::shared_ptr<Object>& key,
    const std::shared_ptr<Object>& defaultVal = None::spawn()) {
    auto it = elements_.find(key);

    if (it == elements_.end()) {
      if (defaultVal->isNone()) {
        throw std::runtime_error(
          "Dictionary::pop: element not found and default not given");
      }
      return defaultVal;
    }
    
    auto result = (*it).second;
    elements_.erase(it);

    return result;
  }

  std::shared_ptr<List> popitem () {
    if (elements_.empty()) {
      throw std::runtime_error("No item to pop");
    }

    auto it = elements_.rbegin();
    if (it == elements_.rend()) {
      throw std::runtime_error("Item could not be popped off successfully");
    }
    
    auto [key, value] = *it;

    this->remove(key);
    
    return List::spawn({key, value});
  }

  std::shared_ptr<Object> setdefault(std::shared_ptr<Object> key,
    std::shared_ptr<Object> defaultValue = None::spawn()) {
    auto it = elements_.find(key);

    if (it != elements_.end()) {
      auto [_, element] = *it;
      return element;
    }

    set(key, defaultValue);

    return elements_[key];
  }

  std::shared_ptr<Number> len() const {
    return Number::spawn(static_cast<int64_t>(elements_.size()));
  }

  std::shared_ptr<List> keys() const {
    auto result = std::make_shared<List>();
    for (const auto& [key, _] : elements_) {
      result->append(key);
    }
    return result;
  }

  std::shared_ptr<List> values() const {
    auto result = std::make_shared<List>();
    for (const auto& [_, value] : elements_) {
      result->append(value);
    }
    return result;
  }

  std::shared_ptr<List> items() const {
    auto result = std::make_shared<List>();
    for (const auto& [key, value] : elements_) {
      auto pair = std::make_shared<List>();
      pair->append(key);
      pair->append(value);
      result->append(pair);
    }
    return result;
  }

  std::shared_ptr<Object> getAttr(const std::string& name) const override {
    throw std::runtime_error("'dict' object has no attribute '" + name + "'");
  }

  void setAttr(const std::string&,
               std::shared_ptr<Object>) override {
    throw std::runtime_error("'dict' object attributes are read-only");
  }

  using MapType = std::map<std::shared_ptr<Object>, std::shared_ptr<Object>, ObjectComparator>;

  MapType::iterator begin() { return elements_.begin(); }
  MapType::iterator end() { return elements_.end(); }
  MapType::const_iterator begin() const { return elements_.begin(); }
  MapType::const_iterator end() const { return elements_.end(); }

  MapType::reverse_iterator rbegin() { return elements_.rbegin(); }
  MapType::reverse_iterator rend() { return elements_.rend(); }
  MapType::const_reverse_iterator rbegin() const { return elements_.rbegin(); }
  MapType::const_reverse_iterator rend() const { return elements_.rend(); }

  std::shared_ptr<Object>& operator[](const std::shared_ptr<Object> key) {
    return elements_[key];
  }

  const std::shared_ptr<Object>& operator[](
    const std::shared_ptr<Object> key) const {
    auto it = elements_.find(key);
    if (it == elements_.end()) {
      throw std::runtime_error("KeyError: " + key->toString());
    }
    return it->second;
  }

  std::shared_ptr<Dictionary> operator|(const Dictionary& other) const {
    auto result = std::make_shared<Dictionary>(*this);
    for (const auto& [key, value] : other.elements_) {
      result->elements_[key] = value;
    }
    return result;
  }

  Dictionary& operator|=(const Dictionary& other) {
    for (const auto& [key, value] : other.elements_) {
      elements_[key] = value;
    }
    return *this;
  }

  Dictionary(const Dictionary& other) : elements_(other.elements_) {}

  Dictionary& operator=(const Dictionary& other) {
    if (this != &other) {
      elements_ = other.elements_;
    }
    return *this;
  }

  friend std::ostream& operator<<(std::ostream& os,
                                  const std::shared_ptr<Dictionary>& obj) {
    return os << *obj;
  }
};

#endif  // DICTIONARY_HPP