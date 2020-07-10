from setuptools import setup
from setuptools import find_packages

setup(
    name="deeputil",
    version="0.2.10",
    description="Commonly re-used logic kept in one library",
    keywords="deeputil",
    author="Deep Compute, LLC",
    author_email="contact@deepcompute.com",
    url="https://github.com/deep-compute/deeputil",
    license="MIT",
    dependency_links=["https://github.com/deep-compute/deeputil"],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 2.7",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=["repoze.lru", "six"],
    packages=find_packages("."),
    include_package_data=True,
    test_suite="test.suite_maker",
)
