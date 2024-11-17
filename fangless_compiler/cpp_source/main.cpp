#include "Value.hpp"
#include <iostream>
void doThings() {
  Thing t = 15;
  if (!t.isNone() && !t.isNone()) {
    std::cout << "t is not none" << std::endl;
    return;
  }
}

int main() {
    doThings();
    return 0;
}