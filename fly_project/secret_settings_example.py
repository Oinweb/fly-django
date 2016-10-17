import sys

#---------------------------------------------------------------------------#
# Generic                                                                   #
#---------------------------------------------------------------------------#
SECRET_DEBUG = True
SECRET_SECRET_KEY = 'blahblahblahblahblahblahblahblah'
SECRET_ALLOWED_HOSTS = ['*']
SECRET_ADMINS = [('Bart', 'your_name@your_domain.com'),]


#---------------------------------------------------------------------------#
# Email (See: https://www.mailgun.com )                                     #
#---------------------------------------------------------------------------#
SECRET_MAILGUN_ACCESS_KEY = 'ACCESS-KEY'
SECRET_MAILGUN_SERVER_NAME = 'SERVER-NAME'
SECRET_DEFAULT_TO_EMAIL = 'your_email@gmail.com'
SECRET_DEFAULT_FROM_EMAIL = 'your_email@gmail.com'


#---------------------------------------------------------------------------#
# Django-Compressor                                                         #
#---------------------------------------------------------------------------#
SECRET_COMPRESS_ENABLED = True


#---------------------------------------------------------------------------#
# Amazon S3                                                                 #
#---------------------------------------------------------------------------#
SECRET_AWS_STORAGE_BUCKET_NAME = ''
SECRET_AWS_ACCESS_KEY_ID = ''
SECRET_AWS_SECRET_ACCESS_KEY = ''


#---------------------------------------------------------------------------#
# Python Social Auth (Third Party)                                          #
#---------------------------------------------------------------------------#
# Facebook ( http://developers.facebook.com )
SECRET_SOCIAL_AUTH_FACEBOOK_KEY = 'your app client id'
SECRET_SOCIAL_AUTH_FACEBOOK_SECRET = 'your app client secret'
SECRET_SOCIAL_AUTH_FACEBOOK_SCOPE = ['public_profile', 'email', ]
SECRET_SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'us_EN'}

# Twitter ( https://apps.twitter.com/app/new )
SECRET_SOCIAL_AUTH_TWITTER_KEY = ''
SECRET_SOCIAL_AUTH_TWITTER_SECRET = ''

# Google ( https://console.developers.google.com/ )
SECRET_SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SECRET_SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''



#---------------------------------------------------------------------------#
# django-htmlmin (See: https://github.com/cobrateam/django-htmlmin )        #
#---------------------------------------------------------------------------#
SECRET_HTML_MINIFY = True
SECRET_KEEP_COMMENTS_ON_MINIFYING = False
