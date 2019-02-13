#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/proc_fs.h>
#include <linux/sched.h>
#include <asm/uaccess.h>
#include <linux/uaccess.h>
#include <linux/slab.h>
#include <linux/fs.h>
#include <linux/time.h>

#include <linux/sched/clock.h>




extern struct pid* find_get_pid(pid_t nr);
extern struct task_struct* get_pid_task(struct pid* pid, enum pid_type type);

static const char *PROC_FILENAME = "cursach";
static struct proc_dir_entry *proc_file = NULL;

char* buffer = NULL;
int LEN = 100;

int counter = 0;


ssize_t cursach_read(struct file *filp, char *buf, size_t count, loff_t *offp)
{
    counter += 1;
    printk(KERN_INFO "cursach read %d\n", counter);
    return 0;
}


ssize_t cursach_write(struct file *filp, const char *buf, size_t count, loff_t *offp)
{
    copy_from_user(buffer, buf, count);
    long pid_l;
    kstrtol(buffer, 10, &pid_l);
    int pid = (int)pid_l;
    printk(KERN_INFO "cursach write pid %d\n", pid);
    struct pid* s_pid;
    s_pid = find_get_pid(pid);
    struct task_struct* task;
    task = get_pid_task(s_pid, PIDTYPE_PID);
    printk(KERN_INFO "cursach write pid %d\n", task->pid);
    printk(KERN_INFO "cursach cpu %llu %llu\n", task->utime, task->stime);
    printk(KERN_INFO "cursach prev cpu %llu %llu\n", task->prev_cputime.utime, task->prev_cputime.stime);
    int len = strlen("123");
    printk(KERN_INFO "strlen %d\n", len);
    return count;
}


int delay(void)
{
    long i, j = 0;
    for (i = 0; i < 1000000; ++i)
        j += i % 37;
    return j;
}


struct file_operations proc_fops = 
{
    read : cursach_read,
    write : cursach_write
};


int proc_init(void)
{
    struct task_struct* task;
    task = get_current();
    int pid = task->pid;
    struct pid* s_pid;
    s_pid = find_get_pid(pid);
    struct task_struct* task2;
    task2 = get_pid_task(s_pid, PIDTYPE_PID);
    int pid2 = task2->pid;

    unsigned long clc = sched_clock();

    struct timespec ts;
    getnstimeofday(&ts);

    printk(KERN_INFO "cursach Hello world from %d %d clock: %lu ts: %ld %ld\n", pid, pid2, clc, ts.tv_sec, ts.tv_nsec);

    int d = delay();

    printk(KERN_INFO "cursach cpu %llu %llu\n", task->utime, task->stime);

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
