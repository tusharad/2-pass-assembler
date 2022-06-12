section .data
    a db "ABC",10,0
    k dd "ABC",10,0
    b dd "Hello"
    c dw "Hello",10
section .rodata
    d db "Hello",10,0
    e dd "Hello"
    l dd "abc"
    f dw "Hello",10
section .bss
    g resb 1
    h resd 2
    i resw 3
section .text
    global main
    extern printf
main:
	mov ecx,ebx
	mov eax,[ebx]
	mov eax,[ecx+2]
	mov eax,[edx+289]
  add ecx,c
  sub edx,l
  xor ebx,f
  mov edx,12
abc:
  mov ebx,ecx
pqr:
  mov eax,ebx
  jmp abc
  jmp abc
  jmp abc
  jmp abc
  jmp abc
  add ecx,ebx
  add ebx,132
  sub ebx,eax
  sub ecx,129
  xor ecx,ebx
  xor ebx,ebx
  add ebx,10
  sub ebx,10
