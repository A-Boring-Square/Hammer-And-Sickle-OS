; Entrypoint of the kernel. The OS starts running here.

global start_kernel

extern K_MAIN

section .text

start_kernel:
    call K_MAIN      ; Call the kernel's main function
    hlt              ; Halt the CPU to prevent unexpected behavior
