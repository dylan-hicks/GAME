#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <glob.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#define MAX_INCLUDE 100
#define MAX_NAME_LENGTH 100

int main(int argc, char **argv){

  //Maybe add check for .game extension later?
  if(argc < 2){
    printf("\nTo compile your .game file, please use the following command:\n\n%s [.game file] ... [-m] [directory]\n\n or \n\n%s *.game [-m] [directory]\n\n", argv[0], argv[0]);
    exit(1);
  }
  int mv_flag = 0;
  int i = 1;
  char mv_directory[100];
  //check if -m flag was used
  while(!mv_flag && i < argc){
    if(strcmp(argv[i], "-m") == 0){//-m flag used
      mv_flag = 1; 
      sprintf(mv_directory, "./%s", argv[++i]);
    }
    i++;
  }

  //Check and process include statements 
  int k;
  int status = 0; 
  pid_t child, pid; 
  for(k = 1; k < argc; k++){
    if(strstr(argv[k], ".game")){
      if((child = fork()) == 0){
        char compiled[100];
        sprintf(compiled, "./%s", argv[k]);
        execlp("python", "python", "./include.py", compiled, 0); 
      }
    }
    else{
      wait(&status); 
    }
  } 

  //Check for existence of directory to move compiled files to if -m flag was used
  if(mv_flag){
    if(mkdir(mv_directory, S_IRWXU | S_IRWXG | S_IRWXO) < 0){// < 0 then directory already exists
    }
  }

  for(k= 1; k < argc; k++){ 
    if(strstr(argv[k], ".game")){
      if((child = fork()) == 0){//child process
        char compiled[100];
        int devNull = open("/dev/null", O_WRONLY);
        int result = dup2(devNull, STDOUT_FILENO);
        sprintf(compiled, "./%s.temp", argv[k]);
        execlp("python", "python", "./game.py", compiled, 0);
      }
      else{
        waitpid(child, &status, 0); 
      }
      if(mv_flag){
        char compiled[100];
        if((child = fork()) == 0){//child process
          sprintf(compiled, "./%s.py", argv[k]);
          execlp("mv", "mv", compiled, mv_directory, 0);
        }
        else{
          waitpid(child, &status, 0);
        }
      }
    }
  }  
/*
  //Remove .temp files
  for(k= 1; k < argc; k++){ 
    if(strstr(argv[k], ".game")){
      if((child = fork()) == 0){//child process
        char compiled[100];
        sprintf(compiled, "./%s.temp", argv[k]);
        execlp("rm", "rm", compiled, 0);
      }
      else{
        waitpid(child, &status, 0); 
      }
    } 
  }
  */
  return 0;
}
