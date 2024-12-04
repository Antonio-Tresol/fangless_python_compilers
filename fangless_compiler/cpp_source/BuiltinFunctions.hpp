#ifndef BUILTIN_FUNCTIONS_HPP
#define BUILTIN_FUNCTIONS_HPP
#include <algorithm>
#include <cstdlib>
#include <cmath>
#include <fstream>
#include <functional>
#include <iostream>
#include <memory>
#include <numeric>
#include <string>
#include <stdexcept>
#include <filesystem>
#include <type_traits>

#include "Bool.hpp"
#include "Dictionary.hpp"
#include "Iterable.hpp"
#include "Function.hpp"
#include "List.hpp"
#include "None.hpp"
#include "Number.hpp"
#include "Set.hpp"
#include "String.hpp"
#include "Tuple.hpp"


// Namespace for builtin functions
namespace BF {
  std::shared_ptr<Number> abs(const std::shared_ptr<Number>& num) {
    if (num->isDouble()) {
      return Number::spawn(std::abs(num->getDouble()));
    }
    return Number::spawn(static_cast<int64_t>(std::abs(num->getInt())));
  }

  std::shared_ptr<Number> abs(const bool& num) {
    return abs(Number::spawn(num? 1: 0));
  }

  std::shared_ptr<Number> abs(const int& num) {
    return abs(Number::spawn(num));
  }

  std::shared_ptr<Bool> any(const std::shared_ptr<String>& string) {
    return Bool::spawn(string->toBool());
  }

  std::shared_ptr<Bool> any(const std::shared_ptr<Dictionary>& structure) {
    bool hasTrue = false;
    std::shared_ptr<List> keys = structure->keys();

    for (auto& item: (*keys)) {
      hasTrue = hasTrue || item->toBool();
      if (hasTrue) break;
    }

    return Bool::spawn(hasTrue);
  }

  template<TIterable TType>
  std::shared_ptr<Bool> any(const std::shared_ptr<TType>& structure) {
    bool hasTrue = false;
    for (auto& item: (*structure)) {
      hasTrue = hasTrue || item->toBool();
      if (hasTrue) break;
    }

    return Bool::spawn(hasTrue);
  }

  std::shared_ptr<Bool> bool_() {
    return Bool::spawn(false);
  }

  std::shared_ptr<Bool> bool_(const std::shared_ptr<Object>& object) {
    return Bool::spawn(object->toBool());
  }

  std::shared_ptr<Bool> bool_(const bool& object) {
    return Bool::spawn(object);
  }

  std::shared_ptr<Bool> bool_(const int& object) {
    return Bool::spawn(object? true : false);
  }

  std::shared_ptr<Tuple> tuple(const std::shared_ptr<Dictionary>& items) {
    std::shared_ptr<List> keys = items->keys();
    return std::make_shared<Tuple>(keys->begin(), keys->end());
  }

  template<TIterable TType>
  std::shared_ptr<Tuple> tuple(const std::shared_ptr<TType>& items) {
    return std::make_shared<Tuple>(items->begin(), items->end());
  }

  std::shared_ptr<String> type(const bool&) {
    return String::spawn("bool");
  }

  std::shared_ptr<String> type(const int&) {
    return String::spawn("bool");
  }

  std::shared_ptr<String> type(const std::shared_ptr<const Object>& anything) {
    return String::spawn(anything->type());
  }

  std::shared_ptr<std::wstring> chr(const std::shared_ptr<Number>& code) {
    std::wstring str;
    const int codeInt = code->getInt();

    if (codeInt <= 0xFFFF) {
      str += static_cast<wchar_t>(codeInt);
    } else if (codeInt <= 0x10FFFF) {
      str += static_cast<wchar_t>(0xD800 + ((codeInt - 0x10000) >> 10));
      str += static_cast<wchar_t>(0xDC00 + ((codeInt - 0x10000) & 0x3FF));
    } else {
      throw std::out_of_range(
        "Code is out of valid Unicode range (0x0 to 0x10FFFF)."
      );
    }

    return std::make_shared<std::wstring>(str);
  }

  std::shared_ptr<std::wstring> chr(const std::shared_ptr<Bool>& code) {
    return chr(Number::spawn(code->toBool()? 1:0));
  }

  std::shared_ptr<std::wstring> chr(const bool& code) {
    return chr(Number::spawn(code? 1:0));
  }

  std::shared_ptr<std::wstring> chr(const int& code) {
    return chr(Number::spawn(code));
  }

  std::shared_ptr<Dictionary> dict() {
    return Dictionary::spawn();
  }

  std::shared_ptr<Tuple> divmod(const std::shared_ptr<Number>& dividend,
    const std::shared_ptr<Number>& divisor) {
    if (divisor == Number::spawn(0)) {
      throw std::runtime_error("Attempted to perform a division by 0");
    }

    if (dividend->isDouble() || divisor->isDouble()) {
      std::shared_ptr<Number> quotient =
        Number::spawn(static_cast<double>(
          ((*dividend) / (*divisor))->getInt()));

      std::shared_ptr<Number> remainder =
        Number::spawn(((*dividend) % (*divisor))->getDouble());

      return Tuple::spawn({quotient, remainder});
    }

    std::shared_ptr<Number> quotient =
      Number::spawn(((*dividend) / (*divisor))->getInt());
    std::shared_ptr<Number> remainder =
      Number::spawn(((*dividend) % (*divisor))->getInt());

    return Tuple::spawn({quotient, remainder});
  }

  std::shared_ptr<Tuple> divmod(const std::shared_ptr<Number>& dividend,
    const std::shared_ptr<Bool>& divisor) {
    return divmod(dividend, Number::spawn(divisor->toBool()? 1 : 0));
  }

  std::shared_ptr<Tuple> divmod(const std::shared_ptr<Bool>& dividend,
    const std::shared_ptr<Number>& divisor) {
    return divmod(Number::spawn(dividend->toBool()? 1 : 0), divisor);
  }

  std::shared_ptr<Tuple> divmod(const std::shared_ptr<Bool>& dividend,
    const std::shared_ptr<Bool>& divisor) {
    return divmod(Number::spawn(dividend->toBool()? 1 : 0),
      Number::spawn(divisor->toBool()? 1 : 0));
  }

  std::shared_ptr<Tuple> divmod(const std::shared_ptr<Number>& dividend,
    const bool& divisor) {
    return divmod(dividend, Number::spawn(divisor? 1 : 0));
  }

  std::shared_ptr<Tuple> divmod(const bool& dividend,
    const std::shared_ptr<Number>& divisor) {
    return divmod(Number::spawn(dividend? 1 : 0), divisor);
  }

  std::shared_ptr<Tuple> divmod(const bool& dividend,
    const bool& divisor) {
    return divmod(Number::spawn(dividend? 1 : 0),
      Number::spawn(divisor? 1 : 0));
  }

