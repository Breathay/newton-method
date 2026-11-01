#include <iostream>
#include "function.cpp"

void test(){
    Vec2 x0{0, 0};
    Vec2 x1{3, 3};
    Vec2 x2{-1, -1};

    iteration(x0);
    iteration(x1);
    iteration(x2);
}

int main(){
    test();

    Vec2 x{0.0, 0.0};
    std::cout << "input x0 y0: ";
    std::cin >> x[0] >> x[1];
    iteration(x);
    return 0;
}
