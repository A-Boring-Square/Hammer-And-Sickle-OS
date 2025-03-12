; Stage 2 bootloader
; This bootloader sets up the CPU for 64-bit mode and initializes the kernel.
[BITS 16]
[ORG 0x1000]
start:
    ; Set VGA text mode (80x25, 16 colors)
    mov ah, 0x00          ; Function 0x00 - Set video mode
    mov al, 0x03          ; Mode 0x03 - 80x25 text mode
    int 0x10              ; Call BIOS interrupt 0x10 to set the video mode
    ; Optional: Clear the screen
    mov ah, 0x06          ; Function 0x06 - Scroll up window
    mov al, 0x00          ; Clear the screen (character 0x20, space)
    mov bh, 0x00          ; Page number (use 0)
    mov cx, 0x0000        ; Upper-left corner of the screen (row 0, column 0)
    mov dx, 0x184F        ; Lower-right corner of the screen (row 24, column 79)
    int 0x10              ; Call BIOS interrupt 0x10 to clear the screen

    cli                      ; Disable interrupts
    mov ax, 0x48             ; Load selector for protected mode
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

    ; Set up paging
    call setup_paging

    ; Far jump to 64-bit code segment
    jmp 0x08:long_mode

; 64-bit mode code
[BITS 64]
long_mode:
    ; Now the CPU is in 64-bit mode
    ; Set the address for the kernel's entry point in higher half memory
    mov rsi, 0x100000000     ; Kernel entry point in the higher-half (above 2GB)

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

; Define the Page Tables for the higher-half kernel
page_directory:
    ; PML4 (Page Map Level 4) Entry for the page directory
    dq page_directory_ptr       ; Points to the page directory pointer table (PDPT)

page_directory_ptr:
    dq page_directory_1         ; Points to the first page directory table (PD)

page_directory_1:
    dq kernel_page_table        ; Points to the page table that maps the kernel

kernel_page_table:
    dq 0x0000000000000000 | 0x3  ; First page, maps 0x0 to 0x100000000
    dq 0x0000000000000000 | 0x3  ; Second page (simple example)

setup_paging:
    ; Set up page directory and page tables for higher-half kernel
    ; PML4 Entry - Points to the PDPT
    mov rax, page_directory_ptr
    mov [page_directory], rax   ; PML4 entry pointing to the page directory pointer table

    ; PDPT Entry - Points to the first Page Directory
    mov rax, page_directory_1
    mov [page_directory_ptr], rax  ; PDPT entry pointing to the first page directory

    ; Page Directory Entry - Maps the physical 0x0 to virtual 0x100000000
    mov rax, kernel_page_table
    mov [page_directory_1], rax   ; Page directory entry pointing to the page table

    ; Page Table Entry - Maps 0x0 to 0x100000000 (first page)
    mov rax, 0x100000000         ; Virtual address 0x100000000 for the kernel
    or rax, 0x3                  ; Present bit and read/write enabled
    mov [kernel_page_table], rax ; First entry in the page table

    ; Set up the page directory to be loaded into CR3
    mov rax, page_directory
    mov cr3, rax                ; Load the address of the page d
