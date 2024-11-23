#ifndef FUNCTION_HPP
#define FUNCTION_HPP
#include <map>
#include <string>

using Arguments = std::map<std::string, std::shared_ptr<Object>>;
class Function : public Object {
 public:
  std::function<std::shared_ptr<Object>(const Arguments&)> callable_;
  std::string name_;
  std::map<std::string, std::shared_ptr<Object>> defaults_;
  static void validateArguments(const Arguments& args) {
    for (const auto& [key, value] : args) {
      if (!value) {
        throw std::runtime_error("Null argument value for key: " + key);
      }
    }
  }
  explicit Function(
      std::function<std::shared_ptr<Object>(const Arguments&)> func,
      std::string name = "lambda", Arguments defaults = {})
      : callable_(std::move(func)),
        name_(std::move(name)),
        defaults_(std::move(defaults)) {
    validateArguments(defaults_);
    if (!callable_) {
      throw std::runtime_error("Null function pointer");
    }
  }

  template <typename T>
  static std::shared_ptr<T> getArg(const Arguments& arguments,
                                   const std::string& name) {
    auto it = arguments.find(name);
    if (it == arguments.end()) {
      throw std::runtime_error("Missing argument: " + name);
    }
    auto result = std::dynamic_pointer_cast<T>(it->second);
    if (!result) {
      throw std::runtime_error("Argument '" + name + "' must be of type " +
                               typeid(T).name());
    }
    return result;
  }
  std::shared_ptr<Object> operator()(const Arguments& namedArguments) const {
    validateArguments(namedArguments);
    // Merge default arguments with provided namedArguments
    Arguments arguments = defaults_;
    for (const auto& [key, value] : namedArguments) {
      arguments[key] = value;
    }
    return callable_(arguments);
  }
  std::shared_ptr<Object> call(const Arguments& namedArguments) const {
    validateArguments(namedArguments);
    Arguments arguments = defaults_;
    for (const auto& [key, value] : namedArguments) {
      arguments[key] = value;
    }
    return callable_(arguments);
  }

  std::shared_ptr<Object> call(
      const std::vector<std::string>& param_names,
      const std::vector<std::shared_ptr<Object>>& arguments) const {
    if (arguments.size() > param_names.size()) {
      throw std::runtime_error("Too many arguments for function " + name_);
    }

    Arguments namedArguments;
    for (size_t i = 0; i < arguments.size(); i++) {
      namedArguments[param_names[i]] = arguments[i];
    }

    for (size_t i = arguments.size(); i < param_names.size(); i++) {
      auto it = defaults_.find(param_names[i]);
      if (it == defaults_.end()) {
        throw std::runtime_error("Missing argument: " + param_names[i]);
      }
      namedArguments[param_names[i]] = it->second;
    }
    return (*this)(namedArguments);
  }

  template <typename Callable>
  static std::shared_ptr<Function> define(
      Callable&& function, const std::string& functionName = "lambda",
      const Arguments& defaultArgs = {}) {
    // Create wrapper that forwards the callable while preserving the signature
    auto wrapper = [callable = std::forward<Callable>(function)](
                       const Arguments& args) -> std::shared_ptr<Object> {
      return callable(args);
    };
    return std::make_shared<Function>(std::move(wrapper), functionName,
                                      defaultArgs);
  }
  std::string type() const override { return "function"; }

  std::string toString() const override { return "<function " + name_ + ">"; }

  bool equals(const Object& other) const override {
    if (auto* funcObj = dynamic_cast<const Function*>(&other)) {
      // Compare function names and defaults
      return name_ == funcObj->name_ && defaults_ == funcObj->defaults_;
    }
    return false;
  }

  size_t hash() const override {
    size_t h = std::hash<std::string>{}(name_);
    for (const auto& [key, value] : defaults_) {
      h ^= std::hash<std::string>{}(key);
      if (value) {
        h ^= value->hash();
      }
    }
    return h;
  }

  bool toBool() const override { return true; }

  bool isInstance(const std::string& type) const override {
    return type == "function" || type == "object";
  }

  std::shared_ptr<Object> getAttr(const std::string& name) const override {
    throw std::runtime_error("'" + type() + "' object has no attribute '" +
                             name + "'");
  }

  void setAttr(const std::string& name,
               std::shared_ptr<Object> value) override {
    throw std::runtime_error("'" + type() +
                             "' object attributes are read-only");
  }
};

#endif // FUNCTION_HPP