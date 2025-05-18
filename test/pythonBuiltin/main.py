from testExceptions import pyramBuiltinsError

class Test:

    @staticmethod
    def testBuiltinTypes() -> None:
        # Test built-in types
        print("Testing built-in types:")
        try:

            tests = {

                isinstance(42, int),
                isinstance(3.14, float),
                isinstance("hello", str),
                isinstance([1, 2, 3], list),
                isinstance((1, 2), tuple),
                isinstance({1, 2}, set),
                isinstance({'a': 1}, dict),

            }

            if not (False in tests):

                print("  Built-in types: OK")
            
            else: raise pyramBuiltinsError("Isinstance failed while verifying types.") 

        except pyramBuiltinsError as e:

            print("  Built-in types: FAIL", e)


    @staticmethod
    def testIterables() -> None:
        # Test iterables

        print("Testing iterables:")

        try:
            lst = [1, 2, 3]

            if sum(lst) != 6:
                raise pyramBuiltinsError("sum failed")
            
            if list(map(str, lst)) != ['1', '2', '3']:
                raise pyramBuiltinsError("map failed")
            
            if [x for x in lst if x > 1] != [2, 3]:
                raise pyramBuiltinsError("list comprehension failed")
            
            print("  Iterables: OK")

        except pyramBuiltinsError as e:

            print("  Iterables: FAIL", e)

    @staticmethod
    def testLogic() -> None:
        # Test logic

        print("Testing logic:")

        try:

            if not (True and not False):
                raise pyramBuiltinsError("logic 1 failed")
            
            if True and False:
                raise pyramBuiltinsError("logic 2 failed")
            
            if not (True or False):
                raise pyramBuiltinsError("logic 3 failed")
            
            print("  Logic: OK")

        except pyramBuiltinsError as e:
            
            print("  Logic: FAIL", e)

    @staticmethod
    def testBuiltinFuncClass() -> None:
        # Test built-in functions and classes
        print("Testing built-in functions and classes:")
        try:
            if len("abc") != 3:
                raise pyramBuiltinsError("len failed")

            if max([1, 5, 2]) != 5:
                raise pyramBuiltinsError("max failed")

            if min([1, 5, 2]) != 1:
                raise pyramBuiltinsError("min failed")

            if not isinstance(object(), object):
                raise pyramBuiltinsError("isinstance object failed")

            print("  Built-in functions and classes: OK")

        except pyramBuiltinsError as e:

            print("  Built-in functions and classes: FAIL", e)


class Meta(type):
    pass

class MyClass(metaclass=Meta):
    pass

class TestMetaClass:
    # Test metaclasses

    def __init__(self, *args, **kwargs) -> None:
        self.myclass = MyClass()


    def testMetaClass(self) -> None:

        print("Testing metaclasses:")

        try:

            if type(self.myclass) is not MyClass:
                raise pyramBuiltinsError("type(obj) failed")

            if not isinstance(self.myclass, MyClass):
                raise pyramBuiltinsError("isinstance(obj) failed")

            if type(MyClass) is not Meta:
                raise pyramBuiltinsError("type(MyClass) failed")

            print("  Metaclasses: OK")

        except pyramBuiltinsError as e:

            print("  Metaclasses: FAIL", e)

if __name__ == "__main__":

    Test.testBuiltinTypes()
    Test.testLogic()
    Test.testIterables()
    Test.testBuiltinFuncClass()

    metaClassTesting = TestMetaClass()
    metaClassTesting.testMetaClass()

    print("All tests finished.")