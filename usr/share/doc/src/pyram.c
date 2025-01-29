#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <string.h>
#include <sys/stat.h>
#include <errno.h>

#define PYPY_PATH "/mnt/pyram_disk/pypy/bin/pypy.elf"
#define RAMDISK_PATH "/mnt/pyram_disk"
#define TAR_FILE_PATH "/usr/lib/pypy.so"
#define SIZE 188960770

void execute_pypy(int argc, char *argv[]) {
    char command[1024];
    char cwd[1024];
    int i;
    if (getcwd(cwd, sizeof(cwd)) == NULL) {
        perror("Error in cwd\n");
        exit(EXIT_FAILURE);
    }
    snprintf(command, sizeof(command), "%s ", PYPY_PATH);
    for (i = 1; i < argc; i++) {
        if (strstr(argv[i], ".py") != NULL && argv[i][0] != '/') {
            snprintf(command + strlen(command), sizeof(command) - strlen(command), "%s/%s ", cwd, argv[i]);
        } else {
            snprintf(command + strlen(command), sizeof(command) - strlen(command), "%s ", argv[i]);
        }
    }

    if (system(command) == -1) {
        perror("Error in pypy.elf\n");
        exit(EXIT_FAILURE);
    }
}

void execute_command(const char *command) {
    if (system(command) == -1) {
        perror("Error while running subprocess\n");
        exit(EXIT_FAILURE);
    }
}

int main(int argc, char *argv[]) {
   pid_t pid;
   int status;
   char command[256];
   pid = fork();
   if (pid < 0) {
      printf("Error while creating subprocess\n");
      exit(EXIT_FAILURE);
   }
   if (pid == 0) {
      if (access(RAMDISK_PATH, F_OK) == 0) {
         snprintf(command, sizeof(command), "rm -rf %s/*", RAMDISK_PATH);
         execute_command(command);
      } else {
         if (mkdir(RAMDISK_PATH, 0777) == -1 && errno != EEXIST) {
            printf("Error creating /mnt/ramdisk\n");
            exit(EXIT_FAILURE);
         }
      }
      snprintf(command,sizeof(command),"sudo mount -t tmpfs -o size=%d tmpfs %s",SIZE,RAMDISK_PATH);
      execute_command(command);
      snprintf(command, sizeof(command), "tar -xJf %s -C %s", TAR_FILE_PATH, RAMDISK_PATH);
      execute_command(command);
      snprintf(command, sizeof(command), "chmod +x %s", PYPY_PATH);
      execute_command(command);
      exit(EXIT_SUCCESS);
   } else {
      waitpid(pid, &status, 0);
      if (WIFEXITED(status) && WEXITSTATUS(status) == EXIT_SUCCESS) {
         execute_pypy(argc, argv);
      } else {
         printf("Error while allocating memory in ram for pypy\n");
      }
   }
   return 0;
}

