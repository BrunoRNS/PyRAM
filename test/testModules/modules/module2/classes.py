class foo1:

	@staticmethod
	def fooHello() -> str:

		return "hello"

class foo2:
	"""
	A simple class that stores and displays a message.

	Attributes:
		msg (str): The message to be displayed, initialized to "hello".

	Methods:
		show() -> str:
			Returns the stored message.
	"""

	def __init__(self, *args, **kwargs) -> None:

		self.msg = "hello"

	def show(self) -> str:

		return self.msg