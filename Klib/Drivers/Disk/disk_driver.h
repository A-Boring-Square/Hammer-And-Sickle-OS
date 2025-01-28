#ifndef K_LIB_DRIVERS_DISK_H
#define K_LIB_DRIVERS_DISK_H
#include "../../common.h"

// ISA DMA stuff
void mask_channel(unsigned char channel, unsigned char mask);
void init_floppy_dma(unsigned int address, unsigned short count);
void prepare_for_floppy_dma_read();
void prepare_for_floppy_dma_write();

#endif // K_LIB_DRIVERS_DISK_H