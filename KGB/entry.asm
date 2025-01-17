; Entrypoint of the kernel the OS starts runing here

global _start
extern K_MAIN

_start:

    ; Call the K_MAIN function defined in kernal.c
    call K_MAIN