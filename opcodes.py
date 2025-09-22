# opcodes.py

# Import the Emulator class
from simple_cpu_emulator import SimpleCPUEmulator

def opcode(code):
    def decorator(func):
        SimpleCPUEmulator.dispatch_table[code] = func
        return func
    return decorator

################
### Arithmetic
################

@opcode(0x02)
def opcode_ADD_B(self):
    print("Executing opcode: ADD B")
    op1 = self.register_A
    op2 = self.register_B
    total = op1 + op2
    result = total & 0xFF  # Truncate to 8 bits.
    self.register_A = result

    # Update flags with the original operands for addition.
    self.update_flags(total, result, op1, op2)

@opcode(0x03)
def opcode_ADD_C(self):
    print("Executing opcode: ADD C")
    op1 = self.register_A
    op2 = self.register_C
    total = op1 + op2
    result = total & 0xFF  # Truncate to 8 bits.
    self.register_A = result

    # Update flags with the original operands for addition.
    self.update_flags(total, result, op1, op2)

# Add with carry. Necessary when doing multi-byte additions
@opcode(0x04)
def opcode_ADC_B(self):
    print("Executing opcode: ADC B")
    op1 = self.register_A
    op2 = self.register_B
    total = op1 + op2 + 1
    result = total & 0xFF  # Truncate to 8 bits.
    self.register_A = result

    # Update flags with the original operands for addition.
    self.update_flags(total, result, op1, op2)

@opcode(0x05)
def opcode_SUB_B(self):
    print("Executing opcode: SUB B")
    op1 = self.register_A
    # Compute two's complement of register_B.
    neg_B = (~self.register_B) & 0xFF
    total = op1 + neg_B + 1
    result = total & 0xFF  # Truncate to 8 bits.
    self.register_A = result

    # Update flags passing op1 and neg_B (i.e., the effective second operand).
    self.update_flags(total, result, op1, neg_B)

@opcode(0x06)
def opcode_SUB_C(self):
    print("Executing opcode: SUB C")
    op1 = self.register_A
    # Compute two's complement of register_C.
    neg_C = (~self.register_C) & 0xFF
    total = op1 + neg_C + 1
    result = total & 0xFF  # Truncate to 8 bits.
    self.register_A = result

    # Update flags passing op1 and neg_B (i.e., the effective second operand).
    self.update_flags(total, result, op1, neg_C)

# Subtract with borrow. Necessary when doing multi-byte subtractions
@opcode(0x07)
def opcode_SUC_B(self):
    print("Executing opcode: SUC B")
    op1 = self.register_A
    # Compute two's complement of register_B.
    neg_B = (~self.register_B) & 0xFF
    total = op1 + neg_B # borrow is taken into account
    result = total & 0xFF  # Truncate to 8 bits.
    self.register_A = result

    # Update flags passing op1 and neg_B (i.e., the effective second operand).
    self.update_flags(total, result, op1, neg_B)

@opcode(0x08)
def opcode_CMP(self):
    print("Executing opcode: CMP")
    op1 = self.register_A
    # Compute two's complement of register_B.
    neg_B = (~self.register_B) & 0xFF
    total = op1 + neg_B + 1
    result = total & 0xFF  # Truncate to 8 bits.
    # Discard the result, just compute the flags

    # Update flags passing op1 and neg_B (i.e., the effective second operand).
    self.update_flags(total, result, op1, neg_B)

@opcode(0x09)
def opcode_INR_A(self):
    print("Executing opcode: INR A")
    op1 = self.register_A
    total = op1 + 1
    result = total & 0xFF  # Truncate to 8 bits.
    self.register_A = result

    # Update flags with the original operands for addition.
    self.update_flags(total, result, op1, 1)

@opcode(0x0A)
def opcode_INR_B(self):
    print("Executing opcode: INR B")
    op1 = self.register_B
    total = op1 + 1
    result = total & 0xFF  # Truncate to 8 bits.
    self.register_B = result

    # Update flags with the original operands for addition.
    self.update_flags(total, result, op1, 1)

@opcode(0x0B)
def opcode_INR_C(self):
    print("Executing opcode: INR C")
    op1 = self.register_C
    total = op1 + 1
    result = total & 0xFF  # Truncate to 8 bits.
    self.register_C = result

    # Update flags with the original operands for addition.
    self.update_flags(total, result, op1, 1)

@opcode(0x0C)
def opcode_DCR_A(self):
    print("Executing opcode: DCR A")
    op1 = self.register_A
    op2 = 1
    # Compute two's complement of op2.
    neg_2 = (~op2) & 0xFF
    total = op1 + neg_2 + 1
    result = total & 0xFF  # Truncate to 8 bits.
    self.register_A = result

    # Update flags passing op1 and neg_B (i.e., the effective second operand).
    self.update_flags(total, result, op1, neg_2)

