#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <glob.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>

int main(int argc, char **argv){

  //Maybe add check for .game extension later?
  if(argc < 2){
    printf("\nTo compile your .game file, please use the following command:\n\n%s [.game file] ... [-m] [directory]\n\n or \n\n%s *.game [-m] [directory]\n\n", argv[0], argv[0]);
    exit(1);
  }
  int mv_flag = 0;
  int i = 1;
  char mv_directory[100];
  //check if -m flag was moved
  while(!mv_flag && i < argc){
    if(strcmp(argv[i], "-m") == 0){//-m flag used
      mv_flag = 1; 
      sprintf(mv_directory, "./%s", argv[++i]);
    }
    i++;
  }

  //Check for existence of directory to move compiled files to if -m flag was used
  if(mv_flag){
    if(mkdir(mv_directory, S_IRWXU | S_IRWXG | S_IRWXO) < 0){// < 0 then directory already exists
    }
  }

  int k = 1;
  pid_t child, pid; 
  int status = 0;
  for(k= 1; k < argc; k++){ 
    if(strstr(argv[k], ".game")){
      if((child = fork()) == 0){//child process
        char compiled[100];
        int devNull = open("/dev/null", O_WRONLY);
        int result = dup2(devNull, STDOUT_FILENO);
        sprintf(compiled, "./%s", argv[k]);
        execlp("python", "python", "./game.py", compiled, 0);
      }
      else{
        wait(&status); 
      }
      if(mv_flag){
        char compiled[100];
        if((child = fork()) == 0){//child process
          sprintf(compiled, "./%s.py", argv[k]);
          printf("Compiled is %s\n", compiled);
          printf("Compiled is %s\n", mv_directory);

          execlp("mv", "mv", compiled, mv_directory, 0);
        }
        else{
          wait(&status);
        }
      }
    }
  }  
  return 0;
}
