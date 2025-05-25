# This file create special exceptions for the tests

class pyramBuiltinsError(Exception):

	name = "pyramBuiltinsError"
    
	def __init__(*args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
        
	def __str__(self) -> str: 
		return f"Error while testing builtins functions of pyram, {self}, {self.__dict__}, {self.name}"
