#include <functional>
#include <iostream>
#include <limits>
#include <vector>

#include "Bool.hpp"
#include "Dictionary.hpp"
#include "Function.hpp"
#include "List.hpp"
#include "None.hpp"
#include "Number.hpp"
#include "Set.hpp"
#include "String.hpp"
#include "Tuple.hpp"
#include "Class.hpp"

void printSection(const std::string& title) {
  std::cout << "\n=== " << title << " ===\n";
}

std::ostream& operator<<(std::ostream& os, const std::shared_ptr<Object>& obj) {
  return os << *obj;
}

std::ostream& operator<<(std::ostream& os,
                         const std::shared_ptr<const Object>& obj) {
  return os << *obj;
}

std::ostream& operator<<(std::ostream& os, const std::shared_ptr<Number>& obj) {
  return os << *obj;
}
std::ostream& operator<<(std::ostream& os, const std::shared_ptr<String>& obj) {
  return os << *obj;
}

template <size_t Size>
std::ostream& operator<<(std::ostream& os,
                         const std::shared_ptr<Tuple<Size>>& obj) {
  return os << *obj;
}

std::ostream& operator<<(std::ostream& os, const std::shared_ptr<List>& obj) {
  return os << *obj;
}

std::ostream& operator<<(std::ostream& os, const std::shared_ptr<Set>& obj) {
  return os << *obj;
}

std::ostream& operator<<(std::ostream& os,
                         const std::shared_ptr<Dictionary>& obj) {
  return os << *obj;
}

std::shared_ptr<Number> operator+(const std::shared_ptr<Number>& a,
                                  const std::shared_ptr<Number>& b) {
  return *a + *b;
}

std::shared_ptr<Number> operator-(const std::shared_ptr<Number>& a,
                                  const std::shared_ptr<Number>& b) {
  return *a - *b;
}

std::shared_ptr<Number> operator*(const std::shared_ptr<Number>& a,
                                  const std::shared_ptr<Number>& b) {
  return *a * *b;
}

std::shared_ptr<Number> operator/(const std::shared_ptr<Number>& a,
                                  const std::shared_ptr<Number>& b) {
  return *a / *b;
}

std::shared_ptr<Number> operator%(const std::shared_ptr<Number>& a,
                                  const std::shared_ptr<Number>& b) {
  return *a % *b;
}

std::shared_ptr<String> operator+(const std::shared_ptr<String>& a,
                                  const std::shared_ptr<String>& b) {
  return *a + *b;
}
std::shared_ptr<String> operator*(const std::shared_ptr<String>& a,
                                  const std::shared_ptr<Number>& b) {
  return *a * *b;
}
std::shared_ptr<List> operator+(const std::shared_ptr<List>& a,
                                const std::shared_ptr<List>& b) {
  return *a + *b;
}
std::shared_ptr<List> operator*(const std::shared_ptr<List>& a,
                                const std::shared_ptr<Number>& b) {
  return *a * *b;
}

std::shared_ptr<Set> operator|(const std::shared_ptr<Set>& a,
                               const std::shared_ptr<Set>& b) {
  return *a | *b;
}

std::shared_ptr<Set> operator+(const std::shared_ptr<Set>& a,
                               const std::shared_ptr<Set>& b) {
  return *a | *b;
}

template <size_t Size>
std::shared_ptr<Tuple<Size + Size>> operator+(
    const std::shared_ptr<Tuple<Size>>& a,
    const std::shared_ptr<Tuple<Size>>& b) {
  return *a + *b;
}
// std::shared_ptr<Bool> operator==(const std::shared_ptr<Object>& a, const
// std::shared_ptr<Object>& b) {
//     return a->equals(*b) ? Bool::spawn(1) : Bool::spawn(0);
// }
void printResult(const std::string& op, const Object& result) {
  std::cout << op << ": " << result << std::endl;
}
void printResult(const std::string& op, const std::shared_ptr<Object>& result) {
  std::cout << op << ": " << result << std::endl;
}

void testFunctions() {
  printSection("1. Basic Named Arguments Function");
  auto greet = Function::define(
      [](const Arguments& args) {
        auto name = Function::getArg<String>(args, "name");
        auto age = Function::getArg<Number>(args, "age");
        return String::spawn("Hello, " + name->toString() + "! You are " +
                             std::to_string(age->getInt()) + " years old.");
      },
      "greet", {{"age", Number::spawn(0)}}  // Default age
  );

  printSection("2. Named Arguments Call");
  Arguments kwargs = {{"name", String::spawn("Alice")},
                      {"age", Number::spawn(25)}};

  std::cout << "Testing greet(name='Alice', age=25):\n";
  std::cout << "  Expected: 'Hello, Alice! You are 25 years old.'\n";
  auto result = (*greet)(kwargs);
  std::cout << "  Actual:   " << result << "\n";

  printSection("3. Default Arguments");
  Arguments partial_args = {{"name", String::spawn("Bob")}};
  std::cout << "Testing greet with default age:\n";
  std::cout << "  Expected: 'Hello, Bob! You are 0 years old.'\n";
  auto default_result = (*greet)(partial_args);
  std::cout << "  Actual:   " << default_result << "\n";

  printSection("4. Positional Arguments");
  auto result2 = greet->call({"name", "age"},
                             {String::spawn("Charlie"), Number::spawn(30)});
  std::cout << "Testing greet('Charlie', 30):\n";
  std::cout << "  Expected: 'Hello, Charlie! You are 30 years old.'\n";
  std::cout << "  Actual:   " << result2 << "\n";

  printSection("5. Error Handling");
  try {
    (*greet)(Arguments{});  // Missing required argument
    std::cout << "❌ Failed: Should have thrown\n";
  } catch (const std::runtime_error& e) {
    std::cout << "✓ Passed: " << e.what() << "\n";
  }

  try {
    (*greet)(Arguments{{"wrong_param", String::spawn("test")}});
    std::cout << "❌ Failed: Should have thrown\n";
  } catch (const std::runtime_error& e) {
    std::cout << "✓ Passed: " << e.what() << "\n";
  }

  printSection("6. Complex Function");
  auto calculate = Function::define(
      [](const Arguments& args) {
        auto operation = Function::getArg<String>(args, "operation");
        auto x = Function::getArg<Number>(args, "x");
        auto y = Function::getArg<Number>(args, "y");

        if (operation->toString() == "'add'") return x + y;
        if (operation->toString() == "'multiply'") return x * y;
        throw std::runtime_error("Unknown operation: " + operation->toString());
      },
      "calculate", {{"operation", String::spawn("add")}}  // Default operation
  );

  Arguments calc_args = {{"x", Number::spawn(10)},
                         {"y", Number::spawn(20)},
                         {"operation", String::spawn("multiply")}};

  std::cout << "Testing calculate(x=10, y=20, operation='multiply'):\n";
  std::cout << "  Expected: 200\n";
  auto calc_result = (*calculate)(calc_args);
  std::cout << "  Actual:   " << calc_result << "\n";
}

