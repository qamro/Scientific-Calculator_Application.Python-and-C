#include <stdio.h>


double PI() {
    return 3.141592653589793;
}

double E() {
    return 2.718281828459045;
}


double factorial(int n) {
    if(n < 0) return -1; 
    double result = 1;
    for(int i = 1; i <= n; i++)
        result *= i;
    return result;
}


double power(double x, int y) {
    double result = 1;
    int abs_y = (y < 0) ? -y : y;
    for(int i = 0; i < abs_y; i++)
        result *= x;
    if(y < 0) result = 1.0 / result;
    return result;
}


double sqrt_func(double x) {
    if(x < 0) return -1; // error
    double guess = x / 2.0;
    for(int i = 0; i < 20; i++)
        guess = (guess + x / guess) / 2.0;
    return guess;
}


double square(double x) {
    return x * x;
}


double add(double a, double b) { return a + b; }
double subtract(double a, double b) { return a - b; }
double multiply(double a, double b) { return a * b; }
double divide(double a, double b) { return (b != 0) ? a / b : 0; }


double ln(double x) {
    if(x <= 0) return -1; // error
    double y = (x - 1) / (x + 1);
    double y2 = y * y;
    double sum = 0;
    double term = y;
    for(int n = 1; n <= 99; n += 2) {
        sum += term / n;
        term *= y2;
    }
    return 2 * sum;
}


double log10_func(double x) {
    double natural_log = ln(x);
    return natural_log / ln(10.0);
}


double sin_func(double x) {
    double term = x;
    double sum = x;
    for(int i = 1; i < 10; i++) {
        term *= -1 * x * x / (2*i*(2*i+1));
        sum += term;
    }
    return sum;
}


double cos_func(double x) {
    double term = 1;
    double sum = 1;
    for(int i = 1; i < 10; i++) {
        term *= -1 * x * x / (2*i*(2*i-1));
        sum += term;
    }
    return sum;
}


double tan_func(double x) {
    double c = cos_func(x);
    if(c == 0) return 0; // prevent division by zero
    return sin_func(x) / c;
}


double deg_to_rad(double deg) {
    return deg * (PI() / 180.0);
}

double rad_to_deg(double rad) {
    return rad * (180.0 / PI());
}