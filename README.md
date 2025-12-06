# Emulador de ISA Mínima de Ponto Flutuante

Este projeto implementa uma **arquitetura mínima de ponto flutuante** e um **emulador em Python** capaz de executar pequenos programas em assembly para computação numérica:

- $\sin(x)$ via série de Taylor  
- $\cos(x)$ via série de Taylor  
- $x^{1/n}$ via método de Newton  
- $\log_b(x)$ via aproximação de $\ln$  

Tudo usando uma **ISA reduzida**, com apenas algumas instruções aritméticas, de memória e desvio condicional.

---

## 1. Estrutura do Projeto

```text
fp_isa_emulator/
├─ cpu.py                # Emulador da CPU e da ISA mínima
├─ main.py               # Programa principal com menu interativo
├─ programs/
│  ├─ sin.asm            # Cálculo de sin(x) por série de Taylor
│  ├─ cos.asm            # Cálculo de cos(x) por série de Taylor
│  ├─ root.asm           # Cálculo de x^(1/n) por Newton
│  └─ log.asm            # Cálculo de log_b(x) via ln(x)/ln(b)
└─ README.md             # Este arquivo
````

---

## 2. Visão Geral da Arquitetura

A arquitetura emulada é extremamente simples:

* **8 registradores de propósito geral** (`R0` a `R7`), todos `float`.
* **64 posições de memória** (`MEM[0]` a `MEM[63]`), também `float`.
* **Program Counter (`pc`)**: índice da instrução atual.
* **Flags de comparação**:

  * `flag_lt`: resultado de comparação `<`
  * `flag_eq`: resultado de comparação `==`
  * `flag_gt`: resultado de comparação `>`

A execução é feita em três etapas:

1. **Carregamento do programa** (`CPU.load_program`):

   * Lê o `.asm`.
   * Realiza **1ª passada**: descobre labels (rótulos).
   * Realiza **2ª passada**: monta a lista de instruções.

2. **Execução** (`CPU.run`):

   * Chama `step()` repetidamente até o PC sair do programa.

3. **Consulta de resultados**:

   * Por convenção, cada programa escreve o resultado em endereços fixos de memória (por exemplo, `MEM[10]`).

---

## 3. Conjunto de Instruções (ISA)

### 3.1. Registradores e Memória

* Registradores: `R0` a `R7`
* Memória: endereçada como `[0]`, `[1]`, ..., `[63]`

### 3.2. Instruções Suportadas

Todas as instruções operam com valores de ponto flutuante.

#### 3.2.1. Movimentação e constantes

* `SET Rd, imed`
  Coloca um valor imediato (float) em um registrador.

  ```asm
  SET R0, 1.0     ; R0 = 1.0
  ```

* `MOV Rd, Rs`
  Copia o valor de um registrador para outro.

  ```asm
  MOV R1, R0      ; R1 = R0
  ```

* `LOAD Rd, [addr]`
  Carrega da memória para um registrador.

  ```asm
  LOAD R0, [10]   ; R0 = MEM[10]
  ```

* `STORE Rs, [addr]`
  Armazena de um registrador na memória.

  ```asm
  STORE R0, [20]  ; MEM[20] = R0
  ```

#### 3.2.2. Aritmética

* `ADD Rd, Rs1, Rs2` → `Rd = Rs1 + Rs2`
* `SUB Rd, Rs1, Rs2` → `Rd = Rs1 - Rs2`
* `MUL Rd, Rs1, Rs2` → `Rd = Rs1 * Rs2`
* `DIV Rd, Rs1, Rs2` → `Rd = Rs1 / Rs2`

Exemplo:

```asm
ADD R2, R0, R1    ; R2 = R0 + R1
MUL R3, R2, R2    ; R3 = R2 * R2
```

#### 3.2.3. Comparação e Desvios

* `CMP Rs1, Rs2`
  Compara `Rs1` com `Rs2` e atualiza as flags internas:

  * `flag_lt = (Rs1 < Rs2)`
  * `flag_eq = (Rs1 == Rs2)`
  * `flag_gt = (Rs1 > Rs2)`

* `BZ label`
  Desvia para `label` se `flag_eq` for verdadeira.

* `BLT label`
  Desvia para `label` se `flag_lt` for verdadeira.

* `JMP label`
  Desvio incondicional para `label`.

Exemplo de loop:

```asm
SET  R0, 0.0

loop:
  ; ... faz algo ...
  CMP  R0, R1
  BLT  loop        ; volta se R0 < R1
