from librariesExceptions import LibException

try:

	from typing import List, Set, Dict

except Exception as e:

	raise LibException(f"Error while testing the default library typing, importing: {e}")

# Test typing

try:
	
	exampleList: List[int] = [1, 2, 3]
	exampleSet: Set[int] = {1, 2, 3}
	exampleDict: Dict[str, int] = {"1": 1, "2": 2, "3": 3}

except Exception as e:

	raise LibException(f"Error while testing the default library typing, in definition: {e}")

try:

	from abc import ABC, ABCMeta, abstractmethod

except Exception as e:

	raise LibException(f"Error while testing the default library abc, importing: {e}")

# Test abc

class Foo:
	...

try:

	class MetaABC(ABCMeta):
		...

	class ChildMetaABC(metaclass=ABCMeta):
		...

except Exception as e:

	raise LibException(f"Error while testing the default library abc, in meta test: {e}")

try:

	class exampleABC(ABC):
		"""
		An abstract base class that defines the interface for working with Foo objects.

		Methods
		-------
		foo() -> Foo
			Abstract method that should return an instance of Foo.

		analyzeFoo() -> None
			Abstract method that should analyze a Foo instance.
		"""

		@abstractmethod
		def foo(self) -> Foo: ...

		@abstractmethod
		def analyzeFoo(self) -> None: ...

except Exception as e:

	raise LibException(f"Error while testing the default library abc, creating child of abc.ABC: {e}")

try:

	class example(exampleABC):

		def foo(self) -> Foo: return Foo()

		def analyzeFoo(self) -> None: return None

	example() # This should execute successfully

except Exception as e:

	raise LibException(f"Error while testing the default library abc, in abc class implementation: {e}")


if __name__ == "__main__":

	print("All tests executed successfully")