from setuptools import find_packages, setup


setup(
    name="widgetastic.bootstrap",
    use_scm_version=True,
    author="Dmitry Misharov",
    author_email="misharov@redhat.com",
    description="Twitter Bootstrap widget library for Widgetastic",
    license="Apache license",
    url="https://github.com/quarckster/widgetastic.bootstrap",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "widgetastic.core>=0.10.0",
    ],
    setup_requires=[
        "setuptools_scm",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
)
