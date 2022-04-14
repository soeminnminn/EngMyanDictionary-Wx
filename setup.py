import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="com.s16.engmyandict",
    version="1.0.0",
    author="Soe Minn Minn",
    author_email="soeminnminn@gmail.com",
    description="English-Myanmar Dictionary",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/soeminnminn/EngMyanDictionary-Wx",
    project_urls={
        "Bug Tracker": "https://github.com/soeminnminn/EngMyanDictionary-Wx/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)