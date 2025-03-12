// common constants and functions used everywhere
#ifndef K_LIB_COMMON_H
#define K_LIB_COMMON_H

// data types
typedef unsigned char  uint8_t;
typedef unsigned short uint16_t;
typedef unsigned int   uint32_t;
typedef unsigned long  uint64_t;


// boolean values
#define true 1
#define false 0

// math stuff
#define PI 3.14159265358979323846
#define TAU 6.28318530717958647692
#define PYTHAGORAS_CONSTANT 1.41421356237309504880
#define ZERO 0
#define NEG_ONE -1

// outb and inb
static inline void outb(unsigned short port, unsigned char value) {
    __asm__ volatile ("outb %0, %1" : : "a"(value), "Nd"(port));
}

static inline void outw(unsigned short port, unsigned short value) {
    __asm__ volatile ("outw %0, %1" : : "a"(value), "Nd"(port));
}

static inline void outl(unsigned short port, unsigned int value) {
    __asm__ volatile ("outl %0, %1" : : "a"(value), "Nd"(port));
}

static inline unsigned char inb(unsigned short port) {
    unsigned char value;
    __asm__ volatile ("inb %1, %0" : "=a"(value) : "Nd"(port));
    return value;
}

static inline unsigned short inw(unsigned short port) {
    unsigned short value;
    __asm__ volatile ("inw %1, %0" : "=a"(value) : "Nd"(port));
    return value;
}

static inline unsigned int inl(unsigned short port) {
    unsigned int value;
    __asm__ volatile ("inl %1, %0" : "=a"(value) : "Nd"(port));
    return value;
}
#endif // K_LIB_COMMON_H