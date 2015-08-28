lazy_property - A package for making properties lazy
====================================================

`Properties <https://docs.python.org/3.4/library/functions.html#property>`_ are a very useful feature of Python, effectively allowing an attribute to masquerade as a method (with no arguments other than ``self``). However, sometimes we want to store the results of an expensive computation in an attribute. The straightforward way to do it would be something like the following:

::

    import time

    def do_some_big_calculation():
        """Simulating some ginormous calculation going on somewhere..."""
        print("{}: Calculations started...".format(time.time))
        time.sleep(5)
        print("{}: Calculations complete!".format(time.time))
        return 42

    class SomeClass(object):

        def __init__(self):
            self.calculation_value = do_some_big_calculation()

And that certainly works. However, this means that whenever you instantiate an object from ``SomeClass``, you'll perform this calculation each time. That could be problematic...

So, what we really want is for this calculation to only be done when it's needed. In other words, what we want is for this attribute to be **lazy**.

To do that, you can create a property, and a "private" attribute, named ``_calculation_value``, used to cache the result, like so:

::

    class SomeOtherClass(object):

    @property
    def calculation_value(self):

        if not hasattr(self, "_calculation_value"):
            self._calculation_value = do_some_big_calculation()

        return self._calculation_value

This package essentially reduces this down to a decorator:

::

    import lazy_property

    class YetAnotherClass(object):

        @lazy_property.LazyProperty
        def calculation_value(self):

            return do_some_big_calculation()

And when called, the "calculation" is only done once:

::

    In [5]:yac = YetAnotherClass()

    In [6]: yac.calculation_value
    1440798443.228256: Calculations started...
    1440798448.229179: Calculations complete!
    Out[6]: 42

    In [7]: yac.calculation_value
    Out[7]: 42

Note, however, that this property is not writable:

::

    In [8]: yac.calculation_value = "something_else"
    ---------------------------------------------------------------------------
    AttributeError                            Traceback (most recent call last)
    <ipython-input-8-0bbfd01ac59a> in <module>()
    ----> 1 yac.calculation_value = "something_else"

    AttributeError: can't set attribute

That's what the ``LazyWritableProperty`` is for.

::

    class SomethingElse(object):

    @lazy_property.LazyWritableProperty
    def overwritable_calculation_value(self):

        return do_some_big_calculation()

::

    In [9]: se = SomethingElse()

    In [10]: se.overwritable_calculation_value
    1440798779.27305: Calculations started...
    1440798784.274711: Calculations complete!
    Out[10]: 42

    In [11]: se.overwritable_calculation_value
    Out[11]: 42

    In [12]: se.overwritable_calculation_value = "foo"

    In [13]: se.overwritable_calculation_value
    Out[13]: 'foo'

Installation
------------

It's up on PyPI:

::

    pip install lazy-property

Or, to do it the hard way, clone this repo, enter the directory into which you cloned the repo, and do a

::

    python setup.py install


Wait...isn't this a solved problem?
-----------------------------------

Well, yes, but I couldn't find a lazy attribute implementation that clearly implemented laziness in the (fairly simple) way discussed above.