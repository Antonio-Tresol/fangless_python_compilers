#ifndef DICT_HPP
#define DICT_HPP

#include <map>

#include "Iterable.hpp"
#include "List.hpp"
#include "Object.hpp"

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

  bool equals(const Object& other) const override {
    if (auto* mapObj = dynamic_cast<const Dictionary*>(&other)) {
      return elements_ == mapObj->elements_;
    }
    return false;
  }

  size_t hash() const override {
    throw std::runtime_error("unhashable type: 'dict'");
  }

  bool toBool() const override { return !elements_.empty(); }

  bool isinstance(const std::string& type) const override {
    return type == "dict" || type == "object";
  }

  void set(std::shared_ptr<Object> key, std::shared_ptr<Object> value) {
    if (!key->hash()) {
      throw std::runtime_error("unhashable type: '" + key->type() + "'");
    }
    elements_[key] = value;
  }

  std::shared_ptr<Object> get(std::shared_ptr<Object> key) const {
    auto it = elements_.find(key);

    if (it == elements_.end()) {
      throw std::runtime_error("KeyError: " + key->toString());
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

  size_t size() const { return elements_.size(); }

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

  void setAttr(const std::string& name,
               std::shared_ptr<Object> value) override {
    throw std::runtime_error("'dict' object attributes are read-only");
  }

  auto begin() { return elements_.begin(); }
  auto end() { return elements_.end(); }
  auto begin() const { return elements_.begin(); }
  auto end() const { return elements_.end(); }

  std::shared_ptr<Object>& operator[](std::shared_ptr<Object> key) {
    return elements_[key];
  }

  std::shared_ptr<Object> operator[](std::shared_ptr<Object> key) const {
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

  bool operator==(const Dictionary& other) const {
    return elements_ == other.elements_;
  }

  bool operator!=(const Dictionary& other) const { return !(*this == other); }

  Dictionary(const Dictionary& other) : elements_(other.elements_) {}

  Dictionary& operator=(const Dictionary& other) {
    if (this != &other) {
      elements_ = other.elements_;
    }
    return *this;
  }
};

#endif  // DICTIONARY_HPP