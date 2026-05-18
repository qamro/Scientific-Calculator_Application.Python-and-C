#include # calculator_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import ctypes
import os
import math

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Scientific Calculator")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        self.root.configure(bg='#2b2b2b')
        
        # Load C library
        self.load_c_library()
        
        # Variables
        self.current = ""
        self.operation = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        self.memory = 0
        self.angle_mode = "deg"  # deg or rad
        
        self.create_widgets()
    
    def load_c_library(self):
        """Load the compiled C library"""
        try:
            # Try to load the shared library
            if os.name == 'nt':  # Windows
                lib_name = 'libcalc_backend.dll'
            else:  # Linux/Mac
                lib_name = 'libcalc_backend.so'
            
            self.c_lib = ctypes.CDLL('libcalc_backend.so')
            
            # Define function signatures
            self.c_lib.add.argtypes = [ctypes.c_double, ctypes.c_double]
            self.c_lib.add.restype = ctypes.c_double
            
            self.c_lib.subtract.argtypes = [ctypes.c_double, ctypes.c_double]
            self.c_lib.subtract.restype = ctypes.c_double
            
            self.c_lib.multiply.argtypes = [ctypes.c_double, ctypes.c_double]
            self.c_lib.multiply.restype = ctypes.c_double
            
            self.c_lib.divide.argtypes = [ctypes.c_double, ctypes.c_double]
            self.c_lib.divide.restype = ctypes.c_double
            
            self.c_lib.power.argtypes = [ctypes.c_double, ctypes.c_double]
            self.c_lib.power.restype = ctypes.c_double
            
            self.c_lib.square_root.argtypes = [ctypes.c_double]
            self.c_lib.square_root.restype = ctypes.c_double
            
            self.c_lib.factorial.argtypes = [ctypes.c_int]
            self.c_lib.factorial.restype = ctypes.c_longlong
            
            self.c_lib.sine.argtypes = [ctypes.c_double, ctypes.c_int]
            self.c_lib.sine.restype = ctypes.c_double
            
            self.c_lib.cosine.argtypes = [ctypes.c_double, ctypes.c_int]
            self.c_lib.cosine.restype = ctypes.c_double
            
            self.c_lib.tangent.argtypes = [ctypes.c_double, ctypes.c_int]
            self.c_lib.tangent.restype = ctypes.c_double
            
            self.c_lib.logarithm.argtypes = [ctypes.c_double]
            self.c_lib.logarithm.restype = ctypes.c_double
            
            self.c_lib.natural_log.argtypes = [ctypes.c_double]
            self.c_lib.natural_log.restype = ctypes.c_double
            
            self.c_lib.exponential.argtypes = [ctypes.c_double]
            self.c_lib.exponential.restype = ctypes.c_double
            
        except OSError:
            messagebox.showwarning("Library Not Found", 
                "C backend library not found. Using Python fallback functions.\n"
                "Compile calc_backend.c to use C backend.")
            self.c_lib = None
    
    def create_widgets(self):
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Display frame
        display_frame = tk.Frame(self.root, bg='#2b2b2b')
        display_frame.pack(pady=20, padx=20, fill='x')
        
        # Display
        display = tk.Entry(display_frame, textvariable=self.result_var, 
                          font=('Arial', 24, 'bold'), 
                          justify='right', bd=0, 
                          bg='#1e1e1e', fg='#00ff00',
                          insertbackground='#00ff00')
        display.pack(fill='x', ipady=15)
        
        # Mode indicator
        mode_frame = tk.Frame(self.root, bg='#2b2b2b')
        mode_frame.pack(pady=5)
        
        self.mode_label = tk.Label(mode_frame, text=f"Mode: {self.angle_mode.upper()}", 
                                   font=('Arial', 10), bg='#2b2b2b', fg='#888888')
        self.mode_label.pack()
        
        # Button frame
        button_frame = tk.Frame(self.root, bg='#2b2b2b')
        button_frame.pack(padx=20, pady=10)
        
        # Button layout
        buttons = [
            ['C', '←', 'M+', 'MR', 'MC'],
            ['sin', 'cos', 'tan', 'π', 'e'],
            ['x²', '√', 'xʸ', 'log', 'ln'],
            ['7', '8', '9', '÷', 'n!'],
            ['4', '5', '6', '×', '('],
            ['1', '2', '3', '-', ')'],
            ['0', '.', '=', '+', 'DEG/RAD']
        ]
        
        # Button colors
        num_color = '#4a4a4a'
        op_color = '#ff9500'
        func_color = '#505050'
        special_color = '#d4d4d2'
        
        for i, row in enumerate(buttons):
            for j, btn_text in enumerate(row):
                # Determine button color
                if btn_text in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
                    bg_color = num_color
                    fg_color = 'white'
                elif btn_text in ['+', '-', '×', '÷', '=']:
                    bg_color = op_color
                    fg_color = 'white'
                elif btn_text in ['C', '←']:
                    bg_color = special_color
                    fg_color = 'black'
                else:
                    bg_color = func_color
                    fg_color = 'white'
                
                btn = tk.Button(button_frame, text=btn_text,
                              font=('Arial', 12, 'bold'),
                              bg=bg_color, fg=fg_color,
                              activebackground=bg_color,
                              activeforeground=fg_color,
                              bd=0, padx=10, pady=15,
                              command=lambda x=btn_text: self.button_click(x))
                btn.grid(row=i, column=j, padx=2, pady=2, sticky='nsew')
                
                # Make buttons expand
                button_frame.grid_columnconfigure(j, weight=1, minsize=80)
                button_frame.grid_rowconfigure(i, weight=1)
    
    def button_click(self, value):
        try:
            if value == 'C':
                self.clear()
            elif value == '←':
                self.backspace()
            elif value == '=':
                self.calculate()
            elif value == 'DEG/RAD':
                self.toggle_angle_mode()
            elif value == 'M+':
                self.memory_add()
            elif value == 'MR':
                self.memory_recall()
            elif value == 'MC':
                self.memory_clear()
            elif value in ['sin', 'cos', 'tan']:
                self.trig_function(value)
            elif value == '√':
                self.square_root()
            elif value == 'x²':
                self.square()
            elif value == 'xʸ':
                self.current = self.result_var.get()
                self.operation = '^'
                self.result_var.set(self.current + '^')
            elif value == 'log':
                self.logarithm()
            elif value == 'ln':
                self.natural_log()
            elif value == 'n!':
                self.factorial()
            elif value == 'π':
                self.result_var.set(str(math.pi))
            elif value == 'e':
                self.result_var.set(str(math.e))
            elif value in ['(', ')']:
                current = self.result_var.get()
                if current == '0':
                    self.result_var.set(value)
                else:
                    self.result_var.set(current + value)
            else:
                current = self.result_var.get()
                if current == '0' and value != '.':
                    self.result_var.set(value)
                else:
                    self.result_var.set(current + value)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.clear()
    
    def clear(self):
        self.result_var.set("0")
        self.current = ""
        self.operation = ""
    
    def backspace(self):
        current = self.result_var.get()
        if len(current) > 1:
            self.result_var.set(current[:-1])
        else:
            self.result_var.set("0")
    
    def calculate(self):
        try:
            expression = self.result_var.get()
            # Replace symbols for eval
            expression = expression.replace('×', '*').replace('÷', '/')
            expression = expression.replace('^', '**')
            result = eval(expression)
            self.result_var.set(str(result))
        except:
            messagebox.showerror("Error", "Invalid expression")
            self.clear()
    
    def toggle_angle_mode(self):
        self.angle_mode = "rad" if self.angle_mode == "deg" else "deg"
        self.mode_label.config(text=f"Mode: {self.angle_mode.upper()}")
    
    def memory_add(self):
        try:
            self.memory = float(self.result_var.get())
            messagebox.showinfo("Memory", f"Stored: {self.memory}")
        except:
            messagebox.showerror("Error", "Invalid value")
    
    def memory_recall(self):
        self.result_var.set(str(self.memory))
    
    def memory_clear(self):
        self.memory = 0
        messagebox.showinfo("Memory", "Memory cleared")
    
    def trig_function(self, func):
        try:
            value = float(self.result_var.get())
            is_deg = 1 if self.angle_mode == "deg" else 0
            
            if self.c_lib:
                if func == 'sin':
                    result = self.c_lib.sine(value, is_deg)
                elif func == 'cos':
                    result = self.c_lib.cosine(value, is_deg)
                elif func == 'tan':
                    result = self.c_lib.tangent(value, is_deg)
            else:
                # Fallback to Python
                if self.angle_mode == "deg":
                    value = math.radians(value)
                if func == 'sin':
                    result = math.sin(value)
                elif func == 'cos':
                    result = math.cos(value)
                elif func == 'tan':
                    result = math.tan(value)
            
            self.result_var.set(str(result))
        except:
            messagebox.showerror("Error", "Invalid input")
    
    def square_root(self):
        try:
            value = float(self.result_var.get())
            if self.c_lib:
                result = self.c_lib.square_root(value)
            else:
                result = math.sqrt(value)
            self.result_var.set(str(result))
        except:
            messagebox.showerror("Error", "Invalid input")
    
    def square(self):
        try:
            value = float(self.result_var.get())
            if self.c_lib:
                result = self.c_lib.power(value, 2.0)
            else:
                result = value ** 2
            self.result_var.set(str(result))
        except:
            messagebox.showerror("Error", "Invalid input")
    
    def logarithm(self):
        try:
            value = float(self.result_var.get())
            if self.c_lib:
                result = self.c_lib.logarithm(value)
            else:
                result = math.log10(value)
            self.result_var.set(str(result))
        except:
            messagebox.showerror("Error", "Invalid input or value <= 0")
    
    def natural_log(self):
        try:
            value = float(self.result_var.get())
            if self.c_lib:
                result = self.c_lib.natural_log(value)
            else:
                result = math.log(value)
            self.result_var.set(str(result))
        except:
            messagebox.showerror("Error", "Invalid input or value <= 0")
    
    def factorial(self):
        try:
            value = int(float(self.result_var.get()))
            if value < 0:
                raise ValueError("Factorial of negative number")
            if value > 20:
                raise ValueError("Number too large (max 20)")
            
            if self.c_lib:
                result = self.c_lib.factorial(value)
            else:
                result = math.factorial(value)
            self.result_var.set(str(result))
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()


