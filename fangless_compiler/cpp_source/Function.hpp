#ifndef FUNCTION_HPP
#define FUNCTION_HPP

#include <tuple>
#include <utility>

template <typename T>
struct is_container_type : std::false_type {};

template <>
struct is_container_type<String> : std::true_type {};
template <>
struct is_container_type<Set> : std::true_type {};
template <>
struct is_container_type<Dictionary> : std::true_type {};
template <>
struct is_container_type<List> : std::true_type {};

namespace Function {
  template <typename... Args>
  auto spawnArgs(Args&&... args) {
    return std::make_tuple(std::forward<Args>(args)...);
  }

  template<std::size_t Index, typename Fallback, typename... Args>
  auto getArgOrDefault(const std::tuple<std::shared_ptr<Args>...>& tuple, Fallback&& fallback) {
    if constexpr (Index < sizeof...(Args)) {
        return std::get<Index>(tuple);
    } else {
        return std::forward<Fallback>(fallback);
    }
  }

  template <typename... Args1, typename... Args2>
  void updateArgs(std::tuple<std::shared_ptr<Args1>...>& args,
                  std::tuple<std::shared_ptr<Args2>...>& newArgs) {

    constexpr size_t minSize = std::min(sizeof...(Args1), sizeof...(Args2));

    auto updateHelper = [&]<std::size_t... I>(std::index_sequence<I...>) {
        ((void)([&] {
            auto& target = std::get<I>(args);
            auto& source = std::get<I>(newArgs);
            using SourceType = typename std::decay_t<decltype(*source)>;
            if constexpr (is_container_type<SourceType>::value) {
                *target = *source;
            }
        }()),
        ...);
    };

    updateHelper(std::make_index_sequence<minSize>{});
  }

  bool boolEval(const char obj) {
    return obj != '\0';
  }

  bool boolEval(const int obj) {
    return obj != 0;
  }

  bool boolEval(const bool obj) {
    return obj;
  }

  bool boolEval(const std::shared_ptr<Object>& obj) {
    return obj->toBool();
  }

  bool boolEval(const std::shared_ptr<std::wstring>& obj) {
    return !obj->empty();
  }

  std::string removeQuotesIfNeeded(const std::string& str) {
  if ((str.front() == '"' && str.back() == '"')||
      (str.front() == '\'' && str.back() == '\'')) {
    return str.substr(1, str.size() - 2);
  }
    return str;
  }
}// namespace Function
#endif  // FUNCTION_HPP