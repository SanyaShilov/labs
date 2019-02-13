#include <linux/sched/clock.h>
#include <linux/sched.h>
#include <linux/module.h>
#include <linux/printk.h>
#include <linux/types.h>
#include <linux/tracepoint.h>
#include <trace/events/sched.h>


MODULE_LICENSE("GPL");
MODULE_AUTHOR("somebody");


void my_sched_switch_probe(void* ignore, bool ignr, struct task_struct* prev, struct task_struct* next) {
    printk("my_sched_switch_probe: %s -> %s at %lu\n", prev->comm, next->comm,
        (unsigned long) sched_clock());
}


int cswtracer_init(void) {
    register_trace_sched_switch(my_sched_switch_probe, 0);
    return 0;
}


void cswtracer_fini(void) {
    unregister_trace_sched_switch(my_sched_switch_probe, 0);
}


module_init(cswtracer_init);
module_exit(cswtracer_fini);
