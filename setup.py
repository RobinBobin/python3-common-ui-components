import setuptools

with open("README.md", "r") as fh:
   long_description = fh.read()

setuptools.setup(
   name="common-ui-components",
   version="0.0.3",
   author="Ruben Shalimov",
   author_email="r_shalimov@inbox.ru",
   description="tkinter.ttk-based UI components",
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://github.com/RobinBobin/python3-common-ui-components",
   packages=setuptools.find_packages(),
   classifiers=[
      "Programming Language :: Python :: 3",
      "Operating System :: OS Independent"
   ]
)
