#ifndef LIST_HPP
#define LIST_HPP

#include <algorithm>
#include <climits>
#include <ranges>
#include <stdexcept>
#include <vector>

#include "Number.hpp"
#include "Object.hpp"
#include "Slice.hpp"
#include "Tuple.hpp"

using std::views::iota;

class List : public Object {
  std::vector<std::shared_ptr<Object>> elements_;

 public:
  List() = default;

  List(const List& other) : elements_(other.elements_) {}

  List(std::initializer_list<std::shared_ptr<Object>> init) : elements_(init) {}

  static std::shared_ptr<List> spawn() { return std::make_shared<List>(); }

  static std::shared_ptr<List> spawn(
      std::initializer_list<std::shared_ptr<Object>> init) {
    return std::make_shared<List>(init);
  }

  inline std::vector<std::shared_ptr<Object>>& getElements() {
    return elements_;
  }

  inline const std::vector<std::shared_ptr<Object>>& getElements() const {
    return elements_;
  }

  std::string type() const override { return "list"; }

  std::string toString() const override {
    std::string result = "[";
    for (size_t i = 0; i < elements_.size(); ++i) {
      result += elements_[i]->toString();
      if (i < elements_.size() - 1) result += ", ";
    }
    return result + "]";
  }

  bool hasSingleType() const {
    if (elements_.size() == 0) return true;

    std::string type = elements_[0]->type();
    for (auto i : iota(1, static_cast<int>(elements_.size()))) {
      if (elements_[i]->type() != type) {
        return false;
      }
    }

    return true;
  }

  std::shared_ptr<Tuple> asTuple() const override {
    return std::make_shared<Tuple>(elements_);
  }

  bool equals(const Object& other) const override {
    if (auto* listObj = dynamic_cast<const List*>(&other)) {
      if (elements_.size() != listObj->elements_.size()) return false;

      for (auto i : iota(0, static_cast<int32_t>(elements_.size()))) {
        if (*elements_[i] != *listObj->elements_[i]) return false;
      }

      return true;
    }
  
    return false;
  }

  bool equals(std::shared_ptr<Object> other) const {
    if (auto* listObj = dynamic_cast<List*>(other.get())) {
      return equals(*listObj);
    }
    return false;
  }

  bool equals(const std::shared_ptr<List>& other) const {
    return equals(*other);
  }

  friend bool operator==(const List& lhs, const List& rhs) {
    return lhs.equals(rhs);
  }

  friend bool operator==(std::shared_ptr<List> lhs, std::shared_ptr<List> rhs) {
    return lhs->equals(*rhs);
  }

  friend bool operator==(std::shared_ptr<List> lhs, const List& rhs) {
    return lhs->equals(rhs);
  }

  friend bool operator==(const List& lhs, std::shared_ptr<List> rhs) {
    return rhs->equals(lhs);
  }

  friend bool operator==(const std::shared_ptr<Object>& lhs,
                         const std::shared_ptr<List>& rhs) {
    return rhs->equals(lhs);
  }

  friend bool operator==(const std::shared_ptr<List>& lhs,
                         const std::shared_ptr<Object>& rhs) {
    return lhs->equals(rhs);
  }

  std::strong_ordering compare(const Object& other) const override {
    // If types differ, fall back to base comparison
    if (type() != other.type()) {
      return Object::compare(other);
    }

    // Safe downcast since we checked types
    const auto* other_list = static_cast<const List*>(&other);

    // Compare element by element using toString()
    size_t min_size = std::min(elements_.size(), other_list->elements_.size());

    for (size_t i = 0; i < min_size; ++i) {
      // Use string comparison instead of <=>
      auto lhs = elements_[i]->toString();
      auto rhs = other_list->elements_[i]->toString();
      if (lhs < rhs) return std::strong_ordering::less;
      if (lhs > rhs) return std::strong_ordering::greater;
    }

    // If all elements up to min_size are equal, shorter list is less
    return elements_.size() <=> other_list->elements_.size();
  }

  size_t hash() const override {
    throw std::runtime_error("unhashable type: 'list'");
  }

  bool toBool() const override { return !elements_.empty(); }
  bool operator!() const { return elements_.empty(); }
  friend bool operator!(const std::shared_ptr<List>& list) {
    return list->operator!();
  }

  bool isInstance(const std::string& type) const override {
    return type == "list" || type == "object";
  }

  // List specific methods
  void append(std::shared_ptr<Object> item) { elements_.push_back(item); }

  void clear() { elements_.clear(); }

  void extend(const List& other) {
    elements_.insert(elements_.end(), other.elements_.begin(),
                     other.elements_.end());
  }

