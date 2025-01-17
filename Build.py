import os
import subprocess
import shutil
import struct

# Directories for the bootloaders, kernel, and Klib
staging_dir = 'build_temp'
bootloader_dir = 'JosephStalin'
kernel_dir = 'KGB'
klib_dir = 'Klib'

# Define file names for the bootloaders
stage1_file = os.path.join(bootloader_dir, 'stage1.asm')
stage2_file = os.path.join(bootloader_dir, 'stage2.asm')
kernel_file = os.path.join(kernel_dir, 'kernel.c')  # C file for the kernel

# Define the output file names
stage1_output = os.path.join(staging_dir, 'stage1.bin')
stage2_output = os.path.join(staging_dir, 'stage2.bin')
kernel_output = os.path.join(staging_dir, 'kernel.bin')
boot_img_file = os.path.join(staging_dir, 'boot.img')

# FAT32 parameters
SECTOR_SIZE = 512
FAT_SECTORS = 2
ROOT_DIR_SECTORS = 32
DATA_SECTORS = 100
TOTAL_SECTORS = 1 + FAT_SECTORS + ROOT_DIR_SECTORS + DATA_SECTORS

def setup_build_dir():
    if not os.path.exists(staging_dir):
        os.makedirs(staging_dir)

def clean_build_dir():
    if os.path.exists(staging_dir):
        shutil.rmtree(staging_dir)

def compile_stage1():
    print(f"Compiling Stage 1 bootloader: {stage1_file}")
    subprocess.run(['nasm', '-f', 'bin', stage1_file, '-o', stage1_output], check=True)

def compile_stage2():
    print(f"Compiling Stage 2 bootloader: {stage2_file}")
    subprocess.run(['nasm', '-f', 'bin', stage2_file, '-o', stage2_output], check=True)

def compile_kernel():
    print(f"Compiling Kernel: {kernel_file}")
    # Use gcc with the flags for x86_64
    subprocess.run([
        'gcc', '-fno-pie', '-fno-stack-protector', '-nostdlib', '-ffreestanding',
        '-m64', '-march=x86-64', '-o', kernel_output, kernel_file
    ], check=True)

def compile_c_file(c_file, output_file):
    """
    Compiles a C file with the specified output file and adds include path to the 'Klib' folder.
    """
    print(f"Compiling C file: {c_file}")
    subprocess.run([
        'gcc', '-fno-pie', '-fno-stack-protector', '-nostdlib', '-ffreestanding',
        '-m64', '-march=x86-64', '-I', klib_dir, '-o', output_file, c_file
    ], check=True)

def create_fat32_filesystem(output_file):
    print("Creating FAT32 filesystem...")
    
    # Boot sector
    boot_sector = bytearray(SECTOR_SIZE)
    boot_sector[0x00:0x03] = b'\xEB\x58\x90'  # JMP instruction
    boot_sector[0x03:0x0B] = b'MSDOS5.0'      # OEM Name
    struct.pack_into('<H', boot_sector, 0x0B, SECTOR_SIZE)  # Bytes per sector
    boot_sector[0x0D] = 1  # Sectors per cluster
    struct.pack_into('<H', boot_sector, 0x0E, 1)  # Reserved sectors
    boot_sector[0x10] = 2  # Number of FATs
    struct.pack_into('<H', boot_sector, 0x11, 0)  # Max root dir entries (FAT32 uses data cluster)
    struct.pack_into('<I', boot_sector, 0x20, TOTAL_SECTORS)  # Total sectors
    boot_sector[0x15] = 0xF8  # Media descriptor
    struct.pack_into('<I', boot_sector, 0x24, FAT_SECTORS)  # Sectors per FAT
    struct.pack_into('<I', boot_sector, 0x2C, 2)  # First data cluster
    boot_sector[0x1FE:0x200] = b'\x55\xAA'  # Boot sector signature

    # FAT table
    fat_table = bytearray(SECTOR_SIZE * FAT_SECTORS)
    fat_table[0:3] = b'\xF8\xFF\xFF'  # Reserved cluster entries

    # Root directory
    root_dir = bytearray(SECTOR_SIZE * ROOT_DIR_SECTORS)
    root_cluster = bytearray(SECTOR_SIZE)

    # Add 'comrade_shared' directory entry
    add_directory_entry(root_cluster, "COMRADE SHARED", 2)

    # Add 'red_bureau' directory entry
    add_directory_entry(root_cluster, "RED BUREAU", 3)

    # Write the filesystem to the output file
    with open(output_file, 'wb') as fs:
        fs.write(boot_sector)
        fs.write(fat_table)
        fs.write(fat_table)  # FAT2 (identical to FAT1)
        fs.write(root_dir)
        fs.write(root_cluster)  # Empty directory space
        fs.write(bytearray(SECTOR_SIZE * DATA_SECTORS))  # Empty data region

    print(f"FAT32 filesystem with 'comrade_shared' and 'red_bureau' directories created at: {output_file}")

def add_directory_entry(cluster, name, cluster_number):
    """Add a directory entry to a cluster."""
    dir_name = name.ljust(11)  # Pad to 11 characters
    dir_entry = bytearray(32)
    dir_entry[0x00:0x0B] = dir_name.encode('ascii')  # Directory name
    dir_entry[0x0B] = 0x10  # Attribute: Directory
    struct.pack_into('<H', dir_entry, 0x1A, cluster_number)  # First cluster
    struct.pack_into('<I', dir_entry, 0x1C, 0)  # File size (directories have size 0)

    # Add to cluster
    for i in range(0, len(cluster), 32):
        if cluster[i] == 0x00:  # Empty slot
            cluster[i:i + 32] = dir_entry
            break

def create_boot_img():
    print("Creating boot image...")

    # Concatenate stage1, stage2, and kernel into a single boot image
    with open(boot_img_file, 'wb') as boot_img:
        # Write stage1
        with open(stage1_output, 'rb') as stage1:
            boot_img.write(stage1.read())

        # Write stage2
        with open(stage2_output, 'rb') as stage2:
            boot_img.write(stage2.read())

        # Write kernel
        with open(kernel_output, 'rb') as kernel:
            boot_img.write(kernel.read())

        # Create and append FAT32 filesystem
        create_fat32_filesystem(boot_img_file)

    print(f"Boot image created at: {boot_img_file}")

def run_qemu():
    print("Running QEMU...")
    subprocess.run([
        'qemu-system-x86_64', '-drive', 'file=build_temp/boot.img,format=raw', '-m', '512'
    ], check=True)

def build():
    setup_build_dir()
    print("Starting build process...")
    compile_stage1()
    compile_stage2()
    compile_kernel()
    create_boot_img()
    print("Build completed successfully.")
    
    # Ask if user wants to run QEMU
    choice = input("Do you want to run the kernel in QEMU? (y/n): ").strip().lower()
    if choice == 'y':
        run_qemu()


def clean():
    print("Cleaning up build artifacts...")
    clean_build_dir()
    print("Cleanup completed.")

def main():
    choice = input("Enter command (build/clean): ").strip().lower()
    if choice == "build":
        build()
    elif choice == "clean":
        clean()
    else:
        print("Invalid command. Please use 'build' or 'clean'.")

if __name__ == "__main__":
    main()
