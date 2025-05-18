# Test importing modules:

try:

	from modules.module1.main import foo1, foo2, hello

	myFoo = foo1()

	if type(myFoo) != foo1:

		raise Exception("Failure testing module 1")

	from modules.module2.classes import foo1 as foo1Mod2, foo2 as foo2Mod2

	if foo2.fooHello() != foo2Mod2.fooHello():

		raise Exception("Failure testing module 2 in classes")

	from modules.module2.functions import hello as helloMod2

	if helloMod2() != hello():

		raise Exception("Failure testing module 2 in functions")

	from modules.module3.main import test

	if test():

		raise Exception("Failure testing module 3")


except Exception as e:

	raise Exception("Failure in {e}")


print("All modules tests worked successfully")
