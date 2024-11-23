//
// Created by joe on 11/20/24.
//

#ifndef SET_HPP
#define SET_HPP

#include <algorithm>
#include <ranges>
#include <set>

#include "Iterable.hpp"
#include "Object.hpp"

class Set final : public Object {
  std::set<std::shared_ptr<Object>, ObjectComparator> elements_{};

 public:
  std::string type() const override { return "Set"; }
  static std::shared_ptr<Set> spawn() { return std::make_shared<Set>(); }
  std::string toString() const override {
    std::string result = "{";
    bool first = true;

    for (const auto& element : elements_) {
      if (!first) result += ", ";
      result += element->toString();
      first = false;
    }

    return result + "}";
  };
  Number len() const { return Number(static_cast<int>(elements_.size())); }
  bool equals(const Object& other) const override {
    auto* otherPtr = dynamic_cast<const Set*>(&other);
    if (!otherPtr) return false;

    std::map<std::shared_ptr<Object>, std::shared_ptr<Object>, ObjectComparator>
        elements;
    std::ranges::transform(elements_, std::inserter(elements, elements.end()),
                           [](const std::shared_ptr<Object>& element) {
                             return std::make_pair(element, element);
                           });

    const size_t size = elements.size();
    for (const auto& object : otherPtr->elements_) {
      elements[object] = object;
    }

    return size == elements.size();
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

  bool isInstance(const std::string& type) const override {
    return type == "set" || type == "object";
  }

  std::shared_ptr<Object> getAttr(const std::string& name) const override {
    throw std::runtime_error("'set' object has no attribute '" + name + "'");
  }

  void setAttr(const std::string& name,
               std::shared_ptr<Object> value) override {
    throw std::runtime_error("'set' object attributes are read-only");
  }

  // STL enabling methods for use with algorithms
  auto begin() { return elements_.begin(); }
  auto end() { return elements_.end(); }

  // Const iterator support
  auto begin() const { return elements_.begin(); }
  auto end() const { return elements_.end(); }

  auto cbegin() const { return elements_.cbegin(); }
  auto cend() const { return elements_.cend(); }

  // set functions
  size_t count() const { return elements_.size(); }

  bool exists(const std::shared_ptr<Object>& obj) const {
    return elements_.contains(obj);
  }

  void add(const std::shared_ptr<Object>& obj) { elements_.insert(obj); }

  void discard(std::shared_ptr<Object> object) {
    auto it = std::find(elements_.begin(), elements_.end(), object);

    if (it != elements_.end()) {
      elements_.erase(it);
    }
  }

  std::shared_ptr<Object> pop() {
    std::shared_ptr<Object> object = *(std::prev(elements_.end()));
    elements_.erase(std::prev(elements_.end()));

    return object;
  }

  void remove(std::shared_ptr<Object> object) {
    auto it = std::find(elements_.begin(), elements_.end(), object);

    if (it != elements_.end()) {
      elements_.erase(it);
    } else {
      throw std::runtime_error(object->toString() + " not in set");
    }
  }

  bool isDisjoint(const std::shared_ptr<Set> other) {
    return !((*this & *other)->count());
  }

  bool operator<=(const std::shared_ptr<Set> other) {
    return !((*this - *other)->count());
  }

  bool operator<(const std::shared_ptr<Set> other) {
    return (*this <= *other) && *this != *other;
  }

  bool operator>=(const std::shared_ptr<Set> other) {
    return !((*other - *this)->count());
  }

  bool operator>(const std::shared_ptr<Set> other) {
    return (*this >= other) && *this != *other;
  }

  bool isDisjoint(const Set& other) const {
      return !(*this & other)->count();
  }
  
  bool operator<=(const Set& other) const {
      return !(*this - other)->count();
  }
  
  bool operator<(const Set& other) const {
      return (*this <= other) && *this != other;
  }
  
  bool operator>=(const Set& other) const {
      return !(other - *this)->count();
  }
  
  bool operator>(const Set& other) const {
      return (*this >= other) && *this != other;
  } 
  std::shared_ptr<Set> operator|(const Set& other) const {
    auto result = std::make_shared<Set>();
    std::vector<std::shared_ptr<Object>> temp;

    std::ranges::set_union(elements_, other.elements_,
                           std::back_inserter(temp));
    result->elements_.insert(temp.begin(), temp.end());
    return result;
  }

  std::shared_ptr<Set> operator|=(const Set& other) {
    std::vector<std::shared_ptr<Object>> temp;

    std::ranges::set_union(elements_, other.elements_,
                           std::back_inserter(temp));

    elements_.clear();
    elements_.insert(temp.begin(), temp.end());
    return std::shared_ptr<Set>(this);
  }

  std::shared_ptr<Set> operator&(const Set& other) const {
    auto result = std::make_shared<Set>();
    std::vector<std::shared_ptr<Object>> temp;

    std::ranges::set_intersection(elements_, other.elements_,
                                  std::back_inserter(temp));
    result->elements_.insert(temp.begin(), temp.end());
    return result;
  }
  std::shared_ptr<Set> operator&=(const Set& other) {
    std::vector<std::shared_ptr<Object>> temp;

    std::ranges::set_intersection(elements_, other.elements_,
                                  std::back_inserter(temp));
    elements_.clear();
    elements_.insert(temp.begin(), temp.end());
    return std::shared_ptr<Set>(this);
  }

  std::shared_ptr<Set> operator^(const Set& other) const {
    auto result = std::make_shared<Set>();
    std::vector<std::shared_ptr<Object>> temp;

    std::ranges::set_symmetric_difference(elements_, other.elements_,
                                          std::back_inserter(temp));
    result->elements_.insert(temp.begin(), temp.end());
    return result;
  }

  std::shared_ptr<Set> operator^=(const Set& other) {
    std::vector<std::shared_ptr<Object>> temp;

    std::ranges::set_symmetric_difference(elements_, other.elements_,
                                          std::back_inserter(temp));
    elements_.clear();
    elements_.insert(temp.begin(), temp.end());
    return std::shared_ptr<Set>(this);
  }

  std::shared_ptr<Set> operator-(const Set& other) const {
    auto result = std::make_shared<Set>();
    std::vector<std::shared_ptr<Object>> temp;

    std::ranges::set_difference(elements_, other.elements_,
                                std::back_inserter(temp));
    result->elements_.insert(temp.begin(), temp.end());
    return result;
  }

  std::shared_ptr<Set> operator-=(const Set& other) {
    std::vector<std::shared_ptr<Object>> temp;
    std::ranges::set_difference(elements_, other.elements_,
                                std::back_inserter(temp));
    elements_.clear();
    elements_.insert(temp.begin(), temp.end());
    return std::shared_ptr<Set>(this);
  }

  void clear() { elements_.clear(); }
};

#endif  // SET_HPP
