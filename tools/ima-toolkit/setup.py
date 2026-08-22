from setuptools import setup, find_packages

setup(
    name="ima-toolkit",
    version="1.1.0",
    description="IMA PR Reviewer - AI code review with recovery plan",
    long_description="AI reviewer that scans your code and gives 8/8 score with fixes",
    author="IMA OS",
    url="https://github.com/imaosglobal/Ima-kernel",
    packages=find_packages(),
    py_modules=["ima"],
    entry_points={
        'console_scripts': [
            'ima=ima:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.8',
)
