from setuptools import setup, find_packages

setup(
    name='CanOrder_JointReplenishment',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy==2.2.3',
        'pandas==2.2.3'
    ],
    entry_points={
        'console_scripts': [
            'your_command=your_module:main_function',
        ],
    },
    author='Jonathan Nicklin',
    author_email='N/A',
    description='Genetic algorithm solution for determining suitable 1-week review order policies',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jonathannicklin/CanOrder_JointReplenishment',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)