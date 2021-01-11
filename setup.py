import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ansible-mdgen-murphy.petercl", # Replace with your own username
    version="0.0.1",
    author="Peter Murphy",
    author_email="murphy.petercl@gmail.com",
    description="A python package to automate documentation generation for ansible roles.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/murphypetercl/ansible-mdgen",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pyyaml',
        'mdutils'
    ],
)