  std::shared_ptr<Tuple> divmod(const std::shared_ptr<Number>& dividend,
    const int& divisor) {
    return divmod(dividend, Number::spawn(divisor));
  }

  std::shared_ptr<Tuple> divmod(const int& dividend,
    const std::shared_ptr<Number>& divisor) {
    return divmod(Number::spawn(dividend), divisor);
  }

  std::shared_ptr<Tuple> divmod(const int& dividend,
    const int& divisor) {
    return divmod(Number::spawn(dividend), Number::spawn(divisor));
  }

  std::shared_ptr<Tuple> divmod(const std::shared_ptr<Bool>& dividend,
    const bool& divisor) {
    return divmod(dividend, Number::spawn(divisor ? 1 : 0));
  }

  std::shared_ptr<Tuple> divmod(const bool& dividend,
    const std::shared_ptr<Bool>& divisor) {
      return divmod(Number::spawn(dividend ? 1 : 0), divisor);
  }

  std::shared_ptr<Tuple> divmod(const std::shared_ptr<Bool>& dividend,
    const int& divisor) {
    return divmod(Number::spawn(dividend->toBool() ? 1 : 0),
      Number::spawn(divisor));
  }

  std::shared_ptr<Tuple> divmod(const int& dividend,
    const std::shared_ptr<Bool>& divisor) {
      return divmod(Number::spawn(dividend),
        Number::spawn(divisor->toBool() ? 1 : 0));
  }

  std::shared_ptr<Tuple> divmod(const bool& dividend, const int& divisor) {
    return divmod(Number::spawn(dividend ? 1 : 0), Number::spawn(divisor));
  }

  std::shared_ptr<Tuple> divmod(const int& dividend, const bool& divisor) {
      return divmod(Number::spawn(dividend), Number::spawn(divisor ? 1 : 0));
  }

  std::shared_ptr<List> enumerate(const std::shared_ptr<String>& items,
    std::shared_ptr<Number> start = Number::spawn(0)) {
    std::shared_ptr<List> result = List::spawn();

    for (Number i = Number(0); i < *(items->len()); ++i) {
      result->append(Tuple::spawn({start, (*items)[i]}));
      start = start + Number::spawn(1);
    }

    return result;
  }

  std::shared_ptr<List> enumerate(const std::shared_ptr<String>& items,
    const std::shared_ptr<Bool> start) {
    return enumerate(items, Number::spawn(start->toBool()? 1: 0));
  }

  std::shared_ptr<List> enumerate(const std::shared_ptr<String>& items,
    const bool& start) {
    return enumerate(items, Number::spawn(start? 1: 0));
  }

  std::shared_ptr<List> enumerate(const std::shared_ptr<String>& items,
    const int& start) {
    return enumerate(items, Number::spawn(start));
  }

  std::shared_ptr<List> enumerate(const std::shared_ptr<Dictionary>& items,
    std::shared_ptr<Number> start = Number::spawn(0)) {
    std::shared_ptr<List> result = List::spawn();
    std::shared_ptr<List> keys = items->keys();

    for (auto& item : (*keys)) {
      result->append(Tuple::spawn({start, item}));
      start = start + Number::spawn(1);
    }

    return result;
  }

  std::shared_ptr<List> enumerate(const std::shared_ptr<Dictionary>& items,
    const bool& start) {
    return enumerate(items, Number::spawn(start? 1: 0));
  }

  std::shared_ptr<List> enumerate(const std::shared_ptr<Dictionary>& items,
    const int& start) {
    return enumerate(items, Number::spawn(start));
  }

  template<TIterable TType>
  std::shared_ptr<List> enumerate(const std::shared_ptr<TType>& items,
    std::shared_ptr<Number> start = Number::spawn(0)) {
    std::shared_ptr<List> result = List::spawn();

    for (auto& item : (*items)) {
      result->append(Tuple::spawn({start, item}));
      start = start + Number::spawn(1);
    }

    return result;
  }

  template<TIterable TType>
  std::shared_ptr<List> enumerate(const std::shared_ptr<TType>& items,
    const bool& start) {
    return enumerate(items, Number::spawn(start? 1: 0));
  }

  template<TIterable TType>
  std::shared_ptr<List> enumerate(const std::shared_ptr<TType>& items,
    const int& start) {
    return enumerate(items, Number::spawn(start));
  }

  std::shared_ptr<Number> float_() {
    return Number::spawn(0.0);
  }

  std::shared_ptr<Number> float_(const std::shared_ptr<Number>& value) {
    return Number::spawn(value->getDouble());
  }

  std::shared_ptr<Number> float_(const std::shared_ptr<Bool>& value) {
    return float_(Number::spawn((value->toBool())? 1.0 : 0.0));
  }

  std::shared_ptr<Number> float_(const bool& value) {
    return float_(Number::spawn((value)? 1.0 : 0.0));
  }

  std::shared_ptr<Number> float_(const int& value) {
    return float_(Number::spawn((value)));
  }

  std::shared_ptr<Number> float_(const std::shared_ptr<String>& value) {
    if ((**value) == "inf") {
      return Number::spawn(std::numeric_limits<double>::infinity());
    } else if ((**value) == "nan") {
      return Number::spawn(std::numeric_limits<double>::quiet_NaN());
    }
    return Number::spawn(std::stod(**value));
  }

  const std::shared_ptr<Set> frozenset() {
    return Set::spawn();
  }

  const std::shared_ptr<Set> frozenset(const std::shared_ptr<String>& items) {
    std::shared_ptr<Set> set = Set::spawn();

    for (Number i = Number(0); i < *(items->len()); ++i) {
      set->add((*items)[i]);
    }

    return set;
  }

  const std::shared_ptr<Set> frozenset(
    const std::shared_ptr<Dictionary>& items) {
    std::shared_ptr<Set> set = Set::spawn();
    std::shared_ptr<List> keys = items->keys();

    for (auto& item : (*keys)) {
      set->add(item);
    }

    return set;
  }

  template<TIterable TType>
  const std::shared_ptr<Set> frozenset(const std::shared_ptr<TType>& items) {
    std::shared_ptr<Set> set = Set::spawn();

    for (auto& item : (*items)) {
      set->add(item);
    }

    return set;
  }

  const std::shared_ptr<Number> id(const std::shared_ptr<Object>& object) {
    return Number::spawn(static_cast<int64_t>(object->id_));
  }

  const std::shared_ptr<Number> id(const bool& object) {
    return Number::spawn(static_cast<int64_t>(Bool::spawn(object)->id_));
  }

  const std::shared_ptr<Number> id(const int& object) {
    return Number::spawn(static_cast<int64_t>(
      Bool::spawn(object? true:false)->id_));
  }

  std::shared_ptr<String> input(const std::shared_ptr<String>& prompt) {
    std::string something;

    std::cout << **prompt;
    std::getline(std::cin, something);

    return String::spawn(something);
  }

