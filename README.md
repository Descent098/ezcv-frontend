THIS PROJECT IS A WIP, IT IS NOT SECURE TO RUN LONG TERM, AND NOT WELL DOCUMENTED

## Current TODO's

- [ ] Ability to create files
  - [ ] Based on fields
  - [ ] Enforce required fields
- [ ] Enforce `required_config`
- [ ] Add unified themeing with an app shell
- [ ] Fix image overview themeing
- [ ] Add warning if non-required attributes are filled out when editing a piece of content


# Ezcv Frontend/gui

This project is to do some digging into the possibility of building out a frontend for ezcv

## Setup

You will need python 3 and pip for python 3

### Install from source

1. Clone this repository [https://github.com/Descent098/ezcv-frontend](https://github.com/Descent098/ezcv-frontend)
2. cd into `ezcv-frontend` and run `pip install .`


## Usage

### With existing ezcv project

1. cd into the project directory (where `config.yml` is) and run either `ezcv-frontend` or `ezcv-gui`

### With new ezcv project

1. Create a new folder for your project (when you run the gui it will create all the files for a project)
2. Run `ezcv-gui` or `ezcv-frontend` and fill out the setup form

## Templates & Routes

Below is a breakdown for the templates found in `ezcv_gui/templates`

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



## Notes

Features in the [extensions](https://ezcv.readthedocs.io/en/latest/usage/#included-extensions) section are not visible in the editor (except formulas, but they have a different format). So for example if you create a footnote then it will render correctly when you're done, but won't show any differently in the editor.

