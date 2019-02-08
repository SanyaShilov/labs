#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/proc_fs.h>
#include <linux/sched.h>
#include <asm/uaccess.h>
#include <linux/uaccess.h>
#include <linux/slab.h>
#include <linux/fs.h>

static const char *PROC_FILENAME = "cursach";
static struct proc_dir_entry *proc_file = NULL;

char* buffer = NULL;
int LEN = 100;

int counter = 0;

ssize_t cursach_read(struct file *filp, char *buf, size_t count, loff_t *offp)
{
    counter += 1;
    printk(KERN_INFO "cursach read %d.\n", counter);
    return 0;
}

ssize_t cursach_write(struct file *filp, const char *buf, size_t count, loff_t *offp)
{
    copy_from_user(buffer, buf, count);
    return count;
}

struct file_operations proc_fops = 
{
    read : cursach_read,
    write : cursach_write
};

int proc_init(void)
{
    buffer = vmalloc(sizeof(char) * LEN);
    memset(buffer, 0, LEN);
    proc_file = proc_create(PROC_FILENAME, 0666, NULL, &proc_fops);
    return 0;
}

void proc_cleanup(void)
{
    vfree(buffer);
    remove_proc_entry(PROC_FILENAME, NULL);
}

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Shilov Alexandr");

module_init(proc_init);
module_exit(proc_cleanup);
