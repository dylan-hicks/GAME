#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <glob.h>
#include <string.h>

int main(int argc, char **argv){

  //Add argument length check
  //Maybe add check for .game extension later?
  if(argc < 2){
    printf("\nTo compile your .game file, please use the following command:\n\n%s [.game file] ...\n\n or \n\n %s *.game\n\n", argv[0], argv[0]);
    exit(1);
  }
  int mv_flag = 0;
  int i = 1;
  char mv_directory[100];
  while(!mv_flag && i < argc){
    if(strcmp(argv[i], "-m") == 0){
      mv_flag = 1; 
      sprintf(mv_directory, "%s", argv[++i]);
    }
    i++;
  }

  char compiled[100];

    int k = 1;
    for(k= 1; k < argc; k++){ 
      if(strstr(argv[k], ".game")){
        printf("python game.py %s\n", argv[k]);
        printf("%d\n", k);
        //execlp("python", "python", "game.py", argv[k]);
        if(mv_flag){
          sprintf(compiled, "%s.py", argv[k]);
          execlp("mv", "mv", compiled, mv_directory);
        }
      }
    }
  return 0;
}
