/*********************************************************************

Program that takes an input of 10 numbers and sorts them

************************************************************************/

.global main
.func main

main:

	MOV R0, #0 @ initialize index variable

readloop:
	CMP r0, #5
	BEQ readdone
	LDR R1, =a   @ array address loaded
	













.data

.balign 4

a:		.skip		400
