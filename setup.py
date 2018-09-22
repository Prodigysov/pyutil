import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyutil",
    version="0.2.8",
    author="Pengyu Nie",
    author_email="prodigy.sov@gmail.com",
    description="Python utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prodigysov/pyutil",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=(
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
    ),
    install_requires=["numpy", "PyYAML", "PyGitHub", "unidiff"],
)
