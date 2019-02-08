ifneq ($(KERNELRELEASE),)
	obj-m := cursach.o
else
	CURRENT = $(shell uname -r)
	KDIR = /lib/modules/$(CURRENT)/build
	PWD = $(shell pwd)
default:
	$(MAKE) -C $(KDIR) M=$(PWD) modules
	make clean
clean:
	rm -r .tmp_versions
	rm *.o
	rm *.mod.c
	rm *.symvers
	rm *.order
	rm .cache.mk
	rm .*.*.cmd

endif
