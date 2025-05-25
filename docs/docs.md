# PYRAM Documentation

## Overview

**PYRAM** is a lightweight, optimized wrapper for **PyPy 3.10**, designed specifically for high speed environments. It streamlines PyPy by removing heavy unnecessary components for high speed tests (such as tcl/tk) and includes usefull packages like Django, PyMySQL, NumPy pre-installed. PYRAM achieves high-speed execution by running the PyPy JIT directly in RAM.

---

## Features

- **Optimized PyPy for servers:** Stripped of non-essential components for minimal footprint.
- **Pre-installed packages:** Includes Django and PyMySQL.
- **Runs in RAM:** Uses a RAM disk for maximum performance.
- **Simple command-line interface:** Run Python scripts with PyPy in RAM using a single command.
- **MIT Licensed:** Open source and free to use.

---

## Benchmarks

To see how fast is PyRAM in real tests look into [benchamrks](../benchmarks/benchmarks.md) and compare the speed between the pythons interpretors with the tests.

## How It Works

PYRAM's core is a C program (`src/pyram.c`) that:

1. **Creates a RAM disk** at `/mnt/pyram_disk` using `tmpfs`.
2. **Extracts a compressed PyPy binary** (`pypy.elf`) and its dependencies into the RAM disk which are a tar.xz file saved as pypy.so in the folder lib/.
3. **Executes PyPy** with your script, ensuring `.py` files are referenced with absolute paths.
4. **Cleans up** the RAM disk after execution.

The program requires `sudo` privileges to mount the RAM disk.

---

## Installation

### DEB package

