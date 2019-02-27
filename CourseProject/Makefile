ifneq ($(KERNELRELEASE),)
        obj-m := course_project.o
else
	CURRENT = $(shell uname -r)
	KDIR = /lib/modules/$(CURRENT)/build
	PWD = $(shell pwd)
default:
	$(MAKE) -C $(KDIR) M=$(PWD) modules
	gcc -o main main.c
	gcc -o test test.c
	gcc -o mysleep mysleep.c
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
