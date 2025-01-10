import os
import subprocess
import shutil
import platform

# Directories for the bootloaders and kernel
staging_dir = 'build_temp'

# Directories for the bootloaders and kernel
bootloader_dir = 'JosephStalin'
kernel_dir = 'KGB'

# Define file names for the bootloaders
stage1_file = os.path.join(bootloader_dir, 'stage1.asm')
stage2_file = os.path.join(bootloader_dir, 'stage2.asm')
kernel_file = os.path.join(kernel_dir, 'entry.asm')

# Define the output file names
stage1_output = os.path.join(staging_dir, 'stage1.bin')
stage2_output = os.path.join(staging_dir, 'stage2.bin')
kernel_output = os.path.join(staging_dir, 'kernel.bin')

# Ensure the build directory exists
def setup_build_dir():
    if not os.path.exists(staging_dir):
        os.makedirs(staging_dir)

# Clean up build artifacts
def clean_build_dir():
    if os.path.exists(staging_dir):
        shutil.rmtree(staging_dir)

# Compile the assembly files using NASM
def compile_stage1():
    print(f"Compiling Stage 1 bootloader: {stage1_file}")
    subprocess.run(['nasm', '-f', 'bin', stage1_file, '-o', stage1_output])

def compile_stage2():
    print(f"Compiling Stage 2 bootloader: {stage2_file}")
    subprocess.run(['nasm', '-f', 'bin', stage2_file, '-o', stage2_output])

def compile_kernel():
    print(f"Compiling Kernel: {kernel_file}")
    subprocess.run(['nasm', '-f', 'bin', kernel_file, '-o', kernel_output])

def create_boot_img():
    print("Creating boot image...")

    # Define the final boot image file
    boot_img_file = os.path.join(staging_dir, 'boot.img')

    # Concatenate stage1, stage2, and kernel into a single boot image
    with open(boot_img_file, 'wb') as boot_img:
        # Write stage1
        with open(stage1_output.strip("\""), 'rb') as stage1:
            boot_img.write(stage1.read())

        # Write stage2
        with open(stage2_output.strip("\""), 'rb') as stage2:
            boot_img.write(stage2.read())

        # Write kernel
        with open(kernel_output.strip("\""), 'rb') as kernel:
            boot_img.write(kernel.read())

    print(f"Boot image created at: {boot_img_file}")
    return boot_img_file  # Return the boot image file path

def run_qemu(boot_img_file):
    print(f"Running QEMU with boot image: {boot_img_file}")
    subprocess.run(['qemu-system-x86_64', '-drive', f'file={boot_img_file},format=raw'])

# Main build function
def build(run=False):
    setup_build_dir()

    print("Starting build process...")
    compile_stage1()
    compile_stage2()
    compile_kernel()
    boot_img_file = create_boot_img()

    print("Build completed successfully.")

    # If 'run' is True, start QEMU
    if run:
        run_qemu(boot_img_file)

# Main clean function
def clean():
    print("Cleaning up build artifacts...")
    clean_build_dir()
    print("Cleanup completed.")

# Command-line interface for user input
def main():
    choice = input("Enter command (build/clean): ").strip().lower()

    if choice == "build":
        run_choice = input("Do you want to run QEMU after build? (yes/no): ").strip().lower()
        build(run=(run_choice == 'yes'))
    elif choice == "clean":
        clean()
    else:
        print("Invalid command. Please use 'build' or 'clean'.")

if __name__ == "__main__":
    main()
