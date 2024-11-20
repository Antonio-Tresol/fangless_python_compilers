//
// Created by joe on 11/19/24.
//

#ifndef TUPLE_HPP
#define TUPLE_HPP

#include <array>
#include <concepts>

#include "Object.hpp"

template <typename T>
concept SharedObject = std::is_convertible<T, std::shared_ptr<Object>>::value;

template <std::size_t ElementAmount>
class Tuple final : public Object {
    std::array<std::shared_ptr<Object>, ElementAmount> elements_;

public:
    template <typename... Args>
        requires (SharedObject<Args>&&...)
    explicit Tuple(Args... args) : elements_{args...} {
        static_assert(sizeof...(Args) == ElementAmount, "Wrong number of arguments");
    }

    std::string type() const override { return "tuple"; }

    std::string toString() const override {
        std::string result = "{";
        bool first = true;

        for (const auto& element : elements_) {
            if (!first) result += ", ";
            result += element->toString();
            first = false;
        }

        return result + "}";
    }

    bool equals(const Object& other) const override {
        if (auto* ptr = dynamic_cast<const Tuple*>(&other)) {
            return elements_ == ptr->elements_;
        }

        return false;
    }

    size_t hash() const override {
        std::size_t hash = 0;

        for (const auto& element : elements_) {
            try {
                hash ^= element->hash();
            } catch (...) {
               throw std::runtime_error("An object in the Tuple is not hashable. Tuple is therefore not hashable.");
            }
        }

        return hash;
    }

    // Python truthiness
    bool toBool() const override { return !elements_.empty(); }

    bool isinstance(const std::string& type) const override {
        return type == "tuple" || type == "object";
    }

    std::shared_ptr<Object> getAttr(const std::string& name) const override {
        throw std::runtime_error("'tuple' object has no attribute '" + name + "'");
    }

    void setAttr(const std::string& name,
                         std::shared_ptr<Object> value) override {
        throw std::runtime_error("'tuple' object attributes are read-only");
    }

    // STL enabling methods for use with algorithms
    auto begin() { return elements_.begin(); }
    auto end() { return elements_.end(); }

    // Const iterator support
    auto begin() const { return elements_.begin(); }
    auto end() const { return elements_.end(); }

    auto cbegin() const { return elements_.cbegin(); }
    auto cend() const { return elements_.cend(); }

    const std::shared_ptr<const Object> operator[](const size_t index) const {
        if (index >= ElementAmount) return std::shared_ptr<Object>(nullptr);
        return elements_[index];
    }

    size_t size() const { return elements_.size(); }
};

#endif //TUPLE_HPP
