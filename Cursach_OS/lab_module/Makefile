ifneq ($(KERNELRELEASE),)
	obj-m := helloworld.o
else
	CURRENT = $(shell uname -r)
	KDIR = /lib/modules/$(CURRENT)/build
	PWD = $(shell pwd)
default:
	$(MAKE) -C $(KDIR) M=$(PWD) modules
	sudo make clean
clean:
	rm *.o
	rm *.mod.c
	rm *.symvers
	rm *.order
	rm .cache.mk
	rm .*.*.cmd

endif
