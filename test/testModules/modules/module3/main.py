
class ShouldntError(Exception):

	def __init__(self, *args, **kwargs) -> None:

		super().__init__(*args, **kwargs)

def test() -> bool: # If works true, else false
	try:
		import foo

		raise ShouldntError("This should have failed")

	except ImportError:

		return True

	except ShouldntError:

		return False

if __name__ == "__main__":

	raise ShouldntError("This shouldnt have been executed")