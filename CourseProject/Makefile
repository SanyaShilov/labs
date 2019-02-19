ifneq ($(KERNELRELEASE),)
        obj-m := course_project.o
else
	CURRENT = $(shell uname -r)
	KDIR = /lib/modules/$(CURRENT)/build
	PWD = $(shell pwd)
default:
	$(MAKE) -C $(KDIR) M=$(PWD) modules
	make clean
	make userspace
clean:
	rm *.o
	rm *.mod.c
	rm *.symvers
	rm *.order
	rm .cache.mk
	rm .*.*.cmd
	rm -r .tmp_versions
userspace:
	gcc -o main args.c main.c logs.c
endif
