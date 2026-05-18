// calc_backend.c
#include <math.h>

#define PI 3.14159265358979323846

double add(double a, double b) { return a + b; }
double subtract(double a, double b) { return a - b; }
double multiply(double a, double b) { return a * b; }
double divide(double a, double b) { 
    return (b == 0.0) ? 0.0 : a / b; 
}
double power(double base, double exponent) { 
    return pow(base, exponent); 
}
double square_root(double x) { 
    return (x < 0.0) ? 0.0 : sqrt(x); 
}

long long factorial(int n) {
    if (n < 0 || n > 20) return -1;
    if (n == 0 || n == 1) return 1;
    long long result = 1;
    for (int i = 2; i <= n; i++) result *= i;
    return result;
}

double sine(double x, int is_degree) {
    return sin(is_degree ? x * PI / 180.0 : x);
}
double cosine(double x, int is_degree) {
    return cos(is_degree ? x * PI / 180.0 : x);
}
double tangent(double x, int is_degree) {
    return tan(is_degree ? x * PI / 180.0 : x);
}

double logarithm(double x) { 
    return (x <= 0.0) ? 0.0 : log10(x); 
}
double natural_log(double x) { 
    return (x <= 0.0) ? 0.0 : log(x); 
}
double exponential(double x) { 
    return exp(x); 
}
