# PYRAM Documentation

## Overview

**PYRAM** is a lightweight, optimized wrapper for PyPy, designed specifically for server environments. It streamlines PyPy by removing unnecessary components (such as pip, setuptools, and tcl/tk) and includes essential packages like Django and PyMySQL pre-installed. PYRAM achieves high-speed execution by running the PyPy JIT directly in RAM.

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
2. **Extracts a compressed PyPy binary** (`pypy.elf`) and its dependencies into the RAM disk.
3. **Executes PyPy** with your script, ensuring `.py` files are referenced with absolute paths.
4. **Cleans up** the RAM disk after execution.

The program requires `sudo` privileges to mount the RAM disk.

---

## Installation

1. **Ensure you have sudo privileges.**
2. **Download the Debian package** from [the releases page](https://github.com/BrunoRNS/PyRAM/releases/tag/1.0.0).
3. **Install the package:**
    ```sh
    sudo dpkg -i PyRAM.deb
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

## Extending PYRAM

If you need additional Python libraries:

1. **Download the `.whl` file** for your library from PyPI.
2. **Install PyPy** (if not already installed).
3. **Enable pip in PyPy:**
    ```sh
    pypy[version] -m ensurepip
    ```
4. **Install your library:**
    ```sh
    sudo pyram -m pip install your_library.whl --target /path/to/your/script
    ```
5. **Run your script with PYRAM:**
    ```sh
    sudo pyram /path/to/your/script/main.py
    ```

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

- Library not supported (we cant do much about it because this relies on pypy).
- C codes or bindings slower than normal python as well as pypy is, but maybe pyram can be faster than the classic pypy in some cases because of the RAM speed.
- Lost logs, cache and saves when running in RAM, because if you stop running even for a second, you lose everything, when restarting the server, so save the important files out of pyram ramdisk workspace.
- Not focused on security, so dont rely on this for professional porpouse mainly if you are serving a robust backend.
- Not much difference between other pythons interpretors, its not as such a big improve and not suitable for all cases, but is very useful for big statistics counts, or very big loops, O(n) too high for normal python execution, show statistics with django framework speeding up requests and stuff.
- Another important thing is that it uses more RAM than pypy, which is famous of using a big amount of it. If your system have low RAM, not recommended.
- Probably using Julia or a speciallized language for that would be better, but if you want to try something new with the power of python, I hope this will be what you were searching for.

---
## License

PYRAM is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contributing

Contributions are welcome! Fork the repository and submit a pull request on GitHub.
