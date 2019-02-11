
    #include <linux/kernel.h>
    #include <linux/module.h>
    #include <linux/init.h>
    #include <linux/sched.h>
    #include <linux/proc_fs.h>
    #include <linux/uaccess.h>
    #include <linux/slab.h>
    #include <linux/fs.h>
    #include <linux/delay.h>
    #include <asm/uaccess.h>
    #include <asm/segment.h>
    #include <linux/buffer_head.h>

    // from related post
    struct file* file_open(const char* path, int flags, int rights) 
    {
        struct file* filp = NULL;
        filp = filp_open(path, flags, rights);
        if (IS_ERR(filp)) {
            printk(KERN_ERR "fuck!\n");
            return NULL;
        }
        return filp;
    }

    // from related post
    int file_read(struct file *file, unsigned long long offset, unsigned char *data, unsigned int size) 
    {
        mm_segment_t oldfs;
        int ret;

        oldfs = get_fs();
        set_fs(get_ds());

        ret = vfs_read(file, data, size, &offset);

        set_fs(oldfs);
        return ret;
    }  

    static int __init myinit(void)
    {
        struct file* file = file_open("/home/sanyash/file.txt", O_RDONLY, 0);
        char* data = vmalloc(sizeof(char) * 100);
        int ret = file_read(file, 0, data, 10); 
        printk(KERN_INFO "init %d %s\n", ret, data);
        return 0;
    }

    static void __exit myexit(void)
    {
        printk(KERN_INFO "exit!\n");
    }

    module_init(myinit);
    module_exit(myexit);

    MODULE_LICENSE("GPL");

