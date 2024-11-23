#ifndef CLASS_HPP
#define CLASS_HPP

#include <functional>
#include <unordered_map>
#include <vector>

#include "Function.hpp"
#include "None.hpp"
#include "Object.hpp"

class Class : public Object, public std::enable_shared_from_this<Class> {
 private:
  std::string className_;
  std::shared_ptr<Class> parent_;
  std::unordered_map<std::string, std::shared_ptr<Object>> attributes_;
  bool isInstantiated_ = false;

 public:
  explicit Class(const std::string& className,
                 std::shared_ptr<const Class> baseClass = nullptr,
                 bool isInstantiated = false)
      : className_(className),
        parent_(std::const_pointer_cast<Class>(baseClass)),
        isInstantiated_(isInstantiated) {}
  // ===== Object interface =====
  std::string type() const override { return className_; }

  std::string toString() const override {
    return "<" + className_ + " object at " +
           std::to_string(reinterpret_cast<uintptr_t>(this)) + ">";
  }

  bool equals(const Object& other) const override {
    if (auto* customObj = dynamic_cast<const Class*>(&other)) {
      return this == customObj;
    }
    return false;
  }

  size_t hash() const override { return std::hash<const Class*>{}(this); }

  bool toBool() const override { return true; }

  bool isInstance(const std::string& type) const override {
    if (type == className_) return true;
    if (type == "object") return true;

    auto current = parent_;
    while (current) {
      if (current->className_ == type) return true;
      current = current->parent_;
    }
    return false;
  }

  std::shared_ptr<Object> getAttr(const std::string& name) const override {
    auto it = attributes_.find(name);
    if (it != attributes_.end()) {
      return it->second;
    }

    auto current = parent_;
    while (current) {
      try {
        return current->getAttr(name);
      } catch (const std::runtime_error&) {
        current = current->parent_;
      }
    }

    throw std::runtime_error("'" + className_ + "': object has no attribute '" +
                             name + "'");
  }

  void setAttr(const std::string& name,
               std::shared_ptr<Object> value) override {
    attributes_[name] = value;
  }

  // ===== Class definition methods =====
  static std::shared_ptr<Class> defineClass(const std::string& name) {
    return std::make_shared<Class>(name);
  }
  static std::shared_ptr<Class> defineSubclass(
      const std::string& name, std::shared_ptr<Class> baseClass) {
    return std::make_shared<Class>(name, baseClass);
  }

  std::shared_ptr<Class> getParent() const { return parent_; }
  template <typename Callable>
  void addMethod(const std::string& name, Callable&& func,
                 const Arguments& defaults = {}) {
    attributes_[name] = Function::define(func, name, defaults);
  }
  bool hasParent() const { return parent_ != nullptr; }

  template <typename Callable>
  void defineInit(Callable&& init, const Arguments& defaults = {}) {
    addMethod(
        "__init__",
        [init](const Arguments& args) {
          auto self = Function::getArg<Class>(args, "self");
          init(self, args);
          return None::spawn();
        },
        defaults);
  }

  template <typename Callable>
  void defineMethod(const std::string& name, Callable&& func,
                    const Arguments& defaults = {}) {
    addMethod(name, std::forward<Callable>(func), defaults);
  }

  void defineAttribute(const std::string& name, std::shared_ptr<Object> value) {
    setAttr(name, value);
  }

  // ===== Class instantiation methods =====
  std::shared_ptr<Class> spawn(const Arguments& args = {}) {
    if (isInstantiated_) {
      throw std::runtime_error("Cannot spawn from instance");
    }

    auto instance = std::make_shared<Class>(className_ + "-Instance",
                                            shared_from_this(), true);

    try {
      if (auto init = instance->getAttr("__init__")) {
        instance->method("__init__", args);
      }
    } catch (const std::runtime_error& e) {
      throw std::runtime_error(formatError("Failed to initialize instance: " +
                                           std::string(e.what())));
    }

    return instance;
  }

  // ===== Class instance methods =====
  std::vector<std::shared_ptr<Class>> getMethodResolutionOrder() const {
    std::vector<std::shared_ptr<Class>> mro;
    mro.push_back(std::make_shared<Class>(*this));

    auto current = parent_;
    while (current) {
      mro.push_back(current);
      current = current->parent_;
    }
    return mro;
  }

  void set(const std::string& name, std::shared_ptr<Object> value) {
    if (attributes_.find(name) == attributes_.end()) {
      throw std::runtime_error(
          formatError("Object has no attribute '" + name + "'"));
    }
    attributes_[name] = value;
  }

  std::shared_ptr<Object> get(const std::string& name) {
    if (attributes_.find(name) == attributes_.end()) {
      throw std::runtime_error(
          formatError("Object has no attribute '" + name + "'"));
    }
    return attributes_[name];
  }
  template <typename ReturnType = Object>
  std::shared_ptr<ReturnType> get(const std::string& attributeName){
    try {
      auto result = get(attributeName);
      auto typed = std::dynamic_pointer_cast<ReturnType>(result);
      if (!typed) {
        throw std::runtime_error(formatError("Attribute '" + attributeName +
                                             "' returned unexpected type"));
      }
      return typed;
    } catch (const std::exception& e) {
      throw std::runtime_error(formatError(e.what()));
    }
  }
  
  std::shared_ptr<Object> method(const std::string& methodName,
                                 const Arguments& args = {}) {
    auto method = std::dynamic_pointer_cast<Function>(getAttr(methodName));
    if (!method) {
      throw std::runtime_error("'" + className_ + "': object has no method '" +
                               methodName + "'");
    }
    Arguments callArgs = {{"self", shared_from_this()}};
    callArgs.insert(args.begin(), args.end());

    return (*method)(callArgs);
  }

  template <typename ReturnType = Object>
  std::shared_ptr<ReturnType> method(const std::string& methodName,
                                     const Arguments& args = {}) {
    try {
      auto result = method(methodName, args);
      auto typed = std::dynamic_pointer_cast<ReturnType>(result);
      if (!typed) {
        throw std::runtime_error(formatError("Method '" + methodName +
                                             "' returned unexpected type"));
      }
      return typed;
    } catch (const std::exception& e) {
      throw std::runtime_error(formatError(e.what()));
    }
  }

  // ===== Class serialization methods =====
  std::string serialize(int indent = 0) const {
    std::string spacing(indent * 2, ' ');
    std::string result = spacing + "Class: " + className_ + "\n";

    result += spacing + "Attributes:\n";
    for (const auto& [name, value] : attributes_) {
      result += spacing + "  " + name + ": " + value->toString() + "\n";
    }

    result += spacing + "Methods:\n";
    for (const auto& [name, value] : attributes_) {
      if (dynamic_cast<Function*>(value.get())) {
        result += spacing + "  " + name + "()\n";
      }
    }

    if (parent_) {
      result += spacing + "Parent:\n" + parent_->serialize(indent + 1);
    }

    return result;
  }
  // Pretty error formatting
  std::string formatError(const std::string& msg) const {
    return "In class '" + className_ + "': " + msg;
  }
};
#endif