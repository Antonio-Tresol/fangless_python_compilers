#include <iostream>
#include <tuple>

#include "Bool.hpp"
#include "Dictionary.hpp"
#include "List.hpp"
#include "Number.hpp"
#include "Set.hpp"
#include "String.hpp"
#include "BuiltinFunctions.hpp"
#include "Function.hpp"


// Template helper to print any tuple of shared pointers while preserving types
template <typename... Args>
auto printTuple(std::tuple<std::shared_ptr<Args>...> tup) {
  // Helper function to print each element with proper type
  auto number = std::get<0>(tup);
  auto str = std::get<1>(tup);
  auto num = std::get<2>(tup);
  auto boolean = std::get<3>(tup);

  number = Number::spawn(2);
  str = str + String::spawn(" world");
  auto sum = number + num;
  std::cout << "tuple 0 + tuple 2: " << number + num << "\n";
  std::cout << "tuple 1 upper: " << str->upper() << "\n";
  std::cout << "tuple 3 not: " << !boolean << "\n";
  auto newArgs = Function::spawnArgs(number, str, num, boolean);
  BF::updateArgs(tup, newArgs);
  return sum;
}

int main() {

  // Create tuple with different types while preserving their specific type
  auto num = Number::spawn(8);
  auto str = String::spawn("hello");
  auto args = Function::spawnArgs(num, str, Number::spawn(3.14), Bool::spawn(true));

  auto bro = printTuple(Function::spawnArgs(num, str, Number::spawn(3.14), Bool::spawn(true)));
  std::cout << "bro: " << bro << "\n";
  std::cout << " Number " << num << "\n";

  std::cout << " Str " << str << "\n";
  std::cout << " Num " << std::get<2>(args) << "\n";
}
