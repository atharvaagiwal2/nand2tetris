// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

@i
M=1 //i=1

@R2
M=0 

//if(i>R0) goto STOP

(LOOP)   
@i
D=M 
@R0
D=D-M //i=i-R0
@STOP
D;JGT

@R1
D=M
@R2
M=D+M

@i
M=M+1 // i++

@LOOP
0;JMP//goto LOOP

(STOP)
@STOP
0;JMP