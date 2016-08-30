# Django Multi-Language Setup.
By: Bartlomiej Mika
Date: April, 28th, 2015


## Pre-Setup

Install gettext GNU tools with Homebrew using Terminal

Install Homebrew :

  ```
  /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  ```

Install GNU gettext :

  ```
  brew install gettext
  ```

Create symlink :

  ```
  brew link gettext --force
  ```

Source: http://stackoverflow.com/a/35101851



## Setup
1. Go to settings.py file.


2. Make sure this is set.
  ```
  USE_I18N = True
  ```


3. Enables language selection based on request by finding the 'MIDDLEWEAR_CLASSES' section and append:
  ```
  'django.middleware.locale.LocaleMiddleware',
  ```


4. Add LOCALE_PATHS, this is where your translation files will be stored:
  ```
  LOCALE_PATHS = (
      os.path.join(BASE_DIR, "locale"),
  )
  ```


5. Set LANGUAGES that you will be translating the site to:
  ```
  ugettext = lambda s: s
  LANGUAGES = (
      ('en', ugettext('English')),
      ('fr', ugettext('French')),
      ('es', ugettext('Spanish')),
  )
  ```


6. Add i18n template context processor, requests will now include LANGUAGES and LANGUAGE_CODE:
  ```
  TEMPLATE_CONTEXT_PROCESSORS = (
      ....
      'django.core.context_processors.i18n', # this one
  )
  ```

7. Now go to the urls.py file. In url_patterns, add the below, it will enable the set language redirect view:
  ```
  url(r'^i18n/', include('django.conf.urls.i18n')),
  ```


8. Add the following imports, and encapsulate the urls you want translated with i18n_patterns. Here is what mine looks like:
  ```
  from django.conf.urls.i18n import i18n_patterns
  from django.utils.translation import ugettext_lazy as _

  urlpatterns = patterns('',
      url(r'^admin/', include(admin.site.urls)),
      url(r'^i18n/', include('django.conf.urls.i18n')),
  )

  urlpatterns += i18n_patterns('',
      (_(r'^dual-lang/'), include('duallang.urls')),
      (r'^', include('home.urls')),
  )



## How to us:
1. You can wrap text that you want translated in your other files, such as models.py, views.py etc.. Here is an example model field with translations for label and help_text:
  ```
  name = models.CharField(_('name'), max_length=255, unique=True, help_text=_("Name of the FAQ
  ```

2. Now you can go into your templates and load the i18n templatetag and use trans and transblock on the static stuff you want to translate. Here is an example:
  ```
  {% load i18n %}

  {% trans "This is a translation" %}<br><br>
  {% blocktrans with book_t='book title'|title author_t='an author'|title %}
  This is {{ book_t }} by {{ author_t }}. Block trans is powerful!
  {% endblocktrans %}
  ```

3. Now run a makemessages for each of your locales:
  ```
  ./manage.py makemessages -l fr
  ./manage.py makemessages -l es
  ```

4. And now all is left is to go into your /locales folder, and edit each of the .po files. Fill in the data for each msgstr. Here is one such example of that:

  ```
  msgid "English"
  msgstr "Angielski"
  ```

5. And finally compile the messages:
  ```
  ./manage.py compilemessages
  ```



**********
* SOURCE *
**********
https://docs.djangoproject.com/en/dev/topics/i18n/
http://stackoverflow.com/a/26520044
