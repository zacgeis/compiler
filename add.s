; http://cs.lmu.edu/~ray/notes/nasmtutorial/
; http://asmtutor.com/#lesson1
; http://www.cs.virginia.edu/~evans/cs216/guides/x86.html
; nasm -fmacho64 add.s && clang add.o && ./a.out

; bss section

global _main
extern _puts

section .data

message:
  db 'print this', 0

section .text

_main:
	push rbx
  lea rdi, [rel message] ; see https://www.nasm.us/doc/nasmdoc3.html#section-3.3 Effective Addresses
  call _puts
	pop rbx
  ret
