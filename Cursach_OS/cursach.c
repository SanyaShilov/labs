#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/proc_fs.h>
#include <linux/sched.h>
#include <asm/uaccess.h>
#include <linux/uaccess.h>
#include <linux/slab.h>
#include <linux/fs.h>
#include <linux/time.h>
#include <linux/list.h>
#include <linux/fdtable.h>
#include <linux/atomic.h>

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
    for (i = 0; i < 100000000; ++i)
        j += i % 37;
    return j;
}


struct task_struct* get_task_by_pid(int pid)
{
    struct pid* s_pid;
    s_pid = find_get_pid(pid);
    return get_pid_task(s_pid, PIDTYPE_PID);
}


unsigned long long cpu_usage(struct task_struct* task)
{
    struct sched_entity se = task->se;
    return se.sum_exec_runtime;
}


unsigned long memory_usage(struct task_struct* task)
{
    struct mm_struct* mm = task->mm;
    struct vm_area_struct *vma = mm->mmap;
    unsigned long count = 0;
    for (; vma; vma = vma->vm_next)
        count += (vma->vm_end - vma->vm_start);
    return count;
}


int children_count(struct task_struct* task)
{
    int count = 0;
    struct list_head* list;
    list_for_each(list, &(task->children))
        count += 1;
    return count;
}

int files_count(struct task_struct* task)
{
    struct files_struct* files = task->files;
    struct file** fd_array = files->fd_array;
    struct fdtable* fdtable = files->fdt;
    struct file** fd = fdtable->fd;
    int i;
    for (i = 0; i < 10; ++i)
    {
        if (fd_array[i])
        {
            printk(KERN_INFO "%d fd_array\n", i);
        }
        else
            break;
    }
    for (i = 0; i < 10; ++i)
    {
        if (fd[i])
        {
            printk(KERN_INFO "%d fd\n", i);
            struct path p = fd[i]->f_path;
            struct dentry* d = p.dentry;
            struct qstr s = d->d_name;
            char* path = vmalloc(256);
            printk(KERN_INFO "%s str\n", s.name);
            dentry_path_raw(d, path, 256);
            printk(KERN_INFO "%c %c path raw\n", path[0], path[1]);
            vfree(path);
        }
        else
            break;
    }
    return i;
}


struct file_operations proc_fops = 
{
    read : cursach_read,
    write : cursach_write
};


int proc_init(void)
{
    struct task_struct* task;
    int pid = 4812;
    task = get_task_by_pid(pid);

    unsigned long clc = sched_clock();

    struct timespec ts;
    getnstimeofday(&ts);

    printk(KERN_INFO "cursach Hello world from %d clock: %lu ts: %ld %ld\n", task->pid, clc, ts.tv_sec, ts.tv_nsec);

    printk(KERN_INFO "cursach cpu %llu\n", cpu_usage(task));
    printk(KERN_INFO "cursach memory %lu\n", memory_usage(task));
    printk(KERN_INFO "cursach children count %d\n", children_count(task));
    printk(KERN_INFO "cursach files count %d\n", files_count(task));



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
