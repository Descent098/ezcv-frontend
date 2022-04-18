import os
import json
from tempfile import TemporaryDirectory
import webbrowser
import time

from ezcv.core import generate_site
from flask import render_template, Flask, request, redirect, send_file
from jinja2.exceptions import TemplateNotFound


template_dir = 'site' # The folder you want to export your site to

app = Flask(__name__, static_url_path='', static_folder="content",  template_folder="templates")

# Turn these on when you're developing
# app.config["DEBUG"] = True
# app.config['TEMPLATES_AUTO_RELOAD'] = True

def store_markdown_from_response(request, path):
    data = json.loads(str(request.data.decode("utf-8") ))

    with open(f"content/{path}", "w+") as f:
        f.write("---\n")
        for value in data["metadata"]:
            f.write(f"{value}: {data['metadata'][value]}\n")
        f.write("---\n\n")
        f.write(data["content"])

def open_in_browser(url):
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
def preview_site():
    with TemporaryDirectory() as tmpdir:
        generate_site(tmpdir)
        open_in_browser(tmpdir)
        time.sleep(5)

    return redirect("/")

@app.route('/content/gallery/<path>')
def gallery_images(path):
    if path.endswith(".jpg") or path.endswith(".jpeg"):
        return send_file(f"content/gallery/{path}", mimetype='image/jpeg')
    elif path.endswith(".png"):
        return send_file(f"content/gallery/{path}", mimetype='image/png')
    else:
        return send_file(f"content/gallery/{path}")


@app.route('/')
def index():
    """display the homepage"""
    files = {}
    sections = []
    for path in os.listdir("content"):
        if os.path.isdir(f"content/{path}"):
            files[path] = []
            sections.append(path)
    for section in sections:
        for path in os.listdir(f"content/{section}"):
            if path.endswith(".md") or path.endswith(".jpg") or path.endswith(".png"):
                files[section].append(path)
    return render_template("index.html", files=files)


@app.route('/images')
def image_overview():
    files = []
    for path in os.listdir("images"):
        files.append(path)
    return render_template('images.html', files=files)

@app.route('/content/<section>/<path>')
def content_with_section(section, path):
    """display the content"""
    return render_template(f"editor.html", path=f"{section}/{path}")


@app.route('/content/<path>')
def content(path):
    """display the content"""
    return render_template(f"editor.html", path=path)

@app.route('/<section>/<path>', methods=['POST'])
def static_file_with_section(section, path):
    """display the content"""
    if path.endswith(".md"):
        store_markdown_from_response(request, path=f"{section}/{path}")
    return render_template(f"editor.html", path=f"{section}/{path}")

@app.route('/<path>',methods = ['GET', 'POST'])
def static_file(path:str):
    """Takes in a path and tries to return the template file with that title
    So if a user types in /test then it will try to find a template called test.html

    Parameters
    ----------
    path : str
        The path the user puts in the browser
    """
    if path.endswith(".md"):
        if request.method == 'POST':
            store_markdown_from_response(request, path)
        else:
            with open(f"content/{path}", "r") as f:
                return f.read()

    elif path.endswith(".js"):
        with open(f"templates/{path}", "r") as f:
            return f.read()

    elif path.endswith(".css"):
        with open(f"templates/{path}", "r") as f:
            return f.read()

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
