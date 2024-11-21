#ifndef STRING_HPP
#define STRING_HPP

#include <algorithm>
#include <cctype>
#include <climits>
#include <compare>
#include <string>

#include "Number.hpp"
#include "Object.hpp"
#include "Slice.hpp"

class String : public Object {
  std::string value_;

 public:
  explicit String(const std::string& value) : value_(value) {}

  std::string type() const override { return "str"; }

  std::string toString() const override { return value_; }

  bool equals(const Object& other) const override {
    if (auto* strObj = dynamic_cast<const String*>(&other)) {
      return value_ == strObj->value_;
    }
    return false;
  }

  size_t hash() const override { return std::hash<std::string>{}(value_); }

  bool toBool() const override { return !value_.empty(); }

  bool isinstance(const std::string& type) const override {
    return type == "str" || type == "object";
  }

  // Python string methods
  std::shared_ptr<String> upper() const {
    std::string result = value_;
    std::transform(result.begin(), result.end(), result.begin(), ::toupper);
    return std::make_shared<String>(result);
  }

  std::shared_ptr<String> lower() const {
    std::string result = value_;
    std::transform(result.begin(), result.end(), result.begin(), ::tolower);
    return std::make_shared<String>(result);
  }

  std::shared_ptr<String> strip() const {
    auto start = value_.find_first_not_of(" \t\n\r");
    auto end = value_.find_last_not_of(" \t\n\r");
    if (start == std::string::npos) return std::make_shared<String>("");
    return std::make_shared<String>(value_.substr(start, end - start + 1));
  }

  bool startswith(const String& prefix) const {
    return value_.substr(0, prefix.value_.length()) == prefix.value_;
  }

  bool endswith(const String& suffix) const {
    if (suffix.value_.length() > value_.length()) return false;
    return value_.substr(value_.length() - suffix.value_.length()) ==
           suffix.value_;
  }

  std::shared_ptr<String> replace(const String& old_str,
                                  const String& new_str) const {
    std::string result = value_;
    size_t pos = 0;
    while ((pos = result.find(old_str.value_, pos)) != std::string::npos) {
      result.replace(pos, old_str.value_.length(), new_str.value_);
      pos += new_str.value_.length();
    }
    return std::make_shared<String>(result);
  }

  std::shared_ptr<String> operator+(const String& other) const {
    return std::make_shared<String>(value_ + other.value_);
  }

  std::shared_ptr<String> operator*(int n) const {
    std::string result;
    for (int i = 0; i < n; ++i) {
      result += value_;
    }
    return std::make_shared<String>(result);
  }

  // Attribute access
  std::shared_ptr<Object> getAttr(const std::string& name) const override {
    if (name == "upper") return std::make_shared<String>(upper()->toString());
    if (name == "lower") return std::make_shared<String>(lower()->toString());
    if (name == "strip") return std::make_shared<String>(strip()->toString());
    throw std::runtime_error("'str' object has no attribute '" + name + "'");
  }

  void setAttr(const std::string& name,
               std::shared_ptr<Object> value) override {
    throw std::runtime_error("'str' object attributes are read-only");
  }

  std::strong_ordering compare(const Object& other) const override {
    auto* strObj = dynamic_cast<const String*>(&other);
    if (strObj == nullptr) return Object::compare(other);
    auto& otherRef = *strObj;

    return value_ <=> otherRef.value_;
  }

  char operator[](int index) const {
    int actual_index = index;
    if (index < 0) actual_index += value_.size();

    if (actual_index < 0 || actual_index >= static_cast<int>(value_.size())) {
      throw std::out_of_range("string index out of range");
    }
    return value_[actual_index];
  }

  std::shared_ptr<String> operator[](const Slice& slice) const {
    int start = slice.start;
    int end = slice.end;

    if (start == INT_MAX) start = 0;
    if (end == INT_MAX) end = value_.size();

    if (start < 0) start += value_.size();
    if (end < 0) end += value_.size();

    start = std::clamp(start, 0, static_cast<int>(value_.size()));
    end = std::clamp(end, 0, static_cast<int>(value_.size()));

    if (start >= end) {
      return std::make_shared<String>("");
    }

    return std::make_shared<String>(value_.substr(start, end - start));
  }
  auto begin() { return value_.begin(); }
  auto end() { return value_.end(); }
  auto begin() const { return value_.begin(); }
  auto end() const { return value_.end(); }

  String& operator=(const String& other) {
    if (this != &other) {
      value_ = other.value_;
    }
    return *this;
  }

  String(const String& other) : value_(other.value_) {}
};

#endif  // STRING_HPP