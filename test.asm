.data
y: .word 0
x: .word 0
z: .word 0
.text
li $t0, 4
sw $t0 ($sp)
add $sp, $sp, 4
sw $t0, x
li $v0, 5
syscall
li $t0, 5
add $a0, $t0, $v0
li $v0, 1
syscall
