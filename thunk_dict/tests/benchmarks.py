import thunk_dict.tests.test_constants as test_constants
from thunk_dict.ThunkDict import ThunkDict


def test_set_and_get_thunk_dict():
    test_dict = ThunkDict()
    test_dict["key1"] = test_constants.calling_function
    test_dict["key1"]


def test_set_and_get_reg_dict():
    test_dict = {}
    test_dict["key1"] = test_constants.calling_function
    test_dict["key1"]()


if __name__ == "__main__":
    from timeit import timeit
    print("## THUNK DICT IMPLEMENTATION ##")
    print(timeit("test_set_and_get_thunk_dict()",
                 globals=globals(),
                 number=100) / 100)

    print("## REG DICT IMPLEMENTATION ##")
    print(timeit("test_set_and_get_reg_dict()",
                 globals=globals(),
                 number=100) / 100)
