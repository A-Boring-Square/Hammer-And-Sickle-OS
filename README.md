Hammer & Sickle OS
==================

**Hammer & Sickle OS** is a parody operating system inspired by the themes of the Soviet Union, developed entirely in **assembly language**. This humorous and low-level operating system features a custom bootloader (`JosephStalin`), a kernel called `The KGB`, and a FAT32-based filesystem. The project provides a deep dive into system programming with a lighthearted take on Soviet themes.

Features:
---------

*   **Bootloader (`JosephStalin`)**: A multi-stage bootloader that sets up the system and loads the kernel.
*   **Kernel (`The KGB`)**: The core of the OS, written in pure assembly, responsible for managing system resources.
*   **Filesystem**: A FAT32 filesystem with a custom directory layout, created and managed using assembly language.
*   **Cross-platform build system**: The build process is automated using a Python script, which uses NASM to assemble the components and create the final bootable image.
*   **Soviet-Themed**: A playful reference to the USSR, with directories named `comrade_shared` and `red_bureau`.

Installation:
-------------

1.  Clone the repository:
    
        git clone https://github.com/yourusername/Hammer-And-Sickle-OS.git
        cd Hammer-And-Sickle-OS
    
2.  Install dependencies:
    *   **NASM**: You will need NASM (Netwide Assembler) to assemble the bootloader and kernel.
    *   **python**: You need python version 3.x.x to run the build scripts
3.  Build the project:
    
        python Build.py

Project Structure:
------------------

    Hammer & Sickle OS
    ├── JosephStalin
    │   ├── stage1.asm
    │   └── stage2.asm
    ├── KGB
    │   └── entry.asm
    └── comrade_shared
        ├── red_bureau
        │   ├── stage2.bin
        │   └── kgb.bin
        └── data
    

Contributing:
-------------

Contributions are welcome! Feel free to fork the repository, make changes, and submit pull requests.
