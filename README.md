THIS PROJECT IS A WIP, IT IS NOT SECURE TO RUN LONG TERM, AND NOT WELL DOCUMENTED

# Ezcv Frontend

This project is to do some digging into the possibility of building out a frontend for ezcv



## Setup

You will need python 3 and pip for python 3

### Install prerequisites

You have two choices:

1. Run `pip install -r requirements.txt`
2. Install the dependencies individually:
   `pip install ezcv` and `pip install flask`



## Templates & Routes

Below is a breakdown for the templates

### index.html

This is the homepage and is invoked whenever a user goes to `/`

### images.html

This is the file that is invoked whenever the user goes to the path `/images`

### editor.html

This is the file that is invoked whenever a user is trying to edit a file with paths at `/content/<filename>` and `/content/<section>/<filename>`

### Static paths

Any paths for files are for the most part proxied to return the file content. Details can be found in `static_file()`. For example `/filename.md` would go into `/content/filename.md` and return the content of the file. 

This is the case for files with the following extensions:

- `.jpg`
- `.png`
- `.md`

There is an exception if the path has `/gallery` at the beginning then it will run `gallery_images()` instead.







