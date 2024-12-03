#ifndef BOOL_HPP
#define BOOL_HPP

#include <memory>

#include "Object.hpp"
#include "Number.hpp"

class Bool : public Object {
  bool value_;

 public:
  //========Constructors========//
  explicit Bool(bool value_) : value_(value_) {}

  explicit Bool(int value_) : value_(bool(value_)) {}
  explicit Bool(const Object& obj) : value_(obj.toBool()) {}
  explicit Bool(std::shared_ptr<Object> obj) : value_(obj->toBool()) {}
  explicit Bool(std::shared_ptr<Bool> obj) : value_(obj->value_) {}

  // Static method to spawn a new Bool object
  static std::shared_ptr<Bool> spawn(bool value_) {
    return std::make_shared<Bool>(value_);
  }

  //========Object interface methods========//
  std::string type() const override { return "Bool"; }

  std::string toString() const override { return value_ ? "True" : "False"; }
  explicit operator bool() const { return value_; }

  bool equals(const Object& other) const override {
    if (other.type() != "Bool") return false;

    auto* otherBool = dynamic_cast<const Bool*>(&other);

    return value_ == otherBool->value_;
  }

  bool operator==(const bool& other) const { return value_ == other; }

  bool operator==(const Bool& other) const { return equals(other); }

  bool operator!=(const Bool& other) const { return !equals(other); }

  friend bool operator==(const Bool& lhs, const Bool& rhs) {
    return lhs.equals(rhs);
  }

  friend bool operator==(const bool& lhs, const Bool& rhs) {
    return lhs == rhs.value_;
  }

  friend bool operator==(const Bool& lhs, const bool& rhs) {
    return lhs.value_ == rhs;
  }

  friend bool operator==(const std::shared_ptr<Bool>& lhs,
                         const std::shared_ptr<Bool>& rhs) {
    return lhs->equals(*rhs);
  }

  friend bool operator==(const std::shared_ptr<Bool>& lhs, const Bool& rhs) {
    return lhs->equals(rhs);
  }

  friend bool operator==(const Bool& lhs, const std::shared_ptr<Bool>& rhs) {
    return rhs->equals(lhs);
  }

  friend bool operator==(const std::shared_ptr<Bool>& lhs, const bool& rhs) {
    return (*lhs).value_ == rhs;
  }

  friend bool operator==(const bool& lhs, const std::shared_ptr<Bool>& rhs) {
    return lhs == (*rhs).value_;
  }

  size_t hash() const override { return std::hash<bool>{}(value_); }

  bool toBool() const override { return value_; }

  std::shared_ptr<Number> real() {
    return Number::spawn(static_cast<int64_t>(value_));
  }

  std::shared_ptr<Number> imag() {
    return Number::spawn(static_cast<int64_t>(0));
  }

  std::shared_ptr<Number> conjugate() {
    return Number::spawn(static_cast<int64_t>(value_));
  }

  // std::shared_ptr<Bool> operator!() const { return Bool::spawn(!value_); }
  std::shared_ptr<Bool> operator!() const { return Bool::spawn(!value_); }

  friend std::shared_ptr<Bool> operator!(const std::shared_ptr<Bool>& obj) {
    return obj->operator!();
  }

  std::shared_ptr<Bool> negate(std::shared_ptr<Bool>) {
    return Bool::spawn(!value_);
  }

  inline std::shared_ptr<Number> operator-() const {
    return -Number::spawn((value_)? 1 : 0);
  }

  friend std::shared_ptr<Number> operator-(const std::shared_ptr<Bool>& obj) {
    return obj->operator-();
  }

  inline std::shared_ptr<Number> operator~() const {
    return ~Number::spawn((value_)? 1 : 0);
  }

  friend std::shared_ptr<Number> operator~(const std::shared_ptr<Bool>& obj) {
    return obj->operator~();
  }

  std::shared_ptr<Object> getAttr(const std::string&) const override {
    throw std::runtime_error("'Bool' object has no attributes");
  }

  void setAttr(const std::string&,
               std::shared_ptr<Object>) override {
    throw std::runtime_error("'Bool' object has no attributes");
  }

  std::strong_ordering compare(const Object& other) const override {
    if (other.type() != "Bool") return other.toBool() <=> value_;

    auto* otherBool = dynamic_cast<const Bool*>(&other);

    return value_ <=> otherBool->value_;
  }

  friend std::strong_ordering operator<=>(const std::shared_ptr<Bool>& lhs,
                                          const Bool& rhs) {
    return lhs->compare(rhs);
  }
  friend std::strong_ordering operator<=>(const Bool& lhs,
                                          const std::shared_ptr<Bool>& rhs) {
    return lhs.compare(*rhs);
  }
  friend std::strong_ordering operator<=>(const std::shared_ptr<Object>& lhs,
                                          const Bool& rhs) {
    return rhs.compare(*lhs);
  }

  friend std::strong_ordering operator<=>(const std::shared_ptr<Bool>& lhs,
                                           const std::shared_ptr<Bool>& rhs) {
    return lhs->compare(*rhs);
  }

  friend std::strong_ordering operator<=>(const std::shared_ptr<Number>& lhs,
                                          const Bool& rhs) {
    return rhs.compare(*lhs);
  } 
  friend std::strong_ordering operator<=>(const Bool& lhs,
                                          const std::shared_ptr<Number>& rhs) {
    return lhs.compare(*rhs);
  }
  friend std::strong_ordering operator<=>(const std::shared_ptr<Number>& lhs,
                                          const std::shared_ptr<Bool>& rhs) {
    return rhs->compare(*lhs);
  }
  friend std::strong_ordering operator<=>(const std::shared_ptr<Bool>& lhs,
                                          const std::shared_ptr<Number>& rhs) {
    return lhs->compare(*rhs);
  }

  friend std::strong_ordering operator<=>(const std::shared_ptr<Object>& lhs,
                                          const std::shared_ptr<Bool>& rhs) {
    return rhs->compare(*lhs);
  }
  bool isInstance(const std::string& type) const override {
    return type == "bool" || type == "object";
  }
  
  friend std::ostream& operator<<(std::ostream& os,
                                  const std::shared_ptr<Bool>& obj) {
    return os << obj->toString();
  }
};

#endif  // BOOL_HPP