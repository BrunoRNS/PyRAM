# Test importing modules:

"""
	This script tests the import and functionality of modules within the project.

	Tested modules and functions:
	- `modules.module1.main`: Imports `foo1`, `foo2`, and `hello`.
		- Instantiates `foo1` and checks its type.
	- `modules.module2.classes`: Imports `foo1` as `foo1Mod2`.
		- Compares the output of `foo2.fooHello()` and `foo1Mod2.fooHello()`.
	- `modules.module2.functions`: Imports `hello` as `helloMod2`.
		- Compares the output of `helloMod2()` and `hello()`.

	Raises:
		Exception: If any of the module imports or function outputs do not match the expected results.

	Prints:
		"All modules tests worked successfully" if all tests pass.
"""

try:

	from modules.module1.main import foo1, foo2, hello

	myFoo = foo1()

	if type(myFoo) != foo1:

		raise Exception("Failure testing module 1")

	from modules.module2.classes import foo1 as foo1Mod2

	if foo2.fooHello() != foo1Mod2.fooHello():

		raise Exception("Failure testing module 2 in classes")

	from modules.module2.functions import hello as helloMod2

	if helloMod2() != hello():

		raise Exception("Failure testing module 2 in functions")


except Exception as e:

	raise Exception(f"Failure in {e}")


print("All modules tests worked successfully")
