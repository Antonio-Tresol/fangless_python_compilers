#ifndef FUNCTION_HPP
#define FUNCTION_HPP
#include <tuple>
#include <utility>

namespace Function {
template <typename... Args>
  auto spawnArgs(Args&&... args) {
    return std::make_tuple(std::forward<Args>(args)...);
  }
}// namespace Function
#endif  // FUNCTION_HPP