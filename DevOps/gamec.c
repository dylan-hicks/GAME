#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv){
  //Add argument length check
  if(argc != 2){
    printf("\nTo compile your .game file, please use the following command:\n\n./%s [.game file]\n\nPlease note that you can only compile one .game file at a time.\n", argv[0]);
    exit(1);
  }
  execlp("python", "python", "game.py", argv[1]);

  return 0;
}
