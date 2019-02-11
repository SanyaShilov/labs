#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

char* char_variable = "hello world!";
int int_variable = 123;

char* switch_param (int n)
{
	printk(KERN_INFO "mod1 switch_param(%d)\n", n);

	if (n < 0)
		return "less than zero";
	else if (n > 0)
		return "greater than zero";
	return "equal to zero";
}

int factorial (int n)
{
	printk(KERN_INFO "mod1 factorial(%d)\n", n);

	int result = 1;
	int i;
	for (i = 2; i <= n; ++i)
		result *= i;

	return result;
}

int return_zero (void)
{
	printk(KERN_INFO "mod1 return_zero()\n");
	return 0;
}

EXPORT_SYMBOL(char_variable);
EXPORT_SYMBOL(int_variable);

EXPORT_SYMBOL(switch_param);
EXPORT_SYMBOL(factorial);
EXPORT_SYMBOL(return_zero);


static int __init init_mod1(void)
{
	printk(KERN_INFO "mod1 init_mod1()\n");
	return 0;
}

static void __exit exit_mod1(void)
{
	printk(KERN_INFO "mod1 exit_mod1()\n");
}

module_init(init_mod1);
module_exit(exit_mod1);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Shilov Alexandr");
