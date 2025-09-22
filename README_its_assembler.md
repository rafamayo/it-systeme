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