void testBool() {
  printSection("1. Bool Creation and Basic Operations");

  // Direct creation
  auto b1 = Bool::spawn(true);
  auto b2 = Bool::spawn(false);

  std::cout << "Basic values:\n";
  std::cout << "  true  -> " << *b1 << "\n";
  std::cout << "  false -> " << *b2 << "\n";

  printSection("2. Type Conversions");
  // From int
  auto b3 = std::make_shared<Bool>(1);
  auto b4 = std::make_shared<Bool>(0);
  std::cout << "From int:\n";
  std::cout << "  1 -> " << *b3 << "\n";
  std::cout << "  0 -> " << *b4 << "\n";

  // From other objects
  auto str1 = String::spawn("hello");  // truthy
  auto str2 = String::spawn("");       // falsy

  auto b5 = std::make_shared<Bool>(str1);
  auto b6 = std::make_shared<Bool>(str2);

  std::cout << "From String:\n";
  std::cout << "  'hello' -> " << *b5 << "\n";
  std::cout << "  ''      -> " << *b6 << "\n";

  printSection("3. Comparison Operations");
  std::cout << "Equality tests:\n";
  std::cout << "  true == true:   " << (b1->equals(*b1) ? "✓" : "❌") << "\n";
  std::cout << "  true == false:  " << (!b1->equals(*b2) ? "✓" : "❌") << "\n";
  std::cout << "  false == false: " << (b2->equals(*b2) ? "✓" : "❌") << "\n";

  std::cout << "\nOrdering tests:\n";
  std::cout << "  false < true:  "
            << (b2->compare(*b1) == std::strong_ordering::less ? "✓" : "❌")
            << "\n";
  std::cout << "  true > false:  "
            << (b1->compare(*b2) == std::strong_ordering::greater ? "✓" : "❌")
            << "\n";
  std::cout << "  true == true:  "
            << (b1->compare(*b1) == std::strong_ordering::equal ? "✓" : "❌")
            << "\n";

  printSection("4. Object Interface");
  std::cout << "Type information:\n";
  std::cout << "  type():           " << b1->type() << "\n";
  std::cout << "  isInstance(Bool): " << (b1->isInstance("Bool") ? "✓" : "❌")
            << "\n";
  std::cout << "  hash() different: " << (b1->hash() != b2->hash() ? "✓" : "❌")
            << "\n";

  printSection("5. Error Handling");
  std::cout << "Testing attribute access:\n";
  try {
    b1->getAttr("nonexistent");
    std::cout << "❌ Should have thrown on getAttr\n";
  } catch (const std::runtime_error& e) {
    std::cout << "✓ Caught expected error: " << e.what() << "\n";
  }

  try {
    b1->setAttr("test", b2);
    std::cout << "❌ Should have thrown on setAttr\n";
  } catch (const std::runtime_error& e) {
    std::cout << "✓ Caught expected error: " << e.what() << "\n";
  }

  printSection("6. Boolean Operations");
  std::cout << "toBool() results:\n";
  std::cout << "  true.toBool():  " << (b1->toBool() ? "✓" : "❌") << "\n";
  std::cout << "  false.toBool(): " << (!b2->toBool() ? "✓" : "❌") << "\n";

  printSection("7. Cross-type Comparisons");
  auto num = Number::spawn(1);
  std::cout << "Bool vs other types:\n";
  std::cout << "  Bool == Number: " << (b1->equals(*num) ? "❌" : "✓") << "\n";
  std::cout << "  Compare order:  "
            << (b1->compare(*num) == std::strong_ordering::less ? "✓" : "❌")
            << "\n";
}
void testNumbers() {
  printSection("Number Creation and Type Checking");
  auto n1 = Number::spawn(10);
  auto n2 = Number::spawn(3);
  auto n3 = Number::spawn(10.5);
  auto n4 = Number::spawn(3.2);

  std::cout << "n1 type: " << n1->type() << std::endl;
  std::cout << "n3 type: " << n3->type() << std::endl;
  std::cout << "n1 isInstance(int): " << n1->isInstance("int") << std::endl;
  std::cout << "n3 isInstance(float): " << n3->isInstance("float") << std::endl;

  printSection("Integer Operations");
  printResult("10 + 3", (n1 + n2));
  printResult("10 - 3", (n1 - n2));
  printResult("10 * 3", (n1 * n2));
  printResult("10 / 3", (n1 / n2));

  printSection("Float Operations");
  printResult("10.5 + 3.2", (n3 + n4));
  printResult("10.5 - 3.2", (n3 - n4));
  printResult("10.5 * 3.2", (n3 * n4));
  printResult("10.5 / 3.2", (n3 / n4));

  printSection("Mixed Operations");
  printResult("10 + 3.2", (n1 + n4));
  printResult("10.5 + 3", (n3 + n2));
  printResult("10 / 3.2", (n1 / n4));
  printResult("10.5 / 3", (n3 / n2));

  printSection("Comparison Operations");
  std::cout << "10 < 3: " << (n1 < n2) << std::endl;
  std::cout << "10.5 > 3.2: " << (n3 > n4) << std::endl;
  std::cout << "10 == 10.0: " << (n1 == Number::spawn(10.0)) << std::endl;
  std::cout << "3.0 <= 3: " << (Number::spawn(3.0) <= n2) << std::endl;
  std::cout << "10.5 >= 10: " << (n3 >= n1) << std::endl;

  printSection("Special Float Values");
  auto inf_pos = Number::spawn(std::numeric_limits<double>::infinity());
  auto inf_neg = Number::spawn(-std::numeric_limits<double>::infinity());
  auto nan = Number::spawn(std::numeric_limits<double>::quiet_NaN());

  printResult("inf", inf_pos);
  printResult("-inf", inf_neg);
  printResult("nan", nan);

  std::cout << "inf.isFinite(): " << inf_pos->isFinite() << std::endl;
  std::cout << "inf.isInf(): " << inf_pos->isInf() << std::endl;
  std::cout << "nan.isNaN(): " << nan->isNaN() << std::endl;
  std::cout << "10.isFinite(): " << n1->isFinite() << std::endl;

  printSection("Boolean Context");
  std::cout << "bool(0): " << bool(Number(0)) << std::endl;
  std::cout << "bool(1): " << bool(Number(1)) << std::endl;
  std::cout << "bool(0.0): " << bool(Number(0.0)) << std::endl;
  std::cout << "bool(nan): " << bool(nan) << std::endl;

  printSection("Hash Consistency");
  auto n5 = std::make_shared<Number>(10);
  std::cout << "hash(10) == hash(10): " << (n1->hash() == n5->hash())
            << std::endl;
  std::cout << "hash(10) == hash(10.0): " << (n1->hash() == Number(10.0).hash())
            << std::endl;
}

