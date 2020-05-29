import setuptools

VERSION = "0.4.0"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qaws",
    version=VERSION,
    author="Jiri Kacirek",
    author_email="kacirek.j@gmail.com",
    description="Search AWS CloudWatch Logs with Insights queries, flexible time ranges and wildcards in log group names from your command line.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kacirekj/saws",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['qaws=qaws.qaws:main'],
    },
    install_requires=[
        'boto3'
    ],
)
