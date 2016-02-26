![alt tag](https://github.com/Oinweb/py-fly/blob/master/docs/media/oin-fly-logo-small.png)

# py-fly 
[![Build Status](https://travis-ci.org/Oinweb/py-fly.svg?branch=master)](https://travis-ci.org/Oinweb/py-fly) [![Coverage Status](https://coveralls.io/repos/github/Oinweb/py-fly/badge.svg?branch=master)](https://coveralls.io/github/Oinweb/py-fly?branch=master)


## Description
An open-source, cross platform, mobile app, supported by a Django/Python web service, which is meant to teach youth financial literacy in multiple languages, while also introducing them to the concept of entrepreneurship.

## Support
You can support this project by testing the app, submitting tickets via GitHub, and sharing this app via social media.

## Features
- Users can login with social media accounts
- Supports educational videos
- Allows user to set and track financial goals
- Gamification elements, such as badges, levels and XP

## System Requirements
* Python 3.4.x+
* Postgres SQL DB 9.4+

## Dependencies
See [requirements.txt](https://github.com/Oinweb/py-fly/blob/master/requirements.txt) for more information.

## Build Instructions
### Application
For Linux and OSX users, run these commands:

1. First clone the project locally and then go into the directory

  ```
  git clone https://github.com/Oinweb/py-fly.git
  cd py-fly
  ```


2. Setup our virtual environment

  ```
  (OSX)
  python3 -m venv env

  (Linux)
  virtualenv env

  ```


3. Now lets activate virtual environment

  ```
  $ source env/bin/activate
  ```


4. **OSX USERS ONLY:** If you are using *Postgres.app*, you’ll need to have *pg_config* setup in your *$PATH*. If you already have set this up, skip this step, else simply run this command in the console to set the path manually.


  ```
  $ export PATH="/Applications/Postgres.app/Contents/Versions/9.4/bin:$PATH"
  ```
  

5. Now lets install the libraries this project depends on.

  ```
  pip install -r requirements.txt
  ```



### Database
We are almost done! Just follow these instructions and the database will be setup for the application to use. Load up your postgres and enter the console. Then to create our database, enter:

  ```
  create database fly_db;

  ```

### Application + Database
Run the following command to create your custom settings instance. Note: Please write all your application passwords here as it won't be tracked on git.

  ```
  $ cd src/fly_project/fly_project
  $ cp secret_settings_example.py secret_settings.py
  ```


Run the following commands to populate the database.

  ```
  cd src/fly_project
  python manage.py migrate 
  python manage.py setup_fly
  ```

## Usage
To run the web-app, you’ll need to run the server instance and access the page from your browser. 

Start up the web-server:

  ```
  source env/bin/activate
  cd src/fly_project
  python manage.py runserver
  ```


In your web-browser, load up the following url
  ```
  http://127.0.0.1:8000/
  ```

Congratulations, you are all setup to run the **py-fly**! Have fun coding!

## License
**Py-fly** is licensed under the **Simplified BSD License**. See [LICENSE](https://github.com/Oinweb/py-fly/blob/master/LICENSE) for more information.


