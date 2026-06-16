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

static char *duplicate_string(const char *src)
{
  if (!src)
  {
    return NULL;
  }

  size_t len = strlen(src) + 1;
  char *dst = malloc(len);
  if (dst)
  {
    memcpy(dst, src, len);
  }
  return dst;
}

#define PYPY_PATH "/mnt/pyram_disk/pypy/bin/pypy.elf"
#define RAMDISK_PATH "/mnt/pyram_disk"
#define TAR_FILE_PATH "/usr/share/pyram/lib/pypy.so"
#define PYFILE_RAMDISK_PATH "/mnt/pyram_pyfile_ramdisk"

// 360MB You shall need at least more than 360MB of ram to run pyram, I would recommend 2GB or more
#define SIZE 377487360

static const char *USAGE_MESSAGE = "Usage: [--toram] [--args|-a] <python_file.py> [args...]\nOr: -m||--help||--version [args...]";

// Raise an error message and exit
void __raise__(const char *message)
{
  perror(message);
  exit(EXIT_FAILURE);
}

static bool has_python_extension(const char *arg)
{
  return arg && strstr(arg, ".py") != NULL;
}

static void print_usage_and_exit(void)
{
  fprintf(stderr, "%s\n", USAGE_MESSAGE);
  exit(EXIT_FAILURE);
}

void execute_command(const char *command)
{
  int ret = system(command);

  if (ret == -1)
  {
    __raise__("Error while running subprocess\n");
  }
  else if (WIFEXITED(ret) && WEXITSTATUS(ret) != 0)
  {
    fprintf(stderr, "Command failed: %s\nExit code: %d\n", command, WEXITSTATUS(ret));
    __raise__("Subprocess returned non-zero exit code\n");
  }
}

bool is_sudo()
{
  return (geteuid() == 0);
}

void execute_pypy(bool use_toram, const char *py_file_name, const char *pyfile_path, const char *args)
{
  char command[2048];
  char cwd[1024];
  const char *target_path = use_toram ? PYFILE_RAMDISK_PATH : pyfile_path;

  if (!use_toram && pyfile_path[0] == '/')
  {
    if (getcwd(cwd, sizeof(cwd)) == NULL)
    {
      __raise__("Error in cwd\n");
    }
    target_path = cwd;
  }

  if (args && args[0] != '\0')
  {
    snprintf(command, sizeof(command), "%s %s/%s %s", PYPY_PATH, target_path, py_file_name, args);
  }
  else
  {
    snprintf(command, sizeof(command), "%s %s/%s", PYPY_PATH, target_path, py_file_name);
  }

  execute_command(command);
}

void allocate_python_file_to_ram(const char *python_file)
{

  char dest_path[1024];
  FILE *src = NULL, *dst = NULL;
  char buffer[8192];
  size_t bytes;

  if (access(PYFILE_RAMDISK_PATH, F_OK) != 0)
  {
    if (mkdir(PYFILE_RAMDISK_PATH, 0777) == -1 && errno != EEXIST)
    {

      __raise__("Error creating pyfile RAM disk directory");
    }

    char mount_cmd[256];
    snprintf(mount_cmd, sizeof(mount_cmd), "sudo mount -t tmpfs -o size=32M tmpfs %s", PYFILE_RAMDISK_PATH);

    execute_command(mount_cmd);
  }

  const char *filename = strrchr(python_file, '/');
  filename = filename ? filename + 1 : python_file;
  snprintf(dest_path, sizeof(dest_path), "%s/%s", PYFILE_RAMDISK_PATH, filename);

  src = fopen(python_file, "rb");

  if (!src)
  {
    __raise__("Error opening source python file");
  }

  dst = fopen(dest_path, "wb");

  if (!dst)
  {
    __raise__("Error creating file in pyfile RAM disk");
    fclose(src);
  }

  while ((bytes = fread(buffer, 1, sizeof(buffer), src)) > 0)
  {

    if (fwrite(buffer, 1, bytes, dst) != bytes)
    {
      __raise__("Error writing to pyfile RAM disk");
      fclose(src);
      fclose(dst);
    }
  }

  fclose(src);
  fclose(dst);
}