1. **Ensure you have sudo privileges.**
2. **Download the Debian package** from [the releases page](https://github.com/BrunoRNS/PyRAM/releases/tag/1.0.0).
3. **Install the package:**

    ```sh
    sudo dpkg -i PyRAM.deb
    ```

### Building from source

If you want to build from source execute this command:

**WARNING**: You **have to** run exactly in the root directory of the repo, otherwise it wont recognize the lib and src folders.

```sh
sudo bash ./build/build
```

This generates a deb package in ./build/pyram-out/
Then you just have to install the package:

```sh
sudo dpkg -i ./build/pyram-out/package-name.deb
```

---

## Testing

To verify that PYRAM is installed successfully, run:
_No need of sudo here, because the program finishes before trying to generate ramdisk_

```sh
pyram --version
```

You should see the version information printed.

To run the included tests, execute:

```sh
sudo bash ./test/testAll.sh
```

---

## Usage

After installation, run your Python script with:

```sh
sudo pyram /path/to/your/script.py
```

- The `sudo` is required to mount the RAM disk.
- PYRAM will automatically set up the RAM disk, extract PyPy, and run your script.

---

### Using the `--args` or `-a` options

The `--args` (or `-a`) option allows you to pass additional command-line arguments directly to your Python script when running it with PYRAM. This is useful if your script expects arguments, such as input files, configuration options, or other parameters.

**Usage:**

```sh
sudo pyram --args /path/to/your/script.py arg1 arg2 arg3
```

Or using the short form:

```sh
sudo pyram -a /path/to/your/script.py arg1 arg2 arg3
```

**Example:**

Suppose your script accepts a filename and a verbosity flag:

```sh
sudo pyram --args /home/user/my_script.py input.txt --verbose
```

In this example, `input.txt` and `--verbose` will be passed to `my_script.py` as if you ran:

```sh
python3 my_script.py input.txt --verbose
```

**Note:**  
All arguments after `--args` (or `-a`) are forwarded to your script. Make sure to place `--args` after the script path.

---

### Using the `--toram` Option

The `--toram` option enables you to copy your Python script file into RAM before execution. This is especially useful when running scripts from slower storage devices (such as USB drives or external hard disks), or when you want to minimize disk access for maximum performance.

**NOTICE:** it can only execute one file in RAM, if this file import anything, it cannot be moved to ram, only if all the imports are stardant, you can add more standart libs if you want, this is more explained in Extending PyRAM section.

When you use `--toram`, PYRAM will:

1. Copy the specified `.py` file into the RAM disk (`/mnt/pyram_disk`).
2. Execute the script directly from RAM using PyPy.
3. Remove the script from RAM after execution is complete.

**Example usage:**

```sh
sudo pyram --toram /path/to/your/script.py
```

Using with --args:

```sh
sudo pyram --toram --args /path/to/your/script.py arg1 arg2 arg3
```

Or

```sh
sudo pyram --toram -a /path/to/your/script.py arg1 arg2 arg3
```

**Benefits of `--toram`:**

- Reduces latency caused by slow disk reads.
- Ensures the script runs entirely from memory, which can be beneficial for high-performance or temporary environments.
- Useful for running scripts from removable or network-mounted drives.

**Note:** Only the Python script specified is copied to RAM. Any additional data files your script needs must be handled separately.

## Extending PYRAM

PyRAM relies on **PyPy 3.10 for amd64 (x86-64)**, which is compressed in pypy.so file in lib directory. While using WHL libraries, download a compatible version for PyPy 3.10.

Running the following command we get all the pre-installed libraries of PyRAM:

```sh
sudo pyram -m pip list
```

This libraries you do not have to install using WHL packages, and you can import them normally:

### PIP List Output

Package           Version
----------------- -------;
asgiref           3.8.1
cffi              1.17.0
Django            5.1.5
greenlet          0.4.13
hpy               0.9.0
numpy             2.2.6
pip               25.1.1
PyMySQL           1.1.1
readline          6.2.4.1
setuptools        65.5.0
sqlparse          0.5.3
typing_extensions 4.12.2

### Step by Step for extending PyRAM with other libraries

1. **Download the `.whl` file** for your library from PyPI.
2. **Install your library:**

    ```sh
    sudo pyram -m pip install your_library.whl --target /path/to/your/script/library_name
    ```

    _You can install the module anywhere you want or prefer to, but for begginers, I suggest that way_.

    You can copy the file of your script to the same folder of the --target of installation, then you dont have to make next step, and usually this avoid errors of library not found, this issue is from pip and not from PyRAM.

3. **Include the library:** if you have installed in the same way as I have, you'll have to include it in this way in your code.

    ```python
    # Do this
    from library_name import library.method|object

    # Instead of this
    import library.method|object
    ```

    For example including matplotlib:

    ```python
    # Do this
    from matplotlib import matplotlib.pyplot as plt

    # Instead of this
    import matplotlib.pyplot as plt
    ```

    I recommend you to import in the way below, but you can do what you prefer to:

    ```python
    from matplotlib.matplotlib import pyplot as plt
    ```

4. **Run your script with PYRAM:**

    ```sh
    sudo pyram /path/to/your/script/main.py
    ```

You can also create an automatizer using shell scripts, making it compile the modules JIT of execution.

For e.g. what I have used in the test/testAll.sh file.

```sh
pyram -m pip install ./externWHLs/${MATPLOTLIB}.whl --target ./externWHLs/matplotlib/

pyram ./externWHLs/main.py
```

### Adding more default libraries

To add more default libraries or update a default one, ore even maybe changing the whole pypy version and structure you can decompress the pypy.so file which is in fact a .tar.xz file, than change anything you want maintaining the structure and compressing again with the name pypy.so and re-building from source, you may get what you want, thats the biggest proof about how costumizable is the PyRAM, in your needs.

You may need to change the source code if the sum of the libraries and the pypy itself its bigger than 360 MB, you will only have to change the pre-defined constant SIZE to the necessary one.

---

## Source Code Overview

### Main Components

- **src/pyram.c**: Main C source file. Handles RAM disk setup, PyPy extraction, and script execution.
- **lib/**: (If present) Additional libraries or dependencies.
- **build/**: Build scripts and packaging files.
- **docs/**: Documentation files.

### Key Functions in `pyram.c`

- `execute_pypy(argc, argv)`: Builds and runs the PyPy command with your script.
- `execute_command(command)`: Helper to run shell commands.
- `main(argc, argv)`: Orchestrates RAM disk setup, extraction, and execution.

---

## Why Sudo?

Mounting a RAM disk requires root privileges. PYRAM uses `sudo` to mount `tmpfs` at `/mnt/pyram_disk`.

## Common issues and Notice

- **Some libraries are not supported:** We cant do much about it because this relies on pypy.
- **Slow C/C++ codes or bindings:** pyram is as slow as pypy is while executing C/C++ code, or while importing a C/C++ library. Pyram can be faster than the classic pypy in some cases because of the RAM speed, but not such big improvement.
- **Data lost:** Lost logs, cache and saves when running in RAM, because if you stop running even for a second, you lose everything, when restarting the server, so save the important files out of pyram ramdisk workspace.
- **Not focused on security:** Dont rely on this for professional porpouse mainly if you are serving a robust backend, we do not offer any warranty of this software, as it is under MIT licence.
- **Not big improvements:**: not _that_ much difference between other pythons interpretors, its not as such a big improve and not suitable for all cases, but is very useful for big statistics counts, or very big loops, O(n) too high for normal python execution, show statistics with django framework speeding up requests and stuff.
- **It uses a big amount of RAM:** An important thing is that it uses more RAM than pypy, which is famous of using a big amount of it. If your system have low RAM, I do not recommend you to use this interpreter.
- **There are better options:** Probably using Julia or a speciallized language for that would be better, but if you want to try something new with the power of python, I hope this will be what you were searching for.

---

## License

PYRAM is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contributing

Contributions are welcome! Fork the repository and submit a pull request on GitHub.
