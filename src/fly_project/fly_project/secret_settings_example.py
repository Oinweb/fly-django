import sys

#---------------------------------------------------------------------------#
# Generic                                                                   #
#---------------------------------------------------------------------------#
SECRET_DEBUG = True
SECRET_SECRET_KEY = 'blahblahblahblahblahblahblahblah'
SECRET_ALLOWED_HOSTS = ['*']
SECRET_ADMINS = [('Bart', 'your_name@your_domain.com'),]


#---------------------------------------------------------------------------#
# Database                                                                  #
#---------------------------------------------------------------------------#
SECRET_DB_USER = "django"
SECRET_DB_PASSWORD = "123password"
SECRET_DB_HOST = "localhost"
SECRET_DB_PORT = "5432"


#---------------------------------------------------------------------------#
# Email                                                                     #
#---------------------------------------------------------------------------#
SECRET_EMAIL_HOST = ''
SECRET_EMAIL_PORT = 587
SECRET_EMAIL_HOST_USER = ''
SECRET_EMAIL_HOST_PASSWORD = ''


#---------------------------------------------------------------------------#
# Python Social Auth (Third Party)                                          #
#---------------------------------------------------------------------------#
# Facebook ( http://developers.facebook.com )
SECRET_SOCIAL_AUTH_FACEBOOK_KEY = 'your app client id'
SECRET_SOCIAL_AUTH_FACEBOOK_SECRET = 'your app client secret'
SECRET_SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', ] 
SECRET_SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'us_EN'}
# Twitter ( https://apps.twitter.com/app/new )
SECRET_SOCIAL_AUTH_TWITTER_KEY = ''
SECRET_SOCIAL_AUTH_TWITTER_SECRET = ''
# Google ( https://console.developers.google.com/ )
SECRET_SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SECRET_SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

#---------------------------------------------------------------------------#
# PayPal Settings                                                           #
#---------------------------------------------------------------------------#
SECRET_PAYPAL_RECEIVER_EMAIL = "yourpaypalemail@example.com"
SECRET_PAYPAL_TEST = True # Note: If True, be sure to use your test email.

#---------------------------------------------------------------------------#
# Google Analytics Settings                                                 #
#---------------------------------------------------------------------------#
#Note: Leaving it blank turns of analytics in the store.
SECRET_GOOGLE_ANALYTICS_KEY = "UA-xxxxxxxx-y"