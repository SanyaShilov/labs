ifneq ($(KERNELRELEASE),)
	obj-m := fortune_cookies.o

else
	CURRENT = $(shell uname -r)
	KDIR = /lib/modules/$(CURRENT)/build
	PWD = $(shell pwd)

default:
	sudo $(MAKE) -C $(KDIR) M=$(PWD) modules
	sudo make clean

clean:
	rm -rf .tmp_versions
	rm .fortune_cookies.*
	rm *.o
	rm *.mod.c
	rm *.order

endif