void testStrings() {
  printSection("1. String Creation");
  auto s1 = String::spawn("Hello");
  auto s2 = String::spawn("World");
  auto s3 = String::spawn("Hello");

  std::cout << "s1: \"" << s1 << "\"\n";
  std::cout << "s2: \"" << s2 << "\"\n";
  std::cout << "s3: \"" << s3 << "\"\n";
  std::cout << "s1 == s3: " << (s1 == s3) << "\n";

  printSection("2. Case Transformations");
  std::cout << "Original:  \"" << s1 << "\"\n";
  std::cout << "Upper:     \"" << s1->upper() << "\"\n";
  std::cout << "Lower:     \"" << s1->lower() << "\"\n";

  printSection("3. Whitespace Handling");
  auto spaces = String::spawn("  trim me  ");
  std::cout << "Original: \"" << spaces << "\"\n";
  std::cout << "Stripped: \"" << spaces->strip() << "\"\n";

  printSection("4. String Operations");
  std::cout << "Concatenation:\n";
  std::cout << "  \"" << s1 << "\" + \"" << s2 << "\" = \"" << (s1 + s2)
            << "\"\n";

  std::cout << "Repetition:\n";
  std::cout << "  \"" << s1 << "\" * 3 = \"" << (s1 * Number::spawn(3))
            << "\"\n";

  printSection("5. String Methods");
  std::cout << "String: \"" << s1 << "\"\n";
  std::cout << "Starts with 'He': " << s1->startswith(String::spawn("He"))
            << "\n";
  std::cout << "Ends with 'lo': " << s1->endswith(String::spawn("lo")) << "\n";

  printSection("6. String Replacement");
  auto oldStr = String::spawn("l");
  auto newStr = String::spawn("L");
  std::cout << "Original:  \"" << s1 << "\"\n";
  std::cout << "Replace '" << oldStr << "' with '" << newStr << "': \""
            << s1->replace(oldStr, newStr) << "\"\n";

  printSection("7. String Comparisons");
  std::cout << "\"" << s1 << "\" < \"" << s2 << "\": " << (s1 < s2) << "\n";
  std::cout << "\"" << s2 << "\" > \"" << s1 << "\": " << (s2 > s1) << "\n";

  printSection("8. Error Cases");
  try {
    std::cout << "Testing setAttr('something')...\n";
    s1->setAttr("something", s2);
  } catch (const std::runtime_error& e) {
    std::cout << "Error (expected): " << e.what() << "\n";
  }

  try {
    std::cout << "Testing getAttr('nonexistent')...\n";
    s1->getAttr("nonexistent");
  } catch (const std::runtime_error& e) {
    std::cout << "Error (expected): " << e.what() << "\n";
  }
  printSection("9. String Indexing");
  std::cout << "String: \"" << s1 << "\"\n";
  std::cout << "s1[0]: '" << s1->at(Number(0)) << "'\n";
  std::cout << "s1[4]: '" << s1->at(Number(4)) << "'\n";
  std::cout << "s1[-1]: '" << s1->at(Number(-1)) << "'\n";  // Last character

  try {
    std::cout << "Testing out of bounds index...\n";
    s1->at(Number(10));
  } catch (const std::out_of_range& e) {
    std::cout << "Error (expected): " << e.what() << "\n";
  }

  printSection("10. String Slicing");
  auto hello = String::spawn("Hello World");
  std::cout << "String: \"" << hello << "\"\n";
  std::cout << "hello[0:5]: \"" << (*hello)[Slice(0, 5)] << "\"\n";  // "Hello"
  std::cout << "hello[6:]: \"" << (*hello)[Slice(6, INT_MAX)]
            << "\"\n";  // "World"
  std::cout << "hello[:5]: \"" << hello->slice(Slice(0, 5))
            << "\"\n";  // "Hello"
  std::cout << "hello[-5:]: \"" << (*hello)[Slice(-5, INT_MAX)]
            << "\"\n";  // "World"
  std::cout << "hello[-5:-1]: \"" << (*hello)[Slice(-5, -1)]
            << "\"\n";  // "Worl"

  // Empty slice tests
  std::cout << "Empty slice hello[5:2]: \"" << (*hello)[Slice(5, 2)] << "\"\n";
  std::cout << "Empty string slice: \""
            << (*hello)[Slice(hello->len(), INT_MAX)] << "\"\n";
}

