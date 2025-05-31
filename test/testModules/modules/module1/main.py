# Test if this can be imported normally

class ShouldntError(Exception):
	"""
	Custom exception to indicate that an error should not have occurred.

	This exception can be raised in situations where an unexpected error state is reached,
	and the code path should not have resulted in an error.

	Args:
		*args: Variable length argument list passed to the base Exception.
		**kwargs: Arbitrary keyword arguments passed to the base Exception.
	"""

	def __init__(self, *args, **kwargs) -> None:

		super().__init__(*args, **kwargs)

class foo1:
	...

class foo2:

	@staticmethod
	def fooHello() -> str:

		return "hello"

def hello() -> str:

	return "hello"


if __name__ == "__main__":

	raise ShouldntError("This shouldnt have been executed")
