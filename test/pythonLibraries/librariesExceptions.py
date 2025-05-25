
class LibException(Exception):

	name = "LibException"

	def __init__(self, *args, **kwargs) -> None:

		return super().__init__(*args, **kwargs)

	def __str__(self) -> str:

		return f"Error while testing python default libraries, {self}, {self.name}, {self.__dict__}"