void testLists() {
  printSection("1. Basic List Operations");
  auto list1 = List::spawn();
  list1->append(Number::spawn(1));
  list1->append(String::spawn("hello"));
  list1->append(Number::spawn(3.14));
  std::cout << "Created list with [1, 'hello', 3.14]:\n";
  std::cout << "  Actual: " << *list1 << std::endl;
  std::cout << "  Is non-empty (true): " << std::boolalpha << bool(*list1)
            << std::endl;

  printSection("2. List Extension");
  auto list2 = List::spawn();
  list2->append(Number::spawn(42));
  list2->append(String::spawn("world"));
  std::cout << "Original lists:\n";
  std::cout << "  List1: " << list1 << std::endl;
  std::cout << "  List2: " << list2 << std::endl;
  list1->extend(list2);
  std::cout << "After extending List1 with List2:\n";
  std::cout << "  Expected: [1, 'hello', 3.14, 42, 'world']\n";
  std::cout << "  Actual:   " << list1 << std::endl;

  printSection("3. Pop Operations");
  std::cout << "Original list: " << list1 << std::endl;
  auto popped = list1->pop();
  std::cout << "Pop from end:\n";
  std::cout << "  Popped value: " << popped << std::endl;
  std::cout << "  Remaining list: " << list1 << std::endl;

  popped = list1->pop(Number::spawn(0));
  std::cout << "Pop from start:\n";
  std::cout << "  Popped value: " << popped << std::endl;
  std::cout << "  Remaining list: " << list1 << std::endl;

  printSection("4. List Equality");
  auto list3 = List::spawn();
  auto list4 = List::spawn();
  list3->append(Number::spawn(42));
  list4->append(Number::spawn(42));
  std::cout << "Comparing equal lists [42] == [42]:\n";
  std::cout << "  Expected: true\n";
  std::cout << "  Actual: " << (*list3 == *list4) << std::endl;

  printSection("5. List Operations");
  std::cout << "5.1 Concatenation:\n";
  auto listExtended = *list1 + *list4;
  std::cout << "  List1 + [42]: " << listExtended << std::endl;

  std::cout << "\n5.2 Repetition:\n";
  auto listRepeated = List::spawn();
  listRepeated->append(Number::spawn(1));
  listRepeated->append(Number::spawn(2));
  listRepeated->append(Number::spawn(3));
  std::cout << "  Original: " << listRepeated << std::endl;
  auto repeated = *listRepeated * Number(3);
  std::cout << "  Times 3: " << repeated << std::endl;

  printSection("6. List Modifications");
  std::cout << "6.1 Reverse:\n";
  std::cout << "  Before: " << listRepeated << std::endl;
  listRepeated->reverse();
  std::cout << "  After:  " << listRepeated << std::endl;

  std::cout << "\n6.2 Sort:\n";
  std::cout << "  Before: " << repeated << std::endl;
  repeated->sort();
  std::cout << "  After:  " << repeated << std::endl;

  std::cout << "\n6.3 Remove:\n";
  std::cout << "  Before: " << listRepeated << std::endl;
  listRepeated->remove(Number::spawn(2));
  std::cout << "  After removing 2: " << listRepeated << std::endl;

  printSection("7. Error Handling");
  try {
    auto empty_list = List::spawn();
    std::cout << "Attempting to pop from empty list..." << std::endl;
    empty_list->pop();
  } catch (const std::runtime_error& e) {
    std::cout << "✓ Caught expected error: " << e.what() << std::endl;
  }

  try {
    std::cout << "Attempting to pop at index 999..." << std::endl;
    list1->pop(Number::spawn(999));
  } catch (const std::out_of_range& e) {
    std::cout << "✓ Caught expected error: " << e.what() << std::endl;
  }

  printSection("8. Slicing Operations");
  auto big_list = List::spawn();
  for (int i = 0; i < 5; i++) {
    big_list->append(Number::spawn(i));
  }
  std::cout << "Original list: " << big_list << std::endl;
  std::cout << "Slicing results:\n";
  std::cout << "  [1:3]:  " << (*big_list)[Slice(1, 3)] << std::endl;
  std::cout << "  [-2:]:  " << (*big_list)[Slice(-2, INT_MAX)] << std::endl;
  std::cout << "  [:3]:   " << big_list->slice(Slice(0, 3)) << std::endl;
  std::cout << "  [0]:  " << (*big_list)[Number(0)] << std::endl;

  printSection("9. Complex List Operations");
  auto complexList = List::spawn();
  complexList->append(Number::spawn(1));
  complexList->append(String::spawn("hello"));
  complexList->append(Number::spawn(3.14));

  auto dict = Dictionary::spawn();
  dict->set(String::spawn("int"), Number::spawn(42));
  dict->set(String::spawn("float"), Number::spawn(3.14));
  dict->set(String::spawn("str"), String::spawn("hello"));

  complexList->append(dict);
  std::cout << "Complex list with mixed types including dictionary:\n";
  std::cout << "  " << complexList << std::endl;
}
void testDictionaries() {
  printSection("1. Dictionary Creation and Basic Operations");
  auto dict = Dictionary::spawn();

  std::cout << "Creating dictionary with key-value pairs:\n";
  std::cout << "Adding: {'int': 42, 'float': 3.14, 'str': 'hello'}\n";

  dict->set(String::spawn("int"), Number::spawn(42));
  dict->set(String::spawn("float"), Number::spawn(3.14));
  dict->set(String::spawn("str"), String::spawn("hello"));

  std::cout << "Result:  " << dict << "\n";

  printSection("2. Complex Value Types");
  std::cout << "Adding list [1, 'two'] with key 'list'\n";
  auto list = List::spawn();
  list->append(Number::spawn(1));
  list->append(String::spawn("two"));
  dict->set(String::spawn("list"), list);
  std::cout << "After adding list: " << dict << "\n";

  printSection("3. Dictionary Methods");
  std::cout << "Original dict: " << dict << "\n";
  std::cout << "Keys   → " << dict->keys() << "\n";
  std::cout << "Values → " << dict->values() << "\n";
  std::cout << "Items  → " << dict->items() << "\n";

  printSection("4. Access and Modification");
  try {
    auto intKey = String::spawn("int");
    std::cout << "Getting value for key 'int':\n";
    std::cout << "  Before: " << dict->get(intKey) << "\n";

    std::cout << "Modifying 'int' value to 100\n";
    dict->set(intKey, Number::spawn(100));
    std::cout << "  After:  " << dict->get(intKey) << "\n";
  } catch (const std::runtime_error& e) {
    std::cout << "❌ Error: " << e.what() << "\n";
  }

  printSection("5. Dictionary Operations");
  auto dict2 = Dictionary::spawn();
  dict2->set(String::spawn("new_key"), Number::spawn(999));

  std::cout << "dict1: " << dict << "\n";
  std::cout << "dict2: " << dict2 << "\n";
  std::cout << "Merging dictionaries (dict1 | dict2):\n";
  auto merged = *dict | *dict2;
  std::cout << "Result: " << merged << "\n";

  printSection("6. Error Handling");
  try {
    std::cout << "Attempting to get nonexistent key...\n";
    dict->get(String::spawn("nonexistent"));
    std::cout << "❌ This should not print\n";
  } catch (const std::runtime_error& e) {
    std::cout << "✓ Caught expected error: " << e.what() << "\n";
  }

  printSection("7. Special Cases");
  auto empty_dict = Dictionary::spawn();
  std::cout << "Empty dictionary:\n";
  std::cout << "  toString(): " << empty_dict << "\n";
  std::cout << "  bool():     " << std::boolalpha << bool(*empty_dict) << "\n";

  try {
    std::cout << "Attempting to use unhashable key (List)...\n";
    dict->set(list, String::spawn("value"));
  } catch (const std::runtime_error& e) {
    std::cout << "✓ Caught expected error: " << e.what() << "\n";
  }

  printSection("8. Dictionary Comparison");
  auto dict3 = Dictionary::spawn();
  dict3->set(String::spawn("int"), Number::spawn(42));

  auto dict4 = Dictionary::spawn();
  dict4->set(String::spawn("int"), Number::spawn(42));

  std::cout << "Comparing identical dictionaries:\n";
  std::cout << "dict3: " << dict3 << "\n";
  std::cout << "dict4: " << dict4 << "\n";
  std::cout << "dict3 == dict4: " << std::boolalpha << (*dict3 == *dict4)
            << "\n";
}

