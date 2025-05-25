/*
MIT License

Copyright (c) 2024 BrunoRNS

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <string.h>
#include <sys/stat.h>
#include <errno.h>
#include <stdbool.h>

#define PYPY_PATH "/mnt/pyram_disk/pypy/bin/pypy.elf"
#define RAMDISK_PATH "/mnt/pyram_disk"
#define TAR_FILE_PATH "/usr/share/pyram/lib/pypy.so"
#define PYFILE_RAMDISK_PATH "/mnt/pyram_pyfile_ramdisk"

// 360MB You shall need at least more than 360MB of ram to run pyram, I would recommend 2GB or more
#define SIZE 377487360

// Raise an error message and exit
void __raise__(const char *message) {

   perror(message);
   exit(EXIT_FAILURE);

}

// execute command in terminal
void execute_command(const char *command) {

  int ret = system(command);

  if ( ret == -1 ) {

      __raise__("Error while running subprocess\n");

  } else if (WIFEXITED(ret) && WEXITSTATUS(ret) != 0) {

      fprintf(stderr, "Command failed: %s\nExit code: %d\n", command, WEXITSTATUS(ret));

      __raise__("Subprocess returned non-zero exit code\n");

  }

}

// check if user is root
bool is_sudo() {

   return (geteuid() == 0);

}

// execute pypy already in ramdisk
void execute_pypy(bool use_toram, const char *py_file_name, const char *pyfile_path, const char *args) {

  char command[2048];
  char cwd[1024];

  if (use_toram) {

    if (args && strlen(args) > 0) {

      snprintf(command, sizeof(command), "%s %s/%s %s", PYPY_PATH, PYFILE_RAMDISK_PATH, py_file_name, args);

    } else {

      snprintf(command, sizeof(command), "%s %s/%s", PYPY_PATH, PYFILE_RAMDISK_PATH, py_file_name);

    }

    execute_command(command);

    return;

  } else if (getcwd(cwd, sizeof(cwd)) == NULL) {

    __raise__("Error in cwd\n");

  }

  if (args && strlen(args) > 0) {

    if (pyfile_path[0] == '/') {

      snprintf(command, sizeof(command), "%s %s/%s %s", PYPY_PATH, cwd, py_file_name, args);

    } else {

      snprintf(command, sizeof(command), "%s %s/%s %s", PYPY_PATH, pyfile_path, py_file_name, args);

    }


  } else {

    if (pyfile_path[0] == '/') {
      
      snprintf(command, sizeof(command), "%s %s/%s", PYPY_PATH, cwd, py_file_name);

    } else {

      snprintf(command, sizeof(command), "%s %s/%s", PYPY_PATH, pyfile_path, py_file_name);

    }


  }

  execute_command(command);
  
}

/* Allocates the given Python file to a dedicated RAM disk and returns the new path.
Returns a newly allocated string with the path in the RAM disk, or NULL on error.
The max size of the python file is 32MB.
It can only allocate one file at a time. */
void allocate_python_file_to_ram(const char *python_file) {

   char dest_path[1024];
   FILE *src = NULL, *dst = NULL;
   char buffer[8192];
   size_t bytes;

   // Create the RAM disk directory if it doesn't exist
   if (access(PYFILE_RAMDISK_PATH, F_OK) != 0) {

     if (mkdir(PYFILE_RAMDISK_PATH, 0777) == -1 && errno != EEXIST) {

       __raise__("Error creating pyfile RAM disk directory");

     }

     // Mount tmpfs for the pyfile RAM disk (e.g., 32MB)
     char mount_cmd[256];
     snprintf(mount_cmd, sizeof(mount_cmd), "sudo mount -t tmpfs -o size=32M tmpfs %s", PYFILE_RAMDISK_PATH);

     execute_command(mount_cmd);

   }

   // Build destination path
   const char *filename = strrchr(python_file, '/');
   filename = filename ? filename + 1 : python_file;
   snprintf(dest_path, sizeof(dest_path), "%s/%s", PYFILE_RAMDISK_PATH, filename);

   // Copy file
   src = fopen(python_file, "rb");

   if (!src) {

     __raise__("Error opening source python file");

   }

   dst = fopen(dest_path, "wb");

   if (!dst) {

     __raise__("Error creating file in pyfile RAM disk");
     fclose(src);

   }

   while ((bytes = fread(buffer, 1, sizeof(buffer), src)) > 0) {

     if (fwrite(buffer, 1, bytes, dst) != bytes) {

       __raise__("Error writing to pyfile RAM disk");
       fclose(src);
       fclose(dst);

     }

   }

   fclose(src);
   fclose(dst);

}

