#ifndef NUMBER_HPP
#define NUMBER_HPP

#include <cmath>
#include <memory>
#include <string>
#include <variant>

#include "Bool.hpp"
#include "Object.hpp"

constexpr double DELTA = 1e-9;

class Number : public Object {
 private:
  std::variant<int, double> value_;

 public:
  explicit Number(int value) : value_(value) {}
  explicit Number(double value) : value_(value) {}
  explicit Number(const Number& other) : value_(other.value_) {}
  explicit Number(const Bool& other) : value_(other.toBool() ? 1 : 0) {}
  explicit Number(std::shared_ptr<Object> obj) {
    if (auto* numObj = dynamic_cast<Number*>(obj.get())) {
      value_ = numObj->value_;
    } else if (auto* boolObj = dynamic_cast<Bool*>(obj.get())) {
      value_ = boolObj->toBool() ? 1 : 0;
    } else {
      throw std::runtime_error("Cannot convert object to number");
    }
  }

  template <typename T>
  static std::shared_ptr<Number> spawn(T value) {
    return std::make_shared<Number>(value);
  }

  std::string type() const override {
    return std::holds_alternative<int>(value_) ? "int" : "float";
  }

  std::string toString() const override {
    return std::visit(
        [](auto&& arg) -> std::string {
          using T = std::decay_t<decltype(arg)>;
          if constexpr (std::is_same_v<T, double>) {
            if (std::isinf(arg)) return arg > 0 ? "inf" : "-inf";
            if (std::isnan(arg)) return "nan";
            return std::to_string(arg);
          } else {
            return std::to_string(arg);
          }
        },
        value_);
  }

  bool equals(const Object& other) const override {
    if (auto* numObj = dynamic_cast<const Number*>(&other)) {
      return std::visit(
          [](auto&& a, auto&& b) -> bool {
            using A = std::decay_t<decltype(a)>;
            using B = std::decay_t<decltype(b)>;
            if constexpr (std::is_same_v<A, double> ||
                          std::is_same_v<B, double>) {
              return std::abs(static_cast<double>(a) - static_cast<double>(b)) <
                     DELTA;
            } else {
              return a == b;
            }
          },
          value_, numObj->value_);
    }
    return false;
  }

  size_t hash() const override {
    return std::visit(
        [](auto&& arg) -> size_t {
          return std::hash<std::decay_t<decltype(arg)>>{}(arg);
        },
        value_);
  }

  bool toBool() const override {
    return std::visit(
        [](auto&& arg) -> bool {
          using T = std::decay_t<decltype(arg)>;
          if constexpr (std::is_same_v<T, double>) {
            return arg != 0.0 && !std::isnan(arg);
          } else {
            return arg != 0;
          }
        },
        value_);
  }

  bool isInstance(const std::string& type) const override {
    if (type == "object") return true;
    if (type == "int") return std::holds_alternative<int>(value_);
    if (type == "float") return std::holds_alternative<double>(value_);
    return false;
  }

  std::shared_ptr<Object> getAttr(const std::string& name) const override {
    throw std::runtime_error("'" + type() + "' object has no attribute '" +
                             name + "'");
  }

  void setAttr(const std::string& name,
               std::shared_ptr<Object> value) override {
    throw std::runtime_error("'" + type() + "' object has no attributes");
  }

  // Arithmetic operators
  std::shared_ptr<Number> operator+(const Number& other) const {
    return std::visit(
        [](auto&& a, auto&& b) -> std::shared_ptr<Number> {
          using A = std::decay_t<decltype(a)>;
          using B = std::decay_t<decltype(b)>;
          if constexpr (std::is_same_v<A, double> ||
                        std::is_same_v<B, double>) {
            return std::make_shared<Number>(static_cast<double>(a) +
                                            static_cast<double>(b));
          } else {
            return std::make_shared<Number>(a + b);
          }
        },
        value_, other.value_);
  }

