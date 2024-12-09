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
#include <optional>

template <typename... Args>
auto printTuple(std::tuple<std::shared_ptr<Args>...> tup) {
  // Helper function to print each element with proper type
  auto number = Function::getArgOrDefault<0>(tup, Number::spawn(0));
  auto str = Function::getArgOrDefault<1>(tup, String::spawn("default"));
  auto second_number = Function::getArgOrDefault<2>(tup, Number::spawn(4));
  str = str + String::spawn(" world");
  auto sum = number + second_number;
  std::cout << "First + second: " << sum << "\n";
  std::cout << "string + world to upper: " << str->upper() << "\n\n";
  auto newArgs = Function::spawnArgs(number, str, second_number);
  Function::updateArgs(tup, newArgs);
  return sum;
}

int main() {

  // Create tuple with different types while preserving their specific type
  auto num = Number::spawn(8);
  auto str = String::spawn("hello");
  auto args = Function::spawnArgs(num, str, Number::spawn(3.14));

  auto bro = printTuple(Function::spawnArgs());
  auto bro2 = printTuple(args);
  std::cout << "str: " << str << "\n";
  auto bro3 = printTuple(Function::spawnArgs(Number::spawn(4)));
}


