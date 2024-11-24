#ifndef BOOL_HPP
#define BOOL_HPP

#include <memory>

#include "Number.hpp"
#include "Object.hpp"
class Bool : public Object {
  bool value_;

 public:
  //========Constructors========//
  Bool(bool value_) : value_(value_) {}

  Bool(int value_) : value_(bool(value_)) {}
  Bool(Object& obj) : value_(obj.toBool()) {}
  Bool(std::shared_ptr<Object> obj) : value_(obj->toBool()) {}

  // Static method to spawn a new Bool object
  static std::shared_ptr<Bool> spawn(bool value_) {
    return std::make_shared<Bool>(value_);
  }

  //========Object interface methods========//
  std::string type() const override { return "Bool"; }

  std::string toString() const override { return value_ ? "True" : "False"; }

  bool equals(const Object& other) const override {
    if (other.type() != "Bool") return false;

    auto* otherBool = dynamic_cast<const Bool*>(&other);

    return value_ == otherBool->value_;
  }

  size_t hash() const override { return std::hash<bool>{}(value_); }

  bool toBool() const override { return value_; }

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

  //========Operators========//
  std::shared_ptr<Bool> operator!() const { return Bool::spawn(!value_); }

  std::shared_ptr<Bool> operator&&(const Object& other) const {
    return Bool::spawn(value_ && other.toBool());
  }

  std::shared_ptr<Bool> operator||(const Object& other) const {
    return Bool::spawn(value_ || other.toBool());
  }

  std::shared_ptr<Bool> operator==(const Object& other) const {
    return Bool::spawn(value_ == other.toBool());
  }

  std::shared_ptr<Number> operator+(const Number& other) const {
    return Number::spawn(value_ + other.getInt());
  }

  std::shared_ptr<Number> operator-(const Number& other) const {
    return Number::spawn(value_ - other.getInt());
  }

  std::shared_ptr<Number> operator*(const Number& other) const {
    return Number::spawn(value_ * other.getInt());
  }

  std::shared_ptr<Number> operator/(const Number& other) const {
    return Number::spawn(value_ / other.getInt());
  }

  std::shared_ptr<Number> operator%(const Number& other) const {
    return Number::spawn(value_ % other.getInt());
  }
};

// Helper function to spawn a new Bool object on operator overloads
std::shared_ptr<Bool> operator!(std::shared_ptr<Bool> obj) {
  return obj->operator!();
}

std::shared_ptr<Bool> operator&&(std::shared_ptr<Bool> obj,
                                 std::shared_ptr<Object> other) {
  return *obj && *other;
}

std::shared_ptr<Bool> operator||(std::shared_ptr<Bool> obj,
                                 std::shared_ptr<Object> other) {
  return *obj || *other;
}

#endif  // BOOL_HPP