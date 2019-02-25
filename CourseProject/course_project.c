#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/proc_fs.h>
#include <linux/sched.h>
#include <linux/uaccess.h>
#include <linux/slab.h>
#include <linux/fs.h>
#include <linux/time.h>
#include <linux/list.h>
#include <linux/fdtable.h>


static const char* COURSE_PROJECT_FILENAME = "course_project";
static struct proc_dir_entry* course_project_file;

static char buffer[1000];
static int pids[100];
static int pids_count = 0;
static int curr_pid = 0;


#define DEBUG printk("debug %s %d", __FUNCTION__, __LINE__);


struct task_struct* get_task_by_pid(int pid)
{
    struct pid* s_pid;
    s_pid = find_get_pid(pid);
    return get_pid_task(s_pid, PIDTYPE_PID);
}


unsigned long long get_cpu_usage(struct task_struct* task)
{
    struct sched_entity se = task->se;
    return se.sum_exec_runtime;
}


unsigned long get_memory_usage(struct task_struct* task)
{
    struct mm_struct* mm = task->mm;
    return mm->total_vm * PAGE_SIZE;
}


unsigned long get_memory_usage_2(struct task_struct* task)
{
    struct mm_struct* mm = task->mm;
    struct vm_area_struct *vma = mm->mmap;
    unsigned long count = 0;
    for (; vma; vma = vma->vm_next)
        count += (vma->vm_end - vma->vm_start);
    return count;
}


int get_children_count(struct task_struct* task)
{
    int count = 0;
    struct list_head* list;
    list_for_each(list, &(task->children))
        count += 1;
    return count;
}


void get_file_count(struct task_struct* task, int* file_count, int* socket_count, int* pipe_count)
{
    struct files_struct* files = task->files;
    struct fdtable* fdtable = files->fdt;
    struct file** fd = fdtable->fd;
    *file_count = 0;
    *socket_count = 0;
    *pipe_count = 0;
    int i = 0;
    for (; i < fdtable->max_fds ; ++i)
    {
        if (fd[i])
        {
            *file_count += 1;
            struct inode* inode = fd[i]->f_inode;
            if (S_ISSOCK(inode->i_mode))
                *socket_count += 1;
            if (S_ISFIFO(inode->i_mode))
                *pipe_count += 1;
        }
    }
}


void get_all_counts(struct task_struct* task, unsigned long long* cpu_usage, unsigned long* memory_usage,
                    int* children_count, int* file_count, int* socket_count, int* pipe_count)
{
    *cpu_usage = get_cpu_usage(task);
    *memory_usage = get_memory_usage(task);
    *children_count = get_children_count(task);
    get_file_count(task, file_count, socket_count, pipe_count);
}


ssize_t course_project_read(struct file *filp, char *buf, size_t count, loff_t *offp)
{
    if (pids_count == 0)
        return 0;

    unsigned long long cpu_usage = 0;
    unsigned long memory_usage = 0;
    int children_count = 0, file_count = 0, socket_count = 0, pipe_count = 0;
    struct task_struct* task;
    struct timespec now;
    task = get_task_by_pid(pids[curr_pid]);
    getnstimeofday(&now);
    if (task)
    {
        get_all_counts(task, &cpu_usage, &memory_usage, &children_count, &file_count, &socket_count, &pipe_count);
        snprintf(buffer, 1000, "%10ld.%09ld | %10llu.%09llu | %20lu | %10d | %10d | %10d | %10d\n",
                 now.tv_sec, now.tv_nsec, cpu_usage / 1000000000, cpu_usage % 1000000000, memory_usage,
                 children_count, file_count, socket_count, pipe_count);
    }
    else
        snprintf(buffer, 1000, "%10ld.%09ld | -\n",
                 now.tv_sec, now.tv_nsec);

    curr_pid = (curr_pid + 1) % pids_count;

    copy_to_user(buf, buffer, 1000);
    int len = strlen(buffer);
    *offp += len;
    return len;
}


ssize_t course_project_write(struct file *filp, const char *buf, size_t count, loff_t *offp)
{
    char* input = vmalloc(1000);
    memset(input, 0, 1000);
    copy_from_user(input, buf, count);
    printk("course project working with %s", input);

    pids_count = 0;
    curr_pid = 0;
    while (input)
    {
        printk("input %s", input);
        char* result_c = strsep(&input, " ,;");
        printk("result_c %s", result_c);
        long result_l;
        kstrtol(result_c, 10, &result_l);
        printk("result_l %ld", result_l);
        int result = (int)result_l;
        printk("result %d", result);
        pids[pids_count++] = result;
    }

    return 1000;
}


struct file_operations course_project_fops =
{
    read : course_project_read,
    write : course_project_write
};


static int course_project_init(void)
{
    course_project_file = proc_create(COURSE_PROJECT_FILENAME, 0666, NULL, &course_project_fops);
    printk("course project module loaded");
    return 0;
}


static void course_project_exit(void)
{
    remove_proc_entry(COURSE_PROJECT_FILENAME, NULL);
    printk("course project module unloaded");
}


MODULE_LICENSE("GPL");
MODULE_AUTHOR("Shilov Alexandr");


module_init(course_project_init);
module_exit(course_project_exit);