void free_python_file_ramdisk(void)
{
  char cmd[256];

  // Unmount and remove the RAM disk directory
  if (access(PYFILE_RAMDISK_PATH, F_OK) == 0)
  {
    snprintf(cmd, sizeof(cmd), "umount %s && rm -rf %s", PYFILE_RAMDISK_PATH, PYFILE_RAMDISK_PATH);
    execute_command(cmd);
  }
}

typedef struct
{
  char *fullpath;
  char *directory;
  char *filename;
} PyFileInfo;

static void free_pyfile_info(PyFileInfo *info)
{
  if (info)
  {
    free(info->fullpath);
    free(info->directory);
    free(info->filename);
    info->fullpath = info->directory = info->filename = NULL;
  }
}

static PyFileInfo parse_python_file(int argc, char *argv[])
{
  PyFileInfo info = {NULL, NULL, NULL};

  for (int i = 1; i < argc; i++)
  {
    if (has_python_extension(argv[i]))
    {
      info.fullpath = duplicate_string(argv[i]);
      if (!info.fullpath)
      {
        __raise__("Memory allocation failed\n");
      }

      const char *slash = strrchr(info.fullpath, '/');
      if (slash)
      {
        info.filename = duplicate_string(slash + 1);
        if (!info.filename)
        {
          free_pyfile_info(&info);
          __raise__("Memory allocation failed\n");
        }

        size_t len = slash - info.fullpath;
        info.directory = malloc(len + 1);
        if (!info.directory)
        {
          free_pyfile_info(&info);
          __raise__("Memory allocation failed\n");
        }
        memcpy(info.directory, info.fullpath, len);
        info.directory[len] = '\0';
      }
      else
      {
        info.filename = duplicate_string(info.fullpath);
        info.directory = duplicate_string("");
        if (!info.filename || !info.directory)
        {
          free_pyfile_info(&info);
          __raise__("Memory allocation failed\n");
        }
      }
      return info;
    }
  }
  return info;
}

static void build_script_args(int argc, char *argv[], char *args, size_t size)
{
  size_t len = 0;
  args[0] = '\0';

  for (int i = 1; i < argc; i++)
  {
    if (strcmp(argv[i], "--args") == 0 || strcmp(argv[i], "-a") == 0)
    {
      for (int j = i + 1; j < argc; j++)
      {
        if (has_python_extension(argv[j]))
        {
          for (int k = j + 1; k < argc; k++)
          {
            size_t needed = strlen(argv[k]) + 2;
            if (len + needed > size)
            {
              break;
            }
            len += snprintf(args + len, size - len, "%s%s", argv[k], k + 1 < argc ? " " : "");
          }
          return;
        }
      }
      return;
    }
  }
}

void validate_arguments(int argc, char *argv[])
{
  if (argc < 2)
  {
    print_usage_and_exit();
  }

  switch (argv[1][0])
  {
  case '-':
    if (strcmp(argv[1], "--toram") == 0)
    {
      if (argc < 3)
      {
        print_usage_and_exit();
      }

      if (strcmp(argv[2], "--args") == 0 || strcmp(argv[2], "-a") == 0)
      {
        if (argc < 4 || !has_python_extension(argv[3]))
        {
          print_usage_and_exit();
        }
        return;
      }
      else if (has_python_extension(argv[2]))
      {
        return;
      }
      else
      {
        print_usage_and_exit();
      }
    }
    else if (strcmp(argv[1], "--args") == 0 || strcmp(argv[1], "-a") == 0)
    {
      if (argc < 3 || !has_python_extension(argv[2]))
      {
        print_usage_and_exit();
      }
      return;
    }
    else if (strcmp(argv[1], "-m") == 0)
    {
      return;
    }
    else if (strcmp(argv[1], "--help") == 0 || strcmp(argv[1], "--version") == 0)
    {
      if (argc > 2)
      {
        print_usage_and_exit();
      }
      return;
    }
    break;

  default:
    if (has_python_extension(argv[1]))
    {
      return;
    }
    break;
  }

  print_usage_and_exit();
}

