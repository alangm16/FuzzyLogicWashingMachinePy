# Fuzzy Washing Machine Controller (Python)
**Fuzzy Logic Control System using Python, Tkinter and scikit-fuzzy**

This project implements a simple **Fuzzy Logic Control System** for a washing machine using **Python**.  
The application provides a graphical interface where the user can adjust input values and observe how the fuzzy controller calculates washing parameters.

The system is designed for educational purposes to demonstrate fuzzy inference, membership functions, and rule-based decision making.

---

## Features

- Graphical user interface built with Tkinter.
- Fuzzy inference system using scikit-fuzzy.
- Multiple input variables (fabric type, dirt level, load weight).
- Multiple output variables (wash time, temperature, drying time, RPM, washing quality).
- Real-time fuzzy computation.
- Easy to modify and extend.

---

## Fuzzy System Overview

### Input Variables
- **Fabric Type** (0–100)
- **Dirt Level** (0–100)
- **Load Weight** (0–100)

### Output Variables
- **Washing Time**
- **Temperature**
- **Drying Time**
- **RPM**
- **Washing Quality**

Each variable is represented using fuzzy membership functions and evaluated through a set of fuzzy rules.

---

## Technologies Used

- Python 3
- Tkinter (GUI)
- NumPy
- scikit-fuzzy

---

By: AlanGM16
