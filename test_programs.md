# Test programs

### 1) Arithmetic (ADD, SUB, INR, DCR)

```python
program_arithmetic = [
    0x20, 0x0A,   # MVI A,0x0A       ; A ← 0A
    0x21, 0x05,   # MVI B,0x05       ; B ← 05
    0x02,         # ADD B             ; A = 0A + 05 = 0F
    0x05,         # SUB B             ; A = 0F - 05 = 0A
    0x09,         # INR A             ; A = 0A + 1  = 0B
    0x0C,         # DCR A             ; A = 0B - 1  = 0A
    0x3F          # HLT
]
```

* **What it tests:**

  * `ADD B` correctly adds `register_B` to `A`
  * `SUB B` (two’s-complement subtract) brings it back
  * `INR A` / `DCR A` increment and decrement by 1
  * Flags (`Z/S/C/V`) are set/reset at each step

---

### 2) Logic (AND, OR, XOR, NOT, immediate variants, TST)

```python
program_logic = [
    0x20, 0xF0,   # MVI A,0xF0
    0x21, 0x0F,   # MVI B,0x0F
    0x0F,         # ANA B    ; A = F0 & 0F = 00
    0x16,         # CMA      ; A = ~00 = FF
    0x17, 0xAA,   # ANI 0xAA ; A = FF & AA = AA
    0x18, 0x55,   # ORI 0x55 ; A = AA | 55 = FF
    0x19, 0x0F,   # XRI 0x0F ; A = FF ^ 0F = F0
    0x11,         # TST      ; flags only on A & B (F0 & 0F = 00 → Z=1)
    0x3F          # HLT
]
```

* **What it tests:**

  * `ANA` and `CMA` and the immediate-AND/OR/XOR
  * That `TST` sets flags but leaves `A` unchanged

---

### 3) Register-to-Register Moves

```python
program_regmove = [
    0x20, 0x11,   # MVI A,0x11
    0x1A,         # MOV A,B ; B was 00 → A=00
    0x21, 0x22,   # MVI B,0x22
    0x1A,         # MOV A,B ; A=22
    0x1C,         # MOV B,A ; B=22
    0x22, 0x33,   # MVI C,0x33
    0x1D,         # MOV B,C ; B=33
    0x1E,         # MOV C,A ; C=22
    0x1F,         # MOV C,B ; C=33
    0x3F          # HLT
]
```

* **What it tests:**

  * `MOV A,B / A,C / B,A / B,C / C,A / C,B` all copy the right register

---

### 4) Memory Access (LDA/STA, via immediate and via C)

```python
program_memory = [
    0x20, 0xAA,   # MVI A,0xAA
    0x26, 0x10,   # STA 0x10   ; mem[0x10] ← AA
    0x21, 0x05,   # MVI B,0x05
    0x24, 0x10,   # LDB 0x10   ; B ← mem[0x10] = AA
    0x22, 0x05,   # MVI C,0x05
    0x29,         # LDA C      ; A ← mem[ C ] = mem[0x05] = (was 0)
    0x2A,         # STA C      ; mem[0x05] ← A (0)
    0x23, 0x10,   # LDA 0x10   ; A ← mem[0x10] = AA
    0x3F          # HLT
]
```

* **What it tests:**

  * `STA Address` / `LDB Address` / `LDA Address`
  * `MVI C,addr` + `LDA C` / `STA C`

---

### 5) Branches (JMP, JS, JZ, JC, JV)

```python
program_branches = [
    0x20, 0x00,   # MVI A,0x00
    0x09,         # INR A      ; A=1, Z=0, S=0, C=0, V=0
    0x2C, 0x07,   # JS 0x07    ; S==0 → no jump
    0x2D, 0x07,   # JZ 0x07    ; Z==0 → no jump
    0x2E, 0x07,   # JC 0x07    ; C==0 → no jump
    0x2F, 0x07,   # JV 0x07    ; V==0 → no jump
    0x2B, 0x0E,   # JMP 0x0E   ; unconditional → skip next HLT
    0x3F,         # HLT        ; (skipped)
    # at 0x0E:
    0x20, 0xFF,   # MVI A,0xFF ; landed here via JMP
    0x3F          # HLT
]
```

