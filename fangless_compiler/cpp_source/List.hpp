#ifndef LIST_HPP
#define LIST_HPP

#include <algorithm>
#include <climits>
#include <stdexcept>
#include <vector>
#include <ranges>
#include "Object.hpp"
#include "Slice.hpp"

using std::views::iota;
class List : public Object {
  std::vector<std::shared_ptr<Object>> elements_;

 public:
  List() = default;
  List(std::initializer_list<std::shared_ptr<Object>> init) : elements_(init) {}

  std::string type() const override { return "list"; }

  std::string toString() const override {
    std::string result = "[";
    for (size_t i = 0; i < elements_.size(); ++i) {
      result += elements_[i]->toString();
      if (i < elements_.size() - 1) result += ", ";
    }
    return result + "]";
  }

  bool equals(const Object& other) const override {
    if (auto* listObj = dynamic_cast<const List*>(&other)) {
      if (elements_.size() != listObj->elements_.size()) return false;

      for (auto i: iota(0, static_cast<int32_t>(elements_.size()))) {
        if (elements_[i] != listObj->elements_[i]) return false;
      }
      
      return true;
    }

    return false;
  }

  size_t hash() const override {
    throw std::runtime_error("unhashable type: 'list'");
  }

  bool toBool() const override { return !elements_.empty(); }

  bool isinstance(const std::string& type) const override {
    return type == "list" || type == "object";
  }

  // List specific methods
  void append(std::shared_ptr<Object> item) { elements_.push_back(item); }

  void extend(const List& other) {
    elements_.insert(elements_.end(), other.elements_.begin(),
                     other.elements_.end());
  }

  std::shared_ptr<Object> pop(int index = -1) {
    if (elements_.empty()) {
      throw std::runtime_error("pop from empty list");
    }

    if (index < 0) index += elements_.size();
    if (index < 0 || size_t(index) >= elements_.size()) {
      throw std::out_of_range("list index out of range");
    }

    auto item = elements_[index];
    elements_.erase(elements_.begin() + index);
    return item;
  }

  void reverse() { std::reverse(elements_.begin(), elements_.end()); }

  size_t size() const { return elements_.size(); }

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

  std::shared_ptr<List> operator[](const Slice& slice) const {
    int start = slice.start;
    int end = slice.end;

    if (start == INT_MAX) start = 0;
    if (end == INT_MAX) end = elements_.size();

    if (start < 0) start += elements_.size();
    if (end < 0) end += elements_.size();

    start = std::clamp(start, 0, static_cast<int>(elements_.size()));
    end = std::clamp(end, 0, static_cast<int>(elements_.size()));

    auto result = std::make_shared<List>();

    for (int i = start; i < end; ++i) {
      result->append(elements_[i]);
    }

    return result;
  }

  std::shared_ptr<List> operator+(const List& other) const {
    auto result = std::make_shared<List>();
    result->elements_ = elements_;
    result->elements_.insert(result->elements_.end(), other.elements_.begin(),
                             other.elements_.end());
    return result;
  }

  std::shared_ptr<List> operator*(int n) const {
    if (n <= 0) return std::make_shared<List>();

    auto result = std::make_shared<List>();
    for (int i = 0; i < n; ++i) {
      result->elements_.insert(result->elements_.end(), elements_.begin(),
                               elements_.end());
    }
    return result;
  }

  List& operator+=(const List& other) {
    elements_.insert(elements_.end(), other.elements_.begin(),
                     other.elements_.end());
    return *this;
  }

  List& operator*=(int n) {
    if (n <= 0) {
      elements_.clear();
    } else {
      auto original = elements_;
      for (int i = 1; i < n; ++i) {
        elements_.insert(elements_.end(), original.begin(), original.end());
      }
    }
    return *this;
  }

  bool operator<(const List& other) const {
    return std::lexicographical_compare(
        elements_.begin(), elements_.end(), other.elements_.begin(),
        other.elements_.end(), [](const auto& a, const auto& b) {
          return a->toString() < b->toString();
        });
  }

  bool operator>(const List& other) const { return other < *this; }

  bool operator<=(const List& other) const { return !(other < *this); }

  bool operator>=(const List& other) const { return !(*this < other); }

  std::shared_ptr<Object> operator[](int index) const {
    if (index < 0) index += elements_.size();
    if (index < 0 || size_t(index) >= elements_.size()) {
      throw std::out_of_range("list index out of range");
    }
    return elements_[index];
  }

  std::shared_ptr<Object>& operator[](int index) {
    if (index < 0) index += elements_.size();
    if (index < 0 || size_t(index) >= elements_.size()) {
      throw std::out_of_range("list index out of range");
    }
    return elements_[index];
  }

  List& operator=(const List& other) {
    if (this != &other) {
      elements_ = other.elements_;
    }
    return *this;
  }

  List(const List& other) : elements_(other.elements_) {}
};

#endif  // LIST_HPP