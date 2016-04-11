import unittest
from lazy_property import *


class LazyClass(object):
    def __init__(self):
        self.counter = 0

    @LazyProperty
    def foo(self):
        self.counter += 1
        return self.counter


lc = LazyClass()


class LazyWritableClass(object):
    def __init__(self):
        self.counter = 0

    @LazyWritableProperty
    def foo(self):
        self.counter += 1
        return 5


lwc = LazyWritableClass()


class LazyPropertyTest(unittest.TestCase):
    def test_cache1(self):
        self.assertEqual(lc.foo, 1,
                         "Counter not incremented after initial call of lazy property")
        self.assertEqual(lc.foo, 1,
                         "Counter incremented after second call of lazy property")

    def test_cache2(self):
        self.assertTrue(hasattr(lc, "_foo"),
                        "The lazy class does not have the cache attribute")

        self.assertEqual(getattr(lc, "_foo"), 1,
                         "The cache attribute doesn't have the correct value")

    def test_delete_cache(self):
        delattr(lc, "_foo")

        self.assertEqual(lc.foo, 2,
                         "Counter not incremented again after deleting the cache attribute")

        self.assertEqual(lc.foo, 2,
                         "Counter incremented again after the second call (after deleting the cache attribute)")


class LazyWritablePropertyTest(unittest.TestCase):
    def test_assignment(self):
        self.assertEqual(lwc.foo, 5, "Wrong value for the attribute...somehow...")

        self.assertEqual(lwc.foo, 5, "Not sure how this would fail, really...")

        self.assertEqual(lwc.counter, 1, "Counter didn't increment correctly")

        lwc.foo = 2

        self.assertEqual(lwc.foo, 2, "Assignment didn't work correctly")

        self.assertEqual(lwc.counter, 1, "The counter is out of whack...")

class DocStringPreservationTest(unittest.TestCase):

    class Foo(object):

        @LazyProperty
        def bar(self):
            """bar's docstring"""
            return 1

    def test_docstring(self):

        f = self.Foo()

        self.assertEqual(f.bar, 1, "Wrong value for the property...somehow...")

        self.assertEqual(self.Foo.bar.__doc__, "bar's docstring",
                         "Docstring is wrong, got '{}'".format(self.Foo.bar.__doc__))

