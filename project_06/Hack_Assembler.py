import re

DEST_MNEMONIC_TO_BITS = {
    None: '000',
    'M': '001',
    'D': '010',
    'MD': '011',
    'A': '100',
    'AM': '101',
    'AD': '110',
    'AMD': '111'
}

COMP_MNEMONIC_TO_BITS = {
    None: '',
    '0': '0101010',
    '1': '0111111',
    '-1': '0111010',
    'D': '0001100',
    'A': '0110000',
    'M': '1110000',
    '!D': '0001101',
    '!A': '0110001',
    '!M': '1110001',
    '-D': '0001111',
    '-A': '0110011',
    '-M': '1110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'M+1': '1110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'M-1': '1110010',
    'D+A': '0000010',
    'D+M': '1000010',
    'D-A': '0010011',
    'D-M': '1010011',
    'A-D': '0000111',
    'M-D': '1000111',
    'D&A': '0000000',
    'D&M': '1000000',
    'D|A': '0010101',
    'D|M': '1010101'
}

JUMP_MNEMONIC_TO_BITS = {
    None: '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
}

PREDEFINED_SYMBOLS = {
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SCREEN': 16384,
    'KBD': 24576
}


def cleaned_line(line):
    line = line.strip()
    line = line.split('//')[0].strip()
    return line


def parser(input_lines, symbol_table):
    num_instr = 0
    for line in input_lines:
        line = cleaned_line(line)
        if not line:
            continue
        elif line.startswith('(') and line.endswith(')'):
            label = line[1:-1]
            symbol_table[label] = num_instr
        else:
            num_instr += 1


def translator(input_lines, output_file, symbol_table):
    char_only_matcher = re.compile('[a-zA-Z]+')
    next_available_address = 16
    for line in input_lines:
        line = cleaned_line(line)
        if not line:
            continue
        elif line.startswith('@'):
            symbol = line[1:]
            not_number = char_only_matcher.match(symbol)

            if not_number:
                if symbol in symbol_table:
                    address = symbol_table[symbol]
                else:
                    symbol_table[symbol] = next_available_address
                    next_available_address += 1

            else:
                address = int(symbol)

            machine_code = '{0:016b}'.format(address)

        else:
            dest_bits = DEST_MNEMONIC_TO_BITS.get(dest_mnemonic(line), '000')
            comp_bits = COMP_MNEMONIC_TO_BITS.get(comp_mnemonic(line), '')
            jump_bits = JUMP_MNEMONIC_TO_BITS.get(jump_mnemonic(line), '000')
            machine_code = f"111{comp_bits}{dest_bits}{jump_bits}"

        if len(machine_code) == 16:
            output_file.write(f"{machine_code}\n")


def dest_mnemonic(line):
    if '=' in line:
        return line.split('=')[0]


def comp_mnemonic(line):
    if '=' in line:
        return line.split('=')[1]
    elif ';' in line:
        return line.split(';')[0]


def jump_mnemonic(line):
    if ';' in line:
        return line.split(';')[1]


def main():
    with open("Input.asm", 'r') as input_file:
        input_lines = input_file.readlines()

        output_file_name = "Output.hack"
        with open(output_file_name, 'w') as output_file:
            symbol_table = dict(PREDEFINED_SYMBOLS)
            parser(input_lines, symbol_table)
            translator(input_lines, output_file, symbol_table)


if __name__ == "__main__":
    main()
