#ifndef NONE_HPP
#define NONE_HPP

#include "Object.hpp"

class None : public Object {
 private:
  None() = default;  // Private constructor for singleton

 public:
  // Singleton access
  static std::shared_ptr<None> spawn() {
    static std::shared_ptr<None> instance = std::shared_ptr<None>(new None());
    return instance;
  }

  // Delete copy/move operations
  None(const None&) = delete;
  None& operator=(const None&) = delete;
  None(None&&) = delete;
  None& operator=(None&&) = delete;

  std::string type() const override { return "NoneType"; }

  std::string toString() const override { return "None"; }

  std::string repr() const { return "None"; }

  bool equals(const Object& other) const override {
    return dynamic_cast<const None*>(&other) != nullptr;
  }

  friend bool operator==(const None& lhs, const None& rhs) {
    return lhs.equals(rhs);
  }

  friend bool operator==(std::shared_ptr<None> lhs, std::shared_ptr<None> rhs) {
    return lhs->equals(*rhs);
  }

  friend bool operator==(std::shared_ptr<None> lhs, const None& rhs) {
    return lhs->equals(rhs);
  }

  friend bool operator==(const None& lhs, std::shared_ptr<None> rhs) {
    return rhs->equals(lhs);
  }

  friend bool operator==(const std::shared_ptr<Object>& lhs, const None& rhs) {
    return rhs.equals(*lhs);
  }

  friend bool operator==(const std::shared_ptr<Object>& lhs,
                         const std::shared_ptr<None>& rhs) {
    return rhs->equals(*lhs);
  }

  size_t hash() const override { return 0; }

  bool toBool() const override { return false; }
  bool operator!() const { return toBool(); }
  friend bool operator!(const std::shared_ptr<None>& none) {
    return !none->toBool();
  }

  bool isInstance(const std::string& type) const override {
    return type == "NoneType" || type == "object";
  }

  std::shared_ptr<Object> getAttr(const std::string& name) const override {
    throw std::runtime_error("'NoneType' object has no attribute '" + name +
                             "'");
  }

  void setAttr(const std::string& name,
               std::shared_ptr<Object> value) override {
    throw std::runtime_error("'NoneType' object has no attribute '" + name +
                             "'");
  }

  // Python-like comparison
  std::strong_ordering compare(const Object& other) const override {
    if (dynamic_cast<const None*>(&other)) {
      return std::strong_ordering::equal;
    }
    return std::strong_ordering::less;  // None is less than everything except
                                        // None
  }

  template <typename T>
  std::shared_ptr<Object> operator+(const T&) const {
    throw std::runtime_error(
        "unsupported operand type(s) for +: 'NoneType' and '" +
        std::string(typeid(T).name()) + "'");
  }

  template <typename T>
  std::shared_ptr<Object> operator-(const T&) const {
    throw std::runtime_error(
        "unsupported operand type(s) for -: 'NoneType' and '" +
        std::string(typeid(T).name()) + "'");
  }

  template <typename T>
  std::shared_ptr<Object> operator*(const T&) const {
    throw std::runtime_error(
        "unsupported operand type(s) for *: 'NoneType' and '" +
        std::string(typeid(T).name()) + "'");
  }

  template <typename T>
  std::shared_ptr<Object> operator/(const T&) const {
    throw std::runtime_error(
        "unsupported operand type(s) for /: 'NoneType' and '" +
        std::string(typeid(T).name()) + "'");
  }

  template <typename... Args>
  std::shared_ptr<Object> operator()(Args&&...) const {
    throw std::runtime_error("'NoneType' object is not callable");
  }

  template <typename T>
  std::shared_ptr<Object> operator[](const T&) const {
    throw std::runtime_error("'NoneType' object is not subscriptable");
  }
};

#endif  // NONE_HPP