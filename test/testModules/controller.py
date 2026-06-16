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

    from modules import *

    myFoo = foo1Mod1()

    if type(myFoo) != foo1Mod1:

        raise Exception("Failure testing module 1")

    if foo2Mod1.fooHello() != foo1Mod2.fooHello():

        raise Exception(
            "Failure comparing foo2 and foo1 in module 2 and module 1 respectively")

    if helloMod2() != helloMod1():

        raise Exception(
            "Failure comparing hello in module 2 and module 1 respectively")


except Exception as e:

    raise Exception(f"Failure in {e}")


print("All modules tests worked successfully")
