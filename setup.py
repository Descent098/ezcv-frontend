"""Contains all the configuration for the package on pip"""
import setuptools
from ezcv_gui import __version__

def get_content(*filename:str) -> str:
    """Gets the content of a file or files and returns
    it/them as a string
    Parameters
    ----------
    filename : (str)
        Name of file or set of files to pull content from 
        (comma delimited)
    
    Returns
    -------
    str:
        Content from the file or files
    """
    content = ""
    for file in filename:
        with open(file, "r", encoding="utf-8") as full_description:
            content += full_description.read()
    return content

setuptools.setup(
    name = "ezcv_frontend",
    version = __version__,
    author = "Kieran Wood",
    author_email = "kieran@canadiancoding.ca",
    description = "A frontend/gui for ezcv",
    long_description = get_content("README.md", "CHANGELOG.md"),
    long_description_content_type = "text/markdown",
    project_urls = {
        "User Docs" :      "https://ezcv.readthedocs.io",
        "API Docs"  :      "https://kieranwood.ca/ezcv-frontend",
        "Forum":           "https://github.com/Descent098/ezcv-frontend/discussions",
        "Source" :         "https://github.com/Descent098/ezcv-frontend",
        "Bug Report":      "https://github.com/Descent098/ezcv-frontend/issues/new?assignees=Descent098&labels=bug&template=bug_report.md&title=%5BBUG%5D",
        "Feature Request": "https://github.com/Descent098/ezcv-frontend/issues/new?labels=enhancement&template=feature_request.md&title=%5BFeature%5D",
        "Roadmap":         "https://github.com/Descent098/ezcv-frontend/projects"
    },
    include_package_data = True,
    packages = setuptools.find_packages(),
    package_data = {"":["./ezcv_gui/templates/*"]},
    entry_points = { 
            'console_scripts': ['ezcv-gui = ezcv_gui.cli:main','ezcv-frontend = ezcv_gui.cli:main']
        },

    install_requires = [
    "docopt",                # Used for argument parsing if you are writing a CLI
    "ezcv",
    "pyyaml",                # Used for config file parsing
        ],
    extras_require = {
        "dev" : ["mkdocs", # Used to create HTML versions of the markdown docs in the docs directory
                "pdoc3",   # Used to create development docs
                ], 
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ],
)