// Traffic lights

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <stdbool.h>


#define BCM2708_PERI_BASE 0x3F000000
#define GPIO_BASE (BCM2708_PERI_BASE + 0x200000) //GPIO controller

#define PAGE_SIZE (4*1024)
#define BLOCK_SIZE (4*1024)

int mem_fd;
void *gpio_map;

//IO-access
volatile unsigned *gpio;

// GPIO setup macros. Always use INP_GPIO(x) before using OUT_GPIO(x) or SET_GPIO_ALT(x,y)
#define INP_GPIO(g) *(gpio+((g)/10)) &= ~(7<<(((g)%10)*3))
#define OUT_GPIO(g) *(gpio+((g)/10)) |=  (1<<(((g)%10)*3))
#define SET_GPIO_ALT(g,a) *(gpio+(((g)/10))) |= (((a)<=3?(a)+4:(a)==4?3:2)<<(((g)%10)*3))

#define GPIO_SET *(gpio+7)  // sets   bits which are 1 ignores bits which are 0
#define GPIO_CLR *(gpio+10) // clears bits which are 1 ignores bits which are 0
  
#define GET_GPIO(g) (*(gpio+13)&(1<<g)) // 0 if LOW, (1<<g) if HIGH
    
#define GPIO_PULL *(gpio+37) // Pull up/pull down
#define GPIO_PULLCLK0 *(gpio+38) // Pull up/pull down clock

void setup_io();


//Setup inputs
const int carGreen = 17;
const int carYello = 27;
const int carRed   = 22;
const int passGreen = 16;
const int passYello = 21;
const int passRed   = 20;
const int button    = 26;
const int motion    = 4;

void printBtn(int g) {
	if (GET_GPIO(g))
		printf("Button %i pressed\n", g);
	else
		printf("Button %i released\n", g);
}

void reset() {
	GPIO_CLR = 1<<carGreen;
	GPIO_CLR = 1<<carYello;
	GPIO_CLR = 1<<carRed;
	GPIO_CLR = 1<<passGreen;
	GPIO_CLR = 1<<passYello;
	GPIO_CLR = 1<<passRed;

	GPIO_SET = 1<<carGreen;
	GPIO_SET = 1<<passRed;
}

void seq() {
	sleep(1);
	GPIO_SET = 1<<passYello;
	GPIO_CLR = 1<<carGreen;
	GPIO_SET = 1<<carYello;
	sleep(1);
	GPIO_CLR = 1<<carYello;
	GPIO_SET = 1<<carRed;
	sleep(1);
	GPIO_CLR = 1<<passYello;
	GPIO_CLR = 1<<passRed;
	GPIO_SET = 1<<passGreen;
	sleep(3);
	GPIO_CLR = 1<<passGreen;
	GPIO_SET = 1<<passRed;
	sleep(1);
	GPIO_CLR = 1<<carRed;
	GPIO_SET = 1<<carYello;
	sleep(1);
	GPIO_CLR = 1<<carYello;
	GPIO_SET = 1<<carGreen;
	sleep(2);
}

int main(int argc, char **argv) {
	
	//Setup the IO
	setup_io();
	
	//Set modes
	INP_GPIO(button);
	INP_GPIO(motion);

	INP_GPIO(17);
	OUT_GPIO(17);
	INP_GPIO(27);
	OUT_GPIO(27);
	INP_GPIO(22);
	OUT_GPIO(22);
	INP_GPIO(16);
	OUT_GPIO(16);
	INP_GPIO(21);
	OUT_GPIO(21);
	INP_GPIO(20);
	OUT_GPIO(20);

	bool btnState = false;
	bool motState = false;
	bool clicked = false;
	while (true) {
		btnState = GET_GPIO(button);
		motState = GET_GPIO(motion);

		if (btnState == true) {
			seq();
			break;
		} else {
			reset();
		}
	}

	return 0;
}

void setup_io() {
	/* open /dev/mem */
	if ((mem_fd = open("/dev/mem", O_RDWR|O_SYNC) ) < 0) {
		printf("can't open /dev/mem \n");
		exit(-1);
	}
	    
	/* mmap GPIO */
	gpio_map = mmap(
				NULL,             //Any adddress in our space will do
				BLOCK_SIZE,       //Map length
				PROT_READ|PROT_WRITE,// Enable reading & writting to mapped memory
				MAP_SHARED,       //Shared with other processes
				mem_fd,           //File to map
				GPIO_BASE         //Offset to GPIO peripheral
				);
		   
	close(mem_fd); //No need to keep mem_fd open after mmap
			  
	if (gpio_map == MAP_FAILED) {
		printf("mmap error %d\n", (int)gpio_map);//errno also set!
		exit(-1);
	}
				 
	// Always use volatile pointer!
	gpio = (volatile unsigned *)gpio_map;
}
