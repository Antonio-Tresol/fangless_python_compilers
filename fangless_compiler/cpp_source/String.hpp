#ifndef STRING_HPP
#define STRING_HPP

#include <algorithm>
#include <cctype>
#include <climits>
#include <compare>
#include <string>

#include "Bool.hpp"
#include "Number.hpp"
#include "Object.hpp"
#include "Slice.hpp"

class String : public Object {
  std::string value_;

 public:
  explicit String(const std::string& value) : value_(value) {}

  static std::shared_ptr<String> spawn(const std::string& value) {
    return std::make_shared<String>(value);
  }

  std::string type() const override { return "str"; }

  std::string toString() const override { return "'" + value_ + "'"; }

  bool equals(const Object& other) const override {
    if (auto* strObj = dynamic_cast<const String*>(&other)) {
      return value_ == strObj->value_;
    }
    return false;
  }
  bool equals(const std::shared_ptr<Object>& other) const {
    return equals(*other);
  }

  friend bool operator==(const String& lhs, const String& rhs) {
    return lhs.equals(rhs);
  }

  friend bool operator==(std::shared_ptr<String> lhs,
                         std::shared_ptr<String> rhs) {
    return lhs->equals(*rhs);
  }

  friend bool operator==(std::shared_ptr<String> lhs, const String& rhs) {
    return lhs->equals(rhs);
  }

  friend bool operator==(const String& lhs, std::shared_ptr<String> rhs) {
    return rhs->equals(lhs);
  }

  friend bool operator==(const std::shared_ptr<Object>& lhs,
                         const String& rhs) {
    return rhs.equals(lhs);
  }

  friend bool operator==(const std::shared_ptr<Object>& lhs,
                         const std::shared_ptr<String>& rhs) {
    return rhs->equals(lhs);
  }
  size_t hash() const override { return std::hash<std::string>{}(value_); }

  bool toBool() const override { return !value_.empty(); }
  bool operator!() const { return value_.empty(); }
  friend bool operator!(const std::shared_ptr<String>& obj) {
    return obj->operator!();
  }