  void extend(std::shared_ptr<List> other) {
    elements_.insert(elements_.end(), other->elements_.begin(),
                     other->elements_.end());
  }

  std::shared_ptr<Number> index(std::shared_ptr<Object> object) const {
    for (auto i : iota(0, static_cast<int>(elements_.size()))) {
      if (*elements_[i] == *object) {
        return std::make_shared<Number>(i);
      }
    }
    throw std::runtime_error(object->toString() + " not in list");
  }

  std::shared_ptr<List> copy() {
    std::shared_ptr<List> copyList = std::make_shared<List>();
    for (auto&& element : elements_) {
      copyList->append(element);
    }

    return copyList;
  }

  void insert(std::shared_ptr<Number> index, std::shared_ptr<Object> object) {
    elements_.insert(elements_.begin() + index->getInt(), object);
  }

  void insert(const Number& index, std::shared_ptr<Object> object) {
    elements_.insert(elements_.begin() + index.getInt(), object);
  }

  std::shared_ptr<Object> pop(std::shared_ptr<Number> index) {
    if (elements_.empty()) {
      throw std::runtime_error("pop from empty list");
    }
    int indexNum = index->getInt();
    if (indexNum < 0) indexNum += elements_.size();
    if (indexNum < 0 || static_cast<size_t>(indexNum) >= elements_.size()) {
      throw std::out_of_range("list index out of range");
    }

    auto item = elements_[indexNum];
    elements_.erase(elements_.begin() + indexNum);
    return item;
  }

  std::shared_ptr<Object> pop(const Number& index = Number(-1)) {
    if (elements_.empty()) {
      throw std::runtime_error("pop from empty list");
    }
    int indexNum = index.getInt();
    if (indexNum < 0) indexNum += elements_.size();
    if (indexNum < 0 || static_cast<size_t>(indexNum) >= elements_.size()) {
      throw std::out_of_range("list index out of range");
    }

    auto item = elements_[indexNum];
    elements_.erase(elements_.begin() + indexNum);
    return item;
  }

  void remove(std::shared_ptr<Object> object) {
    auto it = std::find_if(elements_.begin(), elements_.end(),
                           [&object](const std::shared_ptr<Object>& element) {
                             return element->equals(*object);
                           });

    if (it != elements_.end()) {
      elements_.erase(it);
    } else {
      throw std::runtime_error(object->toString() + " not in list");
    }
  }

  void reverse() { std::reverse(elements_.begin(), elements_.end()); }

  void sort() {
    static constexpr auto sortFunc = [](std::shared_ptr<Object> i,
                                        std::shared_ptr<Object> j) {
      return *i < *j;
    };

    if (!hasSingleType()) {
      throw std::runtime_error(
          "Sort not supported on lists with more than one type");
    }

    std::sort(elements_.begin(), elements_.end(), sortFunc);
  }

  std::shared_ptr<Number> count() const {
    return Number::spawn(static_cast<int64_t>(elements_.size()));
  }

  std::shared_ptr<Number> len() const {
    return Number::spawn(static_cast<int64_t>(elements_.size()));
  }

  // Attribute access
  std::shared_ptr<Object> getAttr(const std::string& name) const override {
    throw std::runtime_error("'list' object has no attribute '" + name + "'");
  }

  void setAttr(const std::string& name,
               std::shared_ptr<Object> value) override {
    throw std::runtime_error("'list' object has no attributes");
  }

  // Iterator support
  auto begin() { return elements_.begin(); }
  auto end() { return elements_.end(); }
  auto begin() const { return elements_.begin(); }
  auto end() const { return elements_.end(); }

  auto rbegin() { return elements_.rbegin(); }
  auto rend() { return elements_.rend(); }
  auto rbegin() const { return elements_.rbegin(); }
  auto rend() const { return elements_.rend(); }

  std::shared_ptr<Object> at(std::shared_ptr<Number> index) const {
    int indexNum = index->getInt();
    if (indexNum < 0) indexNum += elements_.size();
    if (indexNum < 0 || static_cast<size_t>(indexNum) >= elements_.size()) {
      throw std::out_of_range("List index out of range");
    }
    return elements_[indexNum];
  }

  std::shared_ptr<Object> at(const Number& index) const {
    int indexNum = index.getInt();
    if (indexNum < 0) indexNum += elements_.size();
    if (indexNum < 0 || static_cast<size_t>(indexNum) >= elements_.size()) {
      throw std::out_of_range("List index out of range");
    }
    return elements_[indexNum];
  }

