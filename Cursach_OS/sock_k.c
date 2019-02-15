#include "common_k.h"


static struct sock *nl_sk;
static struct nlmsghdr *nlh;
static struct sk_buff *skb;
static struct sk_buff *skb_out;


char* recieve_message(void)
{
    nlh = (struct nlmsghdr*)skb->data;
    return (char*)nlmsg_data(nlh);
}


int sender_pid(void)
{
    return nlh->nlmsg_pid;
}


int send_message(char* msg)
{
    int msg_size = strlen(msg);
    int pid = sender_pid();
    skb_out = nlmsg_new(msg_size, 0);
    nlh = nlmsg_put(skb_out, 0, 0, NLMSG_DONE, msg_size, 0);
    NETLINK_CB(skb_out).dst_group = 0;
    strncpy(nlmsg_data(nlh), msg, msg_size);
    return nlmsg_unicast(nl_sk, skb_out, pid);
}


void handle_message(struct sk_buff *recieved_skb)
{
    skb = recieved_skb;
    char* message = recieve_message();
    printk(KERN_INFO "recieved message: %s\n", message);
    send_message("hello from kernel");
}


int __init hello_init(void)
{
    struct netlink_kernel_cfg cfg = {
        .input = handle_message,
    };
    nl_sk = netlink_kernel_create(&init_net, NETLINK_USER, &cfg);
    return 0;
}

void __exit hello_exit(void)
{
    netlink_kernel_release(nl_sk);
}

module_init(hello_init);
module_exit(hello_exit);

MODULE_LICENSE("GPL");
