![alt tag](https://github.com/Oinweb/fly-django/blob/master/docs/media/oin-fly-logo-small.png)

# fly-django
[![Build Status](https://travis-ci.org/Oinweb/fly-django.svg?branch=master)](https://travis-ci.org/Oinweb/fly-django) [![Coverage Status](https://coveralls.io/repos/github/Oinweb/fly-django/badge.svg?branch=master)](https://coveralls.io/github/Oinweb/fly-django?branch=master)


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
See [requirements.txt](https://github.com/Oinweb/fly-django/blob/master/requirements.txt) for more information.

## Build Instructions
### Application
For Linux, FreeBSD and OS X users, run these commands:

1. First clone the project locally and then go into the directory

  ```bash
  git clone https://github.com/Oinweb/fly-django.git
  cd fly-django
  ```


2. Setup our virtual environment

  **OS X Environment:**

  ```bash
  python3 -m venv env
  ```

  **Linux or FreeBSD Environment:**

  ```bash
  virtualenv env
  ```


3. Activate virtual environment

  ```bash
  source env/bin/activate
  ```


4. **OS X USERS ONLY:** If you are using *Postgres.app*, you’ll need to have *pg_config* setup in your *$PATH*. If you already have set this up, skip this step, else simply run this command in the console to set the path manually.


  ```bash
  export PATH="/Applications/Postgres.app/Contents/Versions/9.4/bin:$PATH"
  ```


5. Now lets install the libraries this project depends on.

  ```bash
  pip install -r requirements.txt
  ```



### Database
We are almost done! Just follow these instructions and the database will be setup for the application to use. Load up your postgres and enter the console. Then to create our database, enter:

  ```sql
  create database fly_db;
  ```

### Application + Database
Run the following command to create your custom settings instance. Note: Please write all your application passwords here as it won't be tracked on git.

  ```bash
  cd fly_project
  cp secret_settings_example.py secret_settings.py
  ```


Run the following commands to populate the database.

  ```bash
  cd ../
  python manage.py migrate
  python manage.py setup_fly
  ```

## Usage
To run the web-app, you’ll need to run the server instance and access the page from your browser.

Start up the web-server:

  ```bash
  source env/bin/activate
  cd src/fly_project
  python manage.py runserver
  ```


In your web-browser, load up the following url
  ```
  http://127.0.0.1:8000/
  ```

Congratulations, you are all setup to run the **fly-django**! Have fun coding!

## License
**fly-django** is licensed under the **Simplified BSD License**. See [LICENSE](https://github.com/Oinweb/fly-django/blob/master/LICENSE) for more information.
