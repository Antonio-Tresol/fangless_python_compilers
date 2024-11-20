// Int.hpp
#ifndef INT_HPP
#define INT_HPP

#include <cmath>
#include <functional>
#include <memory>
#include <string>

#include "Object.hpp"

class Float;  // Forward declaration

class Int : public Object {
 private:
  int value_;

 public:
  explicit Int(int value) : value_(value) {}

  std::string type() const override { return "int"; }

  std::string toString() const override { return std::to_string(value_); }

  bool equals(const Object& other) const override {
    if (auto* intObj = dynamic_cast<const Int*>(&other)) {
      return value_ == intObj->value_;
    }
    return false;
  }

  size_t hash() const override { return std::hash<int>{}(value_); }

  bool toBool() const override {
    return value_ != 0;  // Python's truthiness for int
  }

  bool isinstance(const std::string& type) const override {
    return type == "int" || type == "object";
  }

  std::shared_ptr<Object> getAttr(const std::string& name) const override {
    // Integers don't have attributes in Python
    throw std::runtime_error("'int' object has no attribute '" + name + "'");
  }

  void setAttr(const std::string& name,
               std::shared_ptr<Object> value) override {
    // Integers don't have attributes in Python
    throw std::runtime_error("'int' object has no attribute '" + name + "'");
  }

  // Additional convenience methods
  int getValue() const { return value_; }

  // Arithmetic operators with Int
  std::shared_ptr<Int> operator+(const Int& other) const {
    return std::make_shared<Int>(value_ + other.value_);
  }

  std::shared_ptr<Int> operator-(const Int& other) const {
    return std::make_shared<Int>(value_ - other.value_);
  }

  std::shared_ptr<Int> operator*(const Int& other) const {
    return std::make_shared<Int>(value_ * other.value_);
  }

  std::shared_ptr<Float> operator/(
      const Int& other) const;  // Always returns Float

  // Arithmetic operators with Float
  std::shared_ptr<Float> operator+(const Float& other) const;
  std::shared_ptr<Float> operator-(const Float& other) const;
  std::shared_ptr<Float> operator*(const Float& other) const;
  std::shared_ptr<Float> operator/(const Float& other) const;

  // Comparison operators
  std::strong_ordering compare(const Object& other) const override
  {
    auto* strObj = dynamic_cast<const Int*>(&other);
    if (strObj == nullptr) return std::strong_ordering::greater;
    auto& otherRef = *strObj;

    return value_ <=> otherRef.value_;
  }
};

#endif  // INT_HPP

// Float.hpp
#ifndef FLOAT_HPP
#define FLOAT_HPP

#include <cmath>

class Int;  // Forward declaration

class Float : public Object {
 private:
  double value_;

 public:
  explicit Float(double value) : value_(value) {}

  std::string type() const override { return "float"; }

  std::string toString() const override {
    // Handle special cases like inf and nan
    if (std::isinf(value_)) {
      return value_ > 0 ? "inf" : "-inf";
    }
    if (std::isnan(value_)) {
      return "nan";
    }
    return std::to_string(value_);
  }

  bool equals(const Object& other) const override {
    if (auto* floatObj = dynamic_cast<const Float*>(&other)) {
      return std::abs(value_ - floatObj->value_) <
             1e-9;  // Compare with epsilon
    }
    return false;
  }

  size_t hash() const override { return std::hash<double>{}(value_); }

  bool toBool() const override {
    return value_ != 0.0 && !std::isnan(value_);  // Python's float truthiness
  }

  bool isinstance(const std::string& type) const override {
    return type == "float" || type == "object";
  }

  std::shared_ptr<Object> getAttr(const std::string& name) const override {
    throw std::runtime_error("'float' object has no attribute '" + name + "'");
  }

  void setAttr(const std::string& name,
               std::shared_ptr<Object> value) override {
    throw std::runtime_error("'float' object has no attribute '" + name + "'");
  }

  // Additional convenience methods
  double getValue() const { return value_; }

  // Arithmetic operators with Float
  std::shared_ptr<Float> operator+(const Float& other) const {
    return std::make_shared<Float>(value_ + other.value_);
  }

  std::shared_ptr<Float> operator-(const Float& other) const {
    return std::make_shared<Float>(value_ - other.value_);
  }

  std::shared_ptr<Float> operator*(const Float& other) const {
    return std::make_shared<Float>(value_ * other.value_);
  }

  std::shared_ptr<Float> operator/(const Float& other) const {
    return std::make_shared<Float>(value_ / other.value_);
  }

  // Arithmetic operators with Int
  std::shared_ptr<Float> operator+(const Int& other) const {
    return std::make_shared<Float>(value_ + other.getValue());
  }

  std::shared_ptr<Float> operator-(const Int& other) const {
    return std::make_shared<Float>(value_ - other.getValue());
  }

  std::shared_ptr<Float> operator*(const Int& other) const {
    return std::make_shared<Float>(value_ * other.getValue());
  }

  std::shared_ptr<Float> operator/(const Int& other) const {
    return std::make_shared<Float>(value_ / other.getValue());
  }

  bool isFinite() const { return std::isfinite(value_); }

  bool isInf() const { return std::isinf(value_); }

  bool isNaN() const { return std::isnan(value_); }
};

// Implement Int's Float operations
inline std::shared_ptr<Float> Int::operator/(const Int& other) const {
  return std::make_shared<Float>(static_cast<double>(value_) / other.value_);
}

inline std::shared_ptr<Float> Int::operator+(const Float& other) const {
  return std::make_shared<Float>(value_ + other.getValue());
}

inline std::shared_ptr<Float> Int::operator-(const Float& other) const {
  return std::make_shared<Float>(value_ - other.getValue());
}

inline std::shared_ptr<Float> Int::operator*(const Float& other) const {
  return std::make_shared<Float>(value_ * other.getValue());
}

inline std::shared_ptr<Float> Int::operator/(const Float& other) const {
  return std::make_shared<Float>(value_ / other.getValue());
}

#endif  // FLOAT_HPP