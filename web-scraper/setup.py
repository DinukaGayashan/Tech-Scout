import pathlib
from typing import List

from setuptools import find_packages, setup

long_description = pathlib.Path("README.md").read_text()
version = pathlib.Path("../VERSION").read_text().strip()
packages = find_packages(where="tech-scout-scraper")


def parse_requirements(file_name: str) -> List[str]:
    with open(file_name, "r") as f:
        lines = f.read().splitlines()
    return lines


setup(
    name="tech-scout-scraper",
    version=version,
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "tech-scout-scraper"},
    packages=packages,
    install_requires=parse_requirements("requirements.txt"),
    author="Chathurinda Ranasinghe",
    author_email="chathurindaranasinghe@gmail.com",
    maintainer="Dinuka Gayashan",
    maintainer_email="dinukagayashankasthuriarachchi@gmail.com",
    url="https://github.com/DinukaGayashan/TechScout",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
)
