# Test the simple CPU emulator
from simple_assembler import SimpleAssembler
from simple_cpu_emulator import SimpleCPUEmulator

asm_program = """
    LDA x			; Load the value at address x into register A
    LDB y			; Load the value at address y into register B
    SUB B			; Perform the subtraction A = A - B
    CMA				; Complement A
    JS positiv		; Jump if sign flag is set (A>=B)
    STA d			; Store the value in register A to address d
    HLT				; Stop the program
    positiv:
    CMA				; Complement A
    STA d			; Store the value in register A to address d
    HLT				; Stop the program
    x:				; First number
    0x0A
    y:				; Second number
    0x03
    d:				; Result
    0x00
"""

print(asm_program)

assembler = SimpleAssembler()
mc_program, mc_listing = assembler.assemble_with_listing(asm_program)
print(mc_listing)
print(mc_program)

emulator = SimpleCPUEmulator()

emulator.read_into_memory(mc_program)

print(f"Initial state:")
emulator.display_current_state()

emulator.run()

print(f"Final state:")
emulator.display_current_state()
emulator.memory_dump()
