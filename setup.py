from yoshi import __version__

from setuptools import setup

try:
    from testr.setup_helper import cmdclass
except ImportError:
    cmdclass = {}

setup(name='yoshi',
      author='Jean Connelly, Tom Aldcroft',
      description='ACA catalog evaluator for science targets',
      author_email='jconnelly@cfa.harvard.edu',
      version=__version__,
      zip_safe=False,
      packages=['yoshi'],
      tests_require=['pytest'],
      cmdclass=cmdclass,
      )
