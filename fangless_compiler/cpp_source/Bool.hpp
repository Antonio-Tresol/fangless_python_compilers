#ifndef BOOL_HPP
#define BOOL_HPP

#include <memory>
#include "Object.hpp"


class Bool : public Object {
    bool value_;
public:
    Bool(bool value_) : value_(value_) {}

    Bool(int value_) : value_(bool(value_)) {}
    Bool(Object& obj) : value_(obj.toBool()) {}
    Bool(std::shared_ptr<Object> obj) : value_(obj->toBool()) {}
    
    static std::shared_ptr<Bool> spawn(bool value_) {
        return std::make_shared<Bool>(value_);
    }

    std::string type () const override {
        return "Bool";
    }
    
    std::string toString() const override {
        return value_ ? "True" : "False";
    }

    bool equals(const Object& other) const override {
        if (other.type() != "Bool") return false;

        auto* otherBool = dynamic_cast<const Bool*>(&other);

        return value_ == otherBool->value_;
    }

    size_t hash() const override {
        return std::hash<bool>{}(value_);
    }

    bool toBool() const override {
        return value_;
    }

    bool isInstance(const std::string& type) const override {
        return type == "Bool" || type == "Object";
    }

    std::shared_ptr<Object> getAttr(const std::string& name) const override {
        throw std::runtime_error("'Bool' object has no attributes");
    }

    void setAttr(const std::string& name, std::shared_ptr<Object> value) override {
        throw std::runtime_error("'Bool' object has no attributes");
    }

    std::strong_ordering compare(const Object& other) const override {
        if (other.type() != "Bool") return std::strong_ordering::less;

        auto* otherBool = dynamic_cast<const Bool*>(&other);

        return value_ <=> otherBool->value_;
    }
};

#endif // BOOL_HPP