# On setting up sphynx doc

Based on [this](https://medium.com/@richdayandnight/a-simple-tutorial-on-how-to-document-your-python-project-using-sphinx-and-rinohtype-177c22a15b5b).

```bash
pip install Sphinx rinohtype
pip install rinohtype

cd scripts/

mkdir docs
cd docs

sphinx-quickstart
```

```bash
make html
sphinx-build -b rinoh source build/rinoh
```