@opcode(0x0D)
def opcode_DCR_B(self):
    print("Executing opcode: DCR B")
    op1 = self.register_B
    op2 = 1
    # Compute two's complement of op2.
    neg_2 = (~op2) & 0xFF
    total = op1 + neg_2 + 1
    result = total & 0xFF  # Truncate to 8 bits.
    self.register_B = result

    # Update flags passing op1 and neg_B (i.e., the effective second operand).
    self.update_flags(total, result, op1, neg_2)

@opcode(0x0E)
def opcode_DCR_C(self):
    print("Executing opcode: DCR C")
    op1 = self.register_C
    op2 = 1
    # Compute two's complement of op2.
    neg_2 = (~op2) & 0xFF
    total = op1 + neg_2 + 1
    result = total & 0xFF  # Truncate to 8 bits.
    self.register_C = result

    # Update flags passing op1 and neg_B (i.e., the effective second operand).
    self.update_flags(total, result, op1, neg_2)

###########
### Logic
###########

@opcode(0x0F)
def opcode_ANA_B(self):
    print("Executing opcode: ANA B")
    op1 = self.register_A
    op2 = self.register_B
    total = op1 & op2
    result = total & 0xFF  # Truncate to 8 bits.
    self.register_A = result

    # Update flags passing op1 and op2.
    self.update_flags(total, result, op1, op2)

@opcode(0x10)
def opcode_ANA_C(self):
    print("Executing opcode: ANA C")
    op1 = self.register_A
    op2 = self.register_C
    total = op1 & op2
    result = total & 0xFF  # Truncate to 8 bits.
    self.register_A = result

    # Update flags passing op1 and op2.
    self.update_flags(total, result, op1, op2)

@opcode(0x11)
def opcode_TST(self):
    print("Executing opcode: TST")
    op1 = self.register_A
    op2 = self.register_B
    total = op1 & op2
    result = total & 0xFF  # Truncate to 8 bits.
    # Discard the result, just compute the flags

    # Update flags passing op1 and op2.
    self.update_flags(total, result, op1, op2)

@opcode(0x12)
def opcode_ORA_B(self):
    print("Executing opcode: ORA B")
    op1 = self.register_A
    op2 = self.register_B
    total = op1 | op2
    result = total & 0xFF  # Truncate to 8 bits.
    self.register_A = result

    # Update flags passing op1 and op2.
    self.update_flags(total, result, op1, op2)

@opcode(0x13)
def opcode_ORA_C(self):
    print("Executing opcode: ORA C")
    op1 = self.register_A
    op2 = self.register_C
    total = op1 | op2
    result = total & 0xFF  # Truncate to 8 bits.
    self.register_A = result

    # Update flags passing op1 and op2.
    self.update_flags(total, result, op1, op2)

@opcode(0x14)
def opcode_XRA_B(self):
    print("Executing opcode: XRA B")
    op1 = self.register_A
    op2 = self.register_B
    total = op1 ^ op2
    result = total & 0xFF  # Truncate to 8 bits.
    self.register_A = result

    # Update flags passing op1 and op2.
    self.update_flags(total, result, op1, op2)

@opcode(0x15)
def opcode_XRA_C(self):
    print("Executing opcode: XRA C")
    op1 = self.register_A
    op2 = self.register_C
    total = op1 ^ op2
    result = total & 0xFF  # Truncate to 8 bits.
    self.register_A = result

    # Update flags passing op1 and op2.
    self.update_flags(total, result, op1, op2)

@opcode(0x16)
def opcode_CMA(self):
    print("Executing opcode: CMA")
    op1 = self.register_A
    op2 = 0x00
    total = ~op1
    result = total & 0xFF  # Truncate to 8 bits.
    self.register_A = result

    # Update flags passing op1 and op2.
    self.update_flags(total, result, op1, op2)

@opcode(0x17)
def opcode_ANI(self):
    print("Executing opcode: ANI Byte")
    # The argument of this opcode is the immediate value with which we want to perform a logical AND
    # The instruction pointer should point to the argument (correct value set by the execution cycle)
    # This operation is not memory safe: no checks are done on the validity of the address
    op1 = self.register_A
    op2 = self.memory[self.ip]   # The immediate value Byte
    total = op1 & op2
    result = total & 0xFF  # Truncate to 8 bits.
    self.register_A = result
 
    # We need to advance the instruction pointer
    self.ip += 1
 
    # Update flags passing op1 and op2.
    self.update_flags(total, result, op1, op2)

