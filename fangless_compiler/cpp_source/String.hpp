#ifndef STRING_HPP
#define STRING_HPP

#include <algorithm>
#include <cctype>
#include <climits>
#include <compare>
#include <string>

#include "Iterable.hpp"
#include "Tuple.hpp"
#include "Bool.hpp"
#include "Number.hpp"
#include "Object.hpp"
#include "Slice.hpp"

class String : public Object {
  std::string value_;

 public:
  explicit String(const std::string& value = "") : value_(value) {}

  String(const String& other) : value_(other.value_) {}

  static std::shared_ptr<String> spawn(const std::string& value) {
    return std::make_shared<String>(value);
  }

  String& operator=(const String& other) {
    if (this != &other) {
      value_ = other.value_;
    }
    return *this;
  }

  std::string operator*() const { return value_; }

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

  std::strong_ordering compare(const Object& other) const override {
    if (other.type() != "str") return Object::compare(other);

    auto* otherBool = dynamic_cast<const String*>(&other);

    return value_ <=> otherBool->value_;
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

  // Attribute access
  std::shared_ptr<Object> getAttr(const std::string& name) const override {
    if (name == "upper") return std::make_shared<String>(upper()->toString());
    if (name == "lower") return std::make_shared<String>(lower()->toString());
    if (name == "strip") return std::make_shared<String>(strip()->toString());
    throw std::runtime_error("'str' object has no attribute '" + name + "'");
  }

  void setAttr(const std::string&,
               std::shared_ptr<Object>) override {
    throw std::runtime_error("'str' object attributes are read-only");
  }

  auto begin() { return value_.begin(); }
  auto end() { return value_.end(); }
  auto begin() const { return value_.begin(); }
  auto end() const { return value_.end(); }

  auto rbegin() { return value_.rbegin(); }
  auto rend() { return value_.rend(); }
  auto rbegin() const { return value_.rbegin(); }
  auto rend() const { return value_.rend(); }

  // Python string methods
  std::shared_ptr<String> capitalize() const {
    std::string result = value_;
    result[0] = std::toupper(static_cast<unsigned char>(value_[0]));
    return std::make_shared<String>(result);
  }

  std::shared_ptr<String> casefold() const {
    return lower();
  }

  std::shared_ptr<String> center(const Number& width,
    const String& fill = String(std::string(" "))) {
    if (static_cast<int64_t>(value_.size()) >= width.getInt()) {
        return std::make_shared<String>(value_);
    }

    size_t total_padding = width.getInt() - value_.size();
    size_t left_padding = total_padding / 2;
    size_t right_padding = total_padding - left_padding;

    return std::make_shared<String>(
      std::string(left_padding, (*fill).c_str()[0]) +
      value_ +
      std::string(right_padding, (*fill).c_str()[0])
    );
  }

  std::shared_ptr<String> center(const std::shared_ptr<Number>& width,
    const std::shared_ptr<String>& fill = String::spawn(std::string(" "))) {
    return center(*width, *fill);
  }

  std::shared_ptr<String> expandTabs(const Number& tab = Number(8)) {
    std::string result;
    size_t column = 0;
    const size_t tabSize = tab.getInt();

    for (char c : value_) {
        if (c == '\t') {
            size_t spaces = tabSize - (column % tabSize);
            result.append(spaces, ' ');
            column += spaces;
        } else {
            result += c;
            column++;
        }
    }

    return std::make_shared<String>(result);
  }

  std::shared_ptr<String> expandTabs(
    const std::shared_ptr<Number>& tab = Number::spawn(8)) {
    return expandTabs(*tab);
  }

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

  std::shared_ptr<String> lstrip(const String& chars) {
    size_t start = value_.find_first_not_of(*chars);
    if (start == std::string::npos) {
        return String::spawn(std::string(""));
    }

    return String::spawn(value_.substr(start));
  }

  std::shared_ptr<String> lstrip(
    const std::shared_ptr<String>& chars =
    String::spawn(std::string(" \t\n\r\f\v"))) {
    return lstrip(*chars);
  }

  std::shared_ptr<String> rstrip(const String& chars) {
    size_t start = value_.find_last_not_of(*chars);
    if (start == std::string::npos) {
        return String::spawn(std::string(""));
    }

    return String::spawn(value_.substr(start));
  }

  std::shared_ptr<String> rstrip(
    const std::shared_ptr<String>& chars =
    String::spawn(std::string(" \t\n\r\f\v"))) {
    return rstrip(*chars);
  }

  std::shared_ptr<Tuple> partition(const String& value) {
    size_t pos = value_.find(*value);

    if (pos == std::string::npos) {
        return Tuple::spawn({
            String::spawn(value_),
            String::spawn(""),
            String::spawn("")
        });
    }

    std::shared_ptr<String> before = String::spawn(value_.substr(0, pos));
    std::shared_ptr<String> separator = String::spawn(*value);
    
    size_t after_pos = pos + (*value).size();
    std::shared_ptr<String> after = String::spawn(after_pos < value_.size() ? value_.substr(after_pos) : "");

    return Tuple::spawn({before, separator, after});
  }

  std::shared_ptr<Tuple> partition(const std::shared_ptr<String>& value) {
    return partition(*value);
  }

  std::shared_ptr<Tuple> rpartition(const String& value) {
    size_t pos = value_.rfind(*value);

    if (pos == std::string::npos) {
        return Tuple::spawn({
            String::spawn(value_),
            String::spawn(""),
            String::spawn("")
        });
    }

    std::shared_ptr<String> before = String::spawn(value_.substr(0, pos));
    std::shared_ptr<String> separator = String::spawn(*value);
    
    size_t after_pos = pos + (*value).size();
    std::shared_ptr<String> after = String::spawn(after_pos < value_.size() ? value_.substr(after_pos) : "");

    return Tuple::spawn({before, separator, after});
  }
  
  std::shared_ptr<Tuple> rpartition(const std::shared_ptr<String>& value) {
    return rpartition(*value);
  }
  
  std::shared_ptr<String> strip(const std::shared_ptr<String>& value =
    String::spawn(std::string(" \t\n\r"))) const {
    auto start = value_.find_first_not_of((**value).c_str());
    auto end = value_.find_last_not_of((**value).c_str());

    if (start == std::string::npos) return std::make_shared<String>("");

    return std::make_shared<String>(value_.substr(start, end - start + 1));
  }

  std::shared_ptr<List> rsplit(const String& separator,
    const Number& maxOccurrences = Number(-1)) {
    auto result = std::make_shared<List>();
    size_t end = value_.size();
    size_t start;
    int maxSplits = maxOccurrences.getInt();
    int currentSplit = 0;

    if ((*separator).empty()) {
        result->append(String::spawn(value_));
        return result;
    }

    while ((start = value_.rfind(*separator, end - 1)) != std::string::npos) {
        if (maxSplits >= 0 && currentSplit >= maxSplits) break;
        result->getElements().insert(result->getElements().begin(),
            String::spawn(value_.substr(start + (*separator).size(), end - (start + (*separator).size()))));
        end = start;
        currentSplit++;
    }

    result->getElements().insert(result->getElements().begin(),
        String::spawn(value_.substr(0, end)));

    return result;
  }

  std::shared_ptr<List> rsplit(
    const std::shared_ptr<String>& separator = String::spawn(std::string(" "))
    , const std::shared_ptr<Number>& maxSplit = Number::spawn(-1)) {
    return rsplit(*separator, *maxSplit);
  }

  std::shared_ptr<List> split(const String& separator,
    const Number& maxOcurrences = Number(-1)) {
    auto result = std::make_shared<List>();
    size_t start = 0, end;
    int currentSplit = 0;
    int maxSplits = maxOcurrences.getInt();

    if ((*separator).empty()) {
        result->append(String::spawn(value_));
        return result;
    }

    while ((end = value_.find(*separator, start)) != std::string::npos) {
        if (maxSplits >= 0 && currentSplit >= maxSplits) break;

        result->append(String::spawn(value_.substr(start, end - start)));
        start = end + (*separator).size();
        currentSplit++;
    }

    result->append(String::spawn(value_.substr(start)));
    
    return result;
  }


  std::shared_ptr<List> split(
    const std::shared_ptr<String>& separator =
    String::spawn(std::string(" ")),
    const std::shared_ptr<Number>& maxOcurrences = Number::spawn(-1)) {
    return split(*separator, *maxOcurrences);
  }

  std::shared_ptr<List> splitlines(const Bool& keepLineBreaks) {
    auto result = std::make_shared<List>();
    size_t start = 0;

    for (size_t i = 0; i < value_.size(); ++i) {
      if (value_[i] == '\n' || value_[i] == '\r' ||
        value_[i] == '\v' || value_[i] == '\f' ||
        value_[i] == '\x1c' || value_[i] == '\x1d' ||
        value_[i] == '\x1e' || value_[i] == '\x85') {

        size_t length = i - start;
        if (keepLineBreaks.toBool() && i < value_.size()) {
          length++; // Include the line break
        }
        
        result->append(String::spawn(value_.substr(start, length)));

        if (value_[i] == '\r' && i + 1 < value_.size() && value_[i + 1] == '\n') {
          if (keepLineBreaks.toBool()) {
              result->append(String::spawn(value_.substr(i, 2))); // Add \r\n
          }
          ++i; // Skip the \n
        }

        start = i + 1; // Update start to after the line break
      }
    }

    if (start < value_.size()) {
        result->append(String::spawn(value_.substr(start)));
    }

    return result;
  }

  std::shared_ptr<List> splitlines(const std::shared_ptr<Bool>&
    keepLineBreaks = Bool::spawn(false)) {
    return splitlines(*keepLineBreaks);
  }

  bool startswith(const String& prefix, const Number& start = Number(0),
    const Number& end = Number(0)) const {
    if (end == Number(0)) {
      return value_.substr(
        start.getInt(),
        Number(static_cast<int64_t>(prefix.value_.length())).getInt())
        == prefix.value_;
    }

    return value_.substr(start.getInt(), end.getInt()) == prefix.value_;
  }

  bool endswith(const String& suffix) const {
    if (suffix.value_.length() > value_.length()) return false;
    return value_.substr(value_.length() - suffix.value_.length()) ==
           suffix.value_;
  }

  bool endswith(std::shared_ptr<String> suffix) const {
    return endswith(*suffix);
  }

  bool startswith(const std::shared_ptr<String>& prefix,
    const std::shared_ptr<Number>& start = Number::spawn(0),
    const std::shared_ptr<Number>& end = Number::spawn(0)) const {
    return startswith(*prefix, *start, *end);
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

  std::shared_ptr<String> operator+(const Object& other) const {
    return std::make_shared<String>(value_ + other.toString());
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

  std::shared_ptr<Number> len() const {
    return Number::spawn(static_cast<int>(value_.size()));
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

  std::shared_ptr<String> operator[](const Number& pos) const {
    int index = pos.getInt();
    int actual_index = index;
    if (index < 0) actual_index += value_.size();

    if (actual_index < 0 || actual_index >= static_cast<int>(value_.size())) {
      throw std::out_of_range("string index out of range");
    }
    return std::make_shared<String>(std::string{value_[actual_index]});
  }

  std::shared_ptr<String> operator[](const std::shared_ptr<Number>& pos) const {
    int index = pos->getInt();
    int actual_index = index;
    if (index < 0) actual_index += value_.size();

    if (actual_index < 0 || actual_index >= static_cast<int>(value_.size())) {
      throw std::out_of_range("string index out of range");
    }
    return std::make_shared<String>(std::string{value_[actual_index]});
  }

  std::shared_ptr<String> operator[](const Slice& slice) const {
    int start = slice.start == INT_MAX ? 0 : slice.start;
    int end = slice.end == INT_MAX ? value_.size() : slice.end;
    int step = slice.step == 0 ?
      throw std::invalid_argument("Step cannot be zero") : slice.step;

    if (start < 0) start += value_.size();
    if (end < 0) end += value_.size();

    start = std::clamp(start, 0, static_cast<int>(value_.size()));
    end = std::clamp(end, 0, static_cast<int>(value_.size()));

    std::string result;

    if (step > 0) {
        for (int i = start; i < end; i += step) {
            result += value_[i];
        }
    } else {
        for (int i = start; i > end; i += step) {
            result += value_[i];
        }
    }

    return std::make_shared<String>(result);
  }

  std::shared_ptr<String> slice(const Slice& slice) {
    return this->operator[](slice);
  }
  std::shared_ptr<String> slice(std::shared_ptr<Slice> slice) {
    return this->operator[](*slice);
  }

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

  std::shared_ptr<Bool> isascii_() const {
    return Bool::spawn(true);
  }

  std::shared_ptr<Bool> isalpha() const {
    if (value_.empty()) return Bool::spawn(0);
    return Bool::spawn(
        std::all_of(value_.begin(), value_.end(),
                    [](unsigned char c) { return std::isalpha(c); }));
  }

  std::shared_ptr<Bool> isdecimal() const {
    return isdigit();
  }

  std::shared_ptr<Bool> isnumeric() const {
    return isdigit();
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

  std::shared_ptr<Bool> isidentifier() const {
    if (value_.empty() || !(std::isalpha(value_[0]) || value_[0] == '_')) {
      return Bool::spawn(false);
    }

    for (char c : value_) {
      if (!(std::isalnum(c) || c == '_')) {
          return Bool::spawn(false);
      }
    }

    return Bool::spawn(true);
  }

  std::shared_ptr<Bool> isprintable() const {
    for (char c : value_) {
        if (!std::isprint(static_cast<unsigned char>(c))) {
            return Bool::spawn(false);
        }
    }
    return Bool::spawn(true);
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
  }

  std::shared_ptr<String> join(const String& elements) {
    std::string result;

    auto it = elements.begin();
    if (it != elements.end()) {
        result += *it;  // Add the first element to result
        ++it;

        for (; it != elements.end(); ++it) {
            result += value_;
            result += *it;
        }
    }

    return String::spawn(result);
  }


  template<TIterable TType>
  std::shared_ptr<String> join(const TType& elements) {
    std::string result;

    if (elements.begin() != elements.end()) {
      result += (*(elements.begin()))->toString();
      for (auto i = elements.begin()+1; i != elements.end(); ++i) {
          result += value_ + (*i)->toString();
      }
    }

    return String::spawn(result);
  }

  template<TIterable TType>
  std::shared_ptr<String> join(const std::shared_ptr<TType>& elements) {
    return join(*elements);
  }

  std::shared_ptr<String> ljust(const Number& width,
    const String& fill = String(std::string(" "))) {
    if (static_cast<int64_t>(value_.size()) >= width.getInt()) {
        return String::spawn(value_);
    }

    return String::spawn(value_ +
      std::string(width.getInt() - value_.size(), (*fill).c_str()[0]));
  }

  std::shared_ptr<String> ljust(const std::shared_ptr<Number>& width,
    const std::shared_ptr<String>& fill = String::spawn(std::string(" "))) {
    return ljust(*width, *fill);
  }

std::shared_ptr<String> rjust(const Number& width, const String& fill = String(" ")) {
    size_t currentSize = value_.size();
    int64_t targetWidth = width.getInt();

    if (currentSize >= static_cast<size_t>(targetWidth)) {
        return String::spawn(value_);
    }

    char fillChar = (!(*fill).empty()) ? (*fill).c_str()[0] : ' ';

    size_t paddingSize = targetWidth - currentSize;

    return String::spawn(std::string(paddingSize, fillChar) + value_);
  }

  std::shared_ptr<String> rjust(const std::shared_ptr<Number>& width,
      const std::shared_ptr<String>& fill = String::spawn(" ")) {
      return rjust(*width, *fill);
  }

  std::shared_ptr<String> swapcase() {
    std::string result;

    for (char c : value_) {
        if (std::isalpha(static_cast<unsigned char>(c))) {
            result += std::isupper(static_cast<unsigned char>(c)) ?
                std::tolower(static_cast<unsigned char>(c)) :
                std::toupper(static_cast<unsigned char>(c));
        } else {
            result += c;
        }
    }

    return String::spawn(result);
  }

  std::shared_ptr<String> title () const {
    std::string result;
    
    bool newWord = true;

    for ( char c : value_ ) {
      if (std::isalpha(static_cast<unsigned char>(c))) {
        result += newWord ?
          std::toupper(static_cast<unsigned char>(c))
          : std::tolower(static_cast<unsigned char>(c));
          newWord = false;
      } else {
        result += c;
        newWord = true;
      }
    }

    return String::spawn(result);
  }

  std::shared_ptr<String> zfill(const Number& width) const {
    int64_t amount = width.getInt() - static_cast<int64_t>(value_.length());
    std::string result;

    if (amount > 0) {
      if (!value_.empty() && (value_[0] == '+' || value_[0] == '-')) {
        result += value_[0]; 
        for (int64_t current = 0; current < amount; ++current) {
          result += '0'; 
        }
        result += value_.substr(1); 
      } else {
        for (int64_t current = 0; current < amount; ++current) {
          result += '0';
        }
        result += value_;
      }
    } else {
      result = value_;
    }

    return String::spawn(result);
  }


  std::shared_ptr<String> zfill  ( const std::shared_ptr<Number>& width ) const {
    return zfill(*width);
  }

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

  friend std::shared_ptr<String> operator+(const std::shared_ptr<Object>& first,
    const std::shared_ptr<String>& second) {
    return std::make_shared<String>(first->toString() + second->value_);
  }

  friend std::shared_ptr<String> operator+(const std::shared_ptr<String>& first,
    const std::shared_ptr<Object>& second) {
    return std::make_shared<String>(first->value_ + second->toString());
  }
};

#endif  // STRING_HPP