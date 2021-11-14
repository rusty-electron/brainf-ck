import sys

VALID_INS = ['>', '<', '+', '-', '.', ',', '[', ']']
MEM_LIMIT = 30000
CELL_MAX = 255

class BFMachine:
    def __init__(self, file_path):
        self.code = self.read_file(file_path)
        self.memory = [0] * MEM_LIMIT
        self.dp = 0 # data pointer
        self.ip = 0 # instruction pointer
        self.in_locs = []
        self.jump_lookup = {}

    def __str__(self):
        return "".join([_ for _ in self.code])

    def process_instruction(self, ins):
        if ins == '>':
            self.dp += 1
        elif ins == '<':
            self.dp -= 1
        elif ins == '+':
            self.memory[self.dp] += 1
            self.memory[self.dp] = self.memory[self.dp] % 255
        elif ins == '-':
            self.memory[self.dp] -= 1
            self.memory[self.dp] = self.memory[self.dp] % 255
        elif ins == '.':
            print(chr(self.memory[self.dp]), end='')
            # sys.stdout.write(chr(self.memory[self.dp]))
        elif ins == ',':
            try:
                self.memory[self.dp] = ord(input())
            except Exception:
                print('[ERROR] invalid input!')
                sys.exit(1)
            self.memory[self.dp] = self.memory[self.dp] % 255
        elif ins == '[':
            if self.memory[self.dp] == 0:
                self.ip = self.jump_lookup[self.ip]
        else: # ins == ']'
            if self.memory[self.dp] != 0:
                self.ip = self.inv_jump_lookup[self.ip]

        # ensure valid dp and ip locations
        if self.dp > MEM_LIMIT or self.dp < 0:
            # TODO: show unmatched char location, useful for debugging
            print(f"[ERROR] data pointer value: {self.dp} is out of bounds!")
            sys.exit(1)

    def interpret(self):
        if self.parentheses_match() == False:
            print(f"[ERROR] unmatched hard bracket instruction(s)")
            sys.exit(1)

        self.inv_jump_lookup = {v: k for k, v in self.jump_lookup.items()}

        while self.ip != len(self.code):
            current_ins = self.code[self.ip]
            self.process_instruction(current_ins)
            self.ip += 1

    def parentheses_match(self):
        input_string = self.code
        s = []
        balanced = True
        index = 0
        while index < len(input_string) and balanced:
            token = input_string[index]
            if token == "[":
                s.append(token)
                self.in_locs.append(index)
            elif token == "]":
                if len(s) == 0:
                    balanced = False
                else:
                    s.pop()
                    self.jump_lookup[self.in_locs[-1]] = index
                    self.in_locs.pop()

            index += 1
        return balanced and len(s) == 0

    def read_file(self, file_path):
        """
        reads the file according to the provided file path and then
        strips unrecognized symbols. returns a list of instructions
        """
        # open file and read all lines
        with open(file_path, 'r') as f:
            instruction_data = f.readlines()

        # remove
        instruction_string = "".join([line.strip("\n") for line in instruction_data])

        instruction_list = []
        illegal_count = 0 # keep count of illegal count because why not?
        for ch in instruction_string:
            if ch in VALID_INS: # ignore illegal characters in code
                instruction_list.append(ch)
            else:
                illegal_count += 1

        if illegal_count > 0:
            print(f"Found {illegal_count} illegal character(s)")
        return instruction_list

def main():
    m1 = BFMachine(sys.argv[1])
    m1.interpret()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main()
    else:
        if len(sys.argv) < 2:
            print("input script not provided!")
        else:
            print("too many arguments")
        # TODO: usage()