// Frees the RAM disk used for the Python file.
void free_python_file_ramdisk(void) {

   char cmd[256];

   // Unmount and remove the RAM disk directory
   if (access(PYFILE_RAMDISK_PATH, F_OK) == 0) {

     snprintf(cmd, sizeof(cmd), "umount %s && rm -rf %s", PYFILE_RAMDISK_PATH, PYFILE_RAMDISK_PATH);
     execute_command(cmd);

   }

}

void validate_arguments(int argc, char *argv[]) {

  if (argc < 2) {
    __raise__("Usage: [--toram] [--args|-a] <python_file.py> [args...]\nOr: -m||--help||--version [args...]");
  }

  // Use switch on the first character for main options
  switch (argv[1][0]) {

    case '-':

      if (strcmp(argv[1], "--toram") == 0) {

        if (argc < 3) {
          __raise__("Usage: [--toram] [--args|-a] <python_file.py> [args...]\nOr: -m||--help||--version [args...]");
        }

        // Check for --args or -a after --toram
        if (strcmp(argv[2], "--args") == 0 || strcmp(argv[2], "-a") == 0) {
          if (argc < 4 || strstr(argv[3], ".py") == NULL) {
            __raise__("Usage: [--toram] [--args|-a] <python_file.py> [args...]\nOr: -m||--help||--version [args...]");
          }
          return;
        } else if (strstr(argv[2], ".py") != NULL) {
          return;
        } else {
          __raise__("Usage: [--toram] [--args|-a] <python_file.py> [args...]\nOr: -m||--help||--version [args...]");
        }

      } else if (strcmp(argv[1], "--args") == 0 || strcmp(argv[1], "-a") == 0) {

        if (argc < 3 || strstr(argv[2], ".py") == NULL) {
          __raise__("Usage: [--toram] [--args|-a] <python_file.py> [args...]\nOr: -m||--help||--version [args...]");
        }
        return;

      } else if (strcmp(argv[1], "-m") == 0) {

        return;

      } else if (strcmp(argv[1], "--help") == 0 || strcmp(argv[1], "--version") == 0) {

        if (argc > 2) {
          __raise__("Usage: [--toram] [--args|-a] <python_file.py> [args...]\nOr: -m||--help||--version [args...]");
        }
        return;
      }

      // Fall through for unknown options

      break;

    default:

      // Not an option, check if it's a .py file
      if (strstr(argv[1], ".py") != NULL) {
        return;
      }

      break;

  }

  __raise__("Usage: [--toram] [--args|-a] <python_file.py> [args...]\nOr: -m||--help||--version [args...]");

}

// Print version and exit
void print_version_and_exit() {

  printf("PyRAM version 2.0.0\n");
  exit(EXIT_SUCCESS);

}

