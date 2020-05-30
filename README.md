# Auction Online
Online auction site

This file contains all instructions how to run the project on your PC locally.

Clone the repo in you directory

The project uses **python 3.7** so if you don’t have you just install with 

> `sudo apt-get install python3.7`

Make sure you have **pipenv** installed otherwise you can do

>  `pip3 install pipenv`

 and make sure you have django installed `pipenv install django`.
 Inside the Auction file run `pipenv shell`. If it doesn’t find python executable you can do

>  `pipenv --python /path/to/python3.7`

Now you are ready to run `pipenv shell`.

## Libraries

> `pip3 install celery`

> `pip3 install redis`

These two libraries are used for checking if any auction is expired. *Uses redis from heroku.com in this case.*

> `pip3 install django-crispy-forms`

> `pip3 install django-bootstrap-datepicker-plus`

> `pip3 install schedule`

> `pip3 install django-background-tasks`

> `pip3 install pillow`

> `pip3 install django-bootstrap4`

> `pip3 install textdistance`

## How to run
You need two terminal windows, one for actual **pipenv shell** other for **celery**.
**First teminal** : 

> `pipenv shell`

> `python manage.py startserver`

**Second terminal** :

> `pipenv shell`

> `celery -A Auction worker -B --loglevel=INFO`

*This starts celery*.

## Unittest
Testing of two functions and a view.

> `python manage.py test products`

> `python manage.py test users`

