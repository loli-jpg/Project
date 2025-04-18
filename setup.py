from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
def get_requirements(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            requirements = f.read().splitlines()
    except FileNotFoundError:
        return []
    return [req for req in requirements if req and not req.startswith("#")]


setup(
    name="Project",
    version="0.1.0",
    author="Лоли",
    author_email="loligazd@mail.ru",
    description="Телеграмм-бот для создания плейлиста",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/loli-jpg/Project.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=get_requirements('requirements.txt'),
)
