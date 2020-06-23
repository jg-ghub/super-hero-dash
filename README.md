
# Super Hero Dashboard

A simple bootstrap web application to super heroes spanning every imagination from Star Wards to Marvel comic series. Please visit [Super Hero Dashboard](https://super-hero-test.herokuapp.com) hosted by [Heroku](https://heroku.com).

Credit to [TwentyEight10](http://jommaz.github.io) for allowing access to their free tier [Super Hero API](https://superheroapi.com) - for which this project wouldn't be possible without.

This dashboard allows for persistence layer flexibility, made completely possible by [SQL Alchemy ORM](https://www.sqlalchemy.org/). The web framework utilizes [Flask](https://flask.palletsprojects.com/en/1.1.x) to speak with the front web interface written in [JQuery](https://jquery.com). Data visualizations facilitated with [Plotly](https://plotly.com) interactive graphing library.

## Local Setup
This dashboard can be installed locally by simply pulling this repository, and running the `app.py` script with pyton.

```
$ git pull https://github.com/jg-ghub/super-hero-dash.git
$ pip install -r super-hero-dash/requirements.txt
$ python super-hero-dash/app.py
```

By default, SQLite will be the defaulted RDBMS for this application. No Data will exist in this application, but a helper script has been developed to pull Super Hero data from the _Super Hero API_.

> **Note**
> A token to access this Data is required before the data can be pulled. Please visit [Super Hero API](https://superheroapi.com) to register for your access token prior to running the following.

```
$ export API_TOKEN=<INSERT SUPER HERO API TOEKN HERE>
$ python super-hero-dash/data_pull.py
```

If you wish to store this data on a persistence layer other than SQLite, the following configurations need to be exported as environment variables.

```
$ echo "
  DB_USER=<INSERT DATABASE USERNAME HERE [Optional]>
  DB_PASS=<INSERT DATABASE USER PASSWORD HERE [Optional]>
  DB_HOST=<INSERT DATABASE HOST HERE [Default: localhost]>
  DB_PORT=<INSERT DATABASE HOST PORT HERE [Optional]>
  DB_NAME=<INSERT DATABASE NAME HERE [Default: super_hero_db]>
  DB_SCHEMA=<INSERT DATABASE SCHEMA HERE [Default: sqlite]>
  " > super-hero-dash/local.env

$ export $(cat super-hero-dash/local.env) && python super-hero-dash/app.py
```

> **Note**
> For more information about SQL Alchemy connection strings, please visit [SQL Alchemy Engine configurations](https://docs.sqlalchemy.org/en/13/core/engines.html)

## Cloud Setup
It is recommended to deploy this application on Heroku Free Tier service to leverage their GitHub integration and incredibly simply CI/CD application pipe.

> **Note**
> Please sign up for Heroku's free tier at [Heroku](https://heroku.com) before continuing. Once complete, you should have your application name, which will be referenced within as _\<heroku-app\>_.

Step number 1 - deploy a free-tier cloud managed DB like Postgres on Heroku to store the data pipe from [Super Hero API](https://superheroapi.com). Please follow this [Guide](https://devcenter.heroku.com/articles/heroku-postgresql) to spin up a small free-tier Postgres DB on Heroku.

Once succesfully completed, you should have a connection string formatted like so.

``postgres://<username>:<password>@<host>:<port>/<database>``

Similar to local production, this connections string needs to be formatted into separate environment variables.

```
DB_USER=<username>
DB_PASS=<password>
DB_HOST=<host>
DB_PORT=<port>
DB_NAME=<database>
DB_SCHEMA=postgress (hint: postgres:// at beginning of connection string)
```

This connection configuration needs to be present on the Heroku application service running Flask. Otherwise, the `data_pull.py` nor `app.py` scripts will know which DB to store and query the Super Hero data. This can be completed by running the following lines with the heroku-cli.

> **Note**
> Please visit [Here](https://devcenter.heroku.com/articles/heroku-cli) to learn how to install Heroku Command Line Interface on your development machine

```
$ heroku config:set DB_USER=<username> -a <heroku-app>
$ heroku config:set DB_PASS=<password> -a <heroku-app>
$ heroku config:set DB_HOST=<host> -a <heroku-app>
$ heroku config:set DB_PORT=<port> -a <heroku-app>
$ heroku config:set DB_NAME=<database> -a <heroku-app>
$ heroku config:set DB_SCHEMA=postgress -a <heroku-app>
```

The front end application should now be running, and accessible from the web. Final task left is to populate the Postgres tables. This job can be run once on the local development machine, but recommended to run on Heroku cloud service now that it has been correctly configured.

``
$ heroku run data_pull.py -a <heroku-app>
``

## Footnotes

The incredibly effective drop down search function kindly provided by the [Select2 Javascript Library](https://select2.org/). Python modules statically typed with [PEP-484 Annotations](https://www.python.org/dev/peps/pep-0484/), and styled according to [Google Styling Guide for Python](http://google.github.io/styleguide/pyguide.html). JS styled according to [Google Styling Guide for Javascript](https://google.github.io/styleguide/jsguide.html).
