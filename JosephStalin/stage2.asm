; Stage 2 bootloader
;
; sets up the cpu for 64 bit mode and inits the kernel
[BITS 16]
[ORG 0x1000]            ; Stage 2 bootloader starts at 0x1000

start:
    ; Set up the CPU for 32-bit protected mode
    cli                      ; Disable interrupts
    mov ax, 0x0001           ; Load selector for protected mode
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax

    ; Set up the GDT (Global Descriptor Table)
    lgdt [gdt_descriptor]    ; Load the GDT descriptor

    ; Switch to protected mode (32-bit)
    mov eax, cr0
    or eax, 0x1              ; Set bit 0 to enable protected mode
    mov cr0, eax

    ; Far jump to protected mode code
    jmp 0x08:protected_mode

; 32-bit protected mode code
[BITS 32]
protected_mode:
    mov eax, cr4
    or eax, 0x2000           ; Enable PAE (Physical Address Extension)
    mov cr4, eax

    ; Enable 64-bit mode (long mode)
    mov eax, cr0
    or eax, 0x80000000       ; Set bit 31 to enable long mode (64-bit)
    mov cr0, eax

    ; Far jump to 64-bit code segment
    jmp 0x08:long_mode

; 64-bit mode code
[BITS 64]
long_mode:
    ; Now the CPU is in 64-bit mode
    ; Set the address for the kernel's entry point
    mov rsi, 0x10000

    ; Jump to the kernel entry point
    jmp rsi                  ; Jump to the kernel's entry point

; Define the GDT (Global Descriptor Table) and descriptor for protected and long mode
gdt:
    dq 0x0000000000000000        ; Null descriptor
    dq 0x00CF9A000000FFFF        ; Code segment descriptor (64-bit)
    dq 0x00CF92000000FFFF        ; Data segment descriptor (64-bit)

gdt_descriptor:
    dw gdt_end - gdt - 1         ; Length of the GDT
    dd gdt                       ; Pointer to the GDT
gdt_end: