#include "../../common.h"
#include "vga_driver.h"


volatile vga_entry_t* const video_memory = (volatile vga_entry_t*)VIDEO_MEMORY;  // New higher-half video memory
static unsigned int cursor_x = 0;
static unsigned int cursor_y = 0;

static void update_cursor() {
    unsigned short pos = cursor_y * VGA_WIDTH + cursor_x;

    outb(0x3D4, 0x0E);
    outb(0x3D5, (pos >> 8) & 0xFF);

    outb(0x3D4, 0x0F);
    outb(0x3D5, pos & 0xFF);
}

void clear_screen(unsigned char attribute) {
    for (unsigned int y = 0; y < VGA_HEIGHT; y++) {
        for (unsigned int x = 0; x < VGA_WIDTH; x++) {
            unsigned int index = y * VGA_WIDTH + x;
            video_memory[index].character = ' ';
            video_memory[index].attribute = attribute;
        }
    }
    cursor_x = 0;
    cursor_y = 0;
    update_cursor();
}

void put_char(char c, unsigned char attribute) {
    if (c == '\n') {
        cursor_x = 0;
        cursor_y++;
        if (cursor_y >= VGA_HEIGHT) {
            cursor_y = VGA_HEIGHT - 1;
            scroll_screen();
        }
        update_cursor();
        return;
    }

    unsigned int index = cursor_y * VGA_WIDTH + cursor_x;
    video_memory[index].character = c;
    video_memory[index].attribute = attribute;

    cursor_x++;
    if (cursor_x >= VGA_WIDTH) {
        cursor_x = 0;
        cursor_y++;
        if (cursor_y >= VGA_HEIGHT) {
            cursor_y = VGA_HEIGHT - 1;
            scroll_screen();
        }
    }
    update_cursor();
}

void put_string(const char* str, unsigned char attribute) {
    while (*str) {
        put_char(*str++, attribute);
    }
}

void set_cursor_pos(unsigned int x, unsigned int y) {
    if (x < VGA_WIDTH && y < VGA_HEIGHT) {
        cursor_x = x;
        cursor_y = y;
        update_cursor();
    }
}

void get_text_buffer(vga_entry_t* buffer) {
    for (unsigned int y = 0; y < VGA_HEIGHT; y++) {
        for (unsigned int x = 0; x < VGA_WIDTH; x++) {
            unsigned int index = y * VGA_WIDTH + x;
            buffer[index] = video_memory[index];
        }
    }
}

void scroll_screen() {
    for (unsigned int y = 1; y < VGA_HEIGHT; y++) {
        for (unsigned int x = 0; x < VGA_WIDTH; x++) {
            unsigned int from_index = y * VGA_WIDTH + x;
            unsigned int to_index = (y - 1) * VGA_WIDTH + x;
            video_memory[to_index] = video_memory[from_index];
        }
    }

    for (unsigned int x = 0; x < VGA_WIDTH; x++) {
        unsigned int index = (VGA_HEIGHT - 1) * VGA_WIDTH + x;
        video_memory[index].character = ' ';
        video_memory[index].attribute = COLOR_LIGHT_GREY;
    }
}