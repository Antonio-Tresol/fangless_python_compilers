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
#include "Tuple.hpp"

class Set final : public Object {
  std::set<std::shared_ptr<Object>, ObjectComparator> elements_ {};

 public:
  Set() = default;

  Set(std::initializer_list<std::shared_ptr<Object>> init) : elements_(init) {}

  static std::shared_ptr<Set> spawn() { return std::make_shared<Set>(); }

  static std::shared_ptr<Set> spawn(
      std::initializer_list<std::shared_ptr<Object>> init) {
    return std::make_shared<Set>(init);
  }

  std::string type() const override { return "Set"; }

  std::string toString() const override {
    if (elements_.empty()) {
      return "set()";
    }

    std::string result = "{";
    bool first = true;

    for (const auto& element : elements_) {
      if (!first) result += ", ";
      result += element->toString();
      first = false;
    }

    return result + "}";
  };

  std::shared_ptr<Tuple> asTuple() const override {
    return std::make_shared<Tuple>(elements_.begin(), elements_.end());
  }

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

  std::strong_ordering compare(const Object& other) const override {
    // If types differ, fall back to base comparison
    if (type() != other.type()) {
      return Object::compare(other);
    }

    const auto* other_set = dynamic_cast<const Set*>(&other);
    if (!other_set) {
      return std::strong_ordering::less;  // Consistent ordering for different
                                          // types
    }

    // Transform sets into maps for comparison
    std::map<std::shared_ptr<Object>, std::shared_ptr<Object>, ObjectComparator>
        this_map;
    std::map<std::shared_ptr<Object>, std::shared_ptr<Object>, ObjectComparator>
        other_map;

    // Fill maps
    std::ranges::transform(elements_, std::inserter(this_map, this_map.end()),
                           [](const std::shared_ptr<Object>& element) {
                             return std::make_pair(element, element);
                           });
    std::ranges::transform(other_set->elements_,
                           std::inserter(other_map, other_map.end()),
                           [](const std::shared_ptr<Object>& element) {
                             return std::make_pair(element, element);
                           });

    // Compare sizes
    if (auto size_cmp = this_map.size() <=> other_map.size();
        size_cmp != std::strong_ordering::equal) {
      return size_cmp;
    }

    // Compare elements lexicographically
    auto it1 = this_map.begin();
    auto it2 = other_map.begin();

    while (it1 != this_map.end()) {
      if (auto cmp = (*it1->first) <=> (*it2->first);
          cmp != std::strong_ordering::equal) {
        return cmp;
      }
      ++it1;
      ++it2;
    }

    return std::strong_ordering::equal;
  }

  friend bool operator==(const Set& lhs, const Set& rhs) {
    return lhs.equals(rhs);
  }

  friend bool operator==(std::shared_ptr<Set> lhs, std::shared_ptr<Set> rhs) {
    return lhs->equals(*rhs);
  }

  friend bool operator==(std::shared_ptr<Set> lhs, const Set& rhs) {
    return lhs->equals(rhs);
  }

  friend bool operator==(const Set& lhs, std::shared_ptr<Set> rhs) {
    return rhs->equals(lhs);
  }

  friend bool operator==(const std::shared_ptr<Object>& lhs, const Set& rhs) {
    return rhs.equals(*lhs);
  }

