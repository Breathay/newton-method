#include <algorithm>
#include <array>
#include <cmath>
#include <iostream>
#include <random>

using Vec2 = std::array<double, 2>;
using Mat2 = std::array<std::array<double, 2>, 2>;

enum class Status {Converged, Singular, Diverged, Stagnated, MaxIter};

struct Result{
    Mat2 A{Vec2{0.0, 0.0}, Vec2{0.0, 0.0}};
    Vec2 b{0.0, 0.0};
    Vec2 x{1, 1};
    Status status = Status::MaxIter;
    int iter = 0;
    int singular_tries = 0;
    int stagnated_tries = 0;
};

Vec2 function(Vec2& x){
    double f1 = x[0] * x[0] + x[1] * x[1] - 4; // x ^ 2 + y ^ 2 - 4
    double f2 = x[0] * x[1] - 1; // x * y - 1
    return Vec2{f1, f2};
}

Mat2 jacobi(Vec2& x){
    Vec2 j1 = Vec2{x[0] * 2, x[1] * 2};
    Vec2 j2 = Vec2{x[1], x[0]};
    return Mat2{j1, j2};
}

bool update(Result& result){
    const Mat2 A = result.A;
    const Vec2 b = result.b;
    double det = A[0][0] * A[1][1] - A[0][1] * A[1][0];
    if (std::abs(det) < 1e-10){
        result.status = Status::Singular;
        return false;
    }
    result.x[0] -= (b[0] * A[1][1] - A[0][1] * b[1]) / det;
    result.x[1] -= (A[0][0] * b[1] - b[0] * A[1][0]) / det;
    result.iter += 1;
    return true;
}

void update_init_result(Result& result, std::mt19937& rng, int attempt){
    const double base = 0.1;
    const double radius = base * std::pow(2.0, attempt);                
    const double scale = std::max({1.0, std::abs(result.x[0]), std::abs(result.x[1])});   
    std::uniform_real_distribution<double> uni{-radius * scale, radius * scale}; 
    result.x[0] += uni(rng);
    result.x[1] += uni(rng);
}

Result iteration(Vec2& x, double tol=1e-10, int iter=100){
    Result result;
    result.x = x;
    std::mt19937 rng{12345u};
    const double kUnset = 1e30;
    double best = kUnset;

    for (int i = 0; i < iter; i++){
        result.b = function(result.x);
        result.A = jacobi(result.x);
        double norm = std::hypot(result.b[0], result.b[1]);

        // 找到解
        if (norm < tol){
            result.status = Status::Converged;
            std::cout << "find results:" << result.x[0] << "," << result.x[1] << "\n"; 
            return result;
        }

        // 发散
        if (norm > 1e9){
            result.status = Status::Diverged;
            std::cout << "result diverged, please change the inital result" << "\n";
            return result;
        }

        // 局部收敛
        if (norm < best){
            best = norm;
            result.stagnated_tries = 0;
        }
        else if (++result.stagnated_tries >= 15){
            if (i + 15 >= iter){
                result.status = Status::Stagnated;
                std::cout << "result stagnated" << "\n";
                return result;
            }
            update_init_result(result, rng, 0);
            best = kUnset;
            result.stagnated_tries = 0;
            continue;
        }

        // 矩阵奇异
        if (!update(result)){
            if (result.singular_tries >= 3){
                result.status = Status::Singular;
                std::cout << "result singular" << "\n";
                return result;
            }
            update_init_result(result, rng, result.singular_tries);
            ++result.singular_tries;
            best = kUnset;
            result.stagnated_tries = 0;
        }

        
    }
    result.status = Status::MaxIter;
    std::cout << "result maxiter" << "\n";
    return result;
}