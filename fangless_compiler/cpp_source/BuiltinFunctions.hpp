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

#include "Bool.hpp"
#include "Dictionary.hpp"
#include "Function.hpp"
#include "List.hpp"
#include "None.hpp"
#include "Number.hpp"
#include "Set.hpp"
#include "String.hpp"
#include "Tuple.hpp"

// #define FUNC(call, ...) []() { return call(__VA_ARGS__); }

// template<typename FunctionT>
// struct DefaultFunction {
//     FunctionT function_;

//     explicit DefaultFunction(FunctionT function) : function_(std::move(function)) {}

//     template<typename ReturnT>
//     std::shared_ptr<ReturnT> Call() {
//         return ReturnT::Spawn(function_());
//     }
// };

// auto c = DefaultFunction(FUNC(std::abs, -1)).Call<Number>();
template<typename TClass>
concept TIterable = requires(TClass a) {
  a.begin();
  a.end();
} && std::is_base_of_v<Object, TClass>;

template<typename TIterator>
concept TAdvIterator = requires(TIterator it) {
    { *it };
    std::advance(it, 1);
    typename std::iterator_traits<TIterator>::value_type;
};

// Namespace for builtin functions
namespace BF {
  std::shared_ptr<Number> abs(const std::shared_ptr<Number>& num) {
    if (num->isDouble()) {
      return Number::spawn(std::abs(num->getDouble()));
    }
    return Number::spawn(static_cast<int64_t>(std::abs(num->getInt())));
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

  std::shared_ptr<Tuple> tuple(const std::shared_ptr<Dictionary>& items) {
    std::shared_ptr<List> keys = items->keys();
    return std::make_shared<Tuple>(keys->begin(), keys->end());
  }

  template<TIterable TType>
  std::shared_ptr<Tuple> tuple(const std::shared_ptr<TType>& items) {
    return std::make_shared<Tuple>(items->begin(), items->end());
  }

  std::shared_ptr<String> type(const std::shared_ptr<Object>& anything) {
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

  std::shared_ptr<List> enumerate(const std::shared_ptr<String>& items,
    std::shared_ptr<Number> start = Number::spawn(0)) {
    std::shared_ptr<List> result = List::spawn();

    for (Number i = Number(0); i < *(items->len()); ++i) {
      result->append(Tuple::spawn({start, (*items)[i]}));
      start = start + Number::spawn(1);
    }

    return result;
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

  std::shared_ptr<Number> float_() {
    return Number::spawn(0.0);
  }

  std::shared_ptr<Number> float_(const std::shared_ptr<Number>& value) {
    return Number::spawn(value->getDouble());
  }

  std::shared_ptr<Number> float_(const std::shared_ptr<Bool>& value) {
    return float_(Number::spawn((value->toBool())? 1.0 : 0.0));
  }

  std::shared_ptr<Number> float_(const std::shared_ptr<String>& value) {
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

  std::shared_ptr<Number> int_(const std::shared_ptr<Bool>& value,
    const std::shared_ptr<Number>& base = Number::spawn(10)) {
    return int_(Number::spawn((value->toBool())? 1:0), base);
  }

  std::shared_ptr<Number> int_(const std::shared_ptr<String>& value,
    const std::shared_ptr<Number>& base = Number::spawn(10)) {
    return Number::spawn(std::stoi(**value, nullptr, base->getInt()));
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
      } else if (character == '+' | character == 'w') {
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

  std::shared_ptr<Number> pow(const std::shared_ptr<Number>& base,
    const std::shared_ptr<Number>& exponent,
    const std::shared_ptr<Number>& modulus) {
    return base->pow(exponent) % modulus;
  }

  void print() {
    std::cout << std::endl;
  }

  void print(const std::shared_ptr<String>& object) {
    std::cout << (**object).c_str() << std::endl;
  }

  void print(const std::shared_ptr<Object>& object) {
    std::cout << object->toString().c_str() << std::endl;
  }

  void print(bool boolean) {
    std::cout << (boolean? "True" : "False") << std::endl;
  }

  void print(const std::shared_ptr<std::wstring>& anything) {
    std::wcout << (*anything) << std::endl;
  }

  template<typename Any>
  void print(const std::shared_ptr<Any>& anything) {
    std::cout << (*anything) << std::endl;
  }

  void print(const std::map<
    std::shared_ptr<Object>,
    std::shared_ptr<Object>,
    ObjectComparator>::iterator& iterator) {
    std::cout << (*(iterator->first))
      << " : " 
      << (*(iterator->second))
      << std::endl;
  }

  template<TAdvIterator TIterator>
  void print(const TIterator& iterator) {
    using ValueType = typename std::iterator_traits<TIterator>::value_type;
    if constexpr (std::is_same_v<ValueType, std::shared_ptr<Object>>) {
      const std::shared_ptr<Object>& objPtr = *iterator;
      if (!objPtr.get()) {
        std::cout << "The container has already been freed" << std::endl;
      } else {
        std::cout << objPtr->toString().c_str() << std::endl;
      }
      
    } else {
      std::cout << (*iterator) << std::endl;
    }
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
    return (!reverse? result : reversed(result));
  }

  std::shared_ptr<String> str() {
    return String::spawn(std::string(""));
  }

  std::shared_ptr<String> str(const std::shared_ptr<Object>& object) {
    return String::spawn(object->toString());
  }

  std::shared_ptr<Number> sum(
    const std::shared_ptr<Dictionary>& numbers,
    const std::shared_ptr<Number>& extra = Number::spawn(0)) {
    std::shared_ptr<List> keys = numbers->keys();

    return Number::spawn(std::accumulate(
      keys->begin(),
      keys->end(),
      extra
    ));
    
  }

  template<TIterable TType>
  std::shared_ptr<Number> sum(
    const std::shared_ptr<TType>& numbers,
    const std::shared_ptr<Number>& extra = Number::spawn(0)) {
    return Number::spawn(std::accumulate(
        numbers->begin(),
        numbers->end(),
        extra
      ));
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
};
