import setuptools
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="pyonfleet",  
    version= "1.0.3.3",
    author="James Li",
    author_email="support@onfleet.com",
    description="Onfleet's Python API Wrapper Package",
    long_description=README,
    long_description_content_type="text/markdown",
    url="http://docs.onfleet.com",
    packages=setuptools.find_packages(),
    data_files=[
        ("config", ["config/config.json"])
    ],
    include_package_data=True,
    install_requires=[
        "requests", "configparser", "ratelimit", "backoff", "pathlib"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="LICENSE"
)