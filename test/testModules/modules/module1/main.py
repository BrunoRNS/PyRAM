# Test if this can be imported normally

class ShouldntError(Exception):

	def __init__(self, *args, **kwargs) -> None:

		super().__init__(*args, **kwargs)

class foo1:
	...

class foo2:

	def fooHello() -> str:

		return "hello"

def hello() -> str:

	return "hello"


if __name__ == "__main__":

	raise ShouldntError("This shouldnt have been executed")
