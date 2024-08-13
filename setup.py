from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="PyAissistant",
    version="0.1.8",
    author="Hinx Vietti(Lai)",
    author_email="Hinxvietti@gmail.com",
    description="A Python package designed to provide a user-friendly interface for AI developers working with "
                "Python. This package aims to streamline the integration of AI functionalities into your projects, "
                "making it easier to leverage advanced AI capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HinxCorporation/PyAissistant",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        "ollama-api~=0.1.1",    # hinx vietti dev version for chat api with local run ollama server. chat complete
        "setuptools~=68.2.0",
        "psutil~=6.0.0",
        "tabulate~=0.9.0",
        "colorama~=0.4.6",
        "openai~=1.40.0",
        "requests~=2.32.3",
    ],
)
