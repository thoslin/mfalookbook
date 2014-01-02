mfalookbook
===========
This is a project I built to try out some technologies like [Flask](flask.pocoo.org), [SQLAlchemy](http://www.sqlalchemy.org/), [Scrapy](http://scrapy.org/) which I've heard for long but never used before.

So basically I scraped data from [/r/malefashionadvice](http://reddit.com/r/malefashionadvice/) with Scrapy and display the data on a site built with Flask. The data is stored in Sqlite and driven by SQLAlchemy. Besides I write a [fabric](http://fabfile.org) script to easily deploy the whole thing to a [Vagrant](http://www.vagrantup.com) box (or your ubuntu server if you've got one).

Here's some tips to get you started:

Set up virtualenv
```
mkvirutalenv mfalookbook
pip install -r mfa/requirements.txt
```

Run the crawler to collect some data
```
workon mfalookbook
scrapy crawl mfa
```

Run app and check out http://0.0.0.0:5000/
```
python runapp.py
```

Deploy to a Vagrant box
```
vagrant up
fab vagrant deploy
```

That's it. Happy hacking!
