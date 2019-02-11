#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/proc_fs.h>
#include <linux/sched.h>
#include <asm/uaccess.h>
#include <linux/uaccess.h>
#include <linux/slab.h>
#include <linux/fs.h>

static const size_t COOKIE_BUF_LEN = 100;
static const size_t WORD_LEN = 100;
static const char *PROC_FILENAME = "fortune_cookies";
static const char *PROC_DIRNAME = "fortune_cookies_dir";
static const char *PROC_SYMLINK = "fortune_symlink";

static struct proc_dir_entry *proc_dir = NULL;
static struct proc_dir_entry *proc_file = NULL;
static struct proc_dir_entry *proc_sym = NULL;

typedef struct
{
    size_t word_count;
    char *cookie_buf;
} 
dict_t;

static dict_t dict = 
{
    word_count : 0,
    cookie_buf : NULL
};

ssize_t fortune_read(struct file *filp, char *buf, size_t count, loff_t *offp)
{
    if (*offp > 0 || dict.word_count == 0)
        return 0;

    dict.word_count--;
    copy_to_user(buf, &dict.cookie_buf[dict.word_count * WORD_LEN], WORD_LEN);
    memset(&dict.cookie_buf[dict.word_count * WORD_LEN], 0, WORD_LEN);

    // Hey ho dear friend,
    // this is a simple crutch,
    // so don't remove until you know what you are doing :)
    // more info here: https://stackoverflow.com/questions/30715169/infinite-loop-when-i-read-from-proc-which-is-implemented-with-seq-file
    *offp += WORD_LEN;
    return WORD_LEN;
}

ssize_t fortune_write(struct file *filp, const char *buf, size_t count, loff_t *offp)
{
    if (dict.word_count >= COOKIE_BUF_LEN)
    {
        printk(KERN_ERR "Cookie pot full.\n");
        return -ENOSPC;
    }

    copy_from_user(&dict.cookie_buf[dict.word_count * WORD_LEN], buf, count);
    dict.word_count++;
    return count;
}

struct file_operations proc_fops = 
{
    read : fortune_read,
    write : fortune_write
};

int proc_init(void)
{
    if (!(dict.cookie_buf = vmalloc(sizeof(char *) * COOKIE_BUF_LEN * WORD_LEN)))
    {
        printk(KERN_ERR "Not enough memory for cookie pot.\n");
        return -ENOMEM;
    }

    memset(dict.cookie_buf, 0, COOKIE_BUF_LEN * WORD_LEN);

    if (!(proc_dir = proc_mkdir(PROC_DIRNAME, NULL)))
    {
        vfree(dict.cookie_buf);
        printk(KERN_ERR "Can't create proc directory.\n");
        return -ENOMEM;
    }

    if (!(proc_file = proc_create(PROC_FILENAME, 0666, proc_dir, &proc_fops)))
    {
        remove_proc_entry(PROC_DIRNAME, NULL);
        vfree(dict.cookie_buf);
        printk(KERN_ERR "Can't create fortune file.\n");
        return -ENOMEM;
    }
    
    if (!(proc_sym = proc_symlink(PROC_SYMLINK, NULL, PROC_DIRNAME))) 
    {
        remove_proc_entry(PROC_DIRNAME, NULL);
        remove_proc_entry(PROC_FILENAME, NULL);
        vfree(dict.cookie_buf);
        printk(KERN_ERR "Can't create symlink.\n");
        return -ENOMEM;
    }

    printk(KERN_INFO "Fortune module loaded.\n");
    return 0;
}

void proc_cleanup(void)
{
    remove_proc_entry(PROC_SYMLINK, NULL);
    remove_proc_entry(PROC_FILENAME, NULL);
    remove_proc_entry(PROC_DIRNAME, NULL);

    if (dict.cookie_buf)
        vfree(dict.cookie_buf);

    printk(KERN_INFO "Fortune module unloaded.\n");
}

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Shilov Alexandr");

module_init(proc_init);
module_exit(proc_cleanup);
