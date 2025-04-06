#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <set>
#include <limits>
#include <sstream>
#include <iomanip>

using namespace std;

struct Fraction {
    int numerator;
    int denominator;
    
    Fraction(int num, int den) : numerator(num), denominator(den) {
        simplify();
    }
    
    void simplify() {
        int gcd_val = gcd(abs(numerator), abs(denominator));
        numerator /= gcd_val;
        denominator /= gcd_val;
        if (denominator < 0) {
            numerator *= -1;
            denominator *= -1;
        }
    }
    
    double value() const {
        return static_cast<double>(numerator) / denominator;
    }
    
private:
    static int gcd(int a, int b) {
        return b == 0 ? a : gcd(b, a % b);
    }
};

bool is_square_free(int n) {
    if (n <= 1) return false;
    for (int i = 2; i * i <= n; ++i) {
        if (n % (i*i) == 0) return false;
    }
    return true;
}

vector<Fraction> generate_fractions(int num_min, int num_max, int den_min, int den_max) {
    set<pair<int, int>> unique_fractions;
    for (int num = num_min; num <= num_max; ++num) {
        for (int den = den_min; den <= den_max; ++den) {
            if (den == 0) continue;
            Fraction f(num, den);
            unique_fractions.insert({f.numerator, f.denominator});
        }
    }
    
    vector<Fraction> result;
    for (auto& [num, den] : unique_fractions) {
        result.emplace_back(num, den);
    }
    return result;
}

vector<int> generate_valid_e(int e_min, int e_max) {
    vector<int> valid_e;
    for (int e = max(2, e_min); e <= e_max; ++e) {
        if (is_square_free(e)) {
            valid_e.push_back(e);
        }
    }
    return valid_e;
}

struct Result {
    double error;
    Fraction a;
    Fraction c;
    int e;
    
    Result(double err, Fraction a_frac, Fraction c_frac, int e_val)
        : error(err), a(a_frac), c(c_frac), e(e_val) {}
};

string format_fraction(const Fraction& f) {
    if (f.denominator == 1) return to_string(f.numerator);
    return to_string(f.numerator) + "/" + to_string(f.denominator);
}

string format_result(const Result& res) {
    stringstream ss;
    ss << fixed << setprecision(6);
    
    ss << format_fraction(res.a);
    if (res.c.numerator != 0) {
        ss << " + " << format_fraction(res.c) << "√" << res.e;
    }
    ss << " (误差: " << res.error << ")";
    return ss.str();
}

int main() {
    double target;
    cout << "请输入目标实数: ";
    cin >> target;
    
    // 参数范围设置
    int a_num_min = -20, a_num_max = 20;
    int a_den_min = 1, a_den_max = 20;
    int c_num_min = -20, c_num_max = 20;
    int c_den_min = 1, c_den_max = 20;
    int e_min = 2, e_max = 20;
    int n = 5;

    // 生成有效组合
    auto a_fractions = generate_fractions(a_num_min, a_num_max, a_den_min, a_den_max);
    auto c_fractions = generate_fractions(c_num_min, c_num_max, c_den_min, c_den_max);
    auto valid_e = generate_valid_e(e_min, e_max);

    vector<Result> results;
    
    for (const auto& a : a_fractions) {
        for (const auto& c : c_fractions) {
            for (int e : valid_e) {
                try {
                    double value = a.value() + c.value() * sqrt(e);
                    double error = abs(value - target);
                    results.emplace_back(error, a, c, e);
                } catch (...) {
                    continue;
                }
            }
        }
    }

    // 排序结果
    sort(results.begin(), results.end(), [](const Result& a, const Result& b) {
        if (a.error != b.error) return a.error < b.error;
        if (a.a.numerator != b.a.numerator) return a.a.numerator < b.a.numerator;
        if (a.a.denominator != b.a.denominator) return a.a.denominator < b.a.denominator;
        if (a.c.numerator != b.c.numerator) return a.c.numerator < b.c.numerator;
        if (a.c.denominator != b.c.denominator) return a.c.denominator < b.c.denominator;
        return a.e < b.e;
    });

    // 输出结果
    cout << "\n最佳匹配结果：" << endl;
    int display_num = min(n, static_cast<int>(results.size()));
    for (int i = 0; i < display_num; ++i) {
        cout << i+1 << ". " << format_result(results[i]) << endl;
    }

    return 0;
}