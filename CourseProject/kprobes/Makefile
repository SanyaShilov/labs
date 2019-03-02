ifneq ($(KERNELRELEASE),)
        obj-m := kprobe_example.o kretprobe_example.o jprobe_example.o
else
	CURRENT = $(shell uname -r)
	KDIR = /lib/modules/$(CURRENT)/build
	PWD = $(shell pwd)
default:
	$(MAKE) -C $(KDIR) M=$(PWD) modules
	make clean
clean:
	rm *.o
	rm *.mod.c
	rm *.symvers
	rm *.order
	rm .cache.mk
	rm .*.*.cmd
	rm -r .tmp_versions
endif
