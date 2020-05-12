# Summary
This flask application creates, stores and updates a task database.

# App Files/Folders
## env
Virtual environment directory. To set up, in terminal:  
- create  virtual environment directory (called 'env')  
`virtualenv env`
- enter virtual environment  
`source env/bin/activate`
- install python packages  
  - install single package  
  `*package*==*version*`
  - install list of packages  
    - view packages installed in environment  
    `pip freeze`
    - create requirements.txt with specified packages
    - install packages in text file  
    `python -m pip install -r requirements.txt`
  - install jupyter notebook  
  `pip install ipykernel`  
  `ipython kernel install --user --name=env`  
  `jupyter notebook`
- exit virtual environment  
`deactivate`
- remove virtual environment from jupyter
  - check available kernels  
  `jupyter kernelspec list`
  - remove virtual kernel  
  `jupyter kernelspec uninstall env`

## app.py
Python script with flask. This script does the following:   
- creates instance of flask application
- creates instance of SQLAlchemy database
- specifies functions to be routed through web pages

## test.db
SQLite database file. To create, in terminal:  
- enter python shell  
`python`
- import database package  
`from app import db`
- create database file  
`db.create_all()`
- exit python
`exit()`

## templates
Directory for html scripts. These files organize and display web page content. Files for this app:  
- base.html
  - specifies web page settings and links to css stylesheet
- index.html
  - script for app homepage
  - displays tasks in table
  - creates links for update and delete actions for each task
  - creates text box and submit button for task input
- update.html
  - script for update page
  - creates text box and submit button to update task description

## static
Directory for css, javascript and image subdirectories.
### css
Directory for css scripts. These files style webpage content (html scripts). File for ths app:
- main.css
  - formats margins, tables, text, etc.
### img
Directory for any image files referenced by website.
### js
Directory for javascript files. These files enable enhanced webpage interactivity.

# Deploy App
Create active website for flask application on Heroku.
## local deploy
To test app on local 5000 port, in terminal:  
`export FLASK_APP=*app_filename*`  
`flask run`
## deploy to Heroku
In terminal:  
1. login to heroku account:  
    - ```heroku login```
2. intitiatlize git for app:  
    - ```git init```
3. create Procfile:  
    - ```touch Procfile```
    - within Procfile:  
        - ```web: gunicorn *app_filename*:*app_name_in_file*```
4. create package requirements file:  
    - ```touch requirements.txt```
    - within requirements.txt, include required packages:
        - django
        - gunicorn
        - django-heroku
        - ...python packages used in app
5. create app in heroku:
    - ```heroku create *heroku_app_name*```
6. add files to commit:
    - ```git add .```
7. commit files:
    - ```git commit -m "*commit note*"```
8. push committed files:
    - ```git push heroku master```

# jinja2
Flask template engine. Common jinja2 commands:  
- variable  
{{ --- }}
- block
  - heading block  
  {% block head %}{% endblock %}
  - content  
  {% block body %}{% endblock %}
- copy template to webpage  
{% extends '---.html' %}
- for loop  
{% for --- in ---- %}{% endfor %}
- if statement  
{% if --- %}{% else %}{% endif %}
  - conditional if  
  {% if ---|length == -- %}{% else %}{% endif %}
