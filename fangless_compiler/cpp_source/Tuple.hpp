//
// Created by joe on 11/19/24.
//

#ifndef TUPLE_HPP
#define TUPLE_HPP

#include <array>
#include <concepts>
#include <ranges>

using std::views::iota;

#include "Number.hpp"
#include "Object.hpp"

template <typename T>
concept SharedObject = std::is_convertible<T, std::shared_ptr<Object>>::value;

template <std::size_t ElementAmount>
class Tuple final : public Object {
  const std::array<std::shared_ptr<Object>, ElementAmount> elements_;

 public:
  template <typename... Args>
    requires(SharedObject<Args> && ...)
  explicit Tuple(Args... args) : elements_{args...} {
    static_assert(sizeof...(Args) == ElementAmount,
                  "Wrong number of arguments");
  }

  template <typename... Args>
    requires(SharedObject<Args> && ...)
  static std::shared_ptr<Tuple<sizeof...(Args)>> spawn(Args... args) {
    return std::make_shared<Tuple<sizeof...(Args)>>(args...);
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

  // Python truthiness
  bool toBool() const override { return !elements_.empty(); }

  bool isinstance(const std::string& type) const override {
    return type == "tuple" || type == "object";
  }

  std::shared_ptr<Number> index(std::shared_ptr<Object> object) const {
    for (auto i : iota(0, static_cast<int>(0, elements_.size()))) {
      if (*elements_[i] == *object) {
        return std::make_shared<Number>(i);
      }
    }
    const std::string err = std::string("Error Tuple::index: Coudl not find ") +
                            " could not find [" + object->toString() + "] in " +
                            toString();
    throw std::runtime_error(err);
  }

  std::shared_ptr<Number> count() const {
    return std::make_shared<Number>(static_cast<int>(elements_.size()));
  }

  std::shared_ptr<Number> len() const {
    return std::make_shared<Number>(static_cast<int>(elements_.size()));
  }

  std::shared_ptr<Object> getAttr(const std::string& name) const override {
    throw std::runtime_error("'tuple' object has no attribute '" + name + "'");
  }

  void setAttr(const std::string& name,
               std::shared_ptr<Object> value) override {
    throw std::runtime_error("'tuple' object attributes are read-only");
  }

  auto begin() { return elements_.begin(); }
  auto end() { return elements_.end(); }

  auto begin() const { return elements_.begin(); }
  auto end() const { return elements_.end(); }

  auto cbegin() const { return elements_.cbegin(); }
  auto cend() const { return elements_.cend(); }

  const std::shared_ptr<const Object> operator[](
      const std::shared_ptr<Number>& index) const {
    return elements_[normalizeIndex(index->getInt())];
  }

  const std::shared_ptr<const Object> operator[](const Number& index) const {
    return elements_[normalizeIndex(index.getInt())];
  }

  // at() methods - same behavior as operator[] but clearer intent
  const std::shared_ptr<const Object> at(const Number& index) const {
    return operator[](index);
  }

  const std::shared_ptr<const Object> at(std::shared_ptr<Number> index) const {
    return operator[](*index);
  }
  template <size_t NewSize>
  std::shared_ptr<Tuple<NewSize>> operator[](const Slice& slice) const {
    int start = slice.start;
    int end = slice.end;

    if (start == INT_MAX) start = 0;
    if (end == INT_MAX) end = ElementAmount;

    if (start < 0) start += ElementAmount;
    if (end < 0) end += ElementAmount;

    start = std::clamp(start, 0, static_cast<int>(ElementAmount));
    end = std::clamp(end, 0, static_cast<int>(ElementAmount));

    if (start >= end) {
      return std::make_shared<Tuple<0>>();
    }

    auto result = std::make_shared<Tuple<NewSize>>();
    for (int i = start; i < end && i < static_cast<int>(ElementAmount); ++i) {
      result->elements_[i - start] = elements_[i];
    }

    return result;
  }

  std::shared_ptr<Tuple<ElementAmount>> slice(const Slice& slice) const {
    int start = slice.start;
    int end = slice.end;

    if (start == INT_MAX) start = 0;
    if (end == INT_MAX) end = ElementAmount;

    if (start < 0) start += ElementAmount;
    if (end < 0) end += ElementAmount;

    start = std::clamp(start, 0, static_cast<int>(ElementAmount));
    end = std::clamp(end, 0, static_cast<int>(ElementAmount));

    auto result = std::make_shared<Tuple<ElementAmount>>();
    for (int i = start; i < end; ++i) {
      result->elements_[i - start] = elements_[i];
    }

    return result;
  }

 private:
  int normalizeIndex(int index) const {
    if (index < 0) index += ElementAmount;
    if (index < 0 || index >= ElementAmount) {
      throw std::runtime_error("Index out of bounds error");
    }
    return index;
  }
};

#endif  // TUPLE_HPP