  std::shared_ptr<Number> int_() {
    return Number::spawn(0);
  }

  std::shared_ptr<Number> int_(const std::shared_ptr<Number>& value,
    const std::shared_ptr<Number>& base = Number::spawn(10)) {
    if (base == Number::spawn(10)) {
      return Number::spawn(value->getInt());
    }
    
    int intValue = value->getInt();
    int intBase = value->getInt();
    int placeValue = 1;
    int result = 0;
    
    while (intValue > 0) {
        result += (intValue % intBase) * placeValue;
        intValue /= intBase;
    }
    
    return Number::spawn(result);
  }

  std::shared_ptr<Number> int_(const std::shared_ptr<Number>& value,
    const bool& base) {
    return int_(value, Number::spawn(base? 1:0));
  }

  std::shared_ptr<Number> int_(const std::shared_ptr<Number>& value,
    const int& base) {
    return int_(value, Number::spawn(base));
  }

  std::shared_ptr<Number> int_(const std::shared_ptr<Bool>& value,
    const std::shared_ptr<Number>& base = Number::spawn(10)) {
    return int_(Number::spawn((value->toBool())? 1:0), base);
  }

  std::shared_ptr<Number> int_(const std::shared_ptr<Bool>& value,
    const bool& base) {
    return int_(Number::spawn((value->toBool())? 1:0),
      Number::spawn(base? 1:0));
  }

  std::shared_ptr<Number> int_(const std::shared_ptr<Bool>& value,
    const int& base) {
    return int_(Number::spawn((value->toBool())? 1:0), Number::spawn(base));
  }

  std::shared_ptr<Number> int_(const bool& value,
    const std::shared_ptr<Number>& base = Number::spawn(10)) {
    return int_(Number::spawn((value? 1:0)), base);
  }

  std::shared_ptr<Number> int_(const bool& value,
    const bool& base) {
    return int_(Number::spawn(value? 1:0),
      Number::spawn(base? 1:0));
  }

  std::shared_ptr<Number> int_(const bool& value,
    const int& base) {
    return int_(Number::spawn(value? 1:0), Number::spawn(base));
  }

  std::shared_ptr<Number> int_(const int& value,
    const std::shared_ptr<Number>& base = Number::spawn(10)) {
    return int_(Number::spawn((value)), base);
  }

  std::shared_ptr<Number> int_(const int& value,
    const bool& base) {
    return int_(Number::spawn(value),
      Number::spawn(base? 1:0));
  }

  std::shared_ptr<Number> int_(const int& value,
    const int& base) {
    return int_(Number::spawn(value), Number::spawn(base));
  }

  std::shared_ptr<Number> int_(const std::shared_ptr<String>& value,
    const std::shared_ptr<Number>& base = Number::spawn(10)) {
    return Number::spawn(std::stoi(**value, nullptr, base->getInt()));
  }

  std::shared_ptr<Number> int_(const std::shared_ptr<String>& value,
    const bool& base) {
    return int_(value, Number::spawn(base? 1:0));
  }

  std::shared_ptr<Number> int_(const std::shared_ptr<String>& value,
    const int& base) {
    return int_(value, Number::spawn(base));
  }
  
  template<TIterable TType>
  auto iter(const std::shared_ptr<TType>& structure) {
    return structure->begin();
  }

  template<TIterable TType>
  std::shared_ptr<Number> len(const std::shared_ptr<TType>& structure) {
    return structure->len();
  }

  std::shared_ptr<List> list() {
    return List::spawn();
  }

  const std::shared_ptr<List> list(const std::shared_ptr<String>& items) {
    std::shared_ptr<List> result = List::spawn();

    for (Number i = Number(0); i < *(items->len()); ++i) {
      result->append((*items)[i]);
    }

    return result;
  }

  const std::shared_ptr<List> list(const std::shared_ptr<Dictionary>& items) {
    return items->keys();
  }

  template<TIterable TType>
  std::shared_ptr<List> list(const std::shared_ptr<TType>& items) {
    std::shared_ptr<List> result = List::spawn();

    for (auto& item : (*items)) {
      result->append(item);
    }

    return result;
  }

  template<TIterable TType>
  auto max(const std::shared_ptr<TType>& values) {
    std::shared_ptr<List> realValues = list(values);
    return *(std::max_element(realValues->begin(), realValues->end()));
  }

  template<typename ... TArgs>
    requires (sizeof...(TArgs) > 1) && (SharedObject<TArgs> && ...)
  auto max(TArgs&& ... args) {
    std::shared_ptr<Tuple> realValues =
      Tuple::spawn(std::forward<TArgs>(args)...);
    return *(std::max_element(realValues->begin(), realValues->end()));
  }

  template<TIterable TType>
  auto min(const std::shared_ptr<TType>& values) {
    std::shared_ptr<List> realValues = list(values);
    return *(std::min_element(realValues->begin(), realValues->end()));
  }

  template<typename ... TArgs>
    requires (sizeof...(TArgs) > 1) && (SharedObject<TArgs> && ...)
  auto min(TArgs&& ... args) {
    std::shared_ptr<Tuple> realValues =
      Tuple::spawn(std::forward<TArgs>(args)...);
    return *(std::min_element(realValues->begin(), realValues->end()));
  }

  template <TAdvIterator TIterator>
  TIterator next(TIterator& iter) {
      TIterator current = iter;
      std::advance(iter, 1);
      return current;
  }

  auto open(const std::shared_ptr<String>& path,
      const std::shared_ptr<String>& mode) {
    std::ios_base::openmode resultingMode;
    bool isCreating = false;

    for (const char& character : *mode) {
      if (character == 'r') {
        resultingMode |= std::ios_base::in;
      } else if ((character == '+') | (character == 'w')) {
        resultingMode |= std::ios_base::out;
      } else if (character == 'a') {
        resultingMode |= std::ios_base::out | std::ios_base::app;
      } else if (character == 'b') {
        resultingMode |= std::ios_base::binary;
      } else if (character == 'x') {
        if (!std::filesystem::exists(**path)) {
          throw std::invalid_argument(
            std::string("File: ") + (**path) + " does not exists"
          );
        }
        resultingMode |= std::ios_base::out;
        isCreating = true;
      }
    }

    if (!std::filesystem::exists(**path) && !isCreating) {
      throw std::invalid_argument(
        std::string("File: ") + (**path) + " does not exists"
      );
    }

    return std::fstream((**path).c_str(), resultingMode);
  }

  std::shared_ptr<Number> ord(const std::shared_ptr<String>& character) {
    return Number::spawn(static_cast<int>((**character)[0]));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Number>& base,
    const std::shared_ptr<Number>& exponent) {
    return base->pow(exponent);
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Bool>& base,
    const std::shared_ptr<Number>& exponent) {
    return Number::spawn(base->toBool()? 1:0)->pow(exponent);
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Number>& base,
    const std::shared_ptr<Bool>& exponent) {
    return base->pow(Number::spawn(exponent->toBool()? 1:0));
  }