@opcode(0x18)
def opcode_ORI(self):
    print("Executing opcode: ORI Byte")
    # The argument of this opcode is the immediate value with which we want to perform a logical OR
    # The instruction pointer should point to the argument (correct value set by the execution cycle)
    # This operation is not memory safe: no checks are done on the validity of the address
    op1 = self.register_A
    op2 = self.memory[self.ip]   # The immediate value Byte
    total = op1 | op2
    result = total & 0xFF  # Truncate to 8 bits.
    self.register_A = result
 
    # We need to advance the instruction pointer
    self.ip += 1
 
    # Update flags passing op1 and op2.
    self.update_flags(total, result, op1, op2)

@opcode(0x19)
def opcode_XRI(self):
    print("Executing opcode: XRI Byte")
    # The argument of this opcode is the immediate value with which we want to perform a logical XOR
    # The instruction pointer should point to the argument (correct value set by the execution cycle)
    # This operation is not memory safe: no checks are done on the validity of the address
    op1 = self.register_A
    op2 = self.memory[self.ip]   # The immediate value Byte
    total = op1 ^ op2
    result = total & 0xFF  # Truncate to 8 bits.
    self.register_A = result
 
    # We need to advance the instruction pointer
    self.ip += 1
 
    # Update flags passing op1 and op2.
    self.update_flags(total, result, op1, op2)


##########################
### Register to register
##########################

@opcode(0x1A)
def opcode_MOV_A_B(self):
    print("Executing opcode: MOV A B")
    self.register_A = (self.register_B) & 0xFF
    # No flags are updated

@opcode(0x1B)
def opcode_MOV_A_C(self):
    print("Executing opcode: MOV A C")
    self.register_A = (self.register_C) & 0xFF
    # No flags are updated

@opcode(0x1C)
def opcode_MOV_B_A(self):
    print("Executing opcode: MOV B A")
    self.register_B = (self.register_A) & 0xFF
    # No flags are updated

@opcode(0x1D)
def opcode_MOV_B_C(self):
    print("Executing opcode: MOV B C")
    self.register_B = (self.register_C) & 0xFF
    # No flags are updated

@opcode(0x1E)
def opcode_MOV_C_A(self):
    print("Executing opcode: MOV C A")
    self.register_C = (self.register_A) & 0xFF
    # No flags are updated

@opcode(0x1F)
def opcode_MOV_C_B(self):
    print("Executing opcode: MOV C B")
    self.register_C = (self.register_B) & 0xFF
    # No flags are updated

@opcode(0x20)
def opcode_MVI_A_Byte(self):
    print("Executing opcode: MVI A Byte")
    # The argument of this opcode is the immediate value which we want to copy into A
    # The instruction pointer should point to the argument (correct value set by the execution cycle)
    # This operation is not memory safe: no checks are done on the validity of the address    
    self.register_A = self.memory[self.ip] & 0xFF

    # We need to advance the instruction pointer
    self.ip += 1
    # No flags are updated

@opcode(0x21)
def opcode_MVI_B_Byte(self):
    print("Executing opcode: MVI B Byte")
    # The argument of this opcode is the immediate value which we want to copy into B
    # The instruction pointer should point to the argument (correct value set by the execution cycle)
    # This operation is not memory safe: no checks are done on the validity of the address    
    self.register_B = self.memory[self.ip] & 0xFF

    # We need to advance the instruction pointer
    self.ip += 1
    # No flags are updated

@opcode(0x22)
def opcode_MVI_C_Byte(self):
    print("Executing opcode: MVI C Byte")
    # The argument of this opcode is the immediate value which we want to copy into C
    # The instruction pointer should point to the argument (correct value set by the execution cycle)
    # This operation is not memory safe: no checks are done on the validity of the address    
    self.register_C = self.memory[self.ip] & 0xFF

    # We need to advance the instruction pointer
    self.ip += 1
    # No flags are updated


###################
### Memory access
###################

@opcode(0x23)
def opcode_LDA_Address(self):
    print("Executing opcode: LDA Address")
    # The argument of this opcode is the memory address from which we want to read.
    # The instruction pointer should point to the argument
    # This operation is not memory safe: no checks are done on the validity of the address
    address = self.memory[self.ip]
    self.register_A = self.memory[address]
    # We need to advance the instruction pointer
    self.ip += 1
    # No flags are updated

@opcode(0x24)
def opcode_LDB_Address(self):
    print("Executing opcode: LDB Address")
    # The argument of this opcode is the memory address from which we want to read.
    # The instruction pointer should point to the argument
    # This operation is not memory safe: no checks are done on the validity of the address
    address = self.memory[self.ip]
    self.register_B = self.memory[address]
    # We need to advance the instruction pointer
    self.ip += 1
    # No flags are updated

