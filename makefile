CC      := gcc
ASMBLR  := nasm
LD      := ld
OBJCOPY := objcopy

# Directories
SRC_DIR  := KGB
KLIB_DIR := Klib
OBJ_DIR  := obj
BIN_DIR  := bin
BOOT_DIR := JosephStalin

# Files
ASM_SRC := $(SRC_DIR)/entry.asm
C_SRC   := $(KLIB_DIR)/Drivers/VGA/vga_driver.c \
           $(KLIB_DIR)/Drivers/IO/Input.c \
           $(KLIB_DIR)/Drivers/IO/Output.c
ASM_OBJ := $(OBJ_DIR)/entry.o
C_OBJ   := $(patsubst $(KLIB_DIR)/%.c, $(OBJ_DIR)/%.o, $(C_SRC))
LINKER_SCRIPT := $(SRC_DIR)/link.ld
KERNEL_TMP := $(BIN_DIR)/kernel.tmp
KERNEL_BIN := $(BIN_DIR)/kernel.bin
STAGE1_BIN := $(BIN_DIR)/stage1.bin
STAGE2_BIN := $(BIN_DIR)/stage2.bin

# Flags
CFLAGS  := -ffreestanding -nostdlib -nostartfiles -m64 -I$(KLIB_DIR)
ASFLAGS := -f elf64
LDFLAGS := -T $(LINKER_SCRIPT)

# Default target
all: $(KERNEL_BIN)

# Kernel binary
$(KERNEL_BIN): $(ASM_OBJ) $(C_OBJ)
	mkdir -p $(BIN_DIR)
	$(LD) -o $(KERNEL_TMP) $(ASM_OBJ) $(C_OBJ) $(LDFLAGS)
	$(OBJCOPY) -O binary $(KERNEL_TMP) $@

# Assembly object files
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.asm
	mkdir -p $(OBJ_DIR)
	$(ASMBLR) $(ASFLAGS) $< -o $@

# C object files
$(OBJ_DIR)/%.o: $(KLIB_DIR)/%.c
	mkdir -p $(OBJ_DIR)/Drivers/IO
	mkdir -p $(OBJ_DIR)/Drivers/VGA
	$(CC) $(CFLAGS) -c $< -o $@

# Stage 1 bootloader
$(STAGE1_BIN): $(BOOT_DIR)/stage1.asm
	mkdir -p $(BIN_DIR)
	$(ASMBLR) -f bin $< -o $@

# Stage 2 bootloader
$(STAGE2_BIN): $(BOOT_DIR)/stage2.asm
	mkdir -p $(BIN_DIR)
	$(ASMBLR) -f bin $< -o $@

# Clean build artifacts
clean:
	rm -rf $(OBJ_DIR)/*
	rm -rf $(BIN_DIR)/*
