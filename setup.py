import setuptools
from lazy_property import __version__

setuptools.setup(
    name='lazy-property',
    version=__version__,
    packages=setuptools.find_packages(),
    url='https://github.com/jackmaney/lazy-property.git',
    license='MIT',
    author='Jack Maney',
    author_email='jackmaney@gmail.com',
    description='Makes properties lazy (ie evaluated only when called)'
)
