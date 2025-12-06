LOAD R0, [0]
LOAD R1, [1]
LOAD R5, [2]
SET  R2, 1.0
SET  R7, 1.0
SUB  R3, R1, R7
SET  R4, 0.0

iter_loop:
  CMP  R4, R5
  BLT  do_iter
  JMP  done

do_iter:
  MOV  R6, R2
  SET  R7, 1.0

pow_loop:
  CMP  R7, R3
  BLT  pow_body
  JMP  pow_done

pow_body:
  MUL  R6, R6, R2
  SET  R0, 1.0
  ADD  R7, R7, R0
  JMP  pow_loop

pow_done:
  LOAD R0, [0]
  DIV  R0, R0, R6
  MUL  R6, R3, R2
  ADD  R6, R6, R0
  DIV  R2, R6, R1
  SET  R0, 1.0
  ADD  R4, R4, R0
  JMP  iter_loop

done:
  STORE R2, [10]
