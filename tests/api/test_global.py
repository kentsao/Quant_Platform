TEST_GLOBAL = "original"

def modify_global():
    global TEST_GLOBAL
    TEST_GLOBAL = "modified"

def check_global():
    print(f"Global value inside check_global: {TEST_GLOBAL}")

modify_global()
check_global()

import pytest

@pytest.fixture
def simple_fixture():
    return 1

def test_something(simple_fixture):
    assert simple_fixture == 1