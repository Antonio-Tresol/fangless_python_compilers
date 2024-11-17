#include <algorithm>
#include <cmath>
#include <iostream>
#include <map>
#include <optional>
#include <set>
#include <string>
#include <variant>
#include <vector>
#include <typeindex>

class Thing;

struct None {
 public:
  None() = default;
  ~None() = default;
};

using std::get;
using std::holds_alternative;
using std::map;
using std::set;
using std::string;
using std::variant;
using std::vector;

#define type_universe \
  int, double, string, vector<Thing*>, map<Thing*, Thing*>, set<Thing*>, None

template <class... Ts>
struct overloaded : Ts... {
  using Ts::operator()...;
};


class Thing : public variant<type_universe> {
 public:
  using std::variant<type_universe>::variant;

  inline bool isStructure() const {
    return holds_alternative<vector<Thing*>>(*this) ||
           holds_alternative<map<Thing*, Thing*>>(*this) ||
           holds_alternative<set<Thing*>>(*this);
  }

  inline bool isNone() const { return holds_alternative<None>(*this); };

  inline std::size_t getType() const {
    return this->index();
  }

  

//   auto& get() {
//     return std::visit(overloaded{
//             [] (int& variant) { return static_cast<int>(variant); },
//             [] (double& variant) { return static_cast<double>(variant); },
//             [] (std::string& variant) { return static_cast<std::string>(variant); },
//             [] (vector<Thing*>& variant) { return static_cast<vector<Thing*>>(variant); },
//             [] (map<Thing*, Thing*>& variant) { return static_cast<map<Thing*, Thing*>>(variant); },
//             [] (double& variant) { return static_cast<int>(variant); },
//         }, *this);
//}  
};


