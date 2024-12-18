#ifndef OBJECT_HPP
#define OBJECT_HPP

#include <iostream>
#include <memory>
#include <string>
#include <compare>

class Tuple;

// an object interface to mimic python type behaviour
class Object {
 public:
  size_t id_ {};
  
  Object() {
    static size_t idCounter = 0;
    id_ = idCounter++;
  }

  virtual ~Object() = default;

  template <typename T>
  static std::shared_ptr<Object> spawn() {
    static_assert(std::is_base_of<Object, T>::value,
                  "T must inherit from Object");
    return std::make_shared<T>();
  }

  virtual std::string type() const = 0;

  virtual std::string toString() const = 0;

  virtual bool equals(const Object& other) const = 0;

  virtual size_t hash() const = 0;

  virtual bool toBool() const = 0;

  virtual bool isInstance(const std::string& type) const = 0;

  virtual std::shared_ptr<Object> getAttr(const std::string& name) const = 0;

  virtual void setAttr(const std::string& name,
                       std::shared_ptr<Object> value) = 0;

  bool isNone() const { return type() == "None"; }

  virtual std::shared_ptr<Tuple> asTuple() const {
    throw std::runtime_error("Cannot convert to tuple");
  } 

  // explicit operator bool() const { return toBool(); }
  // operator std::string() const { return toString(); }

  friend bool operator!(const std::shared_ptr<Object>& obj) {
    return !obj->toBool();
  }

  virtual std::strong_ordering compare(const Object& other) const {
    return toString() <=> other.toString();
  }

  virtual std::strong_ordering compare(
      const std::shared_ptr<Object>& other) const {
    return compare(*other);
  }

  std::strong_ordering operator<=>(std::shared_ptr<Object> other) const {
    return compare(*other);
  }

  std::strong_ordering operator<=>(const Object& other) const {
    if (type() != other.type()) return Object::compare(other);
    return compare(other);
  }

  friend std::strong_ordering operator<=>(const std::shared_ptr<Object>& lhs,
                                          const std::shared_ptr<Object>& rhs) {
    return lhs->compare(*rhs);
  }

  bool operator==(const Object& other) const { return equals(other); }

  bool operator==(const std::shared_ptr<Object>& other) const {
    return equals(*other);
  }

  bool operator==(const bool& other) const {
    return toBool() == other;
  }

  bool operator!=(const bool other) const {
    return toBool() != other;
  }

  friend bool operator==(const std::shared_ptr<Object>& lhs,
                         const Object& rhs) {
    return rhs.equals(*lhs);
  }

  friend bool operator==(const std::shared_ptr<Object>& lhs,
                         const std::shared_ptr<Object>& rhs) {
    return rhs->equals(*lhs);
  }

  friend bool operator==(const std::shared_ptr<Object>& lhs,
                         const bool& rhs) {
    return lhs->toBool() == rhs;
  }

  friend bool operator==(const bool& lhs,
                         const std::shared_ptr<Object>& rhs) {
    return rhs->toBool() == lhs;
  }

  friend bool operator==(const bool& lhs,
                         const Object& rhs) {
    return rhs.toBool() == lhs;
  }

  friend bool operator!=(const std::shared_ptr<Object>& lhs,
                         const bool& rhs) {
    return lhs->toBool() != rhs;
  }

  friend bool operator!=(const bool& lhs,
                         const std::shared_ptr<Object>& rhs) {
    return rhs->toBool() != lhs;
  }

  friend bool operator!=(const bool& lhs,
                         const Object& rhs) {
    return rhs.toBool() != lhs;
  }

  friend std::ostream& operator<<(std::ostream& os, const Object& obj) {
    os << obj.toString();
    return os;
  }
};

std::ostream& operator<<(std::ostream& os, const std::shared_ptr<Object>& obj) {
  return os << *obj;
}

#endif
