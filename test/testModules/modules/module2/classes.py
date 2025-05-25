class foo1:

	@staticmethod
	def fooHello() -> str:

		return "hello"

class foo2:

	def __init__(self, *args, **kwargs) -> None:

		self.msg = "hello"

	def show(self) -> str:

		return self.msg