// Print help and exit
void print_help_and_exit() {

  printf(
    "************************************************************\n"
    "*                   PyRAM - Python in RAM                  *\n"
    "*                  Version 2.0.0 | MIT License             *\n"
    "*                  Author: BrunoRNS                        *\n"
    "************************************************************\n"
    "\n"
    "Description:\n"
    "  PyRAM loads the PyPy interpreter and optionally your Python script into RAM\n"
    "  for faster execution. It is designed for systems where running Python from\n"
    "  RAM provides significant performance benefits.\n"
    "\n"
    "Usage:\n"
    "  pyram [--toram] [--args|-a] <python_file.py> [args...]\n"
    "  pyram -m <module> [args...]\n"
    "  pyram --help\n"
    "  pyram --version\n"
    "\n"
    "Options:\n"
    "  --toram         Loads the specified Python file into RAM before execution.\n"
    "                  This can improve performance for large scripts.\n"
    "  --args, -a      Allows passing arguments to the Python file. Must be used\n"
    "                  BEFORE the file name and path, similar to --toram.\n"
    "                  Example:\n"
    "                      pyram --args myscript.py arg1 arg2\n"
    "  -m              Runs a pre-installed library module as a script (like 'python -m').\n"
    "                  Use this to execute a module with arguments:\n"
    "                      pyram -m mymodule arg1 arg2\n"
    "  --help          Shows this detailed help message with usage examples.\n"
    "  --version       Shows the program version.\n"
    "\n"
    "Important Notes:\n"
    "  - The order of options matters! For example, '--toram' and '--args' or '-a' must come\n"
    "    before the Python file name and path. '-m' must be the first argument if used.\n"
    "  - Only one Python file can be loaded into RAM at a time with '--toram'.\n"
    "  - You must run PyRAM as root (sudo).\n"
    "\n"
    "Examples:\n"
    "  pyram --toram --args myscript.py arg1 arg2\n"
    "  pyram --args myscript.py arg1 arg2\n"
    "  pyram myscript.py\n"
    "  pyram -m mymodule arg1 arg2\n"
    "\n"
    "Arguments after the options are passed to the Python script or module.\n"
    "\n"
    "Usage summary:\n"
    "  [--toram] [--args|-a] <python_file.py> [args...]\n"
    "  -m <module> [args...]\n"
    "  --help\n"
    "  --version\n\n"
  );

  exit(EXIT_SUCCESS);

}

// Ensure running as root
void ensure_root() {

  if (!is_sudo()) {
    printf("You need to run this program as root\n");
    exit(EXIT_FAILURE);
  }

}

// Setup RAM disk for PyPy
void setup_pypy_ramdisk() {
  char command[256];

  if (access(RAMDISK_PATH, F_OK) == 0) {

    snprintf(command, sizeof(command), "rm -rf %s/*", RAMDISK_PATH);
    execute_command(command);

  } else {

    if (mkdir(RAMDISK_PATH, 0777) == -1 && errno != EEXIST) {

      __raise__("Error creating /mnt/ramdisk\n");

    }

  }

  snprintf(command, sizeof(command), "sudo mount -t tmpfs -o size=%d tmpfs %s", SIZE, RAMDISK_PATH);
  execute_command(command);

  snprintf(command, sizeof(command), "tar -xJf %s -C %s", TAR_FILE_PATH, RAMDISK_PATH);
  execute_command(command);

  snprintf(command, sizeof(command), "chmod +x %s", PYPY_PATH);
  execute_command(command);

}

// Allocate Python file to RAM if needed
void handle_toram(int argc, char *argv[], bool *use_toram) {

  if (argc > 1 && strcmp(argv[1], "--toram") == 0) {

    free_python_file_ramdisk();
    *use_toram = true;

  }

}

// Extracts and returns the Python file name from argv, or NULL if not found.
// The returned string must be freed by the caller.
char* get_python_file_name(int argc, char *argv[]) {

  for (int i = 1; i < argc; i++) {

    const char *py = strstr(argv[i], ".py");

    if (py != NULL) {

      const char *filename = strrchr(argv[i], '/');
      filename = filename ? filename + 1 : argv[i];

      return strdup(filename);

    }

  }

  return NULL;

}

// Extracts and returns the path (without the file name) of the Python file from argv, or NULL if not found or no path.
// The returned string must be freed by the caller.
char* get_python_file_path(int argc, char *argv[]) {

  for (int i = 1; i < argc; i++) {

    const char *py = strstr(argv[i], ".py");

    if (py != NULL) {

      const char *slash = strrchr(argv[i], '/');

      if (slash) {

        size_t len = slash - argv[i];
        char *path = (char*)malloc(len + 1);

        if (path) {

          strncpy(path, argv[i], len);
          path[len] = '\0';
          return path;

        }

      } else {

        // No path, just file name
        return strdup("");

      }

    }

  }

  return NULL;

}
/* Returns the full path (including file name) of the Python file from argv, or NULL if not found.
  The returned string must be freed by the caller. */
