

#include "../Klib/common.h"
#include "../Klib/Drivers/VGA/vga_driver.h"



// The K_MAIN function, called from entry.asm

void volatile K_MAIN() {
    unsigned char attribute = (COLOR_BLUE << 4) | COLOR_WHITE;
    clear_screen(attribute);
    put_char('h', attribute);
    

    while (true) {
        
    }
}