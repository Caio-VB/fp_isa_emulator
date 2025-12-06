from typing import List, Tuple, Dict

NUM_REGS = 8
MEM_SIZE = 64

class CPU:
    def __init__(self):
        # 8 registradores float
        self.reg: List[float] = [0.0] * NUM_REGS
        # 64 palavras de memória
        self.mem: List[float] = [0.0] * MEM_SIZE

        self.pc: int = 0           # índice da instrução
        self.flag_lt = False
        self.flag_eq = False
        self.flag_gt = False

        self.program: List[Tuple[str, List[str]]] = []
        self.labels: Dict[str, int] = {}

    # Carrega e monta o programa
    def load_program(self, asm_source: str):
        lines = asm_source.splitlines()

        # 1ª passada: descobrir labels -> posição (pc)
        pc = 0
        self.labels.clear()
        for line in lines:
            code = line.split(';')[0].strip()
            if not code:
                continue
            if code.endswith(':'):
                label = code[:-1].strip()
                if label in self.labels:
                    raise ValueError(f"Label duplicado: {label}")
                self.labels[label] = pc
            else:
                pc += 1

        # 2ª passada: parse das instruções
        self.program.clear()
        for line in lines:
            code = line.split(';')[0].strip()
            if not code or code.endswith(':'):
                continue
            parts = code.replace(',', ' ').split()
            op = parts[0].upper()
            args = parts[1:]
            self.program.append((op, args))

        self.pc = 0

    # Helpers de registrador/memória
    def reg_index(self, token: str) -> int:
        token = token.upper()
        if not token.startswith('R'):
            raise ValueError(f"Esperado registrador, obtive {token}")
        idx = int(token[1:])
        if not (0 <= idx < NUM_REGS):
            raise ValueError(f"Registrador inválido: {token}")
        return idx

    def addr_index(self, token: str) -> int:
        token = token.strip()
        if not (token.startswith('[') and token.endswith(']')):
            raise ValueError(f"Endereço inválido: {token}")
        addr = int(token[1:-1])
        if not (0 <= addr < MEM_SIZE):
            raise ValueError(f"Endereço fora da memória: {addr}")
        return addr

    # Executa 1 instrução
    def step(self) -> bool:
        if self.pc < 0 or self.pc >= len(self.program):
            return False  # fim do programa

        op, args = self.program[self.pc]
        self.pc += 1

        if op == 'SET':
            rd = self.reg_index(args[0])
            imm = float(args[1])
            self.reg[rd] = imm

        elif op == 'MOV':
            rd = self.reg_index(args[0])
            rs = self.reg_index(args[1])
            self.reg[rd] = self.reg[rs]

        elif op == 'LOAD':
            rd = self.reg_index(args[0])
            addr = self.addr_index(args[1])
            self.reg[rd] = self.mem[addr]

        elif op == 'STORE':
            rs = self.reg_index(args[0])
            addr = self.addr_index(args[1])
            self.mem[addr] = self.reg[rs]

        elif op in ('ADD', 'SUB', 'MUL', 'DIV'):
            rd = self.reg_index(args[0])
            rs1 = self.reg_index(args[1])
            rs2 = self.reg_index(args[2])
            a = self.reg[rs1]
            b = self.reg[rs2]
            if op == 'ADD':
                self.reg[rd] = a + b
            elif op == 'SUB':
                self.reg[rd] = a - b
            elif op == 'MUL':
                self.reg[rd] = a * b
            elif op == 'DIV':
                self.reg[rd] = a / b

        elif op == 'CMP':
            rs1 = self.reg_index(args[0])
            rs2 = self.reg_index(args[1])
            a = self.reg[rs1]
            b = self.reg[rs2]
            self.flag_lt = (a < b)
            self.flag_eq = (a == b)
            self.flag_gt = (a > b)

        elif op == 'BZ':
            label = args[0]
            if self.flag_eq:
                self.pc = self.labels[label]

        elif op == 'BLT':
            label = args[0]
            if self.flag_lt:
                self.pc = self.labels[label]

        elif op == 'JMP':
            label = args[0]
            self.pc = self.labels[label]

        else:
            raise ValueError(f"Opcode desconhecido: {op}")

        return True

    # Executa até o fim
    def run(self):
        while self.step():
            pass
