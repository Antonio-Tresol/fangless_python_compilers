//
// Created by joe on 11/20/24.
//

#ifndef ITERABLE_HPP
#define ITERABLE_HPP

struct ObjectComparator
{
    bool operator()(const std::shared_ptr<Object>& obj1, const std::shared_ptr<Object>& obj2) const
    {
        if (!(obj1 && obj2)) {
            return false;
        }

        return *obj1 < *obj2;
    }
};


#endif //ITERABLE_HPP
