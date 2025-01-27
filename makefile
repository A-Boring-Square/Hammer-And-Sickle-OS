CC     := gcc
ASMBLR := nasm

SRC_DIR  := KGB
OBJ_DIR  := obj
BIN_DIR  := bin
BOOT_DIR := JosephStalin
SRC := $(shell find $(SRC_DIR) -name '*.c')
ASM := $(SRC_DIR)/entry.asm
OBJ := $(patsubst $(SRC_DIR)/%.c, $(OBJ_DIR)/%.o, $(SRC)) \
	   $(patsubst $(SRC_DIR)/%.asm, $(OBJ_DIR)/asm/%.o, $(ASM))

CFLAGS = -I$(SRC_DIR)

# Generate OS binary and start the qemu virtual machine
all: $(BIN_DIR)/OS.bin run_qemu

# Concatenate all binary into single OS.bin.
# boot.bin has the bootloader
# full_kernel.bin has the actual kernel + kernel_entry

$(BIN_DIR)/OS.bin: $(BIN_DIR)/stage1.bin $(BIN_DIR)/stage2.bin $(BIN_DIR)/full_kernel.bin
	cat $(BIN_DIR)/stage1.bin $(BIN_DIR)/stage2.bin $(BIN_DIR)/full_kernel.bin > $@

$(BIN_DIR)/stage1.bin: $(BOOT_DIR)/stage1.asm
	$(ASMBLR) -f bin $< -o $@ -i $(BOOT_DIR)

$(BIN_DIR)/stage2.bin: $(BOOT_DIR)/stage2.asm
	$(ASMBLR) -f bin $< -o $@ -i $(BOOT_DIR)

$(BIN_DIR)/full_kernel.bin: $(OBJ)
	ld -m elf_i386 -o $@ -Tlink.ld $(OBJ) --oformat binary


$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -fno-pie -fno-stack-protector -ffreestanding -m32 -march=i386 -c $< -o $@

$(OBJ_DIR)/asm/%.o: $(SRC_DIR)/%.asm
	mkdir -p $(dir $@)
	$(ASMBLR) -f elf $< -o $@ -i $(SRC_DIR)

run_qemu:
	qemu-system-x86_64 -drive format=raw,file="$(BIN_DIR)/OS.bin",index=0,if=floppy,  -m 128M
	#qemu-system-x86_64 -drive format=raw,file="$(BIN_DIR)/OS.bin",index=0,if=floppy, -drive format=raw,file=disk.img,

clean:
	rm -rf $(OBJ_DIR)/*
	rm -rf $(BIN_DIR)/*

