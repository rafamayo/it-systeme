# ITS Assembler

The ITS Assembler is a Python-based assembler designed for a custom Instruction Set Architecture (ISA). This assembler reads assembly language code and translates it into machine code specific to the ITS ISA.

## Features

1. **Two-Pass Assembly Process**: The assembler operates in two passes. The first pass collects labels and their corresponding addresses, while the second pass generates the machine code.

2. **Label Handling**: Labels are used to mark specific locations in the code, and the assembler correctly resolves these labels to their corresponding addresses.

3. **Opcode Mapping**: The assembler includes a comprehensive mapping of mnemonics to their respective opcodes and instruction lengths, ensuring accurate translation of

assembly instructions to machine code.

4. **Operand Handling**: The assembler supports both immediate values and label-based operands, correctly interpreting and incorporating them into the machine code.

5. **Comment Support**: Comments (denoted with a semicolon `;`) in the assembly code are preserved alongside the machine code for readability and reference.

6. **Flexible Syntax Handling**: The assembler can handle different syntaxes, such as space-separated or comma-separated operands.

## Structure

The assembler consists of the main function `its_assembler` and two helper functions: `parse_line` and `append_machine_code_line`.

### its_assembler

- **Functionality**: This is the main function that orchestrates the assembly process. It takes a string of assembly code as input and returns a string representing the corresponding machine code.

- **First Pass**: Collects labels and calculates their addresses. Labels are identified by lines ending with `:`.

- **Second Pass**: Parses each line of the assembly code to generate machine code. This includes handling opcodes, operands, comments, and data values.

### parse_line

- **Functionality**: This helper function processes a line of assembly code to extract the opcode and operand parts. It handles different syntaxes and returns the opcode and the parts of the line.

### append_machine_code_line

- **Functionality**: Appends a line of machine code to the output based on the opcode, operand, and comments. It also handles operand resolution, converting label references or immediate values to their correct machine code representation.

## Usage

To use the ITS Assembler, create a string containing the assembly code and pass it to the `its_assembler` function. The function will return the translated machine code as a string.

Example:
```python
program_1_asm = """
MVI A, 00
LDB opr1
CMP
JZ end
MOV A, B
LDC opr2
DCR C
JS zero
start:
ADD B
DCR C
JZ end
JMP start
zero:
XRA B
end:
STA res
opr1:
0x02
opr2:
0x03
res:
0x00
"""
print(its_assembler(program_1_asm))
```


Feel free to modify this README to better fit your project's specifics or to add additional details you find relevant.