```

---

## 4. Emulador (`cpu.py`)

O arquivo `cpu.py` contém a classe `CPU`, que faz o papel de “hardware emulado”.

### 4.1. Dois Passes no Carregamento

Método `load_program(asm_source: str)`:

1. **Primeira passada**: identifica labels.

   * Cada label é uma linha que termina com `:` (ex.: `loop:`).
   * O código conta apenas linhas de instrução (não conta labels) e registra:

     ```python
     self.labels["nome_do_label"] = indice_da_instrucao
     ```

2. **Segunda passada**: parse das instruções.

   * Remove comentários (`; ...`).
   * Troca vírgulas por espaços.
   * Separa opcode e argumentos (ex.: `("ADD", ["R0", "R1", "R2"])`).
   * Preenche `self.program` com a lista de instruções.

### 4.2. Execução

* `CPU.step()`:

  * Busca a instrução atual: `op, args = self.program[self.pc]`
  * Incrementa `pc`.
  * Executa a instrução e atualiza registradores/memória/flags.
  * Retorna `False` quando o `pc` sai do intervalo do programa (fim da execução).

* `CPU.run()`:

  * Simplesmente chama `step()` em loop até acabar.

---

## 5. Programa Principal (`main.py`)

O `main.py` fornece um **menu interativo** em modo texto:

```text
=== MENU ===
1 - sin(x)
2 - cos(x)
3 - x^(1/n) (raiz n-ésima)
4 - log_b(x)
0 - sair
```

Para cada opção, ele:

1. Lê os parâmetros numéricos do usuário (como `x`, `n`, número de termos/iterações).
2. Escreve os valores de entrada em posições específicas da memória da `CPU`.
3. Carrega o correspondente `.asm` da pasta `programs/`.
4. Executa o programa com `cpu.run()`.
5. Lê o resultado de `MEM[10]` (e outros, no caso do log).
6. Imprime:

   * Aproximação obtida pela ISA.
   * Valor real da função usando `math` do Python (para comparação).
7. Imprime o **estado final da CPU** (registradores e memória), via `dump_state(cpu)`.

### 5.1. Organização de Arquivos no `main.py`

O caminho dos programas é montado com `pathlib`:

```python
BASE_DIR = Path(__file__).resolve().parent
PROGRAMS_DIR = BASE_DIR / "programs"
```

E os `.asm` são abertos assim:

```python
prog_path = PROGRAMS_DIR / "sin.asm"
with open(prog_path, "r") as f:
    prog = f.read()
```

---

## 6. Programas em Assembly

Todos os programas seguem o mesmo padrão:

* Entradas em **endereços específicos da memória**.
* Resultado principal em `MEM[10]`.
* No caso de `log.asm`, também usa `MEM[11]` e `MEM[12]` para intermediários/resultados.

### 6.1. `sin.asm` – Série de Taylor para $\sin(x)$

Implementa:

$$
\sin(x) \approx \sum_{k=0}^{N-1} t_k
$$

com:

$$
t_0 = x, \qquad
t_{k+1} = -,t_k \cdot \frac{x^2}{(2k+2)(2k+3)}
$$

**Convenções de memória:**

* `MEM[0]` → $x$ (entrada).
* `MEM[1]` → $N$ (número de termos).
* `MEM[10]` → $\sin(x)$ aproximado (saída).

Trecho principal (simplificado):

```asm
LOAD R0, [0]        ; x
MUL  R1, R0, R0     ; x^2
MOV  R3, R0         ; term = x
MOV  R2, R0         ; result = x
SET  R4, 0.0        ; k = 0
SET  R7, 1.0
LOAD R6, [1]        ; N
; loop: soma N termos usando recorrência
...
STORE R2, [10]      ; resultado final
```

### 6.2. `cos.asm` – Série de Taylor para $\cos(x)$

Implementa:

$$
\cos(x) \approx \sum_{k=0}^{N-1} t_k
$$

com:

$$
t_0 = 1, \qquad
t_{k+1} = -,t_k \cdot \frac{x^2}{(2k+1)(2k+2)}
$$

**Convenções de memória:**

* `MEM[0]` → $x$ (entrada).
* `MEM[1]` → $N$ (número de termos).
* `MEM[10]` → $\cos(x)$ aproximado (saída).

### 6.3. `root.asm` – $x^{1/n}$ por Newton

Resolve:

$$
y = x^{1/n}
$$

Usando método de Newton para a equação:

$$
f(y) = y^n - x = 0
$$

A iteração usada é:

$$
y_{k+1} = \frac{1}{n}\left((n-1),y_k + \frac{x}{y_k^{n-1}}\right)
$$

**Convenções de memória:**

* `MEM[0]` → $x$ (entrada).
* `MEM[1]` → $n$ (ordem da raiz).
* `MEM[2]` → $N_{\text{iter}}$ (número de iterações).
* `MEM[10]` → $x^{1/n}$ aproximado (saída).

### 6.4. `log.asm` – $\log_b(x)$ via séries de $\ln$

Implementa:

$$
\log_b(x) = \frac{\ln(x)}{\ln(b)}
$$

Usando a expansão em série em torno de $z \approx 1$:

$$
\ln(z) = 2 \sum_{k=0}^{N-1} t_k
$$

com:

$$
t_0 = \frac{z-1}{z+1}, \qquad
t_{k+1} = t_k \cdot t^2 \cdot \frac{2k+1}{2k+3}, \qquad t = \frac{z-1}{z+1}
$$

A implementação faz:

1. Calcula $\ln(x)$ com $N$ termos: resultado em `MEM[10]`.
2. Calcula $\ln(b)$ com $N$ termos: resultado em `MEM[11]`.
3. Calcula $\log_b(x) = \ln(x) / \ln(b)$: resultado final em `MEM[12]`.

**Convenções de memória:**

* `MEM[0]` → $x$ (entrada).
* `MEM[1]` → $b$ (base).
* `MEM[2]` → $N_{\text{termos}}$ da série de $\ln$.
* `MEM[10]` → $\ln(x)$ aproximado.
* `MEM[11]` → $\ln(b)$ aproximado.
* `MEM[12]` → $\log_b(x)$ final.

---

## 7. Estados Finais: Dump de Registradores e Memória

Ao final de **cada** operação no `main.py`, é chamada a função:

```python
def dump_state(cpu: CPU):
    print("\n=== ESTADO FINAL DA CPU ===")
    print("Registradores:")
    for i, val in enumerate(cpu.reg):
        print(f"  R{i}: {val}")
    print("\nMemória:")
    for addr, val in enumerate(cpu.mem):
        print(f"  [{addr:02d}]: {val}")
    print("===========================\n")
