import os
import sys


sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('../optiland/'))

project = 'Optiland'
copyright = '2024, Kramer Harrison'
author = 'Kramer Harrison'
release = '0.2.0'

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
              'sphinx.ext.napoleon',
              "sphinx.ext.intersphinx",
              'sphinx.ext.viewcode',
              'nbsphinx',
              'sphinx_gallery.gen_gallery']

add_module_names = False  # Remove module names from class and function names
autosummary_generate = True  # Automatically generate summaries

templates_path = ['_templates']
modindex_common_prefix = ['optiland.']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

sphinx_gallery_conf = {
     'examples_dirs': 'examples',   # path to example scripts
     'gallery_dirs': 'auto_examples',  # gallery output directory
}

autodoc_mock_imports = ['numpy', 'yaml', 'scipy', 'matplotlib', 'numba',
                        'pandas']

pygments_style = 'sphinx'

# Autodoc configuration: include only public members by default
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "private-members": False,
    "special-members": False,
    "inherited-members": True,
}
