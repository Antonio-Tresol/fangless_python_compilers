//
// Created by joe on 11/20/24.
//

#ifndef ITERABLE_HPP
#define ITERABLE_HPP
#include <memory>

struct ObjectComparator {
  bool operator()(const std::shared_ptr<Object>& obj1,
                  const std::shared_ptr<Object>& obj2) const {
    if (!(obj1 && obj2)) {
      return false;
    }

    return *obj1 < *obj2;
  }
};

class String;

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

#endif  // ITERABLE_HPPstd::vector<Object>>>
