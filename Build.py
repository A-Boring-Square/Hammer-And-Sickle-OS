import os
import subprocess
import sys
import platform
from struct import pack
import shutil

def get_nasm_command():
    """Returns the NASM command based on the OS."""
    if platform.system() == "Windows":
        return "nasm"
    elif platform.system() == "Darwin":  # macOS
        return "nasm"
    else:  # Assuming Linux
        return "nasm"

def create_directories():
    """Creates the necessary directories for build output."""
    if not os.path.exists("build"):
        os.makedirs("build")
        print("Created 'build' directory.")

def assemble_source(source, output):
    """Assembles the source file using NASM."""
    nasm_command = get_nasm_command()
    command = [nasm_command, "-f", "bin", "-o", output, source]

    print(f"Assembling {source}...")
    try:
        subprocess.run(command, check=True)
        print(f"Successfully assembled {source} into {output}.")
    except subprocess.CalledProcessError as e:
        print(f"Error during assembly: {e}")
        sys.exit(1)

def write_directory(fs, path, start_cluster, cluster_map, sector_size, reserved_sectors):
    """Writes a directory structure into the FAT32 filesystem."""
    dir_entry_size = 32
    cluster_start = reserved_sectors * sector_size + start_cluster * sector_size
    cluster_map[start_cluster] = 0x0FFFFFFF  # Mark this cluster as EOF

    fs.seek(cluster_start)
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        attr = 0x10 if os.path.isdir(item_path) else 0x20
        cluster = len(cluster_map)
        cluster_map[cluster] = 0x0FFFFFFF if attr == 0x10 else 0

        # Write directory entry
        name = item.upper().ljust(11, ' ')
        fs.write(name.encode())            # File/Directory name
        fs.write(pack("<B", attr))         # Attribute byte
        fs.write(pack("<B", 0))            # Reserved
        fs.write(pack("<B", 0))            # Create time (tenths of a second)
        fs.write(pack("<H", 0))            # Create time
        fs.write(pack("<H", 0))            # Create date
        fs.write(pack("<H", 0))            # Last accessed date
        fs.write(pack("<H", 0))            # High cluster
        fs.write(pack("<H", 0))            # Write time
        fs.write(pack("<H", 0))            # Write date
        fs.write(pack("<H", cluster))      # Starting cluster
        fs.write(pack("<I", 0))            # File size (0 for directories)

        # Write subdirectories recursively
        if attr == 0x10:
            write_directory(fs, item_path, cluster, cluster_map, sector_size, reserved_sectors)

def create_fat32_filesystem(fs_image, root_dir):
    """Creates a FAT32 filesystem with 'comrade_shared' as the root."""
    print(f"Creating FAT32 filesystem {fs_image}...")
    sector_size = 512
    sectors_per_cluster = 1
    reserved_sectors = 32
    num_fats = 2
    fat_size = 9  # Number of sectors per FAT
    total_sectors = 2880  # 1.44MB floppy size for simplicity

    # FAT32 creation logic
    with open(fs_image, "wb") as fs:
        fs.write(bytearray(total_sectors * sector_size))  # Blank disk image

    with open(fs_image, "r+b") as fs:
        # Initialize FAT32 BPB and FATs as in the previous script
        # ...

        # Write directories and files starting with "comrade_shared" as root
        cluster_map = {}
        write_directory(fs, root_dir, 2, cluster_map, sector_size, reserved_sectors)

    print(f"FAT32 filesystem {fs_image} created with custom structure.")

def create_bootable_image(stage1_path, fs_image, output_image):
    """Creates the final bootable image with stage1 at the boot sector."""
    print(f"Creating bootable image {output_image}...")
    with open(stage1_path, "rb") as stage1, open(fs_image, "rb") as fs, open(output_image, "wb") as bootable_image:
        bootable_image.write(stage1.read())  # Write stage1 to boot sector
        fs.seek(512)  # Skip stage1 boot sector
        bootable_image.write(fs.read())  # Append the filesystem

    print(f"Bootable image {output_image} created.")

def clean_up():
    """Cleans up build artifacts and temporary files."""
    if os.path.exists("build"):
        shutil.rmtree("build")
        print("Cleaned up build artifacts.")
    
    if os.path.exists("comrade_shared"):
        shutil.rmtree("comrade_shared")
        print("Cleaned up temporary 'comrade_shared' directory.")

def main():
    # Ask user for configuration option
    print("Choose an option:")
    print("1: Build the project")
    print("2: Clean the build artifacts")
    option = input("Enter your choice (1 or 2): ")

    if option == "1":
        create_directories()

        stage1_source = "JosephStalin/stage1.asm"
        stage2_source = "JosephStalin/stage2.asm"
        kernel_source = "KGB/entry.asm"

        stage1_output = "build/stage1.bin"
        stage2_output = "build/stage2.bin"
        kernel_output = "build/kgb.bin"
        fs_image = "build/filesystem.img"
        output_image = "build/bootable_image.img"

        # Assemble the bootloaders and kernel
        assemble_source(stage1_source, stage1_output)
        assemble_source(stage2_source, stage2_output)
        assemble_source(kernel_source, kernel_output)

        # Create the filesystem
        root_dir = "comrade_shared"
        if not os.path.exists(root_dir):
            os.makedirs(root_dir)

        # Populate filesystem with files
        os.makedirs(f"{root_dir}/red_bureau", exist_ok=True)
        os.makedirs(f"{root_dir}/data", exist_ok=True)
        with open(f"{root_dir}/red_bureau/stage2.bin", "wb") as f:
            f.write(open(stage2_output, "rb").read())
        with open(f"{root_dir}/red_bureau/kgb.bin", "wb") as f:
            f.write(open(kernel_output, "rb").read())

        create_fat32_filesystem(fs_image, root_dir)

        # Create the final bootable image
        create_bootable_image(stage1_output, fs_image, output_image)

        print("Build complete. Bootable image is ready!")

        # Clean up temporary files and directories
        clean_up()

    elif option == "2":
        clean_up()
    else:
        print("Invalid option. Please choose 1 or 2.")

if __name__ == "__main__":
    main()
