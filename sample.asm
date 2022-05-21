section .data
    a db "ABC",10,0
    k dd "ABC",10,0
    b dd "Hello"
    c dw "Hello",10
section .rodata
    d db "Hello",10,0
    e dd "Hello"
    f dw "Hello",10
section .bss
    g resb 1
    h resd 2
    i resw 3
section .text
    global main
    extern printf
main:
	mov eax,[ebx]
	mov eax,[ecx+2]
	mov eax,[edx+289]
    add ecx,ebx
    sub edx,ebp
    add edx,30
	;;mov [ebx],12
	mov ebx,23
abc:
	mov eax,esp
	mov ebx,eax