```

Isso permite:

* Ver quais registradores foram usados para armazenar intermediários (por exemplo, $x^2$, termo atual da série, contador $k$, etc.).
* Conferir onde estão resultados parciais na memória.
* Usar essas informações no relatório para **explicar o fluxo da execução** da ISA.

---

## 8. Como Executar

### 8.1. Pré-requisitos

* Python 3.10+ (3.11/3.12 também funcionam).
* Nenhuma biblioteca externa além da padrão (`math`, `pathlib`, `typing`).

### 8.2. Passos

1. Certifique-se de que a estrutura de pastas está assim:

   ```text
   fp_isa_emulator/
   ├─ cpu.py
   ├─ main.py
   ├─ programs/
   │  ├─ sin.asm
   │  ├─ cos.asm
   │  ├─ root.asm
   │  └─ log.asm
   ```

2. Abra um terminal na pasta do projeto:

   ```bash
   cd caminho/para/fp_isa_emulator
   ```

3. Execute:

   ```bash
   python main.py
   ```

4. Escolha uma opção no menu e siga as instruções.

---

## 9. Exemplos de Uso

### 9.1. Seno

```text
=== MENU ===
1 - sin(x)
2 - cos(x)
3 - x^(1/n) (raiz n-ésima)
4 - log_b(x)
0 - sair
Escolha uma opção: 1
Digite x (radianos) para sin(x): 3.14159265
Número de termos da série de Taylor para sin(x) (>=1): 10

Usando 10 termo(s)
sin(3.14159265) ~ (valor aproximado)
valor real (math.sin): 0.0

=== ESTADO FINAL DA CPU ===
Registradores:
  R0: ...
  ...
Memória:
  [00]: 3.14159265
  [01]: 10.0
  [10]: (resultado da aproximação)
  ...
===========================
```

### 9.2. Raiz n-ésima

```text
Escolha uma opção: 3
Digite x (>0) para calcular x^(1/n): 16
Digite n (ex: 2 para raiz quadrada, 3 para cúbica): 2
Número de iterações de Newton (>=1): 5

Usando 5 iteração(ões) de Newton
16.0^(1/2.0) ~ 4.0
valor real (math.pow): 4.0
```

---

## 10. Possíveis Extensões

Algumas ideias de evolução do projeto:

* Adicionar **mais instruções** à ISA (por exemplo, `NEG`, `ABS`, `NOP`).
* Implementar **redução de argumento** para melhorar a precisão de $\sin$/$\cos$ para valores grandes.
* Adicionar **testes automatizados** em Python (por exemplo, testar diversos valores de $x$, $n$, $b$, $N$ e comparar erros).
* Gerar tabelas/gráficos de **erro relativo** em função de:

  * Número de termos/iterações.
  * Valor da entrada.

Essas extensões são boas para discutir trade-offs entre:

* simplicidade da arquitetura,
* tamanho dos programas em assembly,
* precisão numérica.