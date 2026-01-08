# Assemble and execute
# "Usage: python.py <asm_file.asm>"

import sys
from simple_assembler import SimpleAssembler
from simple_cpu_emulator import SimpleCPUEmulator

def read_asm_file(filename):
    """Reads an assembler file and returns its content, ignoring lines starting with #."""
    with open(filename, 'r') as f:
        lines = f.readlines()
    # Filter out comment lines and strip whitespace
    asm_program = [line.strip() for line in lines if not line.strip().startswith('#')]
    return '\n'.join(asm_program)

def main():
    # check that a file name was provided!
    if len(sys.argv) < 2:
        print("Usage: python.py <asm_file.asm>")
        sys.exit(1)

    asm_file = sys.argv[1]

    # Read in the assembler file
    try:
        asm_program = read_asm_file(asm_file)
    except FileNotFoundError:
        print(f"Error: File '{asm_file}' not found.")
        sys.exit(1)


    print("Assembler program:")
    print(asm_program)

    assembler = SimpleAssembler()
    mc_program, mc_listing = assembler.assemble_with_listing(asm_program)
    
    print("Machine code listing:")
    print(mc_listing)
    print("Machine code program:")
    print(mc_program)

    emulator = SimpleCPUEmulator()

    emulator.read_into_memory(mc_program)

    print(f"Initial state:")
    emulator.display_current_state()

    emulator.run()

    print(f"Final state:")
    emulator.display_current_state()
    emulator.memory_dump()

if __name__ == "__main__":
    main()
