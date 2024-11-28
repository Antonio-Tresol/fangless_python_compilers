#ifndef SLICE_HPP
#define SLICE_HPP
class Slice {
 public:
  int start;
  int end;
  int step;

  Slice(int end) : start(0), end(end), step(1) {};

  Slice(int start, int end, int step = 1)
    : start(start),
      end(end),
      step(step) {};

  Slice(std::shared_ptr<Number> end)
      : start(0),
        end(end->getInt()),
        step(1) {};
  
  Slice(std::shared_ptr<Number> start, std::shared_ptr<Number> end,
    std::shared_ptr<Number> step)
      : start(start->getInt()),
        end(end->getInt()),
        step(step->getInt()) {};
};
#endif