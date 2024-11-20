#ifndef OBJECT_HPP
#define OBJECT_HPP

#include <iostream>  // Add this include for std::ostream
#include <memory>
#include <string>

// an object interface to mimic python type behaviour
class Object {
 public:
  virtual ~Object() = default;

  virtual std::string type() const = 0;

  virtual std::string toString() const = 0;  // __str__

  virtual bool equals(const Object& other) const = 0;  // __eq__
  virtual size_t hash() const = 0;                     // __hash__

  // Python truthiness
  virtual bool toBool() const = 0;  // __bool__

  virtual bool isinstance(const std::string& type) const = 0;

  virtual std::shared_ptr<Object> getAttr(const std::string& name) const = 0;
  virtual void setAttr(const std::string& name,
                       std::shared_ptr<Object> value) = 0;

  bool operator==(const Object& other) const
  {
      return equals(other);
  }

  explicit operator bool() const { return toBool(); }

  virtual std::strong_ordering compare(const Object& other) const
  {
      return toString() <=> other.toString();
  }

  std::strong_ordering operator<=>(const Object& other) const
  {
      if (type() != other.type()) return Object::compare(other);
      return compare(other);
  }

  // Add iostream operator
  friend std::ostream& operator<<(std::ostream& os, const Object& obj) {
    os << obj.toString();
    return os;
  }
};

#endif  // OBJECT_HPP
