class foo2:

	def fooHello() -> str:

		return "hello"

class foo3:

	def __init__(self, *args, **kwargs) -> None:

		self.msg = "hello"

	def show(self) -> str:

		return self.msg