  std::shared_ptr<Number> operator-(const Number& other) const {
    return std::visit(
        [](auto&& a, auto&& b) -> std::shared_ptr<Number> {
          using A = std::decay_t<decltype(a)>;
          using B = std::decay_t<decltype(b)>;
          if constexpr (std::is_same_v<A, double> ||
                        std::is_same_v<B, double>) {
            return std::make_shared<Number>(static_cast<double>(a) -
                                            static_cast<double>(b));
          } else {
            return std::make_shared<Number>(a - b);
          }
        },
        value_, other.value_);
  }

  std::shared_ptr<Number> operator*(const Number& other) const {
    return std::visit(
        [](auto&& a, auto&& b) -> std::shared_ptr<Number> {
          using A = std::decay_t<decltype(a)>;
          using B = std::decay_t<decltype(b)>;
          if constexpr (std::is_same_v<A, double> ||
                        std::is_same_v<B, double>) {
            return std::make_shared<Number>(static_cast<double>(a) *
                                            static_cast<double>(b));
          } else {
            return std::make_shared<Number>(a * b);
          }
        },
        value_, other.value_);
  }
  std::shared_ptr<Number> operator%(const Number& other) const {
    return std::visit(
        [](auto&& a, auto&& b) -> std::shared_ptr<Number> {
          using A = std::decay_t<decltype(a)>;
          using B = std::decay_t<decltype(b)>;

          if constexpr (std::is_same_v<A, double> ||
                        std::is_same_v<B, double>) {
            throw std::runtime_error(
                "Modulo operation not supported on floats");
          } else {
            if (b == 0) {
              throw std::runtime_error("Division by zero");
            }
            return std::make_shared<Number>(a % b);
          }
        },
        value_, other.value_);
  }

  std::shared_ptr<Number> operator/(const Number& other) const {
    return std::visit(
        [](auto&& a, auto&& b) -> std::shared_ptr<Number> {
          using B = std::decay_t<decltype(b)>;

          if constexpr (std::is_same_v<B, double>) {
            if (std::abs(b) < DELTA) {
              throw std::runtime_error("Division by zero");
            }
          } else {
            if (b == 0) {
              throw std::runtime_error("Division by zero");
            }
          }

          return std::make_shared<Number>(static_cast<double>(a) /
                                          static_cast<double>(b));
        },
        value_, other.value_);
  }
  std::strong_ordering compare(const Object& other) const override {
    if (auto* numObj = dynamic_cast<const Number*>(&other)) {
      return std::visit(
          [](auto&& a, auto&& b) -> std::strong_ordering {
            auto cmp = static_cast<double>(a) <=> static_cast<double>(b);
            if (cmp == std::partial_ordering::less)
              return std::strong_ordering::less;
            if (cmp == std::partial_ordering::greater)
              return std::strong_ordering::greater;
            return std::strong_ordering::equal;
          },
          value_, numObj->value_);
    }
    return std::strong_ordering::greater;
  }

  bool isFinite() const {
    return std::visit(
        [](auto&& arg) -> bool {
          using T = std::decay_t<decltype(arg)>;
          if constexpr (std::is_same_v<T, double>) {
            return std::isfinite(arg);
          }
          return true;
        },
        value_);
  }

  bool isInf() const {
    return std::visit(
        [](auto&& arg) -> bool {
          using T = std::decay_t<decltype(arg)>;
          if constexpr (std::is_same_v<T, double>) {
            return std::isinf(arg);
          }
          return false;
        },
        value_);
  }

  bool isNaN() const {
    return std::visit(
        [](auto&& arg) -> bool {
          using T = std::decay_t<decltype(arg)>;
          if constexpr (std::is_same_v<T, double>) {
            return std::isnan(arg);
          }
          return false;
        },
        value_);
  }

  int getInt() const {
    return std::visit(
        [](auto&& arg) -> int {
          using T = std::decay_t<decltype(arg)>;
          if constexpr (std::is_same_v<T, double>) {
            return static_cast<int>(arg);
          }
          return arg;
        },
        value_);
  }

  double getDouble() const {
    return std::visit(
        [](auto&& arg) -> double { return static_cast<double>(arg); }, value_);
  }
};

#endif  // NUMBER_HPP