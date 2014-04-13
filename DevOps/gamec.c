#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <glob.h>
#include <string.h>

int main(int argc, char **argv){
  //Add argument length check
  //Maybe add check for .game extension later?
  if(argc < 2){
    printf("\nTo compile your .game file, please use the following command:\n\n%s [.game file] ...\n\n or \n\n %s *.game\n\nPlease note that you can only compile one .game file at a time.\n", argv[0], argv[0]);
    exit(1);
  }

  if(strcmp(argv[1], "*.game")){
    //compile all .game in current directory
    glob_t data;
    switch( glob("*.game", 0, NULL, &data) ){
      case 0:
        break;
      case GLOB_NOSPACE:
        break;
      case GLOB_ABORTED:
        break;
      case GLOB_NOMATCH:
        printf("No .game files found.\n");
        break;
      default:
        break;
    }
    int j;
    for(j = 0; j < data.gl_pathc; j++){
      printf("python game.py %s\n", data.gl_pathv[j]);
      //execlp("python", "python", "game.py", data.gl_pathv[j]); 
    }
    globfree(&data);  
  }
  else{
    int i;
    for(i= 1; i < argc; i++){
      execlp("python", "python", "game.py", argv[i]);
    }
  }
  return 0;
}
