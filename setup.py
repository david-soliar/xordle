from setuptools import setup, find_packages

setup(
    name="xordle_solver",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.10",
    author="David Soliar",
    author_email="dav.soliar@gmail.com",
    description="xordle",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