void testTuple() {
  printSection("1. Tuple Creation and Basic Operations");

  // Create a Tuple with three elements
  auto tuple1 = Tuple<3>::spawn(Number::spawn(42), String::spawn("hello"),
                                Number::spawn(3.14));

  std::cout << "Created tuple with (42, 'hello', 3.14):\n";
  std::cout << "  Expected: (42, 'hello', 3.14)\n";
  std::cout << "  Actual:   " << tuple1 << "\n";

  std::cout << "\nElement Access:\n";
  std::cout << "  [0] Expected: 42\n";
  std::cout << "      Actual:   " << (*tuple1)[Number::spawn(0)] << "\n";

  std::cout << "  [1] Expected: hello\n";
  std::cout << "      Actual:   " << *tuple1->at(Number(1)) << "\n";
  std::cout << "  [2] Expected: 3.14\n";
  std::cout << "      Actual:   " << *tuple1->at(Number(2)) << "\n";

  printSection("2. Tuple Equality Testing");
  auto tuple2 = Tuple<3>::spawn(Number::spawn(42), String::spawn("hello"),
                                Number::spawn(3.14));

  auto tuple3 = Tuple<3>::spawn(Number::spawn(42),
                                String::spawn("world"),  // Different value
                                Number::spawn(3.14));

  std::cout << "Comparing identical tuples:\n";
  std::cout << "  tuple1: " << tuple1 << "\n";
  std::cout << "  tuple2: " << tuple2 << "\n";
  std::cout << "  tuple1 == tuple2: " << (*tuple1 == *tuple2) << "\n";

  std::cout << "\nComparing different tuples:\n";
  std::cout << "  tuple1: " << tuple1 << "\n";
  std::cout << "  tuple3: " << tuple3 << "\n";
  std::cout << "  tuple1 == tuple3: " << (*tuple1 == *tuple3) << "\n";
  printSection("3. Tuple Hashing");
  std::cout << "Hash values for equal tuples should be equal:\n";
  std::cout << "  Hash(tuple1): " << tuple1->hash() << "\n";
  std::cout << "  Hash(tuple2): " << tuple2->hash() << "\n";
  std::cout << "  Hashes equal: " << (tuple1->hash() == tuple2->hash()) << "\n";

  printSection("4. Empty Tuple");
  auto emptyTuple = Tuple<0>::spawn();
  std::cout << "Empty tuple representation:\n";
  std::cout << "  Expected: ()\n";
  std::cout << "  Actual:   " << emptyTuple << "\n";
  std::cout << "  Bool value (should be false): " << (bool(*emptyTuple))
            << "\n";

  printSection("5. Iterator Testing");
  std::cout << "Iterating over tuple (42, 'hello', 3.14):\n";
  std::cout << "  Elements: ";
  for (const auto& element : *tuple1) {
    if (element) {
      std::cout << element << " ";
    } else {
      std::cout << "null ";
    }
  }
  std::cout << "\n";

  printSection("6. Error Handling");
  std::cout << "Testing invalid index access:\n";
  std::cout << "  Tuple size: " << tuple1->count() << "\n";
  try {
    std::cout << "  Accessing index 5..." << "\n";
    const auto invalidElement = tuple1->at(Number::spawn(5));
    std::cout << "❌ Should not reach here\n";
  } catch (const std::runtime_error& e) {
    std::cout << "✓ Caught expected error: " << e.what() << "\n";
  }
  printSection("7. Tuple operations");
  auto tuple4 = Tuple<3>::spawn(Number::spawn(42), String::spawn("hello"),
                                Number::spawn(3.14));
  auto tuple5 = Tuple<3>::spawn(Number::spawn(42), String::spawn("hello"),
                                Number::spawn(3.14));
  std::cout << "Tuple4: " << tuple4 << "\n";
  std::cout << "Tuple5: " << tuple5 << "\n";
  std::cout << "Tuple4 + Tuple5: " << (*tuple4 + *tuple5) << "\n";
}

