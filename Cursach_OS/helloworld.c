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

#include "constants.h"

extern struct pid* find_get_pid(pid_t nr);
extern struct task_struct* get_pid_task(struct pid* pid, enum pid_type type);

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
    msleep(10000);
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

static int __init hello_init(void)
{
    struct task_struct* task;
    task = get_current();
    int pid = task->pid;
    struct pid* s_pid;
    s_pid = find_get_pid(pid);
    struct task_struct* task2;
    task2 = get_pid_task(s_pid, PIDTYPE_PID);
    int pid2 = task2->pid;
    printk(KERN_INFO "Hello world from %d %d %s %d!\n", pid, pid2, IP, PORT);

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

static void __exit hello_exit(void)
{
    remove_proc_entry(PROC_SYMLINK, NULL);
    printk(KERN_INFO "fortune file deleted.\n");
    remove_proc_entry(PROC_FILENAME, NULL);
    printk(KERN_INFO "fortune dir deleted.\n");
    remove_proc_entry(PROC_DIRNAME, NULL);
    printk(KERN_INFO "fortune symlink deleted.\n");

    if (dict.cookie_buf)
        vfree(dict.cookie_buf);

    printk(KERN_INFO "Fortune module unloaded.\n");
    printk(KERN_INFO "Goodbye!\n");
}

module_init(hello_init);
module_exit(hello_exit);

MODULE_LICENSE("GPL");
