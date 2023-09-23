import os
import sys

sys.path.insert(0, os.path.abspath("../.."))
print(sys.path)
project = "Project Reloaded"
copyright = "Copyright (c) Project"
author = "Project"

version = "1.12"
release = "1.12"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "pipeline.py",
    "main.py",
    "doc_utils.py",
]
autodoc_mock_imports = [
    "pyspark",
    "transforms",
    "Projectrlib",
    "coa",
    "as_designed",
    "expectations",
    "as_built",
    "supbom",
    "data_quality_indicator",
    "digital_costing",
    "as_planned",
]
# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.extlinks",
    "sphinx.ext.viewcode",
]

autodoc_class_signature = "separated"
autodoc_member_order = "bysource"

add_module_names = False
autosummary_generate = True
autodoc_typehints = "both"
autoclass_content = "both"
templates_path = ["_templates"]
exclude_patterns = []
pygments_style = "sphinx"
highlight_language = "python3"

intersphinx_mapping = {
    "python": ("https://docs.python.org/{.major}".format(sys.version_info), None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "matplotlib": ("https://matplotlib.org/stable", None),
    "mayavi": ("http://docs.enthought.com/mayavi/mayavi", None),
    "pyvista": ("https://docs.pyvista.org/", None),
    "sklearn": ("https://scikit-learn.org/stable", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
}
source_suffix = ".rst"
# source_encoding = 'utf-8'

# The master toctree document.
master_doc = "index"
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_short_title = "%s-%s" % (project, version)
html_show_sourcelink = True
html_use_modindex = True
html_logo = "_static/logo.png"
html_theme_options = {
    "logo_only": True,
    "navigation_depth": 1,
    "body_min_width": 1200,
    "style_external_links": True,
}


def skip_util_classes(app, what, name, obj, skip, options):
    if what == "Submodules":
        skip = True
    return skip


def setup(app):
    app.connect("autodoc-skip-member", skip_util_classes)
    app.add_css_file("my_theme.css")
