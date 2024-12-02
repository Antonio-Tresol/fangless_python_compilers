//
// Created by joe on 11/19/24.
//

#ifndef TUPLE_HPP
#define TUPLE_HPP

#include <vector>
#include <concepts>
#include <ranges>

using std::views::iota;

#include "Number.hpp"
#include "Object.hpp"

template <typename T>
concept SharedObject = std::is_convertible<T, std::shared_ptr<Object>>::value;

class Tuple : public Object {
  const std::vector<std::shared_ptr<Object>> elements_;

 public:
  template <typename... Args>
      requires(SharedObject<Args> && ...)
  explicit Tuple(Args&&... args)
      : elements_{{
        std::static_pointer_cast<Object>(std::forward<Args>(args))...}} {}
  
  explicit Tuple(const std::vector<std::shared_ptr<Object>>& vec)
    : elements_(vec) {}

  explicit Tuple(auto begin, auto end) : elements_(begin, end) {}

  template <typename... Args>
    requires(SharedObject<Args> && ...)
  static std::shared_ptr<Tuple> spawn(Args&&... args) {
      std::vector<std::shared_ptr<Object>> elements{
          std::static_pointer_cast<Object>(std::forward<Args>(args))...
      };
      return std::make_shared<Tuple>(elements);
  }

  static std::shared_ptr<Tuple> spawn(
      std::initializer_list<std::shared_ptr<Object>> init) {
      return std::make_shared<Tuple>(
          std::vector<std::shared_ptr<Object>>(init.begin(), init.end()));
  }

  std::string type() const override { return "tuple"; }

  std::string toString() const override {
    std::string result = "(";
    bool first = true;

    for (const auto& element : elements_) {
      if (!first) result += ", ";
      result += element->toString();
      first = false;
    }

    return result + ")";
  }

  bool equals(const Object& other) const override {
    if (auto* ptr = dynamic_cast<const Tuple*>(&other)) {
      if (ptr->elements_.size() != elements_.size()) return false;

      for (auto index : iota(0, static_cast<int32_t>(elements_.size()))) {
        if (*ptr->elements_[index] != *elements_[index]) return false;
      }

      return true;
    }

    return false;
  }

  size_t hash() const override {
    std::size_t hash = 0;

    for (const auto& element : elements_) {
      try {
        hash ^= element->hash();
      } catch (...) {
        throw std::runtime_error(
            "An object in the Tuple is not hashable. Tuple is therefore not "
            "hashable.");
      }
    }

    return hash;
  }

  bool toBool() const override { return !elements_.empty(); }

  std::shared_ptr<Tuple> asTuple() const override {
    return std::make_shared<Tuple>(elements_);
  } 

  friend bool operator==(const Tuple& lhs, const Tuple& rhs) {
      return lhs.equals(rhs);
  }
  
  friend bool operator==(const std::shared_ptr<Tuple>& lhs, const std::shared_ptr<Tuple>& rhs) {
      return lhs->equals(*rhs);
  }
  
  friend bool operator==(const std::shared_ptr<Tuple>& lhs, const Tuple& rhs) {
      return lhs->equals(rhs);
  }
  
  friend bool operator==(const Tuple& lhs, const std::shared_ptr<Tuple>& rhs) {
      return rhs->equals(lhs);
  }
  
  friend bool operator==(const std::shared_ptr<Object>& lhs, const std::shared_ptr<Tuple>& rhs) {
      return rhs->equals(*lhs);
  }
  
  friend bool operator==(const std::shared_ptr<Object>& lhs, const Tuple& rhs) {
      return rhs.equals(*lhs);
  }

  bool operator!() const { return elements_.empty(); }

  friend bool operator!(const std::shared_ptr<Tuple>& tuple) {
    return tuple->operator!();
  }

  bool isInstance(const std::string& type) const override {
    return type == "tuple" || type == "object";
  }

  std::shared_ptr<Object> getAttr(const std::string& name) const override {
    throw std::runtime_error("'tuple' object has no attribute '" + name + "'");
  }

