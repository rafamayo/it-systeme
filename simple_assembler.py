class SimpleAssembler:
    # mnemonic → (opcode_byte, length_in_bytes, mode)
    # mode: "none"=no operand, "imm"=immediate literal, "addr"=label/address
    OPCODES = {
        "ADD B": (0x02, 1, "none"),
        "ADD C": (0x03, 1, "none"),
        "ADC B": (0x04, 1, "none"),
        "SUB B": (0x05, 1, "none"),
        "SUB C": (0x06, 1, "none"),
        "SUC B": (0x07, 1, "none"),
        "CMP":   (0x08, 1, "none"),
        "INR A": (0x09, 1, "none"),
        "INR B": (0x0A, 1, "none"),
        "INR C": (0x0B, 1, "none"),
        "DCR A": (0x0C, 1, "none"),
        "DCR B": (0x0D, 1, "none"),
        "DCR C": (0x0E, 1, "none"),

        "ANA B": (0x0F, 1, "none"),
        "ANA C": (0x10, 1, "none"),
        "TST":   (0x11, 1, "none"),
        "ORA B": (0x12, 1, "none"),
        "ORA C": (0x13, 1, "none"),
        "XRA B": (0x14, 1, "none"),
        "XRA C": (0x15, 1, "none"),
        "CMA":   (0x16, 1, "none"),
        "ANI":   (0x17, 2, "imm"),
        "ORI":   (0x18, 2, "imm"),
        "XRI":   (0x19, 2, "imm"),

        "MOV A,B": (0x1A, 1, "none"),
        "MOV A,C": (0x1B, 1, "none"),
        "MOV B,A": (0x1C, 1, "none"),
        "MOV B,C": (0x1D, 1, "none"),
        "MOV C,A": (0x1E, 1, "none"),
        "MOV C,B": (0x1F, 1, "none"),

        "MVI A": (0x20, 2, "imm"),
        "MVI B": (0x21, 2, "imm"),
        "MVI C": (0x22, 2, "imm"),

        "LDA":   (0x23, 2, "addr"),
        "LDB":   (0x24, 2, "addr"),
        "LDC":   (0x25, 2, "addr"),
        "STA":   (0x26, 2, "addr"),
        "LDA C": (0x29, 1, "none"),
        "STA C": (0x2A, 1, "none"),

        "JMP":   (0x2B, 2, "addr"),
        "JS":    (0x2C, 2, "addr"),
        "JZ":    (0x2D, 2, "addr"),
        "JC":    (0x2E, 2, "addr"),
        "JV":    (0x2F, 2, "addr"),

        "CALL":  (0x30, 2, "addr"),
        "RET":   (0x31, 1, "none"),
        "NOP":   (0x3E, 1, "none"),
        "HLT":   (0x3F, 1, "none"),
 
        "ORG": (None, 0, "imm"),  # Setzt die aktuelle Adresse (kein Machine Code)
        "DB":  (None, 1, "imm"),  # Platziert Bytes ab der aktuellen Adresse
    }

    # Pretty-print ints as 0xHH when you print the list, while staying real ints.
    class _HexInt(int):
        def __repr__(self):
            return f"0x{self:02X}"

    def _split_mnemonic(self, line):
        """
        Return (mnemonic_key, operand_text) by matching longest key.
        Case-insensitive; commas normalized.
        """
        code = line.split(';', 1)[0].strip().upper()
        code = code.replace(', ', ',').replace(' ,', ',')
        for key in sorted(self.OPCODES.keys(), key=len, reverse=True):
            if code.startswith(key):
                rest = code[len(key):].strip()
                return key, rest
        raise ValueError(f"Unknown instruction in line: {line!r}")

    def _normalize_source(self, source):
        """Return list of dicts: [{'raw','code','comment'}] preserving comments."""
        if isinstance(source, str):
            lines = source.splitlines()
        else:
            lines = source
        out = []
        for raw in lines:
            code, sep, comment = raw.partition(';')
            code = code.rstrip()
            comment = comment.strip() if sep else ""
            # keep empty code lines only if they carry a standalone comment? (skip here)
            if code.strip() or comment:  # we only keep non-empty code (comments kept attached)
                out.append({"raw": raw, "code": code.strip(), "comment": comment})
        return out

    def assemble(self, source):
        """Assemble and return the raw integer bytes (for the emulator)."""
        machine, _listing = self.assemble_with_listing(source)
        return machine

    def assemble_with_listing(self, source):
        lines = self._normalize_source(source)

        # First pass: compute addresses for labels; also classify lines
        labels = {}
        addr = 0
        classified = []
        max_addr = 0  # Track the maximum address used
        current_org_addr = 0

        for entry in lines:
            code = entry["code"]
            if not code:
                continue

            if code.upper().startswith("ORG"):
                operand = code[3:].strip()
                try:
                    org_addr = int(operand, 0)
                except ValueError:
                    raise ValueError(f"Invalid address for ORG: {operand!r}")
                classified.append({**entry, "type": "org", "addr": org_addr})
                current_org_addr = org_addr
                max_addr = max(max_addr, org_addr)
                continue

            if code.upper().startswith("DB"):
                operands = [op.strip() for op in code[2:].split(",")]
                db_addr = current_org_addr + len(operands) - 1  # Letzte Adresse, die durch DB belegt wird
                max_addr = max(max_addr, db_addr)
                classified.append({**entry, "type": "db", "operands": operands})
                continue

            if code.endswith(':'):
                label_name = code[:-1].strip().upper()
                labels[label_name] = addr
                classified.append({**entry, "type": "label", "name": label_name})
                continue

            try:
                inst, operand = self._split_mnemonic(code)
                _, length, _ = self.OPCODES[inst]
                classified.append({**entry, "type": "instr", "inst": inst, "operand": operand})
                addr += length
                max_addr = max(max_addr, addr - 1)  # Aktualisiere max_addr auf die letzte verwendete Adresse
            except ValueError:
                try:
                    int(code, 0)
                except ValueError:
                    raise ValueError(f"Line not instruction or data: {entry['raw']!r}")
                classified.append({**entry, "type": "data"})
                addr += 1
                max_addr = max(max_addr, addr - 1)  # Aktualisiere max_addr auf die letzte verwendete Adresse

        # Second pass: emit bytes + build listing
        machine = [None] * (max_addr + 1)  # Initialize with enough space
        listing_lines = []
        addr = 0
        pending_label_comment = None
        current_org_addr = 0

        for entry in classified:
            t = entry["type"]

            if t == "org":
                current_org_addr = entry["addr"]
                addr = current_org_addr
                continue

            if t == "label":
                pending_label_comment = entry["comment"] or None
                continue

            if t == "db":
                for val_str in entry["operands"]:
                    val = int(val_str, 0)
                    if not (0 <= val <= 0xFF):
                        raise ValueError(f"Data byte out of range: {val_str!r}")
                    machine[addr] = self._HexInt(val)
                    comment = entry["comment"] or ""
                    listing_lines.append(f"{addr:02X}: 0x{val:02X}" + (f" ; {comment}" if comment else ""))
                    addr += 1
                continue

            if t == "data":
                val = int(entry["code"], 0)
                if not (0 <= val <= 0xFF):
                    raise ValueError(f"Data byte out of range: {entry['raw']!r}")
                machine[addr] = self._HexInt(val)
                comment = entry["comment"] or pending_label_comment or ""
                listing_lines.append(f"{addr:02X}: 0x{val:02X}" + (f" ; {comment}" if comment else ""))
                addr += 1
                pending_label_comment = None
                continue

            if t == "instr":
                inst = entry["inst"]
                operand_text = entry["operand"]
                opcode, length, mode = self.OPCODES[inst]

                machine[addr] = self._HexInt(opcode)
                comment = entry["comment"] or ""
                listing_lines.append(f"{addr:02X}: 0x{opcode:02X}" + (f" ; {comment}" if comment else ""))
                addr += 1

                if length == 2:
                    if not operand_text:
                        raise ValueError(f"Missing operand for '{inst}'")

                    if mode == "imm":
                        try:
                            val = int(operand_text, 0)
                        except ValueError:
                            raise ValueError(f"Immediate expected for '{inst}', got: {operand_text!r}")
                    else:  # addr mode
                        if operand_text in labels:
                            val = labels[operand_text]
                        else:
                            try:
                                val = int(operand_text, 0)
                            except ValueError:
                                raise ValueError(f"Label/address expected for '{inst}', got: {operand_text!r}")

                    if not (0 <= val <= 0xFF):
                        raise ValueError(f"Operand out of range for '{inst}': {operand_text!r}")

                    machine[addr] = self._HexInt(val)
                    listing_lines.append(f"{addr:02X}: 0x{val:02X}")
                    addr += 1

            pending_label_comment = None

        # Filter out None values and replace them with 0x00
        machine = [byte if byte is not None else 0x00 for byte in machine]

        return list(machine), "\n".join(listing_lines)
