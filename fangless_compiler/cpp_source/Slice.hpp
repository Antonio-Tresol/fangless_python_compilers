#ifndef SLICE_HPP
#define SLICE_HPP

#include "Object.hpp"

class Slice {
 public:
  int start;
  int end;
  int step;

  Slice(int start, int end, int step = 1)
    : start(start),
      end(end),
      step(step) {};

  Slice(int end) : start(0), end(end), step(1) {};

  Slice(std::shared_ptr<Number> start, bool end, bool step = true)
    : start(start->getInt()), end(end ? 1 : 0), step(step ? 1 : 0) {};

  Slice(std::shared_ptr<Number> start, std::shared_ptr<Number> end, bool step)
    : start(start->getInt()), end(end->getInt()), step(step ? 1 : 0) {};

  Slice(bool start, std::shared_ptr<Number> end,
    std::shared_ptr<Number> step = Number::spawn(1))
    : start(start ? 1 : 0), end(end->getInt()), step(step->getInt()) {};

  Slice(bool start, std::shared_ptr<Number> end, bool step)
    : start(start ? 1 : 0), end(end->getInt()), step(step ? 1 : 0) {};

  Slice(bool start, bool end, std::shared_ptr<Number> step)
    : start(start ? 1 : 0), end(end ? 1 : 0), step(step->getInt()) {};

  Slice(bool end)
    : start(0), end(end ? 1 : 0), step(1) {};
  
  Slice(std::shared_ptr<Number> start, std::shared_ptr<Number> end,
    std::shared_ptr<Number> step = Number::spawn(1))
    : start(start->getInt()),
      end(end->getInt()),
      step(step->getInt()) {};

  Slice(std::shared_ptr<Number> end)
    : start(0),
      end(end->getInt()),
      step(1) {};

  Slice(std::shared_ptr<Number> start, std::shared_ptr<Object> end,
    std::shared_ptr<Number> step)
    : start(start->getInt()), end(end->toBool() ? 1 : 0),
      step(step->getInt()) {};
  
  Slice(std::shared_ptr<Object> start, std::shared_ptr<Number> end,
    std::shared_ptr<Number> step = Number::spawn(1))
    : start(start->toBool() ? 1 : 0), end(end->getInt()),
      step(step->getInt()) {};

  Slice(std::shared_ptr<Number> start, std::shared_ptr<Number> end,
    std::shared_ptr<Object> step)
    : start(start->getInt()), end(end->getInt()),
      step(step->toBool() ? 1 : 0) {};

  Slice(std::shared_ptr<Number> start, std::shared_ptr<Object> end,
    std::shared_ptr<Object> step = Number::spawn(1))
    : start(start->getInt()), end(end->toBool() ? 1 : 0),
      step(step->toBool() ? 1 : 0) {};
  
  Slice(std::shared_ptr<Object> start, std::shared_ptr<Object> end,
    std::shared_ptr<Number> step)
    : start(start->toBool() ? 1 : 0), end(end->toBool() ? 1 : 0),
      step(step->getInt()) {};
  
  Slice(std::shared_ptr<Object> start, std::shared_ptr<Object> end,
    std::shared_ptr<Object> step = Number::spawn(1))
    : start(start->toBool()? 1:0),
      end(end->toBool()? 1:0),
      step(step->toBool()? 1:0) {};

  Slice(std::shared_ptr<Object> end)
    : start(0),
      end(end->toBool()? 1:0),
      step(1) {};
};
#endif