#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

extern char* char_variable;
extern int int_variable;
extern char* switch_param (int n);
extern int factorial (int n);
extern int return_zero (void);

static int __init init_mod2(void)
{
	printk(KERN_INFO "mod2 init_mod2()\n");

	printk(KERN_INFO "mod2 char_variable: %s\n", char_variable);
	printk(KERN_INFO "mod2 int_variable: %d\n", int_variable);
	
	char* string = switch_param(-3);
	printk(KERN_INFO "mod2 switch_param(-3): %s\n", string);

	int fact = factorial(3);
	printk(KERN_INFO "mod2 factorial(3): %d\n", fact);
	
	int zero = return_zero();
	printk(KERN_INFO "mod2 return_zero(): %d\n", zero);
	
	return 0;
}

static void __exit exit_mod2(void)
{
	printk(KERN_INFO "mod2 exit_mod2()\n");
}

module_init(init_mod2);
module_exit(exit_mod2);

MODULE_LICENSE("GPL"); 
MODULE_AUTHOR("Shilov Alexandr");
