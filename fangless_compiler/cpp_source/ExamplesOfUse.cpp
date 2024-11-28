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
  auto list2 = List::spawn(
      {
            Number::spawn(1), 
            String::spawn("hello"),
            Bool::spawn(true)
      }
   );
   if (list == list2) {
    std::cout << "======================================" << std::endl;
    std::cout << "lists are great aren't they" << std::endl;
    std::cout << "======================================" << std::endl;
   }
   list2->append(Number::spawn(2));
   if (list != list2) {
    std::cout << "======================================" << std::endl;
    std::cout << "lists are amazing aren't they" << std::endl;
    std::cout << "======================================" << std::endl;
   }
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
  auto dict2 = Dictionary::spawn(
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
  auto my_var = None::spawn();
  if (my_var) {
    std::cout << "======================================" << std::endl;
    std::cout << "None is falsy" << std::endl;
    std::cout << "======================================" << std::endl;
  }

  if (dict == dict2) {
    std::cout << "======================================" << std::endl;
    std::cout << "Dict is great" << std::endl;
    std::cout << "======================================" << std::endl;
  }
  dict2->set(Number::spawn(3), String::spawn("three"));
  if (dict != dict2) {
    std::cout << "======================================" << std::endl;
    std::cout << "Dict is amazing" << std::endl;
    std::cout << "======================================" << std::endl;
  }
  if ((list2 != dict) && (list != dict) && (tuple != dict) && (set != dict)) {
    std::cout << "======================================" << std::endl;
    std::cout << "Types are incredible is amazing" << std::endl;
    std::cout << "======================================" << std::endl;
  }

  auto num_1 = Number::spawn(1);
  auto num_2 = Number::spawn(1);
  if (num_1 == num_2) {
    std::cout << "======================================" << std::endl;
    std::cout << "Numbers are amazing" << std::endl;
    std::cout << "======================================" << std::endl;
  } 
  auto num_3 = Number::spawn(2);
  if (num_1 != num_3) {
    std::cout << "======================================" << std::endl;
    std::cout << "Numbers are amazing" << std::endl;
    std::cout << "======================================" << std::endl;
  }
  auto str_1 = String::spawn("hello");
  auto str_2 = String::spawn("hello");
  if (str_1 == str_2) {
    std::cout << "======================================" << std::endl;
    std::cout << "Strings are amazing" << std::endl;
    std::cout << "======================================" << std::endl;
  }
  auto str_3 = String::spawn("world");
  if (str_1 != str_3) {
    std::cout << "======================================" << std::endl;
    std::cout << "Strings are superb" << std::endl;
    std::cout << "======================================" << std::endl;
  }
  auto bool_1 = Bool::spawn(false);
  auto bool_2 = Bool::spawn(true);
  if (!bool_1 && bool_2) {
    std::cout << "======================================" << std::endl;
    std::cout << "Booleans are amazing" << std::endl;
    std::cout << "======================================" << std::endl;
  }
  auto negative = Number::spawn(-1);
  if (negative) {
    std::cout << "======================================" << std::endl;
    std::cout << "Negatives are amazing" << std::endl;
    std::cout << "======================================" << std::endl;
  }
  auto zero = Number::spawn(0);
  if ((zero + Number::spawn(1))) {
    std::cout << "======================================" << std::endl;
    std::cout << "Zero is amazing" << std::endl;
    std::cout << "======================================" << std::endl;
  }
  auto empty_list = List::spawn();
  if (!empty_list) {
    std::cout << "======================================" << std::endl;
    std::cout << "Empty lists are amazing" << std::endl;
    std::cout << "======================================" << std::endl;
  }

  return 0;
}