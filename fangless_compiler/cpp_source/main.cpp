#include <iostream>
#include <vector>
#include <variant>
#include <string>
#include <map>
#include <any>

// Type definitions
using KeyType = std::variant<int, double, std::string, bool>;
using VarType = std::variant<int, double, bool, std::string, std::map<KeyType, std::any>, std::vector<std::any>>;

// Function to print KeyType
void printKey(const KeyType& key) {
    std::visit([](const auto& k) {
        std::cout << "  Key: " << k << std::endl;
    }, key);
}

// Function to print std::any values
void printAnyValue(const std::any& value) {
    if (value.type() == typeid(int)) {
        std::cout << "  Value: " << std::any_cast<int>(value) << std::endl;
    } else if (value.type() == typeid(double)) {
        std::cout << "  Value: " << std::any_cast<double>(value) << std::endl;
    } else if (value.type() == typeid(std::string)) {
        std::cout << "  Value: " << std::any_cast<std::string>(value) << std::endl;
    } else if (value.type() == typeid(bool)) {
        std::cout << "  Value: " << std::boolalpha << std::any_cast<bool>(value) << std::endl;
    } else {
        std::cout << "  Value: [Unknown Type]" << std::endl;
    }
}

void printVarType(const VarType& var);

void printMap(const std::map<KeyType, std::any>& m) {
    std::cout << "Map:" << std::endl;
    for (const auto& [key, value] : m) {
        printKey(key);
        printAnyValue(value);
    }
}

void printVector(const std::map<KeyType, std::any>& v) {
    std::cout << "Map:" << std::endl;
    for (const auto& value : v) {
        printAnyValue(value);
    }
}

void printVarType(const VarType& var) {
    std::visit([](const auto& arg) {
        using T = std::decay_t<decltype(arg)>;
        if constexpr (std::is_same_v<T, int>) {
            std::cout << "Int: " << arg << std::endl;
        } else if constexpr (std::is_same_v<T, double>) {
            std::cout << "Double: " << arg << std::endl;
        } else if constexpr (std::is_same_v<T, bool>) {
            std::cout << "Bool: " << std::boolalpha << arg << std::endl;
        } else if constexpr (std::is_same_v<T, std::string>) {
            std::cout << "String: " << arg << std::endl;
        } else if constexpr (std::is_same_v<T, std::map<KeyType, std::any>>) {
            printMap(arg);
        }
    }, var);
}

int main() {
    // Create a map equivalent to {"a": 3, "b": 4}
    std::map<KeyType, std::any> myMap = {
        {"a", 3},
        {"b", 4},
        {true, std::string("bool key")},
        {2.5, false}
    };

    // Create a vector of variants
    std::vector<VarType> multi_type = {
        1,
        3.2,
        "a",
        true,
        myMap
    };

    // Access and print the elements
    for (const auto& element : multi_type) {
        printVarType(element);
    }

    return 0;
}