  void setAttr(const std::string& name,
               std::shared_ptr<Object> value) override {
    throw std::runtime_error("'tuple' object attributes are read-only");
  }

  auto begin() const { return elements_.begin(); }
  auto end() const { return elements_.end(); }

  auto cbegin() const { return elements_.cbegin(); }
  auto cend() const { return elements_.cend(); }

  auto rbegin() const { return elements_.rbegin(); }
  auto rend() const { return elements_.rend(); }

  const std::shared_ptr<Object>& operator[](
      const std::shared_ptr<Number>& index) const {
    return elements_[normalizeIndex(index->getInt())];
  }

  const std::shared_ptr<Object>& operator[](const Number& index) const {
    return elements_[normalizeIndex(index.getInt())];
  }

  std::shared_ptr<Number> index(std::shared_ptr<Object> object) const {
    for (auto i : iota(0, static_cast<int>(0, elements_.size()))) {
      if (*elements_[i] == *object) {
        return std::make_shared<Number>(i);
      }
    }
    const std::string err = std::string("Error Tuple::index: Could not find ") +
                            " could not find [" + object->toString() + "] in " +
                            toString();
    throw std::runtime_error(err);
  }

  std::shared_ptr<Number> count() const {
    return Number::spawn(static_cast<int>(elements_.size()));
  }

  std::shared_ptr<Number> len() const {
    return Number::spawn(static_cast<int>(elements_.size()));
  }

  // at() methods - same behavior as operator[] but clearer intent
  std::shared_ptr<Object> at(const Number& index) const {
    return operator[](index);
  }

  std::shared_ptr<Object> at(std::shared_ptr<Number> index) const {
    return operator[](*index);
  }

  auto operator[](const Slice& slice) const {
    int start = slice.start == INT_MAX ? 0 : slice.start;
    int end = slice.end == INT_MAX ? len()->getInt() : slice.end;
    int step = slice.step == 0 ?
      throw std::invalid_argument("Step cannot be zero") : slice.step;

    if (start < 0) start += len()->getInt();
    if (end < 0) end += len()->getInt();

    start = std::clamp(start, 0, static_cast<int>(len()->getInt()));
    end = std::clamp(end, 0, static_cast<int>(len()->getInt()));

    auto vector = std::vector<std::shared_ptr<Object>>();
    if (step > 0) {
        for (int i = start; i < end; i += step) {
            vector.push_back(elements_[i]);
        }
    } else {
        for (int i = start; i > end; i += step) {
            vector.push_back(elements_[i]);
        }
    }
    const size_t newSize = vector.size();

    return std::make_shared<Tuple>(vector);
  }

  auto slice(const Slice& slice) {
    return this->operator[](slice);
  }

  auto slice(std::shared_ptr<Slice> slice) {
    return this->operator[](*slice);
  }


  std::shared_ptr<Tuple> operator+(
      const Tuple& other) const {
    std::vector<std::shared_ptr<Object>> combined;
    combined.reserve(other.len()->getInt());

    // Combine elements from both tuples
    combined.insert(combined.end(), elements_.begin(), elements_.end());
    combined.insert(combined.end(), other.elements_.begin(),
                    other.elements_.end());

    return Tuple::from_vector(combined);
  }

  std::shared_ptr<Tuple> operator+(
      const std::shared_ptr<Tuple>& other) const {
    return (*this) + (*other);
  }

  static std::shared_ptr<Tuple> from_vector(
      const std::vector<std::shared_ptr<Object>>& vec) {
    return std::make_shared<Tuple>(vec);
  }

  friend std::ostream& operator<<(std::ostream& os,
                         const std::shared_ptr<Tuple>& obj) {
    return os << *obj;
  }

  friend std::shared_ptr<Tuple> operator+(
      const std::shared_ptr<Tuple>& a,
      const std::shared_ptr<Tuple>& b) {
    return *a + *b;
  }

 private:
  int normalizeIndex(int index) const {
    if (index < 0) index += len()->getInt();
    if (index < 0 || index >= len()->getInt()) {
      throw std::runtime_error("Index out of bounds error");
    }
    return index;
  }
};



#endif  // TUPLE_HPP
