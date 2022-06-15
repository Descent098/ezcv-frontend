usage ="""Usage:

ezcv-gui [-h] [-v]

-h, --help show this help message and exit
-v, --version show version and exit
"""

from docopt import docopt
from ezcv_gui.frontend import app, open_in_browser
from ezcv_gui.__init__ import __version__ as version

def main():
    args = docopt(usage, version=version)
    open_in_browser("http://localhost:5000")
    app.run(host='localhost', port=5000)
if __name__ == "__main__":
    main()