  friend bool operator==(const std::shared_ptr<Object>& lhs,
                         const std::shared_ptr<Set>& rhs) {
    return rhs->equals(*lhs);
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

  bool operator!() const { return elements_.empty(); }

  friend bool operator!(const std::shared_ptr<Set>& set) {
    return set->operator!();
  }

  bool isInstance(const std::string& type) const override {
    return type == "set" || type == "object";
  }

  std::shared_ptr<Object> getAttr(const std::string& name) const override {
    throw std::runtime_error("'set' object has no attribute '" + name + "'");
  }

  void setAttr(const std::string&,
               std::shared_ptr<Object>) override {
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

  auto rbegin() { return elements_.rbegin(); }
  auto rend() { return elements_.rend(); }
  auto rbegin() const { return elements_.rbegin(); }
  auto rend() const { return elements_.rend(); }

  // set functions
  std::shared_ptr<Number> count() const {
    return Number::spawn(static_cast<int64_t>(elements_.size()));
  }

  std::shared_ptr<Number> len() const {
    return Number::spawn(static_cast<int64_t>(elements_.size()));
  }

  bool exists(const std::shared_ptr<Object>& obj) const {
    return elements_.contains(obj);
  }

  void add(const std::shared_ptr<Object>& obj) { elements_.insert(obj); }

  std::shared_ptr<Object> pop() {
    std::shared_ptr<Object> object = *(std::prev(elements_.end()));
    elements_.erase(std::prev(elements_.end()));

    return object;
  }

  void discard(std::shared_ptr<Object> object) {
    auto it = std::find(elements_.begin(), elements_.end(), object);

    if (it != elements_.end()) {
      elements_.erase(it);
    }
  }

  void remove(std::shared_ptr<Object> object) {
    auto it = std::find(elements_.begin(), elements_.end(), object);

    if (it != elements_.end()) {
      elements_.erase(it);
    } else {
      throw std::runtime_error(object->toString() + " not in set");
    }
  }

  void clear() { elements_.clear(); }

  std::shared_ptr<Set> copy() {
    auto copyElement = std::make_shared<Set>();
    copyElement->elements_ = elements_;
    return copyElement;
  }

  bool isdisjoint(const Set& other) const { return !(*this & other)->count(); }

  bool isdisjoint(const std::shared_ptr<Set> other) {
    return !((*this & *other)->count());
  }
  
  std::shared_ptr<Set> difference(const Set& other) const {
    auto result = std::make_shared<Set>();
    std::vector<std::shared_ptr<Object>> temp;

    std::ranges::set_difference(elements_, other.elements_,
                                std::back_inserter(temp));
    result->elements_.insert(temp.begin(), temp.end());
    return result;
  }

  std::shared_ptr<Set> difference(const std::shared_ptr<Set>& other) const {
    return difference(*other);
  }

  std::shared_ptr<Set> intersection(const Set& other) const {
    auto result = std::make_shared<Set>();
    std::vector<std::shared_ptr<Object>> temp;

    std::ranges::set_intersection(elements_, other.elements_,
                                  std::back_inserter(temp));
    result->elements_.insert(temp.begin(), temp.end());
    return result;
  }

  std::shared_ptr<Set> intersection(const std::shared_ptr<Set>& other) const {
    return intersection(*other);
  }

  std::shared_ptr<Set> symmetric_difference(const Set& other) const {
    auto result = std::make_shared<Set>();
    std::vector<std::shared_ptr<Object>> temp;

    std::ranges::set_symmetric_difference(elements_, other.elements_,
                                          std::back_inserter(temp));
    result->elements_.insert(temp.begin(), temp.end());
    return result;
  }

  std::shared_ptr<Set> symmetric_difference(const std::shared_ptr<Set>& other)
    const {
    return symmetric_difference(*other);
  }

  std::shared_ptr<Set> union_(const Set& other) const {
    auto result = std::make_shared<Set>();
    std::vector<std::shared_ptr<Object>> temp;

    std::ranges::set_union(elements_, other.elements_,
                           std::back_inserter(temp));
    result->elements_.insert(temp.begin(), temp.end());
    return result;
  }

  std::shared_ptr<Set> union_(const std::shared_ptr<Set>& other) const {
    return union_(*other);
  }

  void update(const Set& first) {
      if (&first != this) {
          auto copy = first;
          *this |= copy;
      }
  }

  template <typename... Sets>
  void update(const Set& first, const Sets&... rest) {
      update(first);
      update(rest...);
  }

  void update(const std::shared_ptr<Set>& first) {
      if (first.get() != nullptr && (first.get() != this)) {
          auto copy = *first;
          *this |= copy;
      }
  }

  template <typename... Sets>
  void update(const std::shared_ptr<Set>& first, const Sets&... rest) {
      update(first);
      update(rest...);
  }

  void update() {}

  bool issubset(const std::shared_ptr<Set> other) {
    return !((*this - *other)->count());
  }

  bool issuperset(const std::shared_ptr<Set> other) {
    return !((*other - *this)->count());
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

  bool operator<=(const Set& other) const { return !(*this - other)->count(); }

  bool operator<(const Set& other) const {
    return (*this <= other) && *this != other;
  }

  bool operator>=(const Set& other) const { return !(other - *this)->count(); }

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
    return std::shared_ptr<Set>(this, [](Set*) {});
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
    return std::shared_ptr<Set>(this, [](Set*) {});
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
    return std::shared_ptr<Set>(this, [](Set*) {});
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
    return std::shared_ptr<Set>(this, [](Set*) {});
  }

  friend std::ostream& operator<<(std::ostream& os,
                                  const std::shared_ptr<Set>& obj) {
    return os << *obj;
  }

  friend std::shared_ptr<Set> operator|(const std::shared_ptr<Set>& a,
                                        const std::shared_ptr<Set>& b) {
    return *a | *b;
  }

  friend std::shared_ptr<Set> operator+(const std::shared_ptr<Set>& a,
                                        const std::shared_ptr<Set>& b) {
    return *a | *b;
  }

  friend std::shared_ptr<Set> operator&(const std::shared_ptr<Set>& a,
                                        const std::shared_ptr<Set>& b) {
    return *a & *b;
  }

  friend std::shared_ptr<Set> operator^(const std::shared_ptr<Set>& a,
                                        const std::shared_ptr<Set>& b) {
    return *a ^ *b;
  }

  friend std::shared_ptr<Set> operator-(const std::shared_ptr<Set>& a,
                                        const std::shared_ptr<Set>& b) {
    return *a - *b;
  }

  friend std::shared_ptr<Set> operator+=(const std::shared_ptr<Set>& a,
                                         const std::shared_ptr<Set>& b) {
    return *a |= *b;
  }

  friend std::shared_ptr<Set> operator-=(const std::shared_ptr<Set>& a,
                                         const std::shared_ptr<Set>& b) {
    return *a -= *b;
  }

  friend std::shared_ptr<Set> operator^=(const std::shared_ptr<Set>& a,
                                         const std::shared_ptr<Set>& b) {
    return *a ^= *b;
  }

  friend std::shared_ptr<Set> operator&=(const std::shared_ptr<Set>& a,
                                         const std::shared_ptr<Set>& b) {
    return *a &= *b;
  }

  friend std::shared_ptr<Set> operator|(const std::shared_ptr<Set>& a,
                                        const Set& b) {
    return *a | b;
  }

  friend std::shared_ptr<Set> operator+(const std::shared_ptr<Set>& a,
                                        const Set& b) {
    return *a | b;
  }

  friend std::shared_ptr<Set> operator&(const std::shared_ptr<Set>& a,
                                        const Set& b) {
    return *a & b;
  }

  friend std::shared_ptr<Set> operator^(const std::shared_ptr<Set>& a,
                                        const Set& b) {
    return *a ^ b;
  }

  friend std::shared_ptr<Set> operator-(const std::shared_ptr<Set>& a,
                                        const Set& b) {
    return *a - b;
  }

  friend std::shared_ptr<Set> operator+=(const std::shared_ptr<Set>& a,
                                         const Set& b) {
    return *a |= b;
  }

  friend std::shared_ptr<Set> operator-=(const std::shared_ptr<Set>& a,
                                         const Set& b) {
    return *a -= b;
  }

  friend std::shared_ptr<Set> operator^=(const std::shared_ptr<Set>& a,
                                         const Set& b) {
    return *a ^= b;
  }

  friend std::shared_ptr<Set> operator&=(const std::shared_ptr<Set>& a,
                                         const Set& b) {
    return *a &= b;
  }
};

#endif  // SET_HPP
