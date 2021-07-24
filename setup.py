import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gpxcsv",
    version="0.2.2",
    author="Marcos Huerta",
    author_email="marcos@marcoshuerta.com",
    description="Convert Garmin GPX file to CSV",
    install_requires=["lxml"],
    python_requires=">=3.6",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/astrowonk/gpxcsv",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["gpxcsv=gpxcsv.__main__:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)