* **What it tests:**

  * All five branch types:
    – `JS` (sign), `JZ` (zero), `JC` (carry), `JV` (overflow) each *not* taken
    – then `JMP` to a later address

---

### 6) Subroutine Call & Return

```python
program_call = [
    0x20, 0x02,   # MVI A,0x02
    0x30, 0x07,   # CALL 0x07   ; pushes return addr, jumps
    0x3F,         # HLT         ; runs after RET
    # subroutine @0x07:
    0x21, 0x03,   # MVI B,0x03
    0x02,         # ADD B       ; A = 2 + 3 = 5
    0x31          # RET         ; returns to after CALL → HLT
]
```

* **What it tests:**

  * `CALL Address` stores return address at 0xFF, jumps into subroutine
  * subroutine modifies registers, `RET` brings you back

---

### 7) Miscellaneous (NOP, HLT)

```python
program_misc = [
    0x3E,         # NOP
    0x3E,         # NOP
    0x3F          # HLT
]
```

* **What it tests:**

  * `NOP` consumes a cycle but does nothing
  * `HLT` stops the machine

---

**How to run each test:**

```python
emulator = SimpleCPUEmulator()
emulator.read_into_memory(program_<category>)
emulator.run()
emulator.display_current_state()
# For memory tests, you can also call:
print(emulator.memory_dump())
```

Each snippet touches every opcode (or subgroup) in its category, and you can verify final register values, flags, or memory contents to ensure your emulator behaves correctly.



### 8) Simple For-Loop (decrement B until zero)

| Addr | Bytes   | Mnemonic     | Comment                                  |
| :--- | :------ | :----------- | :--------------------------------------- |
| 0x00 | `21 05` | `MVI B,0x05` | B ← 5                                    |
| 0x02 | `0D`    | `DCR B`      | B ← B – 1; flags ← (B)==0 …              |
| 0x03 | `2D 07` | `JZ 0x07`    | if Z==1 (i.e. B==0) jump to address 0x07 |
| 0x05 | `2B 02` | `JMP 0x02`   | else loop back and decrement again       |
| 0x07 | `3F`    | `HLT`        | stop                                     |

```python
program_loop = [
    0x21, 0x05,   # MVI B,5
    0x0D,         # DCR B
    0x2D, 0x07,   # JZ -> 0x07 (HLT) when B reaches 0
    0x2B, 0x02,   # JMP -> 0x02 to repeat
    0x3F          # HLT
]
```

**What happens:**

1. Load B with 5.
2. Each iteration: `DCR B` decrements B and sets Z when B→0.
3. If Z==1, `JZ 0x07` jumps to the halt; otherwise `JMP 0x02` loops.
4. When B finally hits zero, you break out and halt.

---

### 9) Subroutine Call & Return

| Addr | Bytes   | Mnemonic     | Comment                               |
| :--- | :------ | :----------- | :------------------------------------ |
| 0x00 | `20 03` | `MVI A,0x03` | A ← 3                                 |
| 0x02 | `30 05` | `CALL 0x05`  | push return addr; jump to 0x05        |
| 0x04 | `3F`    | `HLT`        | (after return, execution will halt)   |
| 0x05 | `09`    | `INR A`      | subroutine: A ← A+1                   |
| 0x06 | `31`    | `RET`        | pop return addr; resume at 0x04 (HLT) |

```python
program_call = [
    0x20, 0x03,  # MVI A,3
    0x30, 0x05,  # CALL subroutine at 0x05
    0x3F,        # HLT (will run after RET)
    0x09,        # INR A   (subroutine entry)
    0x31         # RET
]
```

**What happens:**

1. **`MVI A,3`** initializes A to 3.
2. **`CALL 0x05`** saves the address of the next instruction (0x04) into memory\[0xFF], then jumps to byte 0x05.
3. At **0x05**, the subroutine executes **`INR A`**, bumping A from 3→4.
4. **`RET`** loads the saved return address (0x04) from memory\[0xFF] and jumps back—so execution continues at the `HLT` at 0x04.
5. Finally, the machine halts with **A==4**, proving that the subroutine was called and returned correctly.

