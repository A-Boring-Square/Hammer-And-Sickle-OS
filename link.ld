ENTRY(start_kernel)
OUTPUT_FORMAT(elf64-x86-64)

SECTIONS {
    . = 0x10000;

    /* Make sure the entry point is the very first thing that is placed in the binary */
    .entry : { *(.entry) }

    .text : {
        *(.text)
    }

    .rodata : {
        *(.rodata)
    }

    .data : {
        *(.data)
    }

    .bss : {
        *(COMMON)
        *(.bss)
    }
}
