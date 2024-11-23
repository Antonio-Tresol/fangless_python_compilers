#ifndef OBJECT_HPP
#define OBJECT_HPP

#include <iostream>
#include <memory>
#include <string>

// an object interface to mimic python type behaviour
class Object {
 public:
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

  bool operator==(const Object& other) const { return equals(other); }
  explicit operator bool() const { return toBool(); }

  virtual std::strong_ordering compare(const Object& other) const {
    return toString() <=> other.toString();
  }

  std::strong_ordering operator<=>(std::shared_ptr<Object> other) const {
    return compare(*other);
  }

  std::strong_ordering operator<=>(const Object& other) const {
    if (type() != other.type()) return Object::compare(other);
    return compare(other);
  }

  friend std::ostream& operator<<(std::ostream& os, const Object& obj) {
    os << obj.toString();
    return os;
  }

  bool isNone() const {
    return type() == "None";
  }
};

#endif
