from setuptools import setup
from setuptools import find_packages

setup(
    name="deeputil",
    version="0.2.2",
    description="Commonly re-used logic kept in one library",
    keywords="deeputil",
    author="Deep Compute, LLC",
    author_email="contact@deepcompute.com",
    url="https://github.com/deep-compute/deeputil",
    license='MIT',
    dependency_links=[
        "https://github.com/deep-compute/deeputil",
    ],
    install_requires=[
        "repoze.lru",
    ],
    packages=find_packages('.'),
    include_package_data=True,
    test_suite = 'test.suite_maker'
)
