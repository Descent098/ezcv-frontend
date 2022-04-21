# First Party Dependencies
import os                               # Used in path manipulation
import json
from re import M                             # Used to parse & send JSON
import time                             # Used to force sleep when previewing
import webbrowser                       # Used to open installed webbrowsers on client
from typing import Union                # Used to indicating types when there are multiple types 
from tempfile import TemporaryDirectory # Used to generate a temporary directory for the preview

# Third Party Dependencies
import yaml                                     # For reading the config file
from ezcv.core import generate_site             # Used to generate the preview
from jinja2.exceptions import TemplateNotFound  # Used to catch errors when loading a template file
## Used for all forms of HTTP interactions
from flask import render_template, Flask, request, redirect, send_file, Request, Response


template_dir = 'site' # The folder you want to export your site to

app = Flask(__name__, static_url_path='', static_folder="content",  template_folder="templates")

# Turn these on when you're developing
# app.config["DEBUG"] = True
# app.config['TEMPLATES_AUTO_RELOAD'] = True


def store_markdown_from_response(request:Request, path:str):
    """Takes in a POST request and stores the markdown in the file at specified path

    Parameters
    ----------
    request : Request
        The POST request and all it's data

    path : str
        The path to the file to store the markdown in
    """
    data = json.loads(str(request.data.decode("utf-8") ))
    with open(f"content/{path}", "w+") as f:
        f.write("---\n")
        for value in data["metadata"]:
            f.write(f"{value}: {data['metadata'][value]}\n")
        f.write("---\n\n")
        f.write(data["content"])


def open_in_browser(url:str):
    """Opens url in whichever browser is installed"""
    browser_types = ["chromium-browser", "chromium", "chrome", "google-chrome", "firefox", "mozilla", "opera", "safari"] # A list of all the types of browsers to try
    for browser_name in browser_types:   # Look for which browser is installed
        try:
            webbrowser.get(browser_name) # Search for browser
            break                        # Browser has been found
        except webbrowser.Error:         # Browser wasn't found
            continue
    if not url.startswith("http://") and not url.startswith("https://"):
        webbrowser.open(f"file://{url}/index.html", new=2) # Open the preview in the browser
    else:
        webbrowser.open(url, new=2) # Open the preview in the browser


@app.route('/preview')
def preview_site() -> Response:
    with TemporaryDirectory() as tmpdir:
        generate_site(tmpdir)
        open_in_browser(tmpdir)
        time.sleep(60.0)
    return redirect("/")


@app.route('/content/gallery/<path>')
def gallery_images(path:str) -> Response:
    if path.endswith(".jpg") or path.endswith(".jpeg"):
        return send_file(f"content/gallery/{path}", mimetype='image/jpeg')
    elif path.endswith(".png"):
        return send_file(f"content/gallery/{path}", mimetype='image/png')
    else:
        return send_file(f"content/gallery/{path}")


@app.route('/config', methods=['GET', 'POST'])
def config_page() -> Union[Response, str]:
    if request.method == 'GET':
        with open('config.yml') as file:
            data = yaml.safe_load(file)
        return json.dumps(data)
    elif request.method == 'POST':
        data = json.loads(str(request.data.decode("utf-8") ))
        with open('config.yml', 'w+') as file:
            file.write("# See https://ezcv.readthedocs.io for documentation\n")
            yaml.dump(data, file)
        return redirect("/")


@app.route('/setup', methods=['GET', 'POST'])
def setup() -> str:
    if request.method == "GET":
        return render_template("setup-form.html")
    elif request.method == "POST":
        data = json.loads(str(request.data.decode("utf-8") ))
        with open('config.yml', 'w+') as file:
            file.write("# See https://ezcv.readthedocs.io for documentation\n")
            yaml.dump(data, file)
        return redirect("/")


@app.route('/')
def index() -> str:
    """display the homepage"""
    files = {}
    sections = []
    for path in os.listdir("content"):
        if os.path.isdir(f"content/{path}"):
            files[path] = []
            sections.append(path)
    for section in sections:
        #TODO: add in examples toggle to show in main page
        for path in os.listdir(f"content/{section}"):
            if path.endswith(".md") or path.endswith(".jpg") or path.endswith(".png"):
                files[section].append(path)
    return render_template("index.html", files=files)


@app.route('/images')
def image_overview() -> str:
    """Displayes an overview page of all images

    Returns
    -------
    str
        The rendered template of all images
    """
    files = []
    for path in os.listdir("images"):
        files.append(path)
    return render_template('images.html', files=files)


@app.route('/content/<section>/<path>')
def content_with_section(section:str, path:str) -> str:
    """The route to return the editor with the specified file

    Parameters
    ----------
    section : str
        The section the file belongs to i.e. education, experience, etc.

    path : str
        The path of the file to be rendered i.e. filename.md

    Returns
    -------
    str
        The template with the specified file in an editor
    """
    return render_template(f"editor.html", path=f"{section}/{path}")


@app.route('/content/<path>')
def content(path:str) -> str:
    """display the content"""
    return render_template(f"editor.html", path=path)


@app.route('/<section>/<path>', methods=['POST'])
def static_file_with_section(section:str, path:str) -> str:
    """The route to return the editor with the specified file

    Parameters
    ----------
    section : str
        The section the file belongs to i.e. education, experience, etc.

    path : str
        The path of the file to be rendered i.e. filename.md

    Returns
    -------
    str
        The template with the specified file in an editor
    """
    if path.endswith(".md"):
        store_markdown_from_response(request, path=f"{section}/{path}")
    return render_template(f"editor.html", path=f"{section}/{path}")


@app.route('/<path>',methods = ['GET', 'POST'])
def static_file(path:str) -> Union[str, bytes]:
    """Takes in a path and tries to return the template file with that title
    So if a user types in /test then it will try to find a template called test.html

    Parameters
    ----------
    path : str
        The path the user puts in the browser

    Returns
    -------
    str or bytes:
        The file contents as bytes or a string
    """
    if path.endswith(".md"):
        if request.method == 'POST':
            store_markdown_from_response(request, path)
        else:
            with open(f"content/{path}", "r") as f:
                return f.read()

    # If the file is a static file that can be returned as strings
    elif path.endswith(".js"):
        with open(f"templates/{path}", "r", encoding="utf-8") as f:
            return f.read()
    elif path.endswith(".css"):
        with open(f"templates/{path}", "r", encoding="utf-8") as f:
            return f.read()

    # If the file is a static file that can be returned as bytes
    elif path.endswith(".jpg"):
        with open(f"images/{path}", "rb") as f:
            return f.read()
    elif path.endswith(".png"):
        with open(f"images/{path}", "rb") as f:
            return f.read()

    try:
        return render_template(f"{path}.html")
    except TemplateNotFound:
        try: # Try to look for a 404 page
            return render_template("404.html")
        except TemplateNotFound: # If no 404 page exists, return a generic 404 page
            return """<div style='font-size: XXX-large;text-align: center;'>
            <h1>404 page not found</h1>
            </br>
            <button onclick='history.go(-1)'> Click to go back</button>
            </div>"""

if __name__ == '__main__':
    open_in_browser("http://localhost:5000")
    app.run(host='localhost', port=5000)