# ============================================
# C BACKEND CODE (calc_backend.c)
# ============================================
"""
/ -------------------- Constants --------------------
// Return PI constant
double PI() {
    return 3.141592653589793;
}

// Return Euler's number e
double E() {
    return 2.718281828459045;
}

// -------------------- Factorial --------------------
// Compute factorial of a non-negative integer n
double factorial(int n) {
    if(n < 0) return -1; // error
    double result = 1;
    for(int i = 1; i <= n; i++)
        result *= i;
    return result;
}

// -------------------- Power Functions --------------------
// Compute x raised to the power y
double power(double x, int y) {
    double result = 1;
    int abs_y = (y < 0) ? -y : y;
    for(int i = 0; i < abs_y; i++)
        result *= x;
    if(y < 0) result = 1.0 / result;
    return result;
}

// Compute square root using Newton's method
double sqrt_func(double x) {
    if(x < 0) return -1; // error
    double guess = x / 2.0;
    for(int i = 0; i < 20; i++)
        guess = (guess + x / guess) / 2.0;
    return guess;
}

// Square (power of 2)
double square(double x) {
    return x * x;
}

// -------------------- Basic Operations --------------------
double add(double a, double b) { return a + b; }
double subtract(double a, double b) { return a - b; }
double multiply(double a, double b) { return a * b; }
double divide(double a, double b) { return (b != 0) ? a / b : 0; }

// -------------------- Logarithms --------------------
// Natural log using simple series (approximation)
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

// Log base 10
double log10_func(double x) {
    double natural_log = ln(x);
    return natural_log / ln(10.0);
}

// -------------------- Trigonometric Functions --------------------
// sin(x) approximation using Taylor series (x in radians)
double sin_func(double x) {
    double term = x;
    double sum = x;
    for(int i = 1; i < 10; i++) {
        term *= -1 * x * x / (2*i*(2*i+1));
        sum += term;
    }
    return sum;
}

// cos(x) approximation using Taylor series
double cos_func(double x) {
    double term = 1;
    double sum = 1;
    for(int i = 1; i < 10; i++) {
        term *= -1 * x * x / (2*i*(2*i-1));
        sum += term;
    }
    return sum;
}

// tan(x) = sin(x)/cos(x)
double tan_func(double x) {
    double c = cos_func(x);
    if(c == 0) return 0; // prevent division by zero
    return sin_func(x) / c;
}

// -------------------- Angle Conversion --------------------
double deg_to_rad(double deg) {
    return deg * (PI() / 180.0);
}

double rad_to_deg(double rad) {
    return rad * (180.0 / PI());
}
"""