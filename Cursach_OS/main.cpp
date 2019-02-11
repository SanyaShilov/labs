// Kurs.cpp: определяет точку входа для консольного приложения.
//

#include <fstream>
#include <iostream>
#include <cstdlib>
#include <stdio.h>

using namespace std;


int _tmain(int argc, _TCHAR* argv[])
{
	SetConsoleOutputCP(1251);
		//setlocale(LC_ALL,"RUS");
	cout <<"something";
	cout <<"something";
	getchar();
	cout <<"something";
	getchar();
	
	int x,y,c;
char* fileName = new char[10];
char* buf_x = new char [50];
char* buf_y = new char [50];
char* buf_c = new char [50];
{
ifstream* inp = new ifstream("result.txt");
while (!inp->eof())
{
inp->getline(buf_x, 50, ' ');
inp->getline(buf_y, 50, ' ');
inp->getline(buf_c, 50, ' ');
x=atoi(buf_x);
y=atoi(buf_y);
c=atoi(buf_c);
cout << x << " " << y << " " << c;
cout << "\n";
}
if (argc != 2)
    {
        printf("Usage: ./n");
        return -1;
    }

    // 
    status = LoadConfig(argv[1]);
    
    if (!status) // если произошла ошибка загрузки конфига
    {
        printf("Error: Load config failed\n");
        return -1;
    }
    
    // создаем 
    pid = fork();

    if (pid == -1) // если не удалось запустить потомка
    {
        // выведем на экран ошибку и её описание
        printf("Error: Start failed (%s)\n", strerror(errno));
        
        return -1;
    }
    else if (!pid) // 
        // 
        umask(0);
        
        
        setsid();
        
        //
        // 
        chdir("/");
        
        // закрываем дискрипторы 
        close(STDIN_FILENO);
        close(STDOUT_FILENO);
        close(STDERR_FILENO);
        
        // 
        status = MonitorProc();
         char s[80];
  cin.getline(s, 80);
  s < endl;
  system("pause");
        return status;
int      pid;
    int      status;
    int      need_start = 1;
    sigset_t sigset;
    siginfo_t siginfo;

    // 
    sigemptyset(&sigset);
    
    // 
    sigaddset(&sigset, SIGQUIT);
    
    // 
    sigaddset(&sigset, SIGINT);
    
    // 
    sigaddset(&sigset, SIGTERM);
    
    // 
    sigaddset(&sigset, SIGCHLD); 
    
    // 
    sigaddset(&sigset, SIGUSR1); 
    sigprocmask(SIG_BLOCK, &sigset, NULL);

    // 
    SetPidFile(PID_FILE);

    // 
    for (;;)
    {
        // 
        if (need_start)
        {
            // 
            pid = fork();
        }
        
        need_start = 1;
        
        if (pid == -1) // 
        {
            // 
            WriteLog("[MONITOR] Fork failed (%s)\n", strerror(errno));
        }
        else if (!pid) // 
        {
            // 
            
            // 
            status = WorkProc();
            
            // 
            exit(status);
        }
        else // 
        {
            // 
            
            // 
            sigwaitinfo(&sigset, &siginfo);
            
            // 
            if (siginfo.si_signo == SIGCHLD)
            {
                // 
                wait(&status);
                
                // 
                status = WEXITSTATUS(status);

                 // 
                {
                    //         
                    WriteLog("[MONITOR] Child stopped\n");
                    
                    // 
                    break;
                }
                else if (status == CHILD_NEED_WORK) // 
                {
                    // 
                    WriteLog("[MONITOR] Child restart\n");
                }
            }
            else if (siginfo.si_signo == SIGUSR1) // 
            {
                kill(pid, SIGUSR1); // 
                need_start = 0; // 
            }
            else //
            {
                // 
                WriteLog("[MONITOR] Signal %s\n", strsignal(siginfo.si_signo));
                
                // 
                kill(pid, SIGTERM);
                status = 0;
                break;
            }
       read(Share[0], &BufRD, 1);
int k = atoi(BufRD);
if (k > 0) {
signal(SIGUSR1, f1);
printf("\n 1 (%d): (%d)\n", pid1, pid2);
for (int i=0; i<N; i++) write(f, BufWR, 1);
k--;
sprintf (BufRD, "%d", k);
write(Share[1], BufRD, strlen(BufRD)); 
printf(" 1 (%d):  (%d)\n", pid1, pid2);
kill(pid2, SIGUSR2);
return;
}
else {
close(Share[0]);
close(Share[1]);
printf("n");
exit(1);
}
}

void f2(int signum) {
read(Share[0], &BufRD, 1);
int k = atoi(BufRD);
if (k > 0) {
signal(SIGUSR2, f2);
printf("\n 2 (%d):  1 (%d)\n", pid2, pid1);
for (int i=0; i<N; i++) write(f, BufWR, 1);
k--;
sprintf (BufRD, "%d", k);
write(Share[1], BufRD, strlen(BufRD)); 
printf(" 2 (%d):  1 (%d)\n", pid2, pid1);
kill(pid1, SIGUSR1);
return; }
    }

    // 
close(Share[0]);
  write(Share[1], argv[3], strlen(argv[3]));
  close(Share[1]);

  pid0 = getpid();

    WriteLog("[MONITOR] Stop\n");
    
    // 
    unlink(PID_FILE);
    }
    else // 
}
cout <<"something";

	getchar();
	return 0;
}

