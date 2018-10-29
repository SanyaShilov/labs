#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

char* get_mac_address(void)
{
    FILE* f = fopen("/sys/class/net/wlp2s0/address", "r");
    char* mac_address = malloc(256);
    fgets(mac_address, 256, f);
    mac_address[strlen(mac_address) - 1] = '\0';
    fclose(f);
    return mac_address;
}

char* get_password(void)
{
    char* password = malloc(256);
    gets(password);
    return password;
}

char* get_secret_key(void)
{
    FILE* f = fopen("/tmp/.secret_key", "r");
    char* secret_key = malloc(256);
    fgets(secret_key, 256, f);
    fclose(f);
    return secret_key;
}

char* generate_secret_key(void)
{
    srand(time(NULL));
    char* secret_key = malloc(32);
    for (int i = 0; i < 32; i++)
        secret_key[i] = 'a' + rand() % 26;
    FILE* f = fopen("/tmp/.secret_key", "w");
    fprintf(f, "%s", secret_key);
    fclose(f);
    return secret_key;
}

char code[] =
"#include <stdio.h>"
"\n#include <stdlib.h>"
"\n#include <string.h>"
"\n"
"\nchar* get_mac_address(void)"
"\n{"
"\n    FILE* f = fopen(\"/sys/class/net/wlp2s0/address\", \"r\");"
"\n    if (!f)"
"\n        return NULL;"
"\n    char* mac_address = malloc(256);"
"\n    fgets(mac_address, 256, f);"
"\n    fclose(f);"
"\n    mac_address[strlen(mac_address) - 1] = '\\0';"
"\n    return mac_address;"
"\n}"
"\n"
"\nchar* get_password(void)"
"\n{"
"\n    char* password = malloc(256);"
"\n    gets(password);"
"\n    return password;"
"\n}"
"\n"
"\nchar* get_secret_key(void)"
"\n{"
"\n    FILE* f = fopen(\"/tmp/.secret_key\", \"r\");"
"\n    char* secret_key = malloc(256);"
"\n    fgets(secret_key, 256, f);"
"\n    fclose(f);"
"\n    return secret_key;"
"\n}"
"\n"
"\nint main(void)"
"\n{"
"\n    printf(\"Ok, Enter password: \");"
"\n    char* password = get_password();"
"\n    char* mac_address = get_mac_address();"
"\n    char* secret_key = get_secret_key();"
"\n    if ((strcmp(password, \"%s\") != 0) ||"
"\n        (strcmp(mac_address, \"%s\") != 0) ||"
"\n        (strcmp(secret_key, \"%s\") != 0))"
"\n        printf(\"Permission denied\\n\");"
"\n    else"
"\n        printf(\"Hello world!\\n\");"
"\n    free(mac_address);"
"\n    return 0;"
"\n}";

int main (void)
{
    printf("Enter password: ");
    char* password = get_password();
    char* mac_address = get_mac_address();
    char* secret_key = generate_secret_key();
    FILE* f = fopen("program.c", "w");
    fprintf(f, code, password, mac_address, secret_key);
    free(password);
    free(mac_address);
    free(secret_key);
    fclose(f);
    system("gcc program.c -o program");
    remove("program.c");
    return 0;
}