  std::shared_ptr<Number> pow(const bool& base,
    const std::shared_ptr<Number>& exponent) {
    return Number::spawn(base? 1:0)->pow(exponent);
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Number>& base,
    const bool& exponent) {
    return base->pow(Number::spawn(exponent? 1:0));
  }

  std::shared_ptr<Number> pow(const bool& base,
    const bool& exponent) {
    return Number::spawn(base? 1:0)->pow(Number::spawn(exponent? 1:0));
  }

  std::shared_ptr<Number> pow(const int& base,
    const std::shared_ptr<Number>& exponent) {
    return Number::spawn(base)->pow(exponent);
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Number>& base,
    const int& exponent) {
    return base->pow(Number::spawn(exponent));
  }

  std::shared_ptr<Number> pow(const int& base,
    const int& exponent) {
    return Number::spawn(base)->pow(Number::spawn(exponent));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Bool>& base,
    const bool& exponent) {
    return Number::spawn(base->toBool() ? 1 : 0)->pow(
      Number::spawn(exponent ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const bool& base,
    const std::shared_ptr<Bool>& exponent) {
      return Number::spawn(base ? 1 : 0)->pow(
        Number::spawn(exponent->toBool() ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Bool>& base,
    const int& exponent) {
    return Number::spawn(base->toBool() ? 1 : 0)->pow(Number::spawn(exponent));
  }

  std::shared_ptr<Number> pow(const int& base,
    const std::shared_ptr<Bool>& exponent) {
    return Number::spawn(base)->pow(Number::spawn(exponent->toBool() ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const bool& base, const int& exponent) {
    return Number::spawn(base ? 1 : 0)->pow(Number::spawn(exponent));
  }

  std::shared_ptr<Number> pow(const int& base, const bool& exponent) {
      return Number::spawn(base)->pow(Number::spawn(exponent ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Number>& base,
    const std::shared_ptr<Number>& exponent,
    const std::shared_ptr<Number>& modulus) {
    return base->pow(exponent) % modulus;
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Bool>& base,
    const std::shared_ptr<Number>& exponent,
    const std::shared_ptr<Number>& modulus) {
    return pow(Number::spawn(base->toBool()? 1:0), exponent, modulus);
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Number>& base,
    const std::shared_ptr<Bool>& exponent,
    const std::shared_ptr<Number>& modulus) {
    return pow(base, Number::spawn(exponent->toBool() ? 1 : 0), modulus);
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Number>& base,
    const std::shared_ptr<Number>& exponent,
    const std::shared_ptr<Bool>& modulus) {
    return pow(base, exponent, Number::spawn(modulus->toBool() ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Bool>& base,
    const std::shared_ptr<Bool>& exponent,
    const std::shared_ptr<Number>& modulus) {
    return pow(Number::spawn(base->toBool() ? 1 : 0),
      Number::spawn(exponent->toBool() ? 1 : 0), modulus);
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Bool>& base,
    const std::shared_ptr<Number>& exponent,
    const std::shared_ptr<Bool>& modulus) {
    return pow(Number::spawn(base->toBool() ? 1 : 0), exponent,
      Number::spawn(modulus->toBool() ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Number>& base,
    const std::shared_ptr<Bool>& exponent,
    const std::shared_ptr<Bool>& modulus) {
    return pow(base, Number::spawn(exponent->toBool() ? 1 : 0),
      Number::spawn(modulus->toBool() ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Bool>& base,
    const std::shared_ptr<Bool>& exponent,
    const std::shared_ptr<Bool>& modulus) {
    return pow(Number::spawn(base->toBool() ? 1 : 0),
      Number::spawn(exponent->toBool() ? 1 : 0),
      Number::spawn(modulus->toBool() ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const bool& base,
    const std::shared_ptr<Number>& exponent,
    const std::shared_ptr<Number>& modulus) {
    return pow(Number::spawn(base ? 1 : 0), exponent, modulus);
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Number>& base,
    const bool& exponent, const std::shared_ptr<Number>& modulus) {
    return pow(base, Number::spawn(exponent ? 1 : 0), modulus);
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Number>& base,
    const std::shared_ptr<Number>& exponent, const bool& modulus) {
    return pow(base, exponent, Number::spawn(modulus ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const bool& base, const bool& exponent,
    const std::shared_ptr<Number>& modulus) {
    return pow(Number::spawn(base ? 1 : 0),
      Number::spawn(exponent ? 1 : 0), modulus);
  }

  std::shared_ptr<Number> pow(const bool& base,
    const std::shared_ptr<Number>& exponent, const bool& modulus) {
    return pow(Number::spawn(base ? 1 : 0), exponent,
      Number::spawn(modulus ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Number>& base,
    const bool& exponent, const bool& modulus) {
    return pow(base, Number::spawn(exponent ? 1 : 0),
      Number::spawn(modulus ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const bool& base, const bool& exponent,
    const bool& modulus) {
    return pow(Number::spawn(base ? 1 : 0), Number::spawn(exponent ? 1 : 0),
      Number::spawn(modulus ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const int& base,
    const std::shared_ptr<Number>& exponent,
    const std::shared_ptr<Number>& modulus) {
    return pow(Number::spawn(base), exponent, modulus);
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Number>& base,
    const int& exponent, const std::shared_ptr<Number>& modulus) {
    return pow(base, Number::spawn(exponent), modulus);
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Number>& base,
    const std::shared_ptr<Number>& exponent, const int& modulus) {
    return pow(base, exponent, Number::spawn(modulus));
  }

  std::shared_ptr<Number> pow(const int& base, const int& exponent,
    const std::shared_ptr<Number>& modulus) {
    return pow(Number::spawn(base), Number::spawn(exponent), modulus);
  }

  std::shared_ptr<Number> pow(const int& base,
    const std::shared_ptr<Number>& exponent, const int& modulus) {
    return pow(Number::spawn(base), exponent, Number::spawn(modulus));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Number>& base,
    const int& exponent, const int& modulus) {
    return pow(base, Number::spawn(exponent), Number::spawn(modulus));
  }

  std::shared_ptr<Number> pow(const int& base, const int& exponent,
    const int& modulus) {
    return pow(Number::spawn(base), Number::spawn(exponent),
      Number::spawn(modulus));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Number>& base,
    const std::shared_ptr<Bool>& exponent, const bool& modulus) {
    return pow(base, Number::spawn(exponent->toBool() ? 1 : 0),
      Number::spawn(modulus ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Number>& base,
    const std::shared_ptr<Bool>& exponent, const int& modulus) {
    return pow(base, Number::spawn(exponent->toBool() ? 1 : 0),
      Number::spawn(modulus));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Number>& base,
    const bool& exponent, const std::shared_ptr<Bool>& modulus) {
    return pow(base, Number::spawn(exponent ? 1 : 0),
      Number::spawn(modulus->toBool() ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Number>& base,
    const bool& exponent, const int& modulus) {
    return pow(base, Number::spawn(exponent ? 1 : 0),
      Number::spawn(modulus));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Number>& base,
    const int& exponent, const std::shared_ptr<Bool>& modulus) {
    return pow(base, Number::spawn(exponent),
      Number::spawn(modulus->toBool() ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Number>& base,
    const int& exponent, const bool& modulus) {
    return pow(base, Number::spawn(exponent), Number::spawn(modulus ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Bool>& base,
    const std::shared_ptr<Number>& exponent, const bool& modulus) {
    return pow(Number::spawn(base->toBool() ? 1 : 0), exponent,
      Number::spawn(modulus ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Bool>& base,
    const std::shared_ptr<Number>& exponent, const int& modulus) {
    return pow(Number::spawn(base->toBool() ? 1 : 0), exponent,
      Number::spawn(modulus));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Bool>& base,
    const std::shared_ptr<Bool>& exponent, const bool& modulus) {
    return pow(Number::spawn(base->toBool() ? 1 : 0),
      Number::spawn(exponent->toBool() ? 1 : 0),
      Number::spawn(modulus ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Bool>& base,
    const std::shared_ptr<Bool>& exponent, const int& modulus) {
    return pow(Number::spawn(base->toBool() ? 1 : 0),
      Number::spawn(exponent->toBool() ? 1 : 0), Number::spawn(modulus));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Bool>& base,
    const bool& exponent, const std::shared_ptr<Number>& modulus) {
    return pow(Number::spawn(base->toBool() ? 1 : 0),
      Number::spawn(exponent ? 1 : 0), modulus);
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Bool>& base,
    const bool& exponent, const std::shared_ptr<Bool>& modulus) {
    return pow(Number::spawn(base->toBool() ? 1 : 0),
      Number::spawn(exponent ? 1 : 0),
      Number::spawn(modulus->toBool() ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Bool>& base,
    const bool& exponent, const bool& modulus) {
    return pow(Number::spawn(base->toBool() ? 1 : 0),
      Number::spawn(exponent ? 1 : 0), Number::spawn(modulus ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Bool>& base,
    const bool& exponent, const int& modulus) {
    return pow(Number::spawn(base->toBool() ? 1 : 0),
      Number::spawn(exponent ? 1 : 0), Number::spawn(modulus));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Bool>& base,
    const int& exponent, const std::shared_ptr<Number>& modulus) {
    return pow(Number::spawn(base->toBool() ? 1 : 0),
      Number::spawn(exponent), modulus);
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Bool>& base,
    const int& exponent, const std::shared_ptr<Bool>& modulus) {
    return pow(Number::spawn(base->toBool() ? 1 : 0),
      Number::spawn(exponent), Number::spawn(modulus->toBool() ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Bool>& base,
    const int& exponent, const bool& modulus) {
    return pow(Number::spawn(base->toBool() ? 1 : 0),
      Number::spawn(exponent), Number::spawn(modulus ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const std::shared_ptr<Bool>& base,
    const int& exponent, const int& modulus) {
    return pow(Number::spawn(base->toBool() ? 1 : 0),
      Number::spawn(exponent), Number::spawn(modulus));
  }

  std::shared_ptr<Number> pow(const bool& base,
    const std::shared_ptr<Number>& exponent,
    const std::shared_ptr<Bool>& modulus) {
    return pow(Number::spawn(base ? 1 : 0),
      exponent, Number::spawn(modulus->toBool() ? 1 : 0));
}

  std::shared_ptr<Number> pow(const bool& base,
    const std::shared_ptr<Number>& exponent, const int& modulus) {
    return pow(Number::spawn(base ? 1 : 0), exponent, Number::spawn(modulus));
  }

  std::shared_ptr<Number> pow(const bool& base,
    const std::shared_ptr<Bool>& exponent,
    const std::shared_ptr<Number>& modulus) {
    return pow(Number::spawn(base ? 1 : 0),
      Number::spawn(exponent->toBool() ? 1 : 0), modulus);
  }

  std::shared_ptr<Number> pow(const bool& base,
    const std::shared_ptr<Bool>& exponent,
    const std::shared_ptr<Bool>& modulus) {
    return pow(Number::spawn(base ? 1 : 0),
      Number::spawn(exponent->toBool() ? 1 : 0), Number::spawn(modulus->toBool() ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const bool& base,
    const std::shared_ptr<Bool>& exponent, const bool& modulus) {
    return pow(Number::spawn(base ? 1 : 0),
      Number::spawn(exponent->toBool() ? 1 : 0),
      Number::spawn(modulus ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const bool& base,
    const std::shared_ptr<Bool>& exponent, const int& modulus) {
    return pow(Number::spawn(base ? 1 : 0),
      Number::spawn(exponent->toBool() ? 1 : 0), Number::spawn(modulus));
  }

  std::shared_ptr<Number> pow(const bool& base,
    const bool& exponent, const std::shared_ptr<Bool>& modulus) {
    return pow(Number::spawn(base ? 1 : 0), Number::spawn(exponent ? 1 : 0),
      Number::spawn(modulus->toBool() ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const bool& base, const bool& exponent,
    const int& modulus) {
    return pow(Number::spawn(base ? 1 : 0), Number::spawn(exponent ? 1 : 0),
      Number::spawn(modulus));
  }

  std::shared_ptr<Number> pow(const bool& base, const int& exponent,
    const std::shared_ptr<Number>& modulus) {
    return pow(Number::spawn(base ? 1 : 0), Number::spawn(exponent), modulus);
  }

  std::shared_ptr<Number> pow(const bool& base, const int& exponent,
    const std::shared_ptr<Bool>& modulus) {
    return pow(Number::spawn(base ? 1 : 0), Number::spawn(exponent),
      Number::spawn(modulus->toBool() ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const bool& base, const int& exponent,
    const bool& modulus) {
    return pow(Number::spawn(base ? 1 : 0), Number::spawn(exponent),
      Number::spawn(modulus ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const bool& base, const int& exponent,
    const int& modulus) {
    return pow(Number::spawn(base ? 1 : 0), Number::spawn(exponent),
      Number::spawn(modulus));
  }

  std::shared_ptr<Number> pow(const int& base,
    const std::shared_ptr<Number>& exponent,
    const std::shared_ptr<Bool>& modulus) {
    return pow(Number::spawn(base), exponent,
      Number::spawn(modulus->toBool() ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const int& base,
    const std::shared_ptr<Number>& exponent, const bool& modulus) {
    return pow(Number::spawn(base), exponent, Number::spawn(modulus ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const int& base,
    const std::shared_ptr<Bool>& exponent,
    const std::shared_ptr<Number>& modulus) {
    return pow(Number::spawn(base), Number::spawn(exponent->toBool() ? 1 : 0),
      modulus);
  }

  std::shared_ptr<Number> pow(const int& base,
    const std::shared_ptr<Bool>& exponent,
    const std::shared_ptr<Bool>& modulus) {
    return pow(Number::spawn(base), Number::spawn(exponent->toBool() ? 1 : 0),
      Number::spawn(modulus->toBool() ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const int& base,
    const std::shared_ptr<Bool>& exponent, const bool& modulus) {
    return pow(Number::spawn(base), Number::spawn(exponent->toBool() ? 1 : 0),
      Number::spawn(modulus ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const int& base,
    const std::shared_ptr<Bool>& exponent, const int& modulus) {
    return pow(Number::spawn(base), Number::spawn(exponent->toBool() ? 1 : 0),
      Number::spawn(modulus));
  }

  std::shared_ptr<Number> pow(const int& base, const bool& exponent,
    const std::shared_ptr<Number>& modulus) {
    return pow(Number::spawn(base), Number::spawn(exponent ? 1 : 0), modulus);
  }

  std::shared_ptr<Number> pow(const int& base, const bool& exponent,
    const std::shared_ptr<Bool>& modulus) {
    return pow(Number::spawn(base), Number::spawn(exponent ? 1 : 0),
      Number::spawn(modulus->toBool() ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const int& base, const bool& exponent,
    const bool& modulus) {
    return pow(Number::spawn(base), Number::spawn(exponent ? 1 : 0),
      Number::spawn(modulus ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const int& base, const bool& exponent,
    const int& modulus) {
    return pow(Number::spawn(base), Number::spawn(exponent ? 1 : 0),
      Number::spawn(modulus));
  }

  std::shared_ptr<Number> pow(const int& base, const int& exponent,
    const std::shared_ptr<Bool>& modulus) {
    return pow(Number::spawn(base), Number::spawn(exponent),
      Number::spawn(modulus->toBool() ? 1 : 0));
  }

  std::shared_ptr<Number> pow(const int& base, const int& exponent,
    const bool& modulus) {
    return pow(Number::spawn(base), Number::spawn(exponent),
      Number::spawn(modulus ? 1 : 0));
  }

  std::shared_ptr<Number> intDiv(const std::shared_ptr<Number>& dividend,
    const std::shared_ptr<Number>& divisor) {
    return Number::spawn(dividend->getInt() / divisor->getInt());
  }

  std::shared_ptr<Number> intDiv(const std::shared_ptr<Bool>& dividend,
    const std::shared_ptr<Number>& divisor) {
    return intDiv(Number::spawn(dividend->toBool()? 1:0), divisor);
  }

  std::shared_ptr<Number> intDiv(const std::shared_ptr<Number>& dividend,
    const std::shared_ptr<Bool>& divisor) {
    return intDiv(dividend, Number::spawn(divisor->toBool()? 1:0));
  }

  std::shared_ptr<Number> intDiv(const std::shared_ptr<Bool>& dividend,
    const std::shared_ptr<Bool>& divisor) {
    return intDiv(Number::spawn(dividend->toBool()? 1:0),
      Number::spawn(divisor->toBool()? 1:0));
  }

  std::shared_ptr<Number> intDiv(const bool& dividend,
    const std::shared_ptr<Number>& divisor) {
    return intDiv(Number::spawn(dividend? 1:0), divisor);
  }

  std::shared_ptr<Number> intDiv(const std::shared_ptr<Number>& dividend,
    const bool& divisor) {
    return intDiv(dividend, Number::spawn(divisor? 1:0));
  }

  std::shared_ptr<Number> intDiv(const bool& dividend,
    const bool& divisor) {
    return intDiv(Number::spawn(dividend? 1:0),
      Number::spawn(divisor? 1:0));
  }

  std::shared_ptr<Number> intDiv(const int& dividend,
    const std::shared_ptr<Number>& divisor) {
    return intDiv(Number::spawn(dividend), divisor);
  }

  std::shared_ptr<Number> intDiv(const std::shared_ptr<Number>& dividend,
    const int& divisor) {
    return intDiv(dividend, Number::spawn(divisor));
  }

  std::shared_ptr<Number> intDiv(const int& dividend,
    const int& divisor) {
    return intDiv(Number::spawn(dividend),
      Number::spawn(divisor));
  }

  std::shared_ptr<Number> intDiv(const std::shared_ptr<Bool>& dividend,
    const bool& divisor) {
    return intDiv(Number::spawn(dividend->toBool() ? 1 : 0),
      Number::spawn(divisor ? 1 : 0));
  }

  std::shared_ptr<Number> intDiv(const std::shared_ptr<Bool>& dividend,
    const int& divisor) {
    return intDiv(Number::spawn(dividend->toBool() ? 1 : 0),
      Number::spawn(divisor));
  }

  std::shared_ptr<Number> intDiv(const bool& dividend,
    const std::shared_ptr<Bool>& divisor) {
    return intDiv(Number::spawn(dividend ? 1 : 0),
      Number::spawn(divisor->toBool() ? 1 : 0));
  }

  std::shared_ptr<Number> intDiv(const bool& dividend, const int& divisor) {
    return intDiv(Number::spawn(dividend ? 1 : 0),
      Number::spawn(divisor));
  }

  std::shared_ptr<Number> intDiv(const int& dividend,
    const std::shared_ptr<Bool>& divisor) {
    return intDiv(Number::spawn(dividend),
      Number::spawn(divisor->toBool() ? 1 : 0));
  }

  std::shared_ptr<Number> intDiv(const int& dividend, const bool& divisor) {
    return intDiv(Number::spawn(dividend), Number::spawn(divisor ? 1 : 0));
  }

  std::shared_ptr<None> print() {
    std::cout << std::endl;
    return None::spawn();
  }

  std::shared_ptr<None> print(const char object) {
    std::cout << object << std::endl;
    return None::spawn();
  }

  std::shared_ptr<None> print(const std::shared_ptr<String>& object) {
    // if the string stars and ends with a quote, remove them
    std::string str = **object;
    str = Function::removeQuotesIfNeeded(str); 
    std::cout << str << std::endl;
    return None::spawn();
  }

  std::shared_ptr<None> print(const std::shared_ptr<Object>& object) {
    // if type is string, remove quotes
    if (auto strPtr = std::dynamic_pointer_cast<String>(object)) {
      std::string str = **strPtr;
      str = Function::removeQuotesIfNeeded(str); 
      std::cout << str << std::endl;
      return None::spawn();
    }
    std::cout << object->toString().c_str() << std::endl;
    return None::spawn();
  }

  std::shared_ptr<None> print(const bool& boolean) {
    std::cout << (boolean? "True" : "False") << std::endl;
    return None::spawn();
  }

  std::shared_ptr<None> print(const int& integer) {
    std::cout << integer << std::endl;
    return None::spawn();
  }

  std::shared_ptr<None> print(const std::shared_ptr<std::wstring>& anything) {
    std::wcout << (*anything) << std::endl;
    return None::spawn();
  }

  template<typename Any>
  std::shared_ptr<None> print(const std::shared_ptr<Any>& anything) {
    std::cout << (*anything) << std::endl;
    return None::spawn();
  }

  std::shared_ptr<None> print(const std::map<
    std::shared_ptr<Object>,
    std::shared_ptr<Object>,
    ObjectComparator>::iterator& iterator) {
    std::cout << (*(iterator->first))
      << " : " 
      << (*(iterator->second))
      << std::endl;
    return None::spawn();
  }

  template<TAdvIterator TIterator>
  std::shared_ptr<None> print(const TIterator& iterator) {
    using ValueType = typename std::iterator_traits<TIterator>::value_type;
    if constexpr (std::is_same_v<ValueType, std::shared_ptr<Object>>) {
      const std::shared_ptr<Object>& objPtr = *iterator;
      if (!objPtr.get()) {
        std::cout << "The container has already been freed" << std::endl;
      } else {
        // if type is string, remove quotes
        if (auto strPtr = std::dynamic_pointer_cast<String>(objPtr)) {
          std::string str = **strPtr;
          std::cout << Function::removeQuotesIfNeeded(str) << std::endl;
        } else {
          std::cout << objPtr->toString().c_str() << std::endl;
        }
      }
      
    } else {
      std::cout << (*iterator) << std::endl;
    }

    return None::spawn();
  }

  std::shared_ptr<List> range(const std::shared_ptr<Number>& stop) {
    std::shared_ptr<List> result = List::spawn();
  
    for (int64_t i = 0; i < stop->getInt(); ++i) {
      result->append(Number::spawn(i));
    }

    return result;
  }

  std::shared_ptr<List> range(const std::shared_ptr<Number>& start,
    const std::shared_ptr<Number>& stop,
    const std::shared_ptr<Number>& step = Number::spawn(1)) {
    std::shared_ptr<List> result = List::spawn();

    if (*step > *Number::spawn(0)) {
      for (int64_t i = start->getInt()
          ; i < stop->getInt()
          ; i += step->getInt()) {
        result->append(Number::spawn(i));
      }
    } else {
      for (int64_t i = start->getInt()
          ; i > stop->getInt()
          ; i += step->getInt()) {
        result->append(Number::spawn(i));
      }
    }

    return result;
  }

  std::shared_ptr<Set> reversed(
    const std::shared_ptr<Set>& structure) {
    return structure;
  }

  std::shared_ptr<Dictionary> reversed(
    const std::shared_ptr<Dictionary>& structure) {
    return structure;
  }

  std::shared_ptr<Tuple> reversed(const std::shared_ptr<Tuple>& structure) {
    std::shared_ptr<List> result = std::make_shared<List>();

    for (auto& item : (*structure)) {
      result->append(item);
    }

    return tuple(result);
  }

  std::shared_ptr<List> reversed(const std::shared_ptr<List>& structure) {
    std::shared_ptr<List> result = std::make_shared<List>();
    std::shared_ptr<Number> zero = Number::spawn(0);

    for (auto& item : (*structure)) {
      result->insert(zero, item);
    }

    return result;
  }

  std::shared_ptr<String> reversed(const std::shared_ptr<String>& structure) {
    std::shared_ptr<String> result = std::make_shared<String>();
    
    for (std::shared_ptr<Number> i = (structure->len() - Number::spawn(1));
      *i >= *Number::spawn(0); --(*i)) {
      result = result + (*structure)[*i];
    }

    return result;
  }

  std::shared_ptr<Number> round(const std::shared_ptr<Number>& num,
    const std::shared_ptr<Number>& decimals = Number::spawn(0)) {
    if (decimals == Number::spawn(0)) {
      return Number::spawn(static_cast<int64_t>(std::round(
        static_cast<long double>(num->getDouble()))
      ));
    } else if (decimals <= Number::spawn(0)) {
      std::shared_ptr<Number> nearest = Number::spawn(10)->pow(-decimals);

      return Number::spawn(
        static_cast<double>(std::round(
          num->getDouble() / nearest->getDouble()) * nearest->getDouble()));
    }
    
    const double scale = std::pow(10.0, decimals->getInt());
    const long double value = num->getDouble();
    return Number::spawn(static_cast<double>(std::round(
      value * scale)) / scale);
  }

  std::shared_ptr<Number> round(const std::shared_ptr<Bool>& num,
    const std::shared_ptr<Number>& decimals = Number::spawn(0)) {
    return round(Number::spawn(num->toBool()? 1:0), decimals);
  }

  std::shared_ptr<Number> round(const std::shared_ptr<Bool>& num,
    const std::shared_ptr<Bool>& decimals) {
    return round(Number::spawn(num->toBool()? 1:0),
      Number::spawn(decimals->toBool()? 1:0));
  }

  std::shared_ptr<Number> round(const bool& num,
    const std::shared_ptr<Number>& decimals = Number::spawn(0)) {
    return round(Number::spawn(num? 1:0), decimals);
  }

  std::shared_ptr<Number> round(const bool& num,
    const bool& decimals) {
    return round(Number::spawn(num? 1:0),
      Number::spawn(decimals? 1:0));
  }

  std::shared_ptr<Number> round(const int& num,
    const std::shared_ptr<Number>& decimals = Number::spawn(0)) {
    return round(Number::spawn(num), decimals);
  }

  std::shared_ptr<Number> round(const int& num,
    const int& decimals) {
    return round(Number::spawn(num),
      Number::spawn(decimals));
  }

  std::shared_ptr<Number> round(const std::shared_ptr<Bool>& num,
    const int& decimals) {
    return round(Number::spawn(num->toBool()? 1 : 0), Number::spawn(decimals));
  }

  std::shared_ptr<Number> round(const int& num,
    const std::shared_ptr<Bool>& decimals) {
    return round(Number::spawn(num), Number::spawn(decimals->toBool()? 1 : 0));
  }

  std::shared_ptr<Number> round(const bool& num,
    const int& decimals) {
    return round(Number::spawn(num? 1 : 0), Number::spawn(decimals));
  }

  std::shared_ptr<Number> round(const int& num,
    const bool& decimals) {
    return round(Number::spawn(num), Number::spawn(decimals? 1 : 0));
  }

  std::shared_ptr<Number> round(const bool& num,
    const std::shared_ptr<Bool>& decimals) {
    return round(Number::spawn(num? 1 : 0),
      Number::spawn(decimals->toBool()? 1 : 0));
  }

  std::shared_ptr<Number> round(const std::shared_ptr<Bool>& num,
    const bool& decimals) {
    return round(Number::spawn(num->toBool()? 1 : 0),
      Number::spawn(decimals? 1 : 0));
  }

  std::shared_ptr<Set> set() {
    return Set::spawn();
  }

  const std::shared_ptr<Set> set(const std::shared_ptr<String>& items) {
    std::shared_ptr<Set> result = Set::spawn();

    for (Number i = Number(0); i < *(items->len()); ++i) {
      result->add((*items)[i]);
    }

    return result;
  }

  std::shared_ptr<Set> set(const std::shared_ptr<Dictionary>& items) {
    std::shared_ptr<Set> result = Set::spawn();
    std::shared_ptr<List> keys = items->keys();

    for (auto& item : (*keys)) {
      result->add(item);
    }

    return result;
  }

  template<TIterable TType>
  std::shared_ptr<Set> set(const std::shared_ptr<TType>& items) {
    std::shared_ptr<Set> result = Set::spawn();

    for (auto& item : (*items)) {
      result->add(item);
    }

    return result;
  }

  std::shared_ptr<String> sorted(
    const std::shared_ptr<String>& structure,
    const std::shared_ptr<Bool>& reverse = Bool::spawn(false)) {
    std::string result = **structure;
    std::sort(result.begin(), result.end());

    std::shared_ptr<String> realResult = String::spawn(result);
    return (!reverse->toBool()? realResult : reversed(realResult));
  }

  std::shared_ptr<List> sorted(
    const std::shared_ptr<Dictionary>& structure,
    const std::shared_ptr<Bool>& reverse = Bool::spawn(false)) {
    return (!reverse? structure->keys() : reversed(structure->keys()));
  }

  template<TIterable TType>
  std::shared_ptr<List> sorted(const std::shared_ptr<TType>& structure,
    const std::shared_ptr<Bool>& reverse = Bool::spawn(false)) {
    std::shared_ptr<List> result = list(structure);
    if (!result->hasSingleType()) {
      throw std::invalid_argument(
        "Sorted not supported on structures with multiple types");
    }

    std::sort(result->begin(), result->end());
    return (!reverse->toBool()? result : reversed(result));
  }

  std::shared_ptr<String> str() {
    return String::spawn(std::string(""));
  }

  std::shared_ptr<String> str(const std::shared_ptr<Object>& object) {
    return String::spawn(object->toString());
  }

  std::shared_ptr<String> str(const bool& object) {
    return String::spawn(object? "True" : "False");
  }

  std::shared_ptr<String> str(const int& object) {
    return String::spawn(std::to_string(object));
  }

  std::shared_ptr<Number> sum(
    const std::shared_ptr<Dictionary>& numbers,
    const std::shared_ptr<Number>& extra = Number::spawn(0)) {
    std::shared_ptr<List> keys = numbers->keys();
    std::shared_ptr<Number> result = extra;

    for (auto& num : (*keys)) {
      result = result + std::dynamic_pointer_cast<Number>(num);
    }

    return result;
  }

  std::shared_ptr<Number> sum(
    const std::shared_ptr<Dictionary>& numbers,
    const std::shared_ptr<Bool>& extra) {
    return sum(numbers, Number::spawn(extra->toBool()? 1:0));
  }

  std::shared_ptr<Number> sum(
    const std::shared_ptr<Dictionary>& numbers,
    const bool& extra) {
    return sum(numbers, Number::spawn(extra? 1:0));
  }

  std::shared_ptr<Number> sum(
    const std::shared_ptr<Dictionary>& numbers,
    const int& extra) {
    return sum(numbers, Number::spawn(extra));
  }

  template<TIterable TType>
  std::shared_ptr<Number> sum(
    const std::shared_ptr<TType>& numbers,
    const std::shared_ptr<Number>& extra = Number::spawn(0)) {
    std::shared_ptr<Number> result = extra;

    for (auto& num : (*numbers)) {
      result = result + std::dynamic_pointer_cast<Number>(num);
    }

    return result;
  }

  template<TIterable TType>
  std::shared_ptr<Number> sum(
    const std::shared_ptr<TType>& numbers,
    const std::shared_ptr<Bool>& extra) {
    return sum(numbers, Number::spawn(extra->toBool()? 1:0));
  }

  template<TIterable TType>
  std::shared_ptr<Number> sum(
    const std::shared_ptr<TType>& numbers,
    const bool& extra) {
    return sum(numbers, Number::spawn(extra? 1:0));
  }

  template<TIterable TType>
  std::shared_ptr<Number> sum(
    const std::shared_ptr<TType>& numbers,
    const int& extra) {
    return sum(numbers, Number::spawn(extra));
  }

  std::shared_ptr<Tuple> tuple() {
    return Tuple::spawn();
  }

  const std::shared_ptr<Tuple> tuple(const std::shared_ptr<String>& items) {
    std::vector<std::shared_ptr<Object>> result;

    for (Number i = Number(0); i < *(items->len()); ++i) {
      result.push_back((*items)[i]);
    }

    return std::make_shared<Tuple>(result);
  }

  std::shared_ptr<Bool> in(const std::shared_ptr<String>& obj,
    const std::shared_ptr<String>& structure) {
    for (Number i = Number(0); i < *(structure->len()); ++i) {
      if ((*structure)[i] == obj) {
        return Bool::spawn(true);
      }
    }
    return Bool::spawn(false);
  }

  template<TIterable TType>
  std::shared_ptr<Bool> in(const auto& obj,
    const std::shared_ptr<TType>& structure) {
    auto it = std::find_if(structure->begin(), structure->end(),
                           [&obj](const auto& element) -> bool {
                             return element->equals(*obj);
                           });
    return Bool::spawn(it != structure->end());
  }

  std::shared_ptr<Bool> is(const std::shared_ptr<Object>& first,
    const std::shared_ptr<Object>& second) {
    if (first->isNone()) return Bool::spawn(second->isNone());

    if (second->isNone()) return Bool::spawn(first->isNone());

    return Bool::spawn(first.get() == second.get());
  }

  std::shared_ptr<Bool> is(const bool&,
    const std::shared_ptr<Object>&) {
    return Bool::spawn(false);
  }

  std::shared_ptr<Bool> is(const std::shared_ptr<Object>&,
    const bool&) {
    return Bool::spawn(false);
  }

  std::shared_ptr<Bool> is(const bool& first,
    const bool& second) {
    return Bool::spawn(&first == &second);
  }

  std::shared_ptr<Bool> is(const int&,
    const std::shared_ptr<Object>&) {
    return Bool::spawn(false);
  }

  std::shared_ptr<Bool> is(const std::shared_ptr<Object>&,
    const int&) {
    return Bool::spawn(false);
  }

  std::shared_ptr<Bool> is(const int& first,
    const int& second) {
    return Bool::spawn(&first == &second);
  }

  std::shared_ptr<Bool> is(const int&,
    const bool&) {
    return Bool::spawn(false);
  }

  std::shared_ptr<Bool> is(const bool&,
    const int&) {
    return Bool::spawn(false);
  }
};

#endif  // BUILTIN_FUNCTIONS_HPP