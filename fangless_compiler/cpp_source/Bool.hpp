#ifndef BOOL_HPP
#define BOOL_HPP

#include <memory>

#include "Object.hpp"
class Bool : public Object {
  bool value_;

 public:
  //========Constructors========//
  Bool(bool value_) : value_(value_) {}

  Bool(int value_) : value_(bool(value_)) {}
  Bool(Object& obj) : value_(obj.toBool()) {}
  Bool(std::shared_ptr<Object> obj) : value_(obj->toBool()) {}
  Bool(std::shared_ptr<Bool> obj) : value_(obj->value_) {}

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

  bool operator==(const Bool& other) const { return equals(other); }

  bool operator!=(const Bool& other) const { return !equals(other); }

  friend bool operator==(const Bool& lhs, const Bool& rhs) {
    return lhs.equals(rhs);
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

  size_t hash() const override { return std::hash<bool>{}(value_); }

  bool toBool() const override { return value_; }

  bool operator!() const { return !value_; }

  friend bool operator!(const std::shared_ptr<Bool>& obj) {
    return obj->operator!();
  }

  std::shared_ptr<Object> getAttr(const std::string& name) const override {
    throw std::runtime_error("'Bool' object has no attributes");
  }

  void setAttr(const std::string& name,
               std::shared_ptr<Object> value) override {
    throw std::runtime_error("'Bool' object has no attributes");
  }

  std::strong_ordering compare(const Object& other) const override {
    if (other.type() != "Bool") return other.toBool() <=> value_;

    auto* otherBool = dynamic_cast<const Bool*>(&other);

    return value_ <=> otherBool->value_;
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