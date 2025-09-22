# Simple Assembler

This project contains a **Simple Assembler** for a toy CPU architecture.  
It takes assembly source code with labels, instructions, data definitions, and inline comments, and produces a machine-code program suitable for execution on the companion [Simple CPU Emulator](../simple_cpu_emulator.py).

---

## Features

- Two-pass assembler:
  - **Pass 1:** Collects labels and assigns addresses
  - **Pass 2:** Emits opcodes, operands, and data bytes
- Supports three addressing modes:
  - **none** → instructions without operands (e.g. `HLT`, `ADD B`)
  - **imm** → immediate values (e.g. `MVI A 0x12`)
  - **addr** → labels or numeric addresses (e.g. `LDA var`, `JMP loop`)
- Handles both **code labels** (jump/call targets) and **data labels** (memory locations for variables).
- Preserves **inline comments** from the source and attaches them to the machine-code listing.
- Output:
  - **Raw machine code**: list of integer bytes (e.g. `[0x23, 0x11, 0x24, 0x12, …]`) that can be loaded into the emulator.
  - **Assembly listing**: human-readable address + hex dump + comments, similar to traditional assemblers.

---

## Usage

### 1. Install / Clone

Clone this repository and make sure Python 3.9+ is available:

```bash
git clone https://github.com/yourusername/simple-assembler.git
cd simple-assembler
```

---

## 2. Example Program

```asm
    LDA x            ; Load the value at address x into register A
    LDB y            ; Load the value at address y into register B
    SUB B            ; Perform the subtraction A = A - B
    CMA              ; Complement A
    JS positiv       ; Jump if sign flag is set (A>=B)
    STA d            ; Store the value in register A to address d
    HLT              ; Stop the program
positiv:
    CMA              ; Complement A
    STA d            ; Store the value in register A to address d
    HLT              ; Stop the program
x:                  ; First number
    0x0A
y:                  ; Second number
    0x03
d:                  ; Result
    0x00
```

---

## 3. Assembling

```python
from simple_assembler import SimpleAssembler

asm_program = """
    LDA x            ; Load the value at address x into register A
    LDB y            ; Load the value at address y into register B
    SUB B            ; Perform the subtraction A = A - B
    CMA              ; Complement A
    JS positiv       ; Jump if sign flag is set (A>=B)
    STA d            ; Store the value in register A to address d
    HLT              ; Stop the program
positiv:
    CMA              ; Complement A
    STA d            ; Store the value in register A to address d
    HLT              ; Stop the program
x:                  ; First number
    0x0A
y:                  ; Second number
    0x03
d:                  ; Result
    0x00
"""

assembler = SimpleAssembler()
machine_code, listing = assembler.assemble_with_listing(asm_program)

print("Machine code:", machine_code)
print("\nAssembly listing:\n")
print(listing)
```

---

## 4. Sample output

### Machine code

[0x23, 0x0F, 0x24, 0x10, 0x05, 0x16, 0x2C, 0x0B,
 0x26, 0x11, 0x3F, 0x16, 0x26, 0x11, 0x3F, 0x0A,
 0x03, 0x00]

### Listing

```text
00: 0x23 ; Load the value at address x into register A
01: 0x0F
02: 0x24 ; Load the value at address y into register B
03: 0x10
04: 0x05 ; Perform the subtraction A = A - B
05: 0x16 ; Complement A
06: 0x2C ; Jump if sign flag is set (A>=B)
07: 0x0B
08: 0x26 ; Store the value in register A to address d
09: 0x11
0A: 0x3F ; Stop the program
0B: 0x16 ; Complement A
0C: 0x26 ; Store the value in register A to address d
0D: 0x11
0E: 0x3F ; Stop the program
0F: 0x0A ; First number
10: 0x03 ; Second number
11: 0x00 ; Result
```
