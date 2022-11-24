from setuptools import find_packages, setup

__version__ = '1.0.3'

tests_require = [
    "flake8==3.9.2",
    "nose==1.3.7"
]

with open('README.md', 'r') as fh:
    long_description = fh.read()


setup(
    name='next-app-kit',
    author="29next",
    author_email="dev@29next.com",
    url='https://github.com/29next/app-kit',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=__version__,
    install_requires=[
        "PyYAML>=5.4",
        "requests>=2.25",
        "python-decouple>=3.6"
    ],
    entry_points={
        'console_scripts': [
            'nak = nak.nak:main',
        ],
    },
    packages=find_packages(),
    python_requires='>=3.6'
)
