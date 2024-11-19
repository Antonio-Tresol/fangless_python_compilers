#ifndef SLICE_HPP
#define SLICE_HPP
class Slice {
 public:
  Slice(int start, int end) : start(start), end(end) {};
  int start;
  int end;
};
#endif