.data
z: .word 0
x: .word 0
y: .word 0
.textli $t0, 1
add $sp, $sp -4
sw $t0 ($sp)li $t0, 2
add $sp, $sp -4
sw $t0 ($sp)lw $t0, ($sp)
mul $sp 4
lw $t1, (sp)
add $t2, $t1, $t0
sw $t2, ($sp)li $t0, 3
add $sp, $sp -4
sw $t0 ($sp)
lw $t0, ($sp)
add $sp, $sp, 4
lw $t1, ($sp)
add $t2, $t1, $t0
sw $t2, ($sp)
lw $t0 ($sp)
add $sp, $sp, 4
sw $t0, x
li $v0, 5
syscall
sw $v0, y
while0start: 
li $t0, 0
add $sp, $sp -4
sw $t0 ($sp)lw $t0, x
add $sp, $sp, -4
sw $t0, ($sp)
lw $t0 ($sp)
lw $t1 4($sp)
add $sp, $sp, 8
bgt $t0, $t1, while0lw $t0, x
add $sp, $sp, -4
sw $t0, ($sp)
lw $t0, ($sp)
mul $t1, $t0, -1
sw $t0, ($sp)
lw $t0, ($sp)
add $sp, $sp, 4
lw $t1, ($sp)
add $t2, $t1, $t0
sw $t2, ($sp)
lw $t0 ($sp)
add $sp, $sp, 4
sw $t0, xlw $t0, z
add $sp, $sp, -4
sw $t0, ($sp)lw $t0, y
add $sp, $sp, -4
sw $t0, ($sp)
lw $t0, ($sp)
add $sp, $sp, 4
lw $t1, ($sp)
add $t2, $t1, $t0
sw $t2, ($sp)
lw $t0 ($sp)
add $sp, $sp, 4
sw $t0, z
j while0start
while0end:
lw $t0, z
add $sp, $sp, -4
sw $t0, ($sp)li $t0, 1
add $sp, $sp -4
sw $t0 ($sp)
lw $t0 ($sp)
lw $t1 4($sp)
add $sp, $sp, 8
bgt $t0, $t1, if0
li $t0, 0
add $sp, $sp -4
sw $t0 ($sp)
li $v0, 1
lw $a0, ($sp)
syscall
add $sp, $sp, 4
if0:
li $t0, 0
add $sp, $sp -4
sw $t0 ($sp)lw $t0, z
add $sp, $sp, -4
sw $t0, ($sp)
lw $t0 ($sp)
lw $t1 4($sp)
add $sp, $sp, 8
bgt $t0, $t1, if1
lw $t0, z
add $sp, $sp, -4
sw $t0, ($sp)
li $v0, 1
lw $a0, ($sp)
syscall
add $sp, $sp, 4
if1: