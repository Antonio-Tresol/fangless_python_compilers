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
      if (value.get() == nullptr) {
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

  std::strong_ordering compare(const Object& other) const override {
    // If types differ, fall back to base comparison
    if (type() != other.type()) {
      return Object::compare(other);
    }

    // Safe downcast since we checked types
    const auto* other_func = dynamic_cast<const Function*>(&other);
    if (!other_func) {
      return std::strong_ordering::less;
    }

    // Compare function names
    if (auto name_cmp = name_ <=> other_func->name_;
        name_cmp != std::strong_ordering::equal) {
      return name_cmp;
    }

    // Compare number of default arguments
    if (auto size_cmp = defaults_.size() <=> other_func->defaults_.size();
        size_cmp != std::strong_ordering::equal) {
      return size_cmp;
    }

    // Compare default arguments
    std::vector<std::pair<std::string, std::shared_ptr<Object>>> this_defaults(
        defaults_.begin(), defaults_.end());
    std::vector<std::pair<std::string, std::shared_ptr<Object>>> other_defaults(
        other_func->defaults_.begin(), other_func->defaults_.end());

    // Sort for deterministic comparison
    auto comp = [](const auto& a, const auto& b) { return a.first < b.first; };
    std::sort(this_defaults.begin(), this_defaults.end(), comp);
    std::sort(other_defaults.begin(), other_defaults.end(), comp);

    for (size_t i = 0; i < this_defaults.size(); ++i) {
      if (auto name_cmp = this_defaults[i].first <=> other_defaults[i].first;
          name_cmp != std::strong_ordering::equal) {
        return name_cmp;
      }
      if (auto value_cmp =
              (*this_defaults[i].second) <=> (*other_defaults[i].second);
          value_cmp != std::strong_ordering::equal) {
        return value_cmp;
      }
    }

    // Functions with same name and defaults are considered equal
    return std::strong_ordering::equal;
  }
  template <typename T>
  static std::shared_ptr<T> getArg(const Arguments& arguments,
                                   const std::string& name) {
    auto it = arguments.find(name);
    if (it == arguments.end()) {
      throw std::runtime_error("Missing argument: " + name);
    }
    auto result = std::dynamic_pointer_cast<T>(it->second);
    if (result.get() == nullptr) {
      throw std::runtime_error("Argument '" + name + "' must be of type " +
                               typeid(T).name());
    }
    return result;
  }
  std::shared_ptr<Object> operator()(const Arguments& namedArguments) const {
    validateArguments(namedArguments);
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

  bool equals(const std::shared_ptr<Object>& other) const {
    return equals(*other);
  }

  friend bool operator==(const Function& lhs, const Function& rhs) {
    return lhs.equals(rhs);
  }

  friend bool operator==(std::shared_ptr<Function> lhs,
                         std::shared_ptr<Function> rhs) {
    return lhs->equals(*rhs);
  }

  friend bool operator==(std::shared_ptr<Function> lhs, const Function& rhs) {
    return lhs->equals(rhs);
  }

  friend bool operator==(const Function& lhs, std::shared_ptr<Function> rhs) {
    return rhs->equals(lhs);
  }

  friend bool operator==(const std::shared_ptr<Object>& lhs,
                         const Function& rhs) {
    return rhs.equals(*lhs);
  }

  friend bool operator==(const std::shared_ptr<Object>& lhs,
                         const std::shared_ptr<Function>& rhs) {
    return rhs->equals(*lhs);
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
  bool operator!() const { return false; }
  friend bool operator!(const std::shared_ptr<Function>& func) {
    return !func->toBool();
  }

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

  friend std::ostream& operator<<(std::ostream& os, const Function& function) {
    os << function.toString();
    return os;
  }
};

#endif  // FUNCTION_HPP