char* get_python_file_fullpath(int argc, char *argv[]) {

   for (int i = 1; i < argc; i++) {

      if (strstr(argv[i], ".py") != NULL) {

        return strdup(argv[i]);

      }

   }

   return NULL;

}


int main(int argc, char *argv[]) {
  pid_t pid;
  int status;
  bool use_toram = false;
  char *py_file_name = NULL;
  char *pyfile_path = NULL;

  // Validate arguments
  validate_arguments(argc, argv);

  // Handle --version and --help
  if (argc > 1 && strcmp(argv[1], "--version") == 0) {

    print_version_and_exit();

  } else if (argc > 1 && strcmp(argv[1], "--help") == 0) {

    print_help_and_exit();

  }

  // Handle --toram
  handle_toram(argc, argv, &use_toram);

  // Ensure root
  ensure_root();

  // If -m is present, execute pypy with the given args in a subprocess and wait
  if (argc > 1 && strcmp(argv[1], "-m") == 0) {

    pid = fork();

    if (pid < 0) {
      __raise__("Error while creating subprocess\n");
    }

    if (pid == 0) {
      setup_pypy_ramdisk();

      char command[2048] = {0};
      snprintf(command, sizeof(command), "%s", PYPY_PATH);

      for (int i = 1; i < argc; i++) {

        snprintf(command + strlen(command), sizeof(command) - strlen(command), " %s", argv[i]);

      }

      execute_command(command);

      exit(EXIT_SUCCESS);

    } else {

      waitpid(pid, &status, 0);

      if (!(WIFEXITED(status) && WEXITSTATUS(status) == EXIT_SUCCESS)) {

        __raise__("Error while allocating memory in ram for pypy\n");

      }
      // Parent process continues and will exit below
    }

    exit(EXIT_SUCCESS);
  }

  // Get python file name and path before fork so both parent and child can access
  py_file_name = get_python_file_name(argc, argv);

  if (!use_toram) {

    pyfile_path = get_python_file_path(argc, argv);

  } else {

    char* pyfile_fullpath = get_python_file_fullpath(argc, argv);

    if (pyfile_fullpath == NULL) {
        // Handle allocation failure
        fprintf(stderr, "Failed to get Python file full path.\n");
        exit(EXIT_FAILURE);
    }

    allocate_python_file_to_ram(pyfile_fullpath);
    
    free(pyfile_fullpath);

  }

  // Fork subprocess
  pid = fork();

  if (pid < 0) {

    __raise__("Error while creating subprocess\n");

  }

  if (pid == 0) {

    setup_pypy_ramdisk();

    exit(EXIT_SUCCESS);

  } else {

    waitpid(pid, &status, 0);

    if (WIFEXITED(status) && WEXITSTATUS(status) == EXIT_SUCCESS) {

      // Prepare args if --args or -a is present
      char args[1024] = "";

      for (int i = 1; i < argc; i++) {

        if (strcmp(argv[i], "--args") == 0 || strcmp(argv[i], "-a") == 0) {
          // All arguments after the .py file are considered script args
          for (int j = i + 1; j < argc; j++) {

            if (strstr(argv[j], ".py") != NULL) {

                for (int k = j + 1; k < argc; k++) {

                    strncat(args, argv[k], sizeof(args) - strlen(args) - 2);
                    strncat(args, " ", sizeof(args) - strlen(args) - 2);

                }

                break;

            }

          }

          break;

        }

      }

      execute_pypy(use_toram, py_file_name, pyfile_path, args);

    } else {

      __raise__("Error while allocating memory in ram for pypy\n");

    }

  }

  if (use_toram) {

    free_python_file_ramdisk();

  }

  // Free allocated memory

  if (py_file_name) { free(py_file_name); }
  if (pyfile_path) { free(pyfile_path); }

  return 0;

}