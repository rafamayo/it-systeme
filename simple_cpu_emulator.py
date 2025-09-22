class SimpleCPUEmulator:

    # Fixed class-level dispatch table. Shared by all instances of the SimpleCPUEmulator
    dispatch_table = {}
    
    @classmethod
    def opcode(cls, code):
        def decorator(func):
            cls.dispatch_table[code] = func
            return func
        return decorator


    def __init__(self):
        self.memory = [0] * 256 # Assuming 256 memory locations
        self.ip = 0             # The instruction pointer
        
        # The general purpose registers
        self.register_A = 0
        self.register_B = 0
        self.register_C = 0

        # The flags
        self.flag_Z = False
        self.flag_S = False
        self.flag_V = False
        self.flag_C = False
        
        # Controling the machine
        self.halted = False
        self.step_by_step = False

    def read_into_memory(self, program, start_address=0x00):
        """Load a list of byte-values into memory at the given start address."""
        end = start_address + len(program)
        if end > len(self.memory):
            raise ValueError(f"Program (size {len(program)}) exceeds memory bounds at {start_address:02X}.")
        # Copy program bytes in; leave the rest untouched
        for offset, byte in enumerate(program):
            self.memory[start_address + offset] = byte

    def memory_dump(self, start=0x00, end=None):
        """Print a formatted hex dump of memory from start to end (exclusive)."""
        if end is None or end > len(self.memory):
            end = len(self.memory)
        lines = []
        for addr in range(start, end, 16):
            chunk = self.memory[addr:addr+16]
            hex_bytes = ' '.join(f"{b:02X}" for b in chunk)
            lines.append(f"{addr:02X}: {hex_bytes}")
        print("\n".join(lines))
    
    # Updating the flags after executing an ALU operation
    def update_flags(self, total, result, op1, op2):
        
        self.flag_Z = 1 if result == 0 else 0
        self.flag_S = 1 if (result & 0x80) != 0 else 0
        self.flag_C = 1 if total > 0xFF else 0

        msb_op1 = (op1 & 0x80) >> 7
        msb_op2 = (op2 & 0x80) >> 7
        msb_result = (result & 0x80) >> 7
        self.flag_V = 1 if (msb_op1 == msb_op2 and msb_result != msb_op1) else 0

    # Displaying the current state of the machine
    def display_current_state(self):
        # Format registers as two-digit hex values
        registers = f"A: {self.register_A:02X}  B: {self.register_B:02X}  C: {self.register_C:02X}"
    
        # Format flags as 0 or 1 (assuming flags are booleans; otherwise, adjust accordingly)
        flags = f"Z: {int(self.flag_Z)}  S: {int(self.flag_S)}  V: {int(self.flag_V)}  C: {int(self.flag_C)}"
    
        # Format the memory content at the current program counter as a two-digit hex value
        #memory_content = f"{self.memory[self.ip]:02X}"
    
        # Print the formatted output
        print(f"Instruction pointer: {self.ip:02X}")
        print(f"Registers: {registers}")
        print(f"Flags:     {flags}")
        # later don't use len, memory size will be fixed
        if(self.ip) < len(self.memory):
            print(f"Memory Content at IP ({self.ip:02X}): {self.memory[self.ip]:02X}")
        else:
            print(f"Reached end of Memory!")

    # Running the program
    def run(self):
        ans = input("Run step-by-step? (y/N) ").strip().lower()
        if ans == 'y':
            self.run_step_by_step()
        else:
            self.run_full()
    
    def run_full(self):
        while not self.halted and 0 <= self.ip < len(self.memory):
            opcode = self.memory[self.ip]
            self.ip += 1

            operation = self.dispatch_table.get(opcode)
            if operation is None:
                raise Exception(f"Invalid opcode @ {self.ip-1:02X}: {opcode:02X}")
            operation(self)

    def run_step_by_step(self):
        # step loop
        while not self.halted and 0 <= self.ip < len(self.memory):
            opcode = self.memory[self.ip]
            self.ip += 1
            operation = self.dispatch_table.get(opcode)
            if operation is None:
                raise Exception(f"Invalid opcode @ {self.ip-1:02X}: {opcode:02X}")
            operation(self)

            # show state
            self.display_current_state()

            # interactive menu
            while True:
                print("\nOptions: [N]ext  [R]un to end  [D]ump memory  [I]nspect addr  [W]rite addr")
                choice = input("Choice (default N): ").strip().lower() or 'n'
                if choice == 'n':
                    # do one more step
                    break
                elif choice == 'r':
                    # finish the program in full
                    self.run_full()
                    return
                elif choice == 'd':
                    self.memory_dump()
                elif choice == 'i':
                    addr_s = input("  Address (hex or dec)? ")
                    try:
                        addr = int(addr_s, 0)
                        if 0 <= addr < len(self.memory):
                            print(f"  [{addr:02X}] = {self.memory[addr]:02X}")
                        else:
                            print("  >> out of range")
                    except ValueError:
                        print("  >> bad number")
                elif choice == 'w':
                    addr_s = input("  Address (hex or dec)? ")
                    val_s  = input("  New value (hex or dec)? ")
                    try:
                        addr = int(addr_s, 0)
                        val  = int(val_s, 0) & 0xFF
                        if 0 <= addr < len(self.memory):
                            self.memory[addr] = val
                            print(f"  Wrote {val:02X} to [{addr:02X}]")
                        else:
                            print("  >> address out of range")
                    except ValueError:
                        print("  >> bad input")
                else:
                    print("  >> unknown option")
        print("Execution finished.")

import opcodes
