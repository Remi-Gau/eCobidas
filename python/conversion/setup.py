from setuptools import setup


def readfile(filename):
    with open(filename, "r+") as f:
        return f.read()


setup(
    name="conversion",
    version="2021.06.05",
    description="",
    long_description=readfile("README.md"),
    author="Rémi Gau",
    author_email="remi.gau@gmail.com",
    url="",
    py_modules=["conversion"],
    license=readfile("LICENSE"),
    entry_points="""
        [console_scripts]
        convert_to_schema=convert_csv_to_schema:convert_to_schema
    """,
)