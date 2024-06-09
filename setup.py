from setuptools import setup, find_packages

setup(
    name = 'dsp_bp',
    version = '0.1.0',
    packages = find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            # Define any command-line scripts here
        ],
    },
    # Additional metadata
    author = 'Rasmus Stagsted',
    author_email = 'rasmuskarnoestagsted@gmail.com',
    description = 'This is a small project to generate blueprint to the game Dyson Sphere Program (DSP)',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/RasmusStagsted/dsp_bp_generator',
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU GENERAL PUBLIC LICENSE',
        'Operating System :: OS Independent',
    ],
    python_requires = '>=3.8.10',
)