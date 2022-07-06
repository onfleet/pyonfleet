import ast
import pathlib
import setuptools

PROJECT_ROOT = pathlib.Path(__file__).parent


def _get_version():
    with open('onfleet/_meta.py') as meta_file:
        for line in meta_file:
            if line.startswith('__version__'):
                return ast.parse(line).body[0].value.value


VERSION = _get_version() or '0.0.1'
README = (PROJECT_ROOT / 'README.md').read_text()


setuptools.setup(
    name='pyonfleet',
    version=VERSION,
    author='James Li',  # `setuptools` does not support using `author` as a list, nor 'contributors'
    author_email='support@onfleet.com',
    description="Onfleet's Python API Wrapper Package",
    long_description=README,
    long_description_content_type='text/markdown',
    url='http://docs.onfleet.com',
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.json']
    },
    install_requires=[
        'requests', 'ratelimit', 'backoff'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='LICENSE'
)
