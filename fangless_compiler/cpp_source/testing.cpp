#include <iostream>

#include "Number.hpp"
#include "String.hpp"
#include "List.hpp"
#include "Dictionary.hpp"

void printResult(const std::string& op, const Object& result) {
  std::cout << op << ": " << result << std::endl;
}

void printSection(const std::string& title) {
  std::cout << "\n=== " << title << " ===\n";
}

void testNumbers() {
  // Create test numbers
  auto i1 = std::make_shared<Int>(10);
  auto i2 = std::make_shared<Int>(3);
  auto f1 = std::make_shared<Float>(10.5);
  auto f2 = std::make_shared<Float>(3.2);

  std::cout << "=== Integer Operations ===" << std::endl;
  printResult("10 + 3", *(*i1 + *i2));
  printResult("10 - 3", *(*i1 - *i2));
  printResult("10 * 3", *(*i1 * *i2));
  printResult("10 / 3", *(*i1 / *i2));  // Should return float

  std::cout << "\n=== Float Operations ===" << std::endl;
  printResult("10.5 + 3.2", *(*f1 + *f2));
  printResult("10.5 - 3.2", *(*f1 - *f2));
  printResult("10.5 * 3.2", *(*f1 * *f2));
  printResult("10.5 / 3.2", *(*f1 / *f2));

  std::cout << "\n=== Mixed Operations ===" << std::endl;
  printResult("10 + 3.2", *(*i1 + *f2));
  printResult("10.5 + 3", *(*f1 + *i2));
  printResult("10 / 3.2", *(*i1 / *f2));
  printResult("10.5 / 3", *(*f1 / *i2));

  std::cout << "\n=== Comparisons ===" << std::endl;
  std::cout << "10 < 3: " << (*i1 < *i2) << std::endl;
  std::cout << "10.5 > 3.2: " << (*f1 > *f2) << std::endl;

  std::cout << "\n=== Special Cases ===" << std::endl;
  auto inf = std::make_shared<Float>(std::numeric_limits<double>::infinity());
  auto nan = std::make_shared<Float>(std::numeric_limits<double>::quiet_NaN());

  printResult("inf", *inf);
  printResult("nan", *nan);
  std::cout << "inf.isInf(): " << inf->isInf() << std::endl;
  std::cout << "nan.isNaN(): " << nan->isNaN() << std::endl;
}

void testStrings() {
  printSection("Basic String Operations");
  auto s1 = std::make_shared<String>("Hello");
  auto s2 = std::make_shared<String>("World");
  auto s3 = std::make_shared<String>("Hello");

  std::cout << "s1: " << s1 << std::endl;
  std::cout << "s2: " << s2 << std::endl;
  std::cout << "s1 == s3: " << (*s1 == *s3) << std::endl;
  std::cout << "Empty string bool: " << bool(String("")) << std::endl;

  printSection("String Methods");
  auto upper = s1->upper();
  auto lower = s2->lower();
  auto spaces = std::make_shared<String>("  trim me  ");
  auto stripped = spaces->strip();

  std::cout << "Upper: " << *upper << std::endl;
  std::cout << "Lower: " << *lower << std::endl;
  std::cout << "Strip: '" << *stripped << "'" << std::endl;

  printSection("String Operations");
  auto concatenated = *s1 + *s2;
  auto repeated = *s1 * 3;

  std::cout << "Concatenated: " << *concatenated << std::endl;
  std::cout << "Repeated: " << *repeated << std::endl;

  printSection("String Methods");
  std::cout << "Starts with 'He': " << s1->startswith(String("He"))
            << std::endl;
  std::cout << "Ends with 'ld': " << s2->endswith(String("ld")) << std::endl;

  auto replaced = s1->replace(String("l"), String("L"));
  std::cout << "Replace 'l' with 'L': " << *replaced << std::endl;

  printSection("Comparisons");
  std::cout << "s1 < s2: " << (*s1 < *s2) << std::endl;
  std::cout << "s1 > s2: " << (*s1 > *s2) << std::endl;

  printSection("Error Handling");
  try {
    s1->setAttr("something", s2);
  } catch (const std::runtime_error& e) {
    std::cout << "Expected error: " << e.what() << std::endl;
  }

  try {
    s1->getAttr("nonexistent");
  } catch (const std::runtime_error& e) {
    std::cout << "Expected error: " << e.what() << std::endl;
  }
}

