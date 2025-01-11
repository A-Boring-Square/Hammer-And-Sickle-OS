; Stage 1 bootloader
;
; basicaly just sets all registers to zero and sets up a stable state
; for the stage 2 bootloader and kernal to run

; stage1.asm - Simple Stage 1 bootloader for Hammer & Sickle OS
; This bootloader prints a random sentence from a list, waits for 10 seconds, then loads stage2.
 
[BITS 16]               ; 16-bit mode
[ORG 0x7C00]            ; Bootloader loads at 0x7C00

START:
    ; Set up the stack
    xor ax, ax           ; Clear AX register
    mov ss, ax           ; Set the stack segment
    mov sp, 0x7C00       ; Set the stack pointer to the bottom of memory

    ; Print random sentence
    call print_random_sentence

    ; Wait for 10 seconds
    call wait_10_seconds

    ; Load stage2 (next bootloader or kernel) into memory at 0x1000
    mov ah, 0x02         ; BIOS read sector function
    mov al, 1            ; Read 1 sector
    mov ch, 0            ; Cylinder 0
    mov cl, 2            ; Sector 2 (stage2 binary is assumed to be here)
    mov dh, 0            ; Head 0
    mov dl, 0x80         ; Disk 0 (first floppy disk or first hard disk)
    lea bx, [0x1000]     ; Load to 0x1000 (next bootloader location)
    int 0x13             ; BIOS interrupt to read sector

    ; Jump to Stage 2 bootloader (start executing it)
    jmp 0x1000           ; Jump to the start of stage2 in memory

; Print random sentence function
print_random_sentence:
    ; Generate a random number between 0 and 3 to select a sentence
    call random_number
    mov al, bl           ; Store the random number in AL register
    cmp al, 0            ; Check if random number is 0
    je print_sentence_0
    cmp al, 1
    je print_sentence_1
    cmp al, 2
    je print_sentence_2
    cmp al, 3
    je print_sentence_3
    jmp print_done

print_sentence_0:
    mov si, sentence_0
    call print_string
    jmp print_done

print_sentence_1:
    mov si, sentence_1
    call print_string
    jmp print_done

print_sentence_2:
    mov si, sentence_2
    call print_string
    jmp print_done

print_sentence_3:
    mov si, sentence_3
    call print_string
    jmp print_done

print_done:
    ret

; Print string function
print_string:
    ; Print each character until null-terminator
    mov al, [si]
    cmp al, 0
    je print_done_string
    mov ah, 0x0E         ; BIOS teletype function
    int 0x10             ; Call BIOS interrupt
    inc si               ; Move to the next character
    jmp print_string

print_done_string:
    ret

; Generate a random number (0-3) and store it in BL register
random_number:
    ; Using a simple algorithm to generate a random number (using the value of the system's time)
    ; For simplicity, we'll just use the value of the "ticks" register (a register incremented by the system).
    xor ax, ax
    mov dx, 0x40         ; Use port 0x40, a PIT (Programmable Interval Timer) register
    in al, dx            ; Read from the timer
    mov bl, al           ; Store random value in BL
    and bl, 3            ; Mask to get a value between 0 and 3 (4 options)
    ret

; Wait for 10 seconds
wait_10_seconds:
    ; Wait by reading the system timer and introducing a delay
    ; This will make a simple loop that counts for about 10 seconds.
    mov cx, 0xFFFF       ; Use a large loop for delay (approx 10 seconds)
wait_loop:
    nop                  ; No operation (do nothing)
    loop wait_loop
    ret

; Welcome message
sentence_0 db "Peace Labor May", 0
sentence_1 db "Initializing the superior soviet industrial complex", 0
sentence_2 db "Getting rid of western influence", 0
sentence_3 db "Hammer and Sickle beats Stars and Stripes", 0

; Fill the rest of the bootloader with NOPs to reach the 512-byte boot sector
times 510 - ($ - $$) db 0
dw 0xAA55             ; Bootloader signature