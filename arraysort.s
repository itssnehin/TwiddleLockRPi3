/*************************************************************************

Program that takes an input of 5 numbers and sorts them using bubble sort

**************************************************************************/

.global main
.func main

main:
	MOV R0, #0			 @ initialize index variable


/* Need to create an array a[5] */
create:
	

/* Print initial array */
print1:
	

sort:
	
	CMP R0, #4 	   		@ check if end of array
	BEQ print 			@ jump if end

	LDR R1, =a 	
	LSL R2, R0, #2		@ R2 = R0 x 2
	ADD R2, R1, R2 		@ R2 = index position
	ADD R3, R2, #4		@ R3 = next postion
	LDR R5, [R2] 		@ R5 = data in R2	(a[i])
	LDR R6, [R3]		@ R6 = data in R3 (a[i+1])
	CMP R5, R6			@ compare R5 and R6
	MOVGT R7, R5		@ if R5 > R6 (a[i] > a[i+1]) then R7 = R5 as temp
	MOVGT R5, R6		@ "		"		"		"	 then R5 = R6 (a[i] = a[i+1])
	MOVGT R6, R7		@ "		" 		"		" 	 then R6 = old R5	(a[i+1] = a[i])

	STRGT R5, [R2]	@ Write R5 to array (a[i])
	STRGT R6, [R3]	@ Write R6 to array (a[i+1])
	ADDGT R0, R0, #1

	b sort

/*print final array */
print2:

	





.data

.balign 4

a: 	.skip 40
