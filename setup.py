from distutils.core import setup

try:
    import pypandoc
    readme = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError, OSError, RuntimeError):
    readme = ''


setup(name="hugpee",
      version="0.1",
      description="A Python module which simplifies the creation of RESTful CRUD endpoints in hug, for peewee models.",
      author="Kostas Dizas",
      author_email="kdizas@gmail.com",
      url="https://github.com/kostasdizas/hugpee",
      license="MIT",
      packages=["hugpee"],
      download_url="https://github.com/kostasdizas/hugpee/tarball/0.1",
      keywords=["", "", ""],
      classifiers=[],
      requires=["hug", "peewee"]
      )
