import setuptools
from setuptools.command.install import install
from setuptools import Command
import os


class CustomInstall(install):
    """Custom handler for the 'install' command."""

    def run(self):
        # compile c files
        try:
            os.system('pip install -e .')
        except:
            print('Problem installing imf')
        # compile files used for docuemtnation
        #try:
        #    os.system('make _doc')
        #except:
        #    print('Problem compiling html or pdf documenation')
        super(CustomInstall, self).run()


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system("rm -vrf ./build ./dist ./*.pyc ./imfdatapy/imfdatapy.egg-info")


try:
    with open("README.md", "r", encoding="utf-8", errors='ignore') as fh:
        long_description = fh.read()
except:
    long_description = "IMF Data Discovery"

packages = [
    'imfdatapy']

setuptools.setup(
    name="imfdatapy",
    version="1.0",
    author="Sou-Cheng T. Choi and Irina Klein",
    author_email="schoi32@iit.edu",
    license='Apache license 2.0',
    description="IMF Data Discovery API in Python 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Economic-and-Financial-Data-Discovery/imfdatapy",
    download_url="https://github.com/Economic-and-Financial-Data-Discovery/imfdatapy/releases/tag/v1.0.gz",
    packages=packages,
    install_requires=[
        'requests >= 2.28.1',
        'pandas >= 1.0.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"],
    keywords=["IMF data", "JSON API"],
    python_requires=">=3.5",
    include_package_data=True,
    cmdclass={
        'clean': CleanCommand,
        'install': CustomInstall})