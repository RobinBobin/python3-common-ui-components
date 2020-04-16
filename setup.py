import setuptools

with open("README.md", "r") as fh:
   long_description = fh.read()

setuptools.setup(
   author="Ruben Shalimov",
   author_email="r_shalimov@inbox.ru",
   classifiers=[
      "Programming Language :: Python :: 3",
      "Operating System :: OS Independent"
   ],
   description="tkinter.ttk-based UI components",
   install_requires = [
      "simple-common-utils"
   ],
   long_description=long_description,
   long_description_content_type="text/markdown",
   name="common-ui-components",
   packages=setuptools.find_packages(),
   url="https://github.com/RobinBobin/python3-common-ui-components",
   version="0.7.1"
)
