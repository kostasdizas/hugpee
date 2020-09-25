import setuptools

with open("README.md", "r") as fh:
    readme = fh.read()


setuptools.setup(
    name="hugpee",
    version="0.1.1",
    description="A Python module which simplifies the creation of RESTful CRUD endpoints in hug, for peewee models.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Kostas Dizas",
    author_email="kdizas@gmail.com",
    url="https://github.com/kostasdizas/hugpee",
    license="MIT",
    packages=setuptools.find_packages(),
    requires=["hug", "peewee"]
)
