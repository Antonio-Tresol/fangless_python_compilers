//
// Created by joe on 11/20/24.
//

#ifndef SET_HPP
#define SET_HPP

#include <algorithm>
#include <set>
#include <ranges>

#include "Object.hpp"
#include "Iterable.hpp"


class Set final : public Object
{
    std::set<std::shared_ptr<Object>, ObjectComparator> elements_ {};
public:
    std::string type() const override { return "Set"; }

    std::string toString() const override
    {
        std::string result = "{";
        bool first = true;

        for (const auto& element : elements_) {
            if (!first) result += ", ";
            result += element->toString();
            first = false;
        }

        return result + "}";
    };

    bool equals(const Object& other) const override {
        auto* otherPtr = dynamic_cast<const Set*>(&other);
        if (!otherPtr) return false;

        std::map<std::shared_ptr<Object>, std::shared_ptr<Object>, ObjectComparator> elements;
        std::ranges::transform(elements_,
                               std::inserter(elements, elements.end()),
                               [](const std::shared_ptr<Object>& element)
                               {
                                   return std::make_pair(element, element);
                               });

        const size_t size = elements.size();
        for (const auto& object : otherPtr->elements_)
        {
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
                throw std::runtime_error("An object in the Tuple is not hashable. Tuple is therefore not hashable.");
            }
        }

        return hash;
    }

    bool toBool() const override { return !elements_.empty(); }

    bool isinstance(const std::string& type) const override {
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
    size_t size() const { return elements_.size(); }

    bool exists(const std::shared_ptr<Object>& obj) const
    {
        return elements_.contains(obj);
    }

    void add(const std::shared_ptr<Object>& obj)
    {
        elements_.insert(obj);
    }

    std::shared_ptr<Set> operator|(const Set& other) const {
        auto result = std::make_shared<Set>();
        std::vector<std::shared_ptr<Object>> temp;

        std::ranges::set_union(elements_, other.elements_, std::back_inserter(temp));
        result->elements_.insert(temp.begin(), temp.end());
        return result;
    }

    std::shared_ptr<Set> operator&(const Set& other) const {
        auto result = std::make_shared<Set>();
        std::vector<std::shared_ptr<Object>> temp;

        std::ranges::set_intersection(elements_, other.elements_, std::back_inserter(temp));
        result->elements_.insert(temp.begin(), temp.end());
        return result;
    }

    std::shared_ptr<Set> operator^(const Set& other) const {
        auto result = std::make_shared<Set>();
        std::vector<std::shared_ptr<Object>> temp;

        std::ranges::set_symmetric_difference(elements_, other.elements_, std::back_inserter(temp));
        result->elements_.insert(temp.begin(), temp.end());
        return result;
    }

    std::shared_ptr<Set> operator-(const Set& other) const {
        auto result = std::make_shared<Set>();
        std::vector<std::shared_ptr<Object>> temp;

        std::ranges::set_difference(elements_, other.elements_, std::back_inserter(temp));
        result->elements_.insert(temp.begin(), temp.end());
        return result;
    }

    void clear() { elements_.clear(); }
};

#endif //SET_HPP
