#include "disk_driver.h"
/*
 * "Of course all good ideas can have downsides and while Intel can't really be
 * blamed for what is about to be described, IBM certainly can.
 * 
 * In the beginning there was a PC, but the PC was slow. IBM looked down from 
 * the heavens and said "Slap on a DMA controller -- that should speed it up."
 * IBM's heart was in the right place; its collective brains were elsewhere as
 * the DMA controller never met the needs of the system."
 */

// ISA DMA stuff
// Function to mask or unmask a DMA channel
void mask_channel(unsigned char channel, unsigned char mask) {
    // Set the mask bit for the specified channel
    unsigned char command = mask ? (0x04 | channel) : channel;
    outb(0x0A, command); // Write to the DMA mask register
}

// Function to initialize the DMA for floppy disk data transfer
void init_floppy_dma(unsigned int address, unsigned short count) {
    unsigned char channel = 2; // Channel 2 is used for floppy DMA
    unsigned short base_port = 0x00; // Base port for DMA registers

    // Determine base port based on channel
    if (channel == 0 || channel == 1 || channel == 2 || channel == 3) {
        base_port = 0x00; // Channels 0-3 use base 0x00
    } else if (channel == 4 || channel == 5 || channel == 6 || channel == 7) {
        base_port = 0xC0; // Channels 4-7 use base 0xC0
    } else {
        return; // Invalid channel NOTE: add kernel panic
    }

    // Mask the DMA channel during configuration
    mask_channel(channel, 1);

    // Reset the master flip-flop
    outb(0x0C, 0xFF);

    // Set the DMA address
    outb(base_port + 0x04, address & 0xFF);        // Low byte of address
    outb(base_port + 0x04, (address >> 8) & 0xFF); // High byte of address

    // Reset the master flip-flop again
    outb(0x0C, 0xFF);

    // Set the DMA transfer count
    outb(base_port + 0x05, count & 0xFF);        // Low byte of count
    outb(base_port + 0x05, (count >> 8) & 0xFF); // High byte of count

    // Set the external page register to the high byte of the physical address
    outb(0x81, (address >> 16) & 0xFF);

    // Unmask the DMA channel
    mask_channel(channel, 0);
}

// Function to prepare for a DMA read operation
void prepare_for_floppy_dma_read() {
    // Set the DMA controller to read mode (channel 2 = 0x46)
    outb(0x0B, 0x46);
}

// Function to prepare for a DMA write operation
void prepare_for_floppy_dma_write() {
    // Set the DMA controller to write mode (channel 2 = 0x4A)
    outb(0x0B, 0x4A);
}