# PYRAM

**Version:** [latest](https://github.com/BrunoRNS/PyRAM/releases/latest).
Official site: [https://github.com/BrunoRNS/PyRAM](https://github.com/BrunoRNS/PyRAM).

---

**PYRAM** is a lightweight wrapper for PyPy 3.10 that runs your Python scripts directly from RAM for improved performance. It is optimized for server environments, includes Django, PyMySQL, and NumPy, and removes unnecessary components for a smaller footprint.

---

## Installation

1. Download the latest `.deb` package from [the releases page](https://github.com/BrunoRNS/PyRAM/releases/latest).
2. Install it:

   ```sh
   sudo dpkg -i PyRAM_[version].deb
   ```

3. Run your script:

   ```sh
   sudo pyram /path/to/your_script.py
   ```

---

## How It Works

- Checks for root privileges (sudo is required to mount the RAM disk).
- Mounts a RAM disk at `/mnt/pyram_disk`.
- Extracts the PyPy binary from `lib/pypy.so` into the RAM disk.
- Runs your script using PyPy, passing all arguments.
- Cleans up after execution.

---

## Benchmarks

Recent benchmarks show that **PYRAM** matches or slightly outperforms PyPy3 in most scenarios, especially right after boot or on slower disks, and both PyRAM and PyPy overtakes python in tests.

| Test                  | PYRAM Score | PyPy3 Score | Python3 Score |
|-----------------------|-------------|-------------|--------------|
| fibonacci             | 6.19        | 6.38        | 0.80         |
| manual_sort           | 0.24        | 0.22        | 0.012        |
| sum_large_list        | 5,025.11    | 1,513.10    | 274.99       |
| matrix_multiplication | 1,221.97    | 1,217.10    | 224.66       |
| string_concat         | 3.29        | 1.49        | 249.38       |
| **Average Score**     | **1251.36** | **547.66**  | **149.97**   |

- **PYRAM** was faster in most tests and had a higher average score in recent runs.
- For detailed charts and more info, see [benchmarks/benchmarks.md](./benchmarks/benchmarks.md).

![PYRAM Fibonacci Benchmark](./benchmarks/data/pyram_linear_fibonacci.png)
![PyPy3 Fibonacci Benchmark](./benchmarks/data/pypy3_linear_fibonacci.png)
![Python3 Fibonacci Benchmark](./benchmarks/data/python3_linear_fibonacci.png)

---

## Documentation

For more information, advanced usage, and tips for adding libraries, see the [documentation](./docs/docs.md).

---

## License

MIT License. See the [LICENSE](./LICENSE) file for details.

---

## Special Thanks

- Python and PyPy development teams.
- Professors, family, friends, and everyone who contributed or supported this project.

---
