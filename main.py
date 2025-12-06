import math
from pathlib import Path
from cpu import CPU   # importa a classe do outro arquivo

# pasta base = pasta onde está este arquivo main.py
BASE_DIR = Path(__file__).resolve().parent
PROGRAMS_DIR = BASE_DIR / "programs"


def dump_state(cpu: CPU):
    print("\n=== ESTADO FINAL DA CPU ===")
    print("Registradores:")
    for i, val in enumerate(cpu.reg):
        print(f"  R{i}: {val}")
    print("\nMemória:")
    for addr, val in enumerate(cpu.mem):
        print(f"  [{addr:02d}]: {val}")
    print("===========================\n")


def run_sin():
    cpu = CPU()
    x = float(input("Digite x (radianos) para sin(x): "))
    n_terms = int(input("Número de termos da série de Taylor para sin(x) (>=1): "))

    if n_terms < 1:
        n_terms = 1  # evita zero ou negativo

    cpu.mem[0] = x               # x
    cpu.mem[1] = float(n_terms)  # N termos

    prog_path = PROGRAMS_DIR / "sin.asm"
    with open(prog_path, "r") as f:
        prog = f.read()

    cpu.load_program(prog)
    cpu.run()

    aprox = cpu.mem[10]
    print(f"\nUsando {n_terms} termo(s)")
    print(f"sin({x}) ~ {aprox}")
    print(f"valor real (math.sin): {math.sin(x)}\n")

    dump_state(cpu)


def run_cos():
    cpu = CPU()
    x = float(input("Digite x (radianos) para cos(x): "))
    n_terms = int(input("Número de termos da série de Taylor para cos(x) (>=1): "))

    if n_terms < 1:
        n_terms = 1

    cpu.mem[0] = x
    cpu.mem[1] = float(n_terms)

    prog_path = PROGRAMS_DIR / "cos.asm"
    with open(prog_path, "r") as f:
        prog = f.read()

    cpu.load_program(prog)
    cpu.run()

    aprox = cpu.mem[10]
    print(f"\nUsando {n_terms} termo(s)")
    print(f"cos({x}) ~ {aprox}")
    print(f"valor real (math.cos): {math.cos(x)}\n")

    dump_state(cpu)


def run_root():
    cpu = CPU()
    x = float(input("Digite x (>0) para calcular x^(1/n): "))
    n = float(input("Digite n (ex: 2 para raiz quadrada, 3 para cúbica): "))
    n_iter = int(input("Número de iterações de Newton (>=1): "))

    if n_iter < 1:
        n_iter = 1

    cpu.mem[0] = x               # x
    cpu.mem[1] = n               # n
    cpu.mem[2] = float(n_iter)   # N iterações

    prog_path = PROGRAMS_DIR / "root.asm"
    with open(prog_path, "r") as f:
        prog = f.read()

    cpu.load_program(prog)
    cpu.run()

    aprox = cpu.mem[10]
    print(f"\nUsando {n_iter} iteração(ões) de Newton")
    print(f"{x}^(1/{n}) ~ {aprox}")
    print(f"valor real (math.pow): {math.pow(x, 1.0/n)}\n")

    dump_state(cpu)


def run_log():
    cpu = CPU()
    x = float(input("Digite x (>0) para log_b(x): "))
    b = float(input("Digite b (>0, !=1) base do log: "))
    n_terms = int(input("Número de termos da série para ln (>=1): "))

    if n_terms < 1:
        n_terms = 1

    cpu.mem[0] = x                # x
    cpu.mem[1] = b                # b
    cpu.mem[2] = float(n_terms)   # N termos

    prog_path = PROGRAMS_DIR / "log.asm"
    with open(prog_path, "r") as f:
        prog = f.read()

    cpu.load_program(prog)
    cpu.run()

    ln_x  = cpu.mem[10]
    ln_b  = cpu.mem[11]
    logbx = cpu.mem[12]

    print(f"\nUsando {n_terms} termo(s) da série para ln")
    print(f"ln({x}) (aprox)  ~ {ln_x}")
    print(f"ln({b}) (aprox)  ~ {ln_b}")
    print(f"log_{b}({x}) ~ {logbx}")
    print(f"valor real (math.log(x, b)): {math.log(x, b)}\n")

    dump_state(cpu)


if __name__ == "__main__":
    while True:
        print("=== MENU ===")
        print("1 - sin(x)")
        print("2 - cos(x)")
        print("3 - x^(1/n) (raiz n-ésima)")
        print("4 - log_b(x)")
        print("0 - sair")
        opc = input("Escolha uma opção: ").strip()

        if opc == "0":
            print("Saindo...")
            break
        elif opc == "1":
            run_sin()
        elif opc == "2":
            run_cos()
        elif opc == "3":
            run_root()
        elif opc == "4":
            run_log()
        else:
            print("Opção inválida.\n")
