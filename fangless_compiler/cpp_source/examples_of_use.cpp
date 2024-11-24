#include "Headers.hpp"
int main() {
  // example building a list using the initialiser list
  auto list = List::spawn(
      {
            Number::spawn(1), 
            String::spawn("hello"),
            Bool::spawn(true)
      }
   );
  std::cout << "Created list with [1, 'hello', true]:\n"
            << "  Actual: " << list << std::endl;

  // example of building tuple with 3 elements using initialiser list
  auto tuple = Tuple<3>::spawn(
    {
        Number::spawn(42), 
        String::spawn("hello"), 
        Bool::spawn(true)
      }
  );

  std::cout << "Created tuple with (42, 'hello', True):\n"
            << "  Actual: " << tuple << std::endl;  

  // example of building a set using initialiser list
  auto set = Set::spawn(
      {
        Number::spawn(1), 
      Number::spawn(2), 
      String::spawn("hello"), 
      tuple
      }
      );
  std::cout << "Created set with {1, 2, 'hello', (42, 'hello', True)}:\n"
            << "  Actual: " << set << std::endl;

  // example of building a dictionary using initialiser list
  auto dict = Dictionary::spawn(
      {
        {Number::spawn(1), String::spawn("one")}, 
        {Number::spawn(2), String::spawn("two")},
        {String::spawn("My Beautiful Tuple"), tuple},
        {String::spawn("My Magnificent List"), list},
        {String::spawn("My AllMighty Set"), set}
      }
  );
  std::cout << "Created dictionary with key-value pairs:\n"
            << "  Expected: {1: 'one', 2: 'two', 'My Beautiful Tuple': (42, "
               "'hello', True), 'My Magnificent List': [1, 'hello', True], 'My "
               "AllMight Set': {1, 2, 'hello', (42, 'hello', True)}}\n"
            << "  Actual: " << dict << std::endl;
  return 0;
}