import unittest
import logging

import thunk_dict.tests.test_constants as test_constants
from thunk_dict.ThunkDict import ThunkDict

logger = logging.getLogger("tests")
logger.setLevel("ERROR")


class TestInit(unittest.TestCase):
    def test(self):
        self.assertTrue(self.regular_init())
        self.assertTrue(self.dictlike_init())
        self.assertTrue(self.bad_init())

    def regular_init(self):
        try:
            test_dict = ThunkDict(dictionary=test_constants.TEST_DICT)
            return True
        except BaseException as e:
            logger.error(
                "TestInit.regular_init failed with exception:\n {}".format(e))
            return False

    def dictlike_init(self):
        # Creating a mock dict-like object
        obj = {"key": "value"}

        test_dict = ThunkDict(dictionary=obj)
        return True

    def bad_init(self):
        try:
            test_dict = ThunkDict("not a dictionary")
            logger.error("TestInit.bad_init failed to raise TypeError.")
            return False
        except TypeError:
            return True


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


class TestGet(unittest.TestCase):
    def test(self):
        test_dict = ThunkDict(dictionary=test_constants.TEST_DICT)
        self.assertEqual(test_dict["key1"], test_constants.TEST_DICT["key1"])
        self.assertEqual(test_dict["key2"], test_constants.TEST_DICT["key2"])
        return True


class TestSetAndGet(unittest.TestCase):
    def test(self):
        self.get_item()
        self.set_and_get_nonwrappable()
        self.set_and_get_wrappable()

    def get_item(self):
        test_dict = ThunkDict(dictionary=test_constants.TEST_DICT)

        self.assertEqual(test_dict["key1"], test_constants.TEST_DICT["key1"])
        self.assertEqual(test_dict["key2"], test_constants.TEST_DICT["key2"])

    def set_and_get_nonwrappable(self):
        test_dict = ThunkDict()
        test_dict["key1"] = test_constants.TEST_DICT["key1"]

        self.assertNotIsInstance(
            test_dict.__dictionary__["key1"], ThunkDict.__LazyInternal__)
        self.assertEqual(test_dict["key1"], test_constants.TEST_DICT["key1"])

    def set_and_get_wrappable(self):
        test_dict = ThunkDict()
        test_dict["key1"] = test_constants.calling_function

        self.assertEqual(test_dict["key1"],
                         test_constants.additional_callback)
        # Ensure that double access does not accidently call additional_callback
        self.assertEqual(test_dict["key1"],
                         test_constants.additional_callback)


if __name__ == "__main__":
    unittest.main()
