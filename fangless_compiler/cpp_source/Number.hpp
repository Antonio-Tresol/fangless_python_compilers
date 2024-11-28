#ifndef NUMBER_HPP
#define NUMBER_HPP

#include <cmath>
#include <memory>
#include <string>
#include <stdexcept>
#include <variant>
#include <sstream>

#include "Object.hpp"

constexpr double DELTA = 1e-9;

template <typename T>
concept Numerable = std::is_same_v<T, int64_t> || std::is_same_v<T, double>
  || std::is_same_v<T, int32_t> || std::is_same_v<T, size_t>;

class Number : public Object {
 private:
  std::variant<int64_t, double> value_;

 public:
  template<Numerable TType>
  explicit Number(const TType& value) : value_(value) {}

  explicit Number(const Number& other) : value_(other.value_) {}

  explicit Number(const Object& other) : value_(static_cast<int64_t>(other.toBool() ? 1 : 0)) {}

  explicit Number(std::shared_ptr<Object> obj) {
    if (auto* numObj = dynamic_cast<Number*>(obj.get())) {
      value_ = numObj->value_;
      return;
    }

    value_ = static_cast<int64_t>(obj->toBool()? 1 : 0);
  }

  template <typename T>
  static std::shared_ptr<Number> spawn(T value) {
    return std::make_shared<Number>(value);
  }

  std::string type() const override {
    return std::holds_alternative<int64_t>(value_) ? "int" : "float";
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
        }, value_);
  }

  inline bool isDouble() const {
    return std::visit(
        [](auto&& arg) -> bool {
          using T = std::decay_t<decltype(arg)>;
        
          if constexpr (std::is_same_v<T, double>) {
            return true;
          } else {
            return false;
          }
        }, value_);
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

  bool equals(const std::shared_ptr<Object>& other) const {
    return equals(*other);
  }

  friend bool operator==(const Number& lhs, const Number& rhs) {
    return lhs.equals(rhs);
  }

  friend bool operator==(std::shared_ptr<Number> lhs,
                         std::shared_ptr<Number> rhs) {
    return lhs->equals(*rhs);
  }

  friend bool operator==(std::shared_ptr<Number> lhs, const Number& rhs) {
    return lhs->equals(rhs);
  }

  friend bool operator==(const Number& lhs, std::shared_ptr<Number> rhs) {
    return rhs->equals(lhs);
  }

  friend bool operator==(const std::shared_ptr<Object>& lhs,
                         const Number& rhs) {
    return rhs.equals(lhs);
  }

  friend bool operator==(const std::shared_ptr<Object>& lhs,
                         const std::shared_ptr<Number>& rhs) {
    return rhs->equals(lhs);
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

  bool operator!() const { return !toBool(); }
  friend bool operator!(const std::shared_ptr<Number>& num) {
    return !num->toBool();
  }

  bool isInstance(const std::string& type) const override {
    if (type == "object") return true;
    if (type == "int") return std::holds_alternative<int64_t>(value_);
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

  // numeric specific methods

  int64_t getInt() const {
    return std::visit(
        [](auto&& arg) -> int64_t {
          using T = std::decay_t<decltype(arg)>;
          if constexpr (std::is_same_v<T, double>) {
            return static_cast<int64_t>(arg);
          }
          return arg;
        },
        value_);
  }

  operator int64_t() const { return getInt(); }

  double getDouble() const {
    return std::visit(
        [](auto&& arg) -> double { return static_cast<double>(arg); }, value_);
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

  std::shared_ptr<Number> operator~() const {
    if (this->isDouble()) {
      throw(std::invalid_argument("Can not use a double for ~ operation"));
    }
    return Number::spawn(~(this->getInt()));
  }

  // Arithmetic operators
  inline std::shared_ptr<Number> operator+() const {
    return std::make_shared<Number>(*this);
  }

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

  std::shared_ptr<Number> operator-() const {
    if (this->isDouble()) {
      const double value = -(this->getDouble());
      return Number::spawn(value);
    }

    const int value = -(this->getInt());
    return Number::spawn(value);
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
            int quotient = static_cast<int>(a / b);
            double remainder = a - (static_cast<double>(quotient) * b);
            return std::make_shared<Number>(remainder);

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

  std::shared_ptr<Number> pow(std::shared_ptr<Number> other) const {
    if (isDouble() || other->isDouble()) {
      return std::make_shared<Number>(
          std::pow(getDouble(), other->getDouble()));
    }
    return std::make_shared<Number>(std::pow(getInt(), other->getInt()));
  }
  
  // pre-increment
  std::shared_ptr<Number> operator++() {
    std::visit([](auto&& arg) {
          using T = std::decay_t<decltype(arg)>;
          if constexpr (std::is_same_v<T, double>) {
            arg += 1.0;
          } else {
            arg += 1;
          }
        }, value_);
  
    return std::make_shared<Number>(*this);
  }

  // post-increment
  std::shared_ptr<Number> operator++(int) {
    std::shared_ptr<Number> old_value = std::make_shared<Number>(*this);
    std::visit([](auto&& arg) {
          using T = std::decay_t<decltype(arg)>;
          if constexpr (std::is_same_v<T, double>) {
            arg += 1.0;
          } else {
            arg += 1;
          }
        }, value_);
        
    return std::make_shared<Number>(old_value);
  }

  friend std::shared_ptr<Number> operator~(const std::shared_ptr<Number>& num) {
    return num->operator~();
  }

  friend std::shared_ptr<Number> operator+(const std::shared_ptr<Number>& num) {
    return num->operator+();
  }

  friend std::shared_ptr<Number> operator+(const std::shared_ptr<Number>& a,
                                           const std::shared_ptr<Number>& b) {
    return *a + *b;
  }

  friend std::shared_ptr<Number> operator-(const std::shared_ptr<Number>& num) {
    return num->operator-();
  }

  friend std::shared_ptr<Number> operator-(const std::shared_ptr<Number>& a,
                                           const std::shared_ptr<Number>& b) {
    return *a - *b;
  }

  friend std::shared_ptr<Number> operator*(const std::shared_ptr<Number>& a,
                                           const std::shared_ptr<Number>& b) {
    return *a * *b;
  }

  friend std::shared_ptr<Number> operator/(const std::shared_ptr<Number>& a,
                                           const std::shared_ptr<Number>& b) {
    return *a / *b;
  }

  friend std::shared_ptr<Number> operator%(const std::shared_ptr<Number>& a,
                                           const std::shared_ptr<Number>& b) {
    return *a % *b;
  }

  friend std::ostream& operator<<(std::ostream& os,
                                  const std::shared_ptr<Number>& obj) {
    return os << *obj;
  }
};

#endif  // NUMBER_HPP