  bool isInstance(const std::string& type) const override {
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

  bool endswith(std::shared_ptr<String> suffix) const {
    return endswith(*suffix);
  }

  bool startswith(const std::shared_ptr<String>& prefix) const {
    return startswith(*prefix);
  }

  std::shared_ptr<String> replace(const String& oldStr,
                                  const String& newStr) const {
    std::string result = value_;
    size_t pos = 0;
    while ((pos = result.find(oldStr.value_, pos)) != std::string::npos) {
      result.replace(pos, oldStr.value_.length(), newStr.value_);
      pos += newStr.value_.length();
    }
    return std::make_shared<String>(result);
  }

  std::shared_ptr<String> replace(std::shared_ptr<String> oldStr,
                                  std::shared_ptr<String> newStr) const {
    return replace(*oldStr, *newStr);
  }

  std::shared_ptr<String> operator+(const String& other) const {
    return std::make_shared<String>(value_ + other.value_);
  }

  std::shared_ptr<String> operator*(const Number& number) const {
    std::string result;
    int n = number.getInt();
    for (int i = 0; i < n; ++i) {
      result += value_;
    }
    return std::make_shared<String>(result);
  }

  std::shared_ptr<String> operator*(std::shared_ptr<Number> number) const {
    std::string result;
    int n = number->getInt();
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
  std::shared_ptr<Number> len() const {
    return std::make_shared<Number>(static_cast<int>(value_.size()));
  }
  void setAttr(const std::string& name,
               std::shared_ptr<Object> value) override {
    throw std::runtime_error("'str' object attributes are read-only");
  }

  std::strong_ordering compare(const Object& other) const override {
    if (other.type() != "str") return Object::compare(other);

    auto* otherBool = dynamic_cast<const String*>(&other);

    return value_ <=> otherBool->value_;
  }

  std::shared_ptr<String> operator[](const Number& pos) const {
    int index = pos.getInt();
    int actual_index = index;
    if (index < 0) actual_index += value_.size();

    if (actual_index < 0 || actual_index >= static_cast<int>(value_.size())) {
      throw std::out_of_range("string index out of range");
    }
    return std::make_shared<String>(std::string{value_[actual_index]});
  }

  std::shared_ptr<String> operator[](std::shared_ptr<Number> pos) const {
    int index = pos->getInt();
    int actual_index = index;
    if (index < 0) actual_index += value_.size();

    if (actual_index < 0 || actual_index >= static_cast<int>(value_.size())) {
      throw std::out_of_range("string index out of range");
    }
    return std::make_shared<String>(std::string{value_[actual_index]});
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

  std::shared_ptr<String> at(const Number& pos) const {
    int index = pos.getInt();
    int actual_index = index;
    if (index < 0) actual_index += value_.size();

    if (actual_index < 0 || actual_index >= static_cast<int>(value_.size())) {
      throw std::out_of_range("string index out of range");
    }
    return std::make_shared<String>(std::string{value_[actual_index]});
  }

  std::shared_ptr<String> at(std::shared_ptr<Number> pos) const {
    int index = pos->getInt();
    int actual_index = index;
    if (index < 0) actual_index += value_.size();

    if (actual_index < 0 || actual_index >= static_cast<int>(value_.size())) {
      throw std::out_of_range("string index out of range");
    }
    return std::make_shared<String>(std::string{value_[actual_index]});
  }

  std::shared_ptr<String> slice(const Slice& slice) const {
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

  std::shared_ptr<Number> find(
      std::shared_ptr<String> sub,
      std::shared_ptr<Number> startNum = Number::spawn(0),
      std::shared_ptr<Number> endNum = Number::spawn(INT_MAX)) const {
    int start = startNum->getInt();
    int end = endNum->getInt();
    if (end == INT_MAX) end = value_.size();
    if (start < 0) start += value_.size();
    if (end < 0) end += value_.size();

    start = std::clamp(start, 0, static_cast<int>(value_.size()));
    end = std::clamp(end, 0, static_cast<int>(value_.size()));

    if (start > end) return std::make_shared<Number>(-1);

    size_t pos = value_.find(sub->value_, start);
    if (pos == std::string::npos || pos >= static_cast<size_t>(end)) {
      return std::make_shared<Number>(-1);
    }
    return std::make_shared<Number>(static_cast<int>(pos));
  }

  std::shared_ptr<Number> find(const String& sub, Number startNum = Number(0),
                               Number endNum = Number(INT_MAX)) const {
    int start = startNum.getInt();
    int end = endNum.getInt();
    if (end == INT_MAX) end = value_.size();
    if (start < 0) start += value_.size();
    if (end < 0) end += value_.size();

    start = std::clamp(start, 0, static_cast<int>(value_.size()));
    end = std::clamp(end, 0, static_cast<int>(value_.size()));

    if (start > end) return std::make_shared<Number>(-1);

    size_t pos = value_.find(sub.value_, start);
    if (pos == std::string::npos || pos >= static_cast<size_t>(end)) {
      return std::make_shared<Number>(-1);
    }
    return std::make_shared<Number>(static_cast<int>(pos));
  }

  std::shared_ptr<Number> rfind(const String& sub, Number startNum = Number(0),
                                Number endNum = Number(INT_MAX)) const {
    int start = startNum.getInt();
    int end = endNum.getInt();
    if (end == INT_MAX) end = value_.size();
    if (start < 0) start += value_.size();
    if (end < 0) end += value_.size();

    start = std::clamp(start, 0, static_cast<int>(value_.size()));
    end = std::clamp(end, 0, static_cast<int>(value_.size()));

    if (start > end) return std::make_shared<Number>(-1);

    size_t pos = value_.rfind(sub.value_, end);
    if (pos == std::string::npos || pos < static_cast<size_t>(start)) {
      return std::make_shared<Number>(-1);
    }
    return std::make_shared<Number>(static_cast<int>(pos));
  }

  std::shared_ptr<Number> index(const String& sub, Number startNum = Number(0),
                                Number endNum = Number(INT_MAX)) const {
    auto pos = find(sub, Number(startNum), Number(endNum));
    if (pos->getInt() == -1) {
      throw std::runtime_error("substring not found");
    }
    return pos;
  }

  std::shared_ptr<Number> rindex(const String& sub, Number startNum = Number(0),
                                 Number endNum = Number(INT_MAX)) const {
    auto pos = rfind(sub, Number(startNum), Number(endNum));

    if (pos->getInt() == -1) {
      throw std::runtime_error("substring not found");
    }
    return pos;
  }

  std::shared_ptr<Number> count(const String& sub, Number startNum = Number(0),
                                Number endNum = Number(INT_MAX)) const {
    int start = startNum.getInt();
    int end = endNum.getInt();
    if (end == INT_MAX) end = value_.size();
    if (start < 0) start += value_.size();
    if (end < 0) end += value_.size();

    start = std::clamp(start, 0, static_cast<int>(value_.size()));
    end = std::clamp(end, 0, static_cast<int>(value_.size()));

    if (start > end || sub.value_.empty()) return std::make_shared<Number>(0);

    int count = 0;
    size_t pos = start;
    while ((pos = value_.find(sub.value_, pos)) != std::string::npos &&
           pos < static_cast<size_t>(end)) {
      count++;
      pos += sub.value_.length();
    }
    return std::make_shared<Number>(count);
  }

  std::shared_ptr<Number> rfind(
      std::shared_ptr<String> sub,
      std::shared_ptr<Number> startNum = Number::spawn(0),
      std::shared_ptr<Number> endNum = Number::spawn(INT_MAX)) const {
    int start = startNum->getInt();
    int end = endNum->getInt();
    if (end == INT_MAX) end = value_.size();
    if (start < 0) start += value_.size();
    if (end < 0) end += value_.size();

    start = std::clamp(start, 0, static_cast<int>(value_.size()));
    end = std::clamp(end, 0, static_cast<int>(value_.size()));

    if (start > end) return std::make_shared<Number>(-1);

    size_t pos = value_.rfind(sub->value_, end);
    if (pos == std::string::npos || pos < static_cast<size_t>(start)) {
      return std::make_shared<Number>(-1);
    }
    return std::make_shared<Number>(static_cast<int>(pos));
  }

  std::shared_ptr<Number> index(
      std::shared_ptr<String> sub,
      std::shared_ptr<Number> startNum = Number::spawn(0),
      std::shared_ptr<Number> endNum = Number::spawn(INT_MAX)) const {
    auto pos = find(sub, startNum, endNum);
    if (pos->getInt() == -1) {
      throw std::runtime_error("substring not found");
    }
    return pos;
  }

  std::shared_ptr<Number> rindex(
      std::shared_ptr<String> sub,
      std::shared_ptr<Number> startNum = Number::spawn(0),
      std::shared_ptr<Number> endNum = Number::spawn(INT_MAX)) const {
    auto pos = rfind(sub, startNum, endNum);
    if (pos->getInt() == -1) {
      throw std::runtime_error("substring not found");
    }
    return pos;
  }

  std::shared_ptr<Number> count(
      std::shared_ptr<String> sub,
      std::shared_ptr<Number> startNum = Number::spawn(0),
      std::shared_ptr<Number> endNum = Number::spawn(INT_MAX)) const {
    int start = startNum->getInt();
    int end = endNum->getInt();
    if (end == INT_MAX) end = value_.size();
    if (start < 0) start += value_.size();
    if (end < 0) end += value_.size();

    start = std::clamp(start, 0, static_cast<int>(value_.size()));
    end = std::clamp(end, 0, static_cast<int>(value_.size()));

    if (start > end || sub->value_.empty()) return std::make_shared<Number>(0);

    int count = 0;
    size_t pos = start;
    while ((pos = value_.find(sub->value_, pos)) != std::string::npos &&
           pos < static_cast<size_t>(end)) {
      count++;
      pos += sub->value_.length();
    }
    return std::make_shared<Number>(count);
  }

  std::shared_ptr<Bool> isalpha() const {
    if (value_.empty()) return Bool::spawn(0);
    return Bool::spawn(
        std::all_of(value_.begin(), value_.end(),
                    [](unsigned char c) { return std::isalpha(c); }));
  }

  std::shared_ptr<Bool> isdigit() const {
    if (value_.empty()) return Bool::spawn(0);
    return Bool::spawn(
        std::all_of(value_.begin(), value_.end(),
                    [](unsigned char c) { return std::isdigit(c); }));
  }

  std::shared_ptr<Bool> isalnum() const {
    if (value_.empty()) return Bool::spawn(0);
    return Bool::spawn(
        std::all_of(value_.begin(), value_.end(),
                    [](unsigned char c) { return std::isalnum(c); }));
  }

  std::shared_ptr<Bool> isspace() const {
    if (value_.empty()) return Bool::spawn(0);
    return Bool::spawn(
        std::all_of(value_.begin(), value_.end(),
                    [](unsigned char c) { return std::isspace(c); }));
  }

  std::shared_ptr<Bool> isupper() const {
    if (value_.empty()) return Bool::spawn(0);
    bool hasUpper = false;
    for (unsigned char c : value_) {
      if (std::islower(c)) return Bool::spawn(0);
      if (std::isupper(c)) hasUpper = true;
    }
    return Bool::spawn(hasUpper);
  }

  std::shared_ptr<Bool> islower() const {
    if (value_.empty()) return Bool::spawn(0);
    bool hasLower = false;
    for (unsigned char c : value_) {
      if (std::isupper(c)) return Bool::spawn(0);
      if (std::islower(c)) hasLower = true;
    }
    return Bool::spawn(hasLower);
  }

  std::shared_ptr<Bool> istitle() const {
    if (value_.empty()) return Bool::spawn(0);
    bool prevCased = false;
    bool hasUpper = false;

    for (size_t i = 0; i < value_.size(); ++i) {
      if (std::isalpha(value_[i])) {
        if (prevCased) {
          if (std::isupper(value_[i])) return Bool::spawn(0);
        } else {
          if (std::islower(value_[i])) return Bool::spawn(0);
          hasUpper = true;
        }
        prevCased = true;
      } else {
        prevCased = false;
      }
    }
    return Bool::spawn(hasUpper);
  };
  friend std::ostream& operator<<(std::ostream& os,
                                  const std::shared_ptr<String>& obj) {
    return os << *obj;
  }

  friend std::shared_ptr<String> operator+(const std::shared_ptr<String>& a,
                                           const std::shared_ptr<String>& b) {
    return *a + *b;
  }

  friend std::shared_ptr<String> operator*(const std::shared_ptr<String>& a,
                                           const std::shared_ptr<Number>& b) {
    return *a * *b;
  }
};

#endif  // STRING_HPP