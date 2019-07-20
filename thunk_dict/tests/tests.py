import unittest
import logging

import thunk_dict.tests.test_constants as test_constants
from thunk_dict.ThunkDict import ThunkDict


class TestInit(unittest.TestCase):
    def test(self):
        self.assertTrue(self.regular_init())
        self.assertTrue(self.dictlike_init())
        self.bad_init()

    def regular_init(self):
        try:
            test_dict = ThunkDict(dictionary=test_constants.TEST_DICT)
            return True
        except BaseException as e:
            return False

    def dictlike_init(self):
        # Creating a mock dict-like object
        obj = {"key": "value"}

        test_dict = ThunkDict(dictionary=obj)
        return True

    def bad_init(self):
        with self.assertRaises(TypeError):
            test_dict = ThunkDict("not a dictionary")


class TestDictMethods(unittest.TestCase):
    def test_keys(self):
        test_dict = ThunkDict(test_constants.TEST_DICT)
        self.assertEqual(test_dict.keys(),
                         list(test_constants.TEST_DICT.keys()))

    def test_items(self):
        test_dict = ThunkDict(test_constants.TEST_DICT)
        called_dict = {"key1": test_constants.TEST_DICT["key1"],
                       "key2": test_constants.TEST_DICT["key2"]()}
        self.assertEqual(test_dict.items(), list(
            called_dict.items()))

    def test_values(self):
        test_dict = ThunkDict(test_constants.TEST_DICT)
        called_dict = {"key1": test_constants.TEST_DICT["key1"],
                       "key2": test_constants.TEST_DICT["key2"]()}
        self.assertEqual(test_dict.values(), list(
            called_dict.values()))

    def test_get(self):
        test_dict = ThunkDict(test_constants.TEST_DICT)
        self.assertEqual(test_dict.get("key1", None),
                         test_constants.TEST_DICT.get("key1"))
        self.assertEqual(test_dict.get("nonexistent_key", None), None)

    def test_fromkeys(self):
        keys = ("key1", "key2", "key3")
        test_dict = ThunkDict.fromkeys(keys, 1)
        self.assertEqual(test_dict.get_dict(), dict.fromkeys(keys, 1))

    def test_clear(self):
        test_dict = ThunkDict(test_constants.TEST_DICT)
        test_dict.clear()
        self.assertEqual(test_dict.get_dict(), {})


class TestThunkInit(unittest.TestCase):
    def test(self):
        test_dict = ThunkDict()
        thunk = test_dict.__lazy__wrapper__(test_constants.calling_function)
        self.assertIsInstance(thunk, test_dict.__LazyInternal__)


class TestDethunk(unittest.TestCase):
    def test(self):
        test_dict = ThunkDict()
        thunk = test_dict.__lazy__wrapper__(test_constants.calling_function)
        dethunked = test_dict.__dethunk__(thunk)
        self.assertEqual(dethunked, test_constants.additional_callback)


class TestInitAndGet(unittest.TestCase):
    def test_no_thunkable_init(self):
        test_dict = ThunkDict(dictionary=test_constants.TEST_DICT)
        self.assertEqual(test_dict["key1"], test_constants.TEST_DICT["key1"])
        self.assertEqual(test_dict["key2"], test_constants.TEST_DICT["key2"]())

    def test_thunkable_init(self):
        test_dict = ThunkDict(
            dictionary={"key1": test_constants.calling_function})
        self.assertEqual(test_dict["key1"], test_constants.additional_callback)
        # Ensure that double access does not accidently call additional_callback
        self.assertEqual(test_dict["key1"],
                         test_constants.additional_callback)


class TestSetAndGet(unittest.TestCase):
    def test_get_item(self):
        test_dict = ThunkDict(dictionary=test_constants.TEST_DICT)

        self.assertEqual(test_dict["key1"], test_constants.TEST_DICT["key1"])
        self.assertEqual(test_dict["key2"], test_constants.TEST_DICT["key2"]())

    def test_set_and_get_nonwrappable(self):
        test_dict = ThunkDict()
        test_dict["key1"] = test_constants.TEST_DICT["key1"]

        self.assertNotIsInstance(
            test_dict.__dictionary__["key1"], ThunkDict.__LazyInternal__)
        self.assertEqual(test_dict["key1"], test_constants.TEST_DICT["key1"])

    def test_set_and_get_wrappable(self):
        test_dict = ThunkDict()
        test_dict["key1"] = test_constants.calling_function

        self.assertEqual(test_dict["key1"],
                         test_constants.additional_callback)
        # Ensure that double access does not accidently call additional_callback
        self.assertEqual(test_dict["key1"],
                         test_constants.additional_callback)
