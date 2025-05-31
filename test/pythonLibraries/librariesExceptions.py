
class LibException(Exception):
	"""
	Custom exception class for errors encountered while testing Python default libraries.

	Attributes:
		name (str): Name of the exception class.

	Methods:
		__init__(*args, **kwargs): Initializes the exception instance.
		__str__(): Returns a string representation of the exception, including the error message,
				   the class name, and the instance's attribute dictionary.
	"""

	name = "LibException"

	def __init__(self, *args, **kwargs) -> None:

		return super().__init__(*args, **kwargs)

	def __str__(self) -> str:

		return f"Error while testing python default libraries, {self}, {self.name}, {self.__dict__}"
