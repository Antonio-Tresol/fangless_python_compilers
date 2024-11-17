#include <optional>
#include <vector>
#include <map>
#include <tuple>
#include <string>
#include <iostram>
#include <cmath>
#include <variant>

class Thing;

using el_universo_de_tipos = int, double, std::string, std::map<Thing>, std::vector<Thing>,

template<class... Ts> struct overloaded : Ts... { using Ts::operator()...; };

class Thing : public std::variant<el_universo_de_tipos> {
    public:
};

// jaja saludos :/
// 1. class None
// 2. class Thing: public std::variant<el universo de tipos + None>
// 3. Thing a = b
// 4. joseph plantillas


// std::visit(overloaded {
//     [](int cosaInt) {
//         cosaInt += 1;
//     }
// }, cosa);


