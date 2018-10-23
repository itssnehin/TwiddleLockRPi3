/***************************************************************

Insertion sort algorithm using ARM Assembly

****************************************************************/

.text
.global main

main:

	@ Initialize
	ldr r7, =result				@ save
	str lr, [r7]				@ link register for result
	mov r6, #0				@ counter in r6
	ldr r4, =array				@ constant array in r4

inputloop:

	ldr r0, =prompt
	bl puts

	ldr r0, =FormatScan @ r0 <- &scan format
	ldr r1, =number @ r1 <- &number
	bl scanf @ call to scanf

	ldr r1, =number
	ldr r1, [r1]
	cmp r1, #0 @ look for sentinal (negative)
	blt isort @ goto isort function

	add r0, r4, r6, LSL #2 @ r0 <- &array[4*count]
	str r1, [r0] @ array[4*count] <- number
	add r6, r6, #1 @ count = count + 1

	b inputloop


isort:   @ Implement a double loop (forand while)
	mov r0, r4 @ r0 <- &array (a)
	mov r1, r6 @ r1 <- count = length (n)

	mov r2, #1 @ i = 1

iloop:@ for-loop
	
	cmp r2, r1 @ i - n
	bge iloopend @ i >= n then go to loopend
	add r10, r0, r2, LSL #2 @ temp = &array[4*j]  (left shift of 2)
	ldr r10, [r10] @ temp = array [4*i]
	sub r3, r2, #1 @ j = 1 - 1

jloop: @ while-loop
	cmp r3, #0 @ j >= 0 ?
	blt jloopend
	add r9, r0, r3, LSL #2 @ r9 <- &array[4*j]
	ldr r9, [r9] @ r9 <- array[4*j]
	cmp r10, r9 @ temp < array[4*j] ?
	bge jloopend
	add r8, r0, r3, LSL #2
	add r8, r8, #4 @ r8 <- &array[4*(j+1)]
	str r9, [r8] @ a[j+1] <- a[j]
	sub r3, r3, #1 @ j <- j - 1
	
	b jloop

@ end j loop
jloopend:
	add r3, r3, #1 @ j <- j+1
	add r8, r0, r3, LSL #2 @ r8 <- &array[4*(j+1)]
	str r10, [r8] @ a[j+1] <- temp
	add r2, r2, #1 @ i++
	b iloop

@ end i loop
iloopend:
	

/******************* OUTPUT ************************/

output:

	ldr r0, =outputMSG
	bl puts
	mov r5, #0 @ r5 counter	

printloop: cmp r6, r5 @ n - counter

	ble exit @ done printing
	add r3, r4, r5, LSL #2 @ r3 <- &array[4*counter]
	ldr r1, [r3] @ r1 <- array[4*counter]
	ldr r0, =FormatPrint @ r0 <- &print format
	bl printf
	add r5, r5, #1
	b printloop

exit:
	mov r0, r6 @ r0 = r6 result code = n
	ldr r1, =result @ r1 <- &result
	ldr lr, [r1] @ lr <- *r1 saved result address
	bx lr

.data
number: .word 0 @ place to hold input number
array: .space 100 @ room for 25 integers = 100 bytes
result: .word 0 @ place for result address of main
prompt: .asciz "Input a positive integer (negative to quit): "
outputMSG: .asciz "Sorted, those integers are: \n"
FormatScan: .asciz "%d"
FormatPrint: .asciz " %d\n"

/* External */
.global printf
.global scanf
.global puts
