#ifndef K_LIB_DRIVERS_VGA_H
#include "../../common.h"

#define K_LIB_DRIVERS_VGA_H
#define VIDEO_MEMORY (char*)0xB8000
#define VGA_WIDTH    80
#define VGA_HEIGHT   25

#define COLOR_BLACK        0x0
#define COLOR_BLUE         0x1
#define COLOR_GREEN        0x2
#define COLOR_CYAN         0x3
#define COLOR_RED          0x4
#define COLOR_MAGENTA      0x5
#define COLOR_BROWN        0x6
#define COLOR_LIGHT_GREY   0x7
#define COLOR_DARK_GREY    0x8
#define COLOR_LIGHT_BLUE   0x9
#define COLOR_LIGHT_GREEN  0xA
#define COLOR_LIGHT_CYAN   0xB
#define COLOR_LIGHT_RED    0xC
#define COLOR_LIGHT_MAGENTA 0xD
#define COLOR_LIGHT_BROWN  0xE
#define COLOR_WHITE        0xF

typedef struct {
    unsigned char character;
    unsigned char attribute;
} vga_entry_t;


void clear_screen(unsigned char attribute);
void put_char(char c, unsigned char attribute);
void put_string(const char* str, unsigned char attribute);
void set_cursor_pos(unsigned int x, unsigned int y);
void get_text_buffer(vga_entry_t* buffer);
void scroll_screen();

#endif