  auto& operator[](const Number& pos) const {
    int index = pos.getInt();
    int actual_index = index;
    if (index < 0) actual_index += elements_.size();

    if (actual_index < 0 || actual_index >= static_cast<int>(elements_.size())) {
      throw std::out_of_range("List index out of range");
    }
    return elements_[actual_index];
  }

  auto& operator[](const std::shared_ptr<Number>& pos) const {
    int index = pos->getInt();
    int actual_index = index;
    if (index < 0) actual_index += elements_.size();

    if (actual_index < 0 || actual_index >= static_cast<int>(elements_.size())) {
      throw std::out_of_range("List index out of range");
    }
    return elements_[actual_index];
  }

  auto& operator[](const std::shared_ptr<Number>& pos) {
    int index = pos->getInt();
    int actual_index = index;
    if (index < 0) actual_index += elements_.size();

    if (actual_index < 0 || actual_index >= static_cast<int>(elements_.size())) {
      throw std::out_of_range("List index out of range");
    }
    return elements_[actual_index];
  }

  std::shared_ptr<List> operator[](const Slice& slice) const {
    int start = slice.start == INT_MAX ? 0 : slice.start;
    int end = slice.end == INT_MAX ? elements_.size() : slice.end;
    int step = slice.step == 0 ?
      throw std::invalid_argument("Step cannot be zero") : slice.step;

    if (start < 0) start += elements_.size();
    if (end < 0) end += elements_.size();

    start = std::clamp(start, 0, static_cast<int>(elements_.size()));
    end = std::clamp(end, 0, static_cast<int>(elements_.size()));

    auto result = std::make_shared<List>();

    if (step > 0) {
        for (int i = start; i < end; i += step) {
            result->append(elements_[i]);
        }
    } else {
        for (int i = start; i > end; i += step) {
            result->append(elements_[i]);
        }
    }

    return result;
  }

  std::shared_ptr<List> slice(const Slice& slice) {
    return this->operator[](slice);
  }

  std::shared_ptr<List> slice(std::shared_ptr<Slice> slice) {
    return this->operator[](*slice);
  }

  // List arithmetic and comparison operators
  std::shared_ptr<List> operator+(const List& other) const {
    auto result = std::make_shared<List>();
    result->elements_ = elements_;
    result->elements_.insert(result->elements_.end(), other.elements_.begin(),
                             other.elements_.end());
    return result;
  }

  std::shared_ptr<List> operator*(const Number& number) const {
    int n = number.getInt();
    if (n <= 0) return std::make_shared<List>();

    auto result = std::make_shared<List>();
    for (int i = 0; i < n; ++i) {
      result->elements_.insert(result->elements_.end(), elements_.begin(),
                               elements_.end());
    }
    return result;
  }

  std::shared_ptr<List> operator*(std::shared_ptr<Number> number) const {
    int n = number->getInt();
    if (n <= 0) return std::make_shared<List>();

    auto result = std::make_shared<List>();
    for (int i = 0; i < n; ++i) {
      result->elements_.insert(result->elements_.end(), elements_.begin(),
                               elements_.end());
    }
    return result;
  }

  std::shared_ptr<List> operator+=(const List& other) {
    elements_.insert(elements_.end(), other.elements_.begin(),
                     other.elements_.end());
    return std::shared_ptr<List>(this);
  }

  std::shared_ptr<List> operator*=(const Number& number) {
    int n = number.getInt();
    if (n <= 0) {
      elements_.clear();
    } else {
      auto original = elements_;
      for (int i = 1; i < n; ++i) {
        elements_.insert(elements_.end(), original.begin(), original.end());
      }
    }
    return std::shared_ptr<List>(this);
  }

  std::shared_ptr<List> operator*=(std::shared_ptr<Number> number) {
    int n = number->getInt();
    if (n <= 0) {
      elements_.clear();
    } else {
      auto original = elements_;
      for (int i = 1; i < n; ++i) {
        elements_.insert(elements_.end(), original.begin(), original.end());
      }
    }
    return std::shared_ptr<List>(this);
  }

  List& operator=(const List& other) {
    if (this != &other) {
      elements_ = other.elements_;
    }
    return *this;
  }

  friend std::ostream& operator<<(std::ostream& os,
                                  const std::shared_ptr<List>& obj) {
    return os << *obj;
  }

  friend std::shared_ptr<List> operator+(const std::shared_ptr<List>& a,
                                         const std::shared_ptr<List>& b) {
    return *a + *b;
  }

  friend std::shared_ptr<List> operator*(const std::shared_ptr<List>& a,
                                         const std::shared_ptr<Number>& b) {
    return *a * *b;
  }
};

#endif  // LIST_HPP