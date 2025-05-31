# This file create special exceptions for the tests

class pyramBuiltinsError(Exception):
	"""
	Custom exception for errors encountered while testing built-in functions of the pyram module.
	Attributes:
		name (str): The name of the exception class.
	Methods:
		__init__(*args, **kwargs): Initializes the exception with optional arguments.
		__str__(): Returns a string representation of the exception, including its name and attributes.
	"""

	name = "pyramBuiltinsError"
    
	def __init__(*args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
        
	def __str__(self) -> str: 
		return f"Error while testing builtins functions of pyram, {self}, {self.__dict__}, {self.name}"
