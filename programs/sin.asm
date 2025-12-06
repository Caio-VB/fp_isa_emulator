LOAD R0, [0]
MUL  R1, R0, R0
MOV  R3, R0
MOV  R2, R0
SET  R4, 0.0
SET  R7, 1.0
LOAD R6, [1]

loop:
  MOV  R5, R6
  SUB  R5, R5, R7
  CMP  R4, R5
  BLT  do_term
  JMP  done

do_term:
  SET  R5, 2.0
  MUL  R5, R5, R4
  SET  R0, 2.0
  ADD  R5, R5, R0
  SET  R0, 1.0
  ADD  R0, R5, R0
  MUL  R5, R5, R0
  MUL  R3, R3, R1
  DIV  R3, R3, R5
  SET  R0, 0.0
  SUB  R3, R0, R3
  ADD  R2, R2, R3
  ADD  R4, R4, R7
  JMP  loop

done:
  STORE R2, [10]
