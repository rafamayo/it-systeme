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
        """
        Assemble and return (machine_bytes, listing_text).
        - machine_bytes: List[int] (pretty-print as 0xHH if printed)
        - listing_text:  A human-readable listing with addresses and comments
        """
        lines = self._normalize_source(source)

        # First pass: compute addresses for labels; also classify lines
        labels = {}
        addr = 0
        classified = []  # list of dicts with type: 'label'|'instr'|'data'
        for entry in lines:
            code = entry["code"]
            if not code:
                continue
            if code.endswith(':'):
                label_name = code[:-1].strip().upper()
                labels[label_name] = addr
                classified.append({**entry, "type": "label", "name": label_name})
            else:
                # instruction or data?
                try:
                    inst, operand = self._split_mnemonic(code)
                    _, length, _ = self.OPCODES[inst]
                    classified.append({**entry, "type": "instr", "inst": inst, "operand": operand})
                    addr += length
                except ValueError:
                    # must be a data byte literal
                    try:
                        int(code, 0)
                    except ValueError:
                        raise ValueError(f"Line not instruction or data: {entry['raw']!r}")
                    classified.append({**entry, "type": "data"})
                    addr += 1

        # Second pass: emit bytes + build listing
        machine = []
        listing_lines = []
        addr = 0
        pending_label_comment = None  # attach label's comment to the very next data byte if that data line has none

        for entry in classified:
            t = entry["type"]
            if t == "label":
                pending_label_comment = entry["comment"] or None
                continue

            if t == "data":
                val = int(entry["code"], 0)
                if not (0 <= val <= 0xFF):
                    raise ValueError(f"Data byte out of range: {entry['raw']!r}")
                machine.append(self._HexInt(val))
                comment = entry["comment"] or pending_label_comment or ""
                listing_lines.append(f"{addr:02X}: 0x{val:02X}" + (f" ; {comment}" if comment else ""))
                addr += 1
                pending_label_comment = None
                continue

            # instruction
            inst = entry["inst"]
            operand_text = entry["operand"]
            opcode, length, mode = self.OPCODES[inst]

            # Emit opcode byte (comment attached to the opcode line)
            machine.append(self._HexInt(opcode))
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

                machine.append(self._HexInt(val))
                # Typically no comment on the operand byte line (to match your example)
                listing_lines.append(f"{addr:02X}: 0x{val:02X}")
                addr += 1

            # labels' pending comment does NOT apply to instructions; only to subsequent data
            pending_label_comment = None

        return list(machine), "\n".join(listing_lines)
