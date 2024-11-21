#ifndef SLICE_HPP
#define SLICE_HPP
class Slice {
 public:
  Slice(int start, int end) : start(start), end(end) {};
  
  Slice(std::shared_ptr<Number> start, std::shared_ptr<Number> end)
      : start(start->getInt()),
        end(end->getInt()) {};
  
  Slice(std::shared_ptr<Number> start, int end)
      : start(start->getInt()),
        end(end) {};
  
  Slice(int start, std::shared_ptr<Number> end)
      : start(start),
        end(end->getInt()) {};
  int start;
  int end;
};
#endif