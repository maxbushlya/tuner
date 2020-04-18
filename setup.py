from distutils.core import setup
import py2exe

setup(
    name="tuner",
    author="Max Bushlya",
    windows=[{"script":"tuner.py"}],
    options={"py2exe": {"includes":["sip"]}}
)