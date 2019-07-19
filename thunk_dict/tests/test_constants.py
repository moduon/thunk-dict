import time

TEST_DICT = {
    "key1": 1,
    "key2": lambda: "Hello, world"
}


def long_operation():
    time.sleep(0.1)
    return True


def additional_callback():
    return True


def calling_function():
    long_operation()
    return additional_callback