@opcode(0x25)
def opcode_LDC_Address(self):
    print("Executing opcode: LDC Address")
    # The argument of this opcode is the memory address from which we want to read.
    # The instruction pointer should point to the argument
    # This operation is not memory safe: no checks are done on the validity of the address
    address = self.memory[self.ip]
    self.register_C = self.memory[address]
    # We need to advance the instruction pointer
    self.ip += 1
    # No flags are updated

@opcode(0x26)
def opcode_STA_Address(self):
    print("Executing opcode: STA Address")
    # The argument of this opcode is the memory address to which we want to write.
    # The instruction pointer should point to the argument
    # This operation is not memory safe: no checks are done on the validity of the address
    address = self.memory[self.ip]
    self.memory[address] = self.register_A
    # We need to advance the instruction pointer
    self.ip += 1
    # No flags are updated

@opcode(0x29)
def opcode_LDA_C(self):
    print("Executing opcode: LDA C")
    # This operation is not memory safe: no checks are done on the validity of the address in register C
    address = self.register_C
    self.register_A = self.memory[address]
    # No flags are updated

@opcode(0x2A)
def opcode_STA_C(self):
    print("Executing opcode: STA C")
    # This operation is not memory safe: no checks are done on the validity of the address in register C
    address = self.register_C
    self.memory[address] = self.register_A
    # No flags are updated


##############
### Branches
##############

@opcode(0x2B)
def opcode_JMP(self):
    print("Executing opcode: JMP Address")
    # The argument of this opcode is the memory address to which we want to jump.
    # The instruction pointer should point to the argument (correct value set by the execution cycle)
    # This operation is not memory safe: no checks are done on the validity of the address
    address = self.memory[self.ip]
    self.ip = address
    # No flags are updated

@opcode(0x2C)
def opcode_JS(self):
    print("Executing opcode: JS Address")
    # The argument of this opcode is the memory address to which we want to jump.
    # The instruction pointer should point to the argument (correct value set by the execution cycle)
    # This operation is not memory safe: no checks are done on the validity of the address
    if self.flag_S == 1:
        address = self.memory[self.ip]
        self.ip = address
    else:
        self.ip += 1
    # No flags are updated

@opcode(0x2D)
def opcode_JZ(self):
    print("Executing opcode: JZ Address")
    # The argument of this opcode is the memory address to which we want to jump.
    # The instruction pointer should point to the argument (correct value set by the execution cycle)
    # This operation is not memory safe: no checks are done on the validity of the address
    if self.flag_Z == 1:
        address = self.memory[self.ip]
        self.ip = address
    else:
        self.ip += 1
    # No flags are updated

@opcode(0x2E)
def opcode_JC(self):
    print("Executing opcode: JC Address")
    # The argument of this opcode is the memory address to which we want to jump.
    # The instruction pointer should point to the argument (correct value set by the execution cycle)
    # This operation is not memory safe: no checks are done on the validity of the address
    if self.flag_C == 1:
        address = self.memory[self.ip]
        self.ip = address
    else:
        self.ip += 1
    # No flags are updated

@opcode(0x2F)
def opcode_JV(self):
    print("Executing opcode: JV Address")
    # The argument of this opcode is the memory address to which we want to jump.
    # The instruction pointer should point to the argument (correct value set by the execution cycle)
    # This operation is not memory safe: no checks are done on the validity of the address
    if self.flag_V == 1:
        address = self.memory[self.ip]
        self.ip = address
    else:
        self.ip += 1
    # No flags are updated

##########################
### Call methods
##########################

@opcode(0x30)
def opcode_CALL(self):
    print("Executing opcode: CALL Address")
    # The argument of this opcode is the memory address where the routine is found
    # The instruction pointer should point to the argument (correct value set by the execution cycle)
    # This operation is not memory safe: no checks are done on the validity of the address
    address = self.memory[self.ip]      # The address where the routine is
    self.ip += 1                        # The address whre we want to return to
    self.memory[0xFF] = self.ip         # Store the return address at 0xFF
    self.ip = address                   # Jump to the routine
    # No flags are updated

@opcode(0x31)
def opcode_RET(self):
    print("Executing opcode: RET")
    # Return from a routine call
    # The return address is expected to be at position 0xFF
    # This operation is not memory safe: no checks are done on the validity of the address
    address = self.memory[0xFF]      # The return address
    self.ip = address                # Return!
    # No flags are updated

##########################
### Miscellaneous
##########################

@opcode(0x3E)
def opcode_NOP(self):
    print("Executing opcode: NOP")
    # No operation—just consume the cycle and return.
    pass


@opcode(0x3F)
def opcode_HLT(self):
    print("Executing opcode: HLT")
    # Just stop the machine. Flags are not touched
    self.halted = True
