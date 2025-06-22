# FeASM - Incredibly simple assembler for x86 written in Python3
# Designed to generate bootable BIOS applications
# Converts bits to bytes, then writes boot signature and saves to file

import sys

# Function to convert bits to hexadecimal bytes
def bits_to_bytes(bits_string):
    return bytes(int(bits_string[i:i+8], 2) for i in range(0, len(bits_string), 8))

# Function to parse command-line arguments
def parse_arguments():
    try:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]

    # Handle IndexError
    except IndexError:
        print(f"Usage: python3 {sys.argv[0]} <input_file> <output_file>")
        sys.exit(1)

    # Return input and output filenames
    return input_filename, output_filename

# Function to parse input file
def parse_input_file(filename):
    bits_string = ""

    with open(filename, "r") as file:

        # Iterate over lines in the file
        for line in file:

            # Ignore comments
            if line.startswith("#"):
                continue

            # append to output
            bits_string += line

    # Strip output for spaces and newlines
    bits_string = bits_string.replace(" ", "").replace("\n", "")

    # Return output
    return bits_string

# Function to generate a BIOS-compliant boot sector from x86 machine code bits
def generate_boot_sector(bits_string):
    # Pad to 510 bytes
    while len(bits_string) < 510 * 8:
        bits_string += '00000000'

    # Append boot signature: 0x55AA
    bits_string += '01010101'  # 0x55
    bits_string += '10101010'  # 0xAA

    # Return bits string
    return bits_string

# Program entrypoint
def main():
    # Get command-line arguments
    input_file, output_file = parse_arguments()

    # Parse input file
    bits_string = parse_input_file(input_file)

    # Generate boot sector
    boot_sector_bits = generate_boot_sector(bits_string)

    # Convert boot sector bits to bytes
    boot_sector_bytes = bits_to_bytes(boot_sector_bits)

    # Write boot sector bytes to output file
    with open(output_file, "wb") as file:
        file.write(boot_sector_bytes)

    # Exit with error code 0
    sys.exit(0)

if __name__ == "__main__":
    try:
        main()

    except Exception as error:
        print(f"An error occurred: {error}")
        sys.exit(1)

