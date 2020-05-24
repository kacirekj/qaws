import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qaws",
    version="0.0.1",
    author="Jiri Kacirek",
    author_email="kacirek.j@gmail.com",
    description="Search AWS CloudWatch Logs with Insights queries and flexible time ranges from your command line.",
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
)