void testLists() {
    printSection("List Creation and Basic Operations");
    auto list1 = std::make_shared<List>();
    list1->append(std::make_shared<Int>(1));
    list1->append(std::make_shared<String>("hello"));
    list1->append(std::make_shared<Float>(3.14));
    
    std::cout << "List1: " << *list1 << std::endl;
    std::cout << "List1 bool value: " << bool(*list1) << std::endl;
    
    printSection("List Extension");
    auto list2 = std::make_shared<List>();
    list2->append(std::make_shared<Int>(42));
    list2->append(std::make_shared<String>("world"));
    
    std::cout << "List2: " << *list2 << std::endl;
    list1->extend(*list2);
    std::cout << "List1 after extend: " << *list1 << std::endl;
    
    printSection("Pop Operations");
    auto popped = list1->pop();
    std::cout << "Popped from end: " << *popped << std::endl;
    std::cout << "List after pop: " << *list1 << std::endl;
    
    popped = list1->pop(0);
    std::cout << "Popped from start: " << *popped << std::endl;
    std::cout << "List after pop(0): " << *list1 << std::endl;
    
    printSection("Equality Testing");
    auto list3 = std::make_shared<List>();
    list3->append(std::make_shared<Int>(42));
    auto list4 = std::make_shared<List>();
    list4->append(std::make_shared<Int>(42));
    
    std::cout << "list3 == list4: " << (*list3 == *list4) << std::endl;
    
    printSection("Exception Handling");
    try {
        auto empty_list = std::make_shared<List>();
        empty_list->pop();
    } catch (const std::runtime_error& e) {
        std::cout << "Expected error: " << e.what() << std::endl;
    }
    
    try {
        list1->pop(999);
    } catch (const std::out_of_range& e) {
        std::cout << "Expected error: " << e.what() << std::endl;
    }
    
    printSection("Slicing");
    auto big_list = std::make_shared<List>();
    for(int i = 0; i < 5; i++) {
        big_list->append(std::make_shared<Int>(i));
    }
    
    std::cout << "Original list: " << *big_list << std::endl;
    std::cout << "Slice [1:3]: " << *(*big_list)[Slice(1,3)] << std::endl;
    std::cout << "Slice [-2:]: " << *(*big_list)[Slice(-2, INT_MAX)] << std::endl;
    std::cout << "Slice [:3]: " << *(*big_list)[Slice(0, 3)] << std::endl;
}

void testDictionaries() {
    printSection("Basic Dictionary Operations");
    auto dict = std::make_shared<Dictionary>();
    
    // Add different types of values
    dict->set(std::make_shared<String>("int"), std::make_shared<Int>(42));
    dict->set(std::make_shared<String>("float"), std::make_shared<Float>(3.14));
    dict->set(std::make_shared<String>("string"), std::make_shared<String>("hello"));
    
    // Create and add a list
    auto list = std::make_shared<List>();
    list->append(std::make_shared<Int>(1));
    list->append(std::make_shared<String>("two"));
    dict->set(std::make_shared<String>("list"), list);
    
    std::cout << "Dictionary: " << *dict << std::endl;

    printSection("Dictionary Methods");
    std::cout << "Keys: " << *(dict->keys()) << std::endl;
    std::cout << "Values: " << *(dict->values()) << std::endl;
    std::cout << "Items: " << *(dict->items()) << std::endl;

    printSection("Access and Modification");
    // Wrap key access in try-catch
    try {
        auto key = std::make_shared<String>("int");
        auto value = dict->get(key);
        std::cout << "Get 'int': " << *value << std::endl;
        
        // Modify value
        dict->set(key, std::make_shared<Int>(100));
        std::cout << "After modification: " << *dict << std::endl;
    } catch (const std::runtime_error& e) {
        std::cout << "Error accessing key: " << e.what() << std::endl;
    }

    printSection("Dictionary Merging");
    auto dict2 = std::make_shared<Dictionary>();
    dict2->set(std::make_shared<String>("new_key"), std::make_shared<Int>(999));
    
    auto merged = *dict | *dict2;
    std::cout << "Merged dictionary: " << *merged << std::endl;

    printSection("Error Handling");
    try {
        // Try to get non-existent key
        dict->get(std::make_shared<String>("nonexistent"));
        std::cout << "This should not print" << std::endl;
    } catch (const std::runtime_error& e) {
        std::cout << "Expected error: " << e.what() << std::endl;
    }

    // Test empty dictionary
    auto empty_dict = std::make_shared<Dictionary>();
    std::cout << "Empty dictionary: " << *empty_dict << std::endl;
    std::cout << "Empty dictionary bool value: " << bool(*empty_dict) << std::endl;
}

int main() {
  testNumbers();
  testStrings();
  testLists();
  // not working
  testDictionaries();
  return 0;
}