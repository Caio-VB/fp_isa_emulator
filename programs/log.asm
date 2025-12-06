LOAD R6, [2]
STORE R6, [42]
SET  R7, 1.0
LOAD R0, [0]
SET  R1, 1.0
SUB  R1, R0, R1
SET  R2, 1.0
ADD  R2, R0, R2
DIV  R3, R1, R2
STORE R3, [40]
MUL  R3, R3, R3
STORE R3, [41]
LOAD R0, [40]
SET  R1, 0.0
SET  R2, 0.0

lnx_loop:
  ADD  R1, R1, R0
  LOAD R6, [42]
  SUB  R6, R6, R7
  CMP  R2, R6
  BLT  lnx_next
  JMP  lnx_done

lnx_next:
  LOAD R5, [41]
  SET  R3, 2.0
  MUL  R3, R3, R2
  ADD  R3, R3, R7
  MOV  R4, R3
  SET  R6, 2.0
  ADD  R4, R4, R6
  DIV  R3, R3, R4
  MUL  R0, R0, R5
  ; term *= ratio
  MUL  R0, R0, R3
  ADD  R2, R2, R7
  JMP  lnx_loop

lnx_done:
  SET  R3, 2.0
  MUL  R1, R1, R3
  STORE R1, [10]

LOAD R0, [1]
SET  R1, 1.0
SUB  R1, R0, R1
SET  R2, 1.0
ADD  R2, R0, R2
DIV  R3, R1, R2
STORE R3, [40]
MUL  R3, R3, R3
STORE R3, [41]
LOAD R0, [40]
SET  R1, 0.0
SET  R2, 0.0

lnb_loop:
  ADD  R1, R1, R0
  LOAD R6, [42]
  SUB  R6, R6, R7
  CMP  R2, R6
  BLT  lnb_next
  JMP  lnb_done

lnb_next:
  ; carrega t^2
  LOAD R5, [41]
  SET  R3, 2.0
  MUL  R3, R3, R2
  ADD  R3, R3, R7
  MOV  R4, R3
  SET  R6, 2.0
  ADD  R4, R4, R6
  DIV  R3, R3, R4
  MUL  R0, R0, R5
  MUL  R0, R0, R3
  ADD  R2, R2, R7
  JMP  lnb_loop

lnb_done:
  SET  R3, 2.0
  MUL  R1, R1, R3
  STORE R1, [11]

LOAD R0, [10]
LOAD R1, [11]
DIV  R2, R0, R1
STORE R2, [12]
