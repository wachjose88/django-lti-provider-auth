import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-lti-provider-auth",
    version="0.0.2",
    author="Josef Wachtler",
    author_email="josef.wachtler@gmail.com",
    description="This is a highly confirgurable LTI provider for django projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wachjose88/django-lti-provider-auth",
    packages=setuptools.find_packages(),
    python_requires='>=3.4',
    install_requires=[
       'lti>=0.9.2',
       'django>=1.11,<2.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