void testSet() {
  printSection("1. Set Creation and Basic Operations");
  auto set1 = Set::spawn();
  set1->add(Number::spawn(1));
  set1->add(Number::spawn(2));
  set1->add(String::spawn("hello"));

  std::cout << "Created set with {1, 2, 'hello'}:\n";
  std::cout << "  Expected: {1, 2, 'hello'}\n";
  std::cout << "  Actual:   " << set1 << "\n";
  std::cout << "  Count:    " << set1->count() << " (Expected: 3)\n";

  printSection("2. Membership Testing");
  std::cout << "Testing membership:\n";
  std::cout << "  Contains 1:      " << (set1->exists(Number::spawn(1)))
            << "\n";
  std::cout << "  Contains 'world': " << (set1->exists(String::spawn("world")))
            << "\n";

  printSection("3. Duplicate Handling");
  std::cout << "Adding duplicate element (1):\n";
  std::cout << "  Before: " << set1 << "\n";
  set1->add(Number::spawn(1));
  std::cout << "  After:  " << set1 << " (should be unchanged)\n";

  printSection("4. Set Operations");
  auto set2 = Set::spawn();
  set2->add(Number::spawn(3));
  set2->add(String::spawn("world"));

  std::cout << "Set1: " << set1 << "\n";
  std::cout << "Set2: " << set2 << "\n";

  std::cout << "\nUnion Operation (|):\n";
  std::cout << "  Expected: {1, 2, 'hello', 3, 'world'}\n";
  std::cout << "  Actual:   " << (*set1 | *set2) << "\n";

  std::cout << "\nIntersection Operation (&):\n";
  std::cout << "  Expected: {}\n";
  std::cout << "  Actual:   " << (*set1 & *set2) << "\n";

  std::cout << "\nDifference Operation (-):\n";
  std::cout << "  Expected: {1, 2, 'hello'}\n";
  std::cout << "  Actual:   " << (*set1 - *set2) << "\n";

  std::cout << "\nSymmetric Difference Operation (^):\n";
  std::cout << "  Expected: {1, 2, 'hello', 3, 'world'}\n";
  std::cout << "  Actual:   " << (*set1 ^ *set2) << "\n";

  printSection("5. Set Equality");
  auto set3 = Set::spawn();
  set3->add(Number::spawn(1));
  set3->add(Number::spawn(2));
  set3->add(String::spawn("hello"));

  std::cout << "Comparing identical sets:\n";
  std::cout << "  Set1: " << set1 << "\n";
  std::cout << "  Set3: " << set3 << "\n";
  std::cout << "  Equal: " << (set1->equals(*set3) ? "✓" : "❌") << "\n";

  std::cout << "\nHash consistency check:\n";
  std::cout << "  Hash(Set1) == Hash(Set3): "
            << (set1->hash() == set3->hash() ? "✓" : "❌") << "\n";

  printSection("6. Error Handling");
  try {
    std::cout << "Testing getAttr('nonexistent')...\n";
    set1->getAttr("nonexistent");
    std::cout << "❌ Should have thrown\n";
  } catch (const std::runtime_error& e) {
    std::cout << "✓ Caught expected error: " << e.what() << "\n";
  }

  try {
    std::cout << "\nTesting setAttr('key', 42)...\n";
    set1->setAttr("key", Number::spawn(42));
    std::cout << "❌ Should have thrown\n";
  } catch (const std::runtime_error& e) {
    std::cout << "✓ Caught expected error: " << e.what() << "\n";
  }

  printSection("7. Set Clearing");
  std::cout << "Before clear: " << set1 << "\n";
  set1->clear();
  std::cout << "After clear:\n";
  std::cout << "  Expected: {}\n";
  std::cout << "  Actual:   " << set1 << "\n";
  std::cout << "  Count:    " << set1->count() << " (Expected: 0)\n";
}
void testNone() {
  printSection("1. None Singleton Pattern");
  auto none1 = None::spawn();
  auto none2 = None::spawn();

  std::cout << "Singleton pattern:\n";
  std::cout << "  Same instance: " << (none1 == none2 ? "✓" : "❌") << "\n";
  std::cout << "  Address equality: "
            << (none1.get() == none2.get() ? "✓" : "❌") << "\n";

  printSection("2. Basic Properties");
  std::cout << "String representation:\n";
  std::cout << "  toString(): " << none1->toString() << "\n";
  std::cout << "  type(): " << none1->type() << "\n";
  std::cout << "  repr(): " << none1->repr() << "\n";

  printSection("3. Boolean Context");
  std::cout << "None is always false:\n";
  std::cout << "  toBool(): " << (none1->toBool() ? "❌" : "✓") << "\n";
  std::cout << "  bool cast: " << (bool(*none1) ? "❌" : "✓") << "\n";

  printSection("4. Comparison Operations");
  auto none3 = None::spawn();
  auto number = Number::spawn(42);

  std::cout << "Equality:\n";
  std::cout << "  None == None: " << (none1->equals(*none2) ? "✓" : "❌")
            << "\n";
  std::cout << "  None == Number: " << (!none1->equals(*number) ? "✓" : "❌")
            << "\n";

  std::cout << "\nOrdering:\n";
  std::cout << "  None < Number: "
            << (none1->compare(*number) == std::strong_ordering::less ? "✓"
                                                                      : "❌")
            << "\n";
  std::cout << "  None == None: "
            << (none1->compare(*none2) == std::strong_ordering::equal ? "✓"
                                                                      : "❌")
            << "\n";

  printSection("5. Type Checking");
  std::cout << "isinstance checks:\n";
  std::cout << "  NoneType: " << (none1->isInstance("NoneType") ? "✓" : "❌")
            << "\n";
  std::cout << "  object: " << (none1->isInstance("object") ? "✓" : "❌")
            << "\n";
  std::cout << "  other: " << (!none1->isInstance("other") ? "✓" : "❌")
            << "\n";

  printSection("6. Error Handling");
  std::cout << "Testing operations:\n";

  try {
    none1->operator+(*number);
    std::cout << "❌ Should have thrown on addition\n";
  } catch (const std::runtime_error& e) {
    std::cout << "✓ Addition error: " << e.what() << "\n";
  }

  try {
    none1->getAttr("something");
    std::cout << "❌ Should have thrown on getAttr\n";
  } catch (const std::runtime_error& e) {
    std::cout << "✓ Attribute error: " << e.what() << "\n";
  }

  try {
    none1->setAttr("something", number);
    std::cout << "❌ Should have thrown on setAttr\n";
  } catch (const std::runtime_error& e) {
    std::cout << "✓ Attribute error: " << e.what() << "\n";
  }

  printSection("7. Hash Consistency");
  std::cout << "Hash value:\n";
  std::cout << "  None hash is 0: " << (none1->hash() == 0 ? "✓" : "❌")
            << "\n";
  std::cout << "  Consistent hash: "
            << (none1->hash() == none2->hash() ? "✓" : "❌") << "\n";
}
void testClass() {
    const std::string BLUE = "\033[34m";
    const std::string CYAN = "\033[36m";
    const std::string YELLOW = "\033[33m";
    const std::string RESET = "\033[0m";

    auto compareResult = [&](const std::string& testName,
                           const std::string& expected,
                           const std::string& actual) {
        std::cout << testName << ":\n"
                 << "  Expected: " << CYAN << expected << RESET << "\n"
                 << "  Actual:   " << YELLOW << actual << RESET << "\n\n";
    };

    std::cout << BLUE << "=== 1. Class Definition ===" << RESET << "\n";
    auto Animal = Class::defineClass("Animal");
    compareResult("Class type", "Animal", Animal->type());
    compareResult("Instance check", "true", 
                 std::to_string(Animal->isInstance("object")));

    std::cout << BLUE << "\n=== 2. Method Definition ===" << RESET << "\n";
    Animal->defineMethod("speak", [](const Arguments& args) {
        return String::spawn("Generic animal sound");
    });

    Animal->defineInit([](auto self, const Arguments& args) {
        auto species = Function::getArg<String>(args, "species");
        self->defineAttribute("species", species);
    });

    std::cout << "Class structure:\n" << YELLOW 
              << Animal->serialize() << RESET << "\n";

    std::cout << BLUE << "\n=== 3. Instance Creation ===" << RESET << "\n";
    auto instance = Animal->spawn({
        {"species", String::spawn("mammal")}
    });
    
    compareResult("Instance type", "Animal", instance->type());
    compareResult("Species attribute", "'mammal'", 
                 instance->getAttr("species")->toString());
    compareResult("Speak method", "'Generic animal sound'",
                 instance->method("speak")->toString());

    std::cout << BLUE << "\n=== 4. Inheritance ===" << RESET << "\n";
    auto Dog = Class::defineSubclass("Dog", Animal);
    Dog->defineMethod("speak", [](const Arguments& args) {
        return String::spawn("Woof!");
    });

    auto dogInstance = Dog->spawn({
        {"species", String::spawn("canine")}
    });

    compareResult("Inherited type check", "True",
                 (dogInstance->isInstance("Animal")? "True" : "False"));
    compareResult("Method override", "'Woof!'",
                 dogInstance->method("speak")->toString());

    std::cout << BLUE << "\n=== 5. Error Handling ===" << RESET << "\n";
    try {
        instance->getAttr("nonexistent");
    } catch (const std::runtime_error& e) {
        compareResult("Attribute error",
                     "'Animal-Instance': object has no attribute 'nonexistent'",
                     e.what());
    }

    try {
        Animal->defineMethod("speak", [](const Arguments&) {
            return None::spawn();
        });
    } catch (const std::runtime_error& e) {
        compareResult("Method redefinition error",
                     "Cannot redefine method after class instantiation",
                     e.what());
    }

    std::cout << BLUE << "\n=== 6. Method Resolution Order ===" << RESET << "\n";
    auto mro = dogInstance->getMethodResolutionOrder();
    std::cout << "Inheritance chain:\n";
    for (size_t i = 0; i < mro.size(); ++i) {
        std::cout << CYAN << "  " << i << ": " 
                 << mro[i]->serialize(1) << RESET << "\n";
    }
}
void testComplexClasses() {
    const std::string BLUE = "\033[34m";
    const std::string CYAN = "\033[36m";
    const std::string YELLOW = "\033[33m";
    const std::string RESET = "\033[0m";

    auto compareResult = [&](const std::string& testName,
                           const std::string& expected,
                           const std::string& actual) {
        std::cout << testName << ":\n"
                 << "  Expected: " << CYAN << expected << RESET << "\n"
                 << "  Actual:   " << YELLOW << actual << RESET << "\n\n";
    };

    std::cout << BLUE << "=== 1. Vehicle Base Class ===" << RESET << "\n";
    auto Vehicle = Class::defineClass("Vehicle");
    Vehicle->defineInit([](auto self, const Arguments& args) {
        auto brand = Function::getArg<String>(args, "brand");
        auto year = Function::getArg<Number>(args, "year");
        self->defineAttribute("brand", brand);
        self->defineAttribute("year", year);
    });

    Vehicle->defineMethod("describe", [](const Arguments& args) {
        auto self = Function::getArg<Class>(args, "self");
        auto brand = self->get("brand");
        auto year = self->get("year");
        return String::spawn("Vehicle: " + brand->toString() + " (" + 
                           year->toString() + ")");
});

    std::cout << BLUE << "\n=== 2. Car Subclass ===" << RESET << "\n";
    auto Car = Class::defineSubclass("Car", Vehicle);
    Car->defineInit([](auto self, const Arguments& args) {
        auto brand = Function::getArg<String>(args, "brand");
        auto year = Function::getArg<Number>(args, "year");
        self->defineAttribute("brand", brand);
        self->defineAttribute("year", year);
        self->defineAttribute("wheels", Number::spawn(4));
    });
    Car->defineMethod("describe", [](const Arguments& args) {
        auto self = Function::getArg<Class>(args, "self");
        auto brand = self->get("brand");
        auto year = self->get("year");
        return String::spawn("Car: " + brand->toString() + " (" + 
                           year->toString() + ")");
    });
    Car->defineMethod("compute_value", [](const Arguments& args) {
        auto self = Function::getArg<Class>(args, "self");
        auto year = self->get<Number>("year");
        return Number::spawn(year * Number::spawn(1000));
    });

    std::cout << BLUE << "\n=== 3. Instance Creation ===" << RESET << "\n";
    auto toyota = Car->spawn({
        {"brand", String::spawn("Toyota")},
        {"year", Number::spawn(2023)}
    });

    compareResult("Instance type", "Car-Instance", toyota->type());
    compareResult("Description", "'Car: Toyota (2023)'",
                 toyota->method("describe")->toString());
    std::cout << "Value: " << toyota->method("compute_value") << "\n";

    std::cout << BLUE << "\n=== 4. Attribute Access ===" << RESET << "\n";
    compareResult("Brand", "'Toyota'", 
                 toyota->getAttr("brand")->toString());
    compareResult("Year", "2023", 
                 toyota->getAttr("year")->toString());

    std::cout << BLUE << "\n=== 5. Error Cases ===" << RESET << "\n";
try {
        toyota->getAttr("nonexistent");
    } catch (const std::runtime_error& e) {
        compareResult("Missing attribute",
                     "In class 'Car': no such attribute 'nonexistent'",
                     e.what());
    }

    try {
        Car->spawn({{"brand", String::spawn("Honda")}});  // Missing year
    } catch (const std::runtime_error& e) {
        compareResult("Missing argument",
                     "In class 'Car': missing required argument 'year'",
                     e.what());
    }
}
// Helper to define a method
int main(int argc, char** argv) {
  std::vector<std::function<void()>> tests{
      testNumbers,      testBool, testStrings,   testLists, testTuple,
      testDictionaries, testSet,  testFunctions, testNone, testClass, testComplexClasses};

  if (argc == 2) {
    size_t testNumber = std::stoi(std::string(argv[1]));

    if (testNumber >= tests.size()) {
      std::cerr << "Test number " << std::to_string(testNumber)
                << " given when test amount is "
                << std::to_string(tests.size());
      return 1;
    }

    tests[testNumber]();
  } else {
    for (auto& test : tests) test();
  }

  return 0;
}