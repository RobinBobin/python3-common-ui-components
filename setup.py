from commonuicomponents.version import __version__
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
   long_description = fh.read()

setup(
   author="Ruben Shalimov",
   author_email="r_shalimov@inbox.ru",
   classifiers=[
      "Programming Language :: Python :: 3",
      "Operating System :: OS Independent"
   ],
   description="tkinter.ttk-based UI components",
   install_requires = [
      "simple-common-utils",
      "stringcase"
   ],
   long_description=long_description,
   long_description_content_type="text/markdown",
   name="common-ui-components",
   packages=find_packages(),
   url="https://github.com/RobinBobin/python3-common-ui-components",
   version=__version__
)
