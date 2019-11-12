import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CasperCore-KodexDataSystems", # Replace with your own username
    version="0.0.3",
    author="Kodex Data Systems",
    author_email="kodex.data@gmail.com",
    description="A simple tool for interacting with Cardano's "Shelley" Testnet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kodex-Data-Systems/Casper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

)
