# Assembler Programming Exercises

## 1. Arithmetic and Logic

### **1.1. Absolute Difference**
+ **Goal:** Compute the absolute difference between two memory bytes `x` and `y` and store the result in `d`.
+ **Concepts:** Subtraction, branching (sign test), complement logic, conditional jump (`JS`).

---

### **1.2. Maximum of Two Numbers**

+ **Goal:** Store the larger of two numbers (`x`, `y`) in `max`.
+ **Concepts:** Comparison (`CMP`), conditional jump (`JC`, `JS`), branching.
+ **Hint:** After `CMP`, check which register had the greater value.

---

### **1.3. Minimum of Three Numbers**

+ **Goal:** Given three numbers `a`, `b`, and `c`, store the smallest in `min`.
+ **Concepts:** Multi-step comparison, nested branches.
+ **Hint:** Compare `a` and `b`, store the smaller in `A`, then compare `A` with `c`.

---

### **1.4. Increment Until Limit**

+ **Goal:** Starting from 0, repeatedly increment `A` until it reaches 10.
+ **Concepts:** Loops, zero and sign flags, unconditional jump (`JMP`).
+ **Hint:** Use `INR A` and a decrementing counter.

---

### **1.5. Bitwise Logic Test**

+ **Goal:** Given two bytes `x` and `y`, compute AND, OR, XOR, and NOT, and store results at `and_r`, `or_r`, `xor_r`, and `not_r`.
+ **Concepts:** Bitwise operators (`ANA`, `ORA`, `XRA`, `CMA`), memory store (`STA`).

---

## 2. Control Flow and Branching

### **2.1. Countdown**

+ **Goal:** Store a number `N` in `C`, then repeatedly decrement and store to memory until zero.
+ **Concepts:** Looping, decrement, conditional jump (`JZ`), storing in memory.
+ **Hint:** You can use register `C` as the loop counter and `STA` to write to a moving memory address.

---

### **2.2. Parity Checker**

+ **Goal:** Determine if a number `x` has even or odd parity.
+ **Concepts:** Bitwise logic and condition flags.
+ **Hint:** Repeatedly rotate or mask bits and count 1s. If the count is even → store 0, else 1.

---

### **2.3. Compare and Swap**

+ **Goal:** Given two numbers `x` and `y`, swap them if `x > y`.
+ **Concepts:** Conditional logic, temporary registers, `CMP`, `JC`, `JMP`.
+ **Hint:** Use `A` as a temporary register for swap.

---

## 3. Memory Operations

### **3.1. Copy a Value**

+ **Goal:** Copy the content of memory address `src` into `dst`.
+ **Concepts:** `LDA`, `STA`, memory addressing.
+ **Hint:** The simplest data-move task.

---

### **3.2. Copy a Sequence of Bytes**

+ **Goal:** Copy 10 bytes starting from address `src` to address `dst`.
+ **Concepts:** Loops, address incrementing, indirect memory access via `C`.
+ **Hint:** Use `MOV C,A` to hold current address, then `LDA C` / `STA C`.

---

### **3.3. Fill Memory with a Constant**

+ **Goal:** Write the value 0xFF into the first 16 memory locations.
+ **Concepts:** Loops, memory addressing, indirect access.
+ **Hint:** Use a counter (`B`) and increment the address register (`C`).

---

## 4. Subroutines and CALL/RET

### **4.1. Square a Number (via Subroutine)**

+ **Goal:** Implement a subroutine at label `SQR` that returns `A*A` (by repeated addition).
+ **Concepts:** `CALL`, `RET`, loops, accumulator usage.
+ **Hint:** Use register `B` as a counter.

---

### **4.2. Add Three Numbers Using a Subroutine**

+ **Goal:** Create a subroutine `ADD_TWO` that adds two registers and returns result in `A`.
Then use it twice to add three numbers (`A+B+C`).
+ **Concepts:** Reusable subroutines, register passing.

---

### **4.3. Factorial (up to 5!)**

+ **Goal:** Compute 5! = 120 and store result at `res`.
+ **Concepts:** Loops, decrement, conditional stop (`JZ`).
+ **Hint:** Use `A` for result, `B` for counter, repeated addition to simulate multiplication.

---

## 5. Mixed Tasks / Challenge Problems

### **5.1. Sum of N Consecutive Numbers**

+ **Goal:** Sum the numbers 1 to N (N given in memory). Store the result at `sum`.
+ **Concepts:** Looping, incrementing, addition, flag checking.

---

### **5.2. Reverse Three Values**

+ **Goal:** Given memory bytes `[A,B,C]`, reverse their order in place.
+ **Concepts:** Memory load/store, temporary registers, sequencing.

---

### **5.3. Conditional Complement**

+ **Goal:** Read `x`. If negative (sign bit = 1), complement and add 1 (absolute value). Store to `res`.
+ **Concepts:** Arithmetic, sign testing, conditional branch.

---

### **5.4. Simulated LED Counter**

+ **Goal:** Increment memory location `led` repeatedly, wrapping after 0x0F.
+ **Concepts:** Looping, masking (`ANA`), overflow detection.

---

## 6. Extra (Creative / Open-ended)

### **6.1. Blink Simulation**

+ **Goal:** Alternate writing 0x00 and 0xFF to `port` memory location in an endless loop.
+ **Concepts:** Infinite loops, alternating logic, memory writes.

---

### **6.2. Greatest Common Divisor (GCD)**

+ **Goal:** Implement the Euclidean algorithm using subtraction only.
+ **Concepts:** Loops, comparison, branching, subtraction.

---

### **6.3. 8-bit Negation Table**

+ **Goal:** Generate the two’s complement of numbers from 0x00 to 0x0F and store them sequentially.
+ **Concepts:** Looping, complement, addition, indirect addressing.
