# Mini Language Interpreter 🧠💻

A lightweight interpreter for a custom-designed programming language built using **Python** and **PLY (Python Lex-Yacc)**. This interpreter supports:

- 🧮 Variable assignments and arithmetic
- 🗣️ `print()` statements
- 🧠 Conditional statements (`if`, `else`)
- 🔁 Loops (`while`)
- 🔧 Function definitions and calls

---

## 🔧 Features

- ✅ Assignment: `x = 10`
- ✅ Arithmetic: `x + y * 2`
- ✅ Conditionals: `if (x == 5): print("yes")`
- ✅ Loops: `while (x == 3): x = x + 1`
- ✅ Functions:
    ```python
    def greet():
        print("Hello!")

    greet()
    ```

---

## 🚀 Getting Started

### 📦 Requirements

- Python 3.x
- `ply` library

### 🔧 Installation

pip install ply

▶️ Run the Interpreter

python ply_interpreter.py

Then type your code interactively:

>>> x = 5
>>> y = 10
>>> print(x + y)
15
>>> def hello(): print("Hi")
>>> hello()
Hi

🧪 Example Programs

x = 10
y = 5
print(x + y)

if (x == 10): 
    print("x is 10")
else: 
    print("x is not 10")

def square(): 
    print(x * x)

square()

🛠️ Built With

Python
PLY (Python Lex-Yacc)

📄 License

MIT License