void print_version_and_exit()
{

  printf("PyRAM version 2.0.0\n");
  exit(EXIT_SUCCESS);
}

void print_help_and_exit()
{
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
      "  --version\n\n");

  exit(EXIT_SUCCESS);
}

void ensure_root()
{
  if (!is_sudo())
  {
    printf("You need to run this program as root\n");
    exit(EXIT_FAILURE);
  }
}

void setup_pypy_ramdisk()
{
  char command[256];

  if (access(RAMDISK_PATH, F_OK) == 0)
  {

    snprintf(command, sizeof(command), "rm -rf %s/*", RAMDISK_PATH);
    execute_command(command);
  }
  else
  {

    if (mkdir(RAMDISK_PATH, 0777) == -1 && errno != EEXIST)
    {

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
void handle_toram(int argc, char *argv[], bool *use_toram)
{
  if (argc > 1 && strcmp(argv[1], "--toram") == 0)
  {
    free_python_file_ramdisk();
    *use_toram = true;
  }
}

int main(int argc, char *argv[])
{
  pid_t pid;
  int status;
  bool use_toram = false;
  char *py_file_name = NULL;
  char *pyfile_path = NULL;

  validate_arguments(argc, argv);

  if (argc > 1 && strcmp(argv[1], "--version") == 0)
  {
    print_version_and_exit();
  }
  else if (argc > 1 && strcmp(argv[1], "--help") == 0)
  {
    print_help_and_exit();
  }

  handle_toram(argc, argv, &use_toram);

  ensure_root();

  if (argc > 1 && strcmp(argv[1], "-m") == 0)
  {

    pid = fork();

    if (pid < 0)
    {
      __raise__("Error while creating subprocess\n");
    }

    if (pid == 0)
    {
      setup_pypy_ramdisk();

      char command[2048] = {0};
      snprintf(command, sizeof(command), "%s", PYPY_PATH);

      for (int i = 1; i < argc; i++)
      {

        snprintf(command + strlen(command), sizeof(command) - strlen(command), " %s", argv[i]);
      }

      execute_command(command);

      exit(EXIT_SUCCESS);
    }
    else
    {

      waitpid(pid, &status, 0);

      if (!(WIFEXITED(status) && WEXITSTATUS(status) == EXIT_SUCCESS))
      {

        __raise__("Error while allocating memory in ram for pypy\n");
      }

    }

    exit(EXIT_SUCCESS);
  }

  PyFileInfo pyfile = parse_python_file(argc, argv);
  if (!pyfile.fullpath)
  {
    print_usage_and_exit();
  }

  py_file_name = pyfile.filename;
  if (!use_toram)
  {
    pyfile_path = pyfile.directory;
    free(pyfile.fullpath);
  }
  else
  {
    allocate_python_file_to_ram(pyfile.fullpath);
    free(pyfile.fullpath);
    free(pyfile.directory);
    pyfile_path = NULL;
  }

  pid = fork();

  if (pid < 0)
  {

    __raise__("Error while creating subprocess\n");
  }

  if (pid == 0)
  {

    setup_pypy_ramdisk();

    exit(EXIT_SUCCESS);
  }
  else
  {

    waitpid(pid, &status, 0);

    if (WIFEXITED(status) && WEXITSTATUS(status) == EXIT_SUCCESS)
    {
      char args[1024];
      build_script_args(argc, argv, args, sizeof(args));
      execute_pypy(use_toram, py_file_name, pyfile_path, args);
    }
    else
    {

      __raise__("Error while allocating memory in ram for pypy\n");
    }
  }

  if (use_toram)
  {
    free_python_file_ramdisk();
  }

  if (py_file_name)
  {
    free(py_file_name);
  }
  if (pyfile_path)
  {
    free(pyfile_path);
  }

  return 0;
}