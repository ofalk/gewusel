Gewusel
=======

Very simplistic Django application with Facebook, Google
authentication allowing scout masters to keep track of points
their patrols achieved during the "Das große Gewusel".

"Das große Gewusel" was a game we played during Pinakarri
(www.pinakarri.at - no longer online), in summer 2016. Pinakarri
was an international Jamboree of the the Lower Austrian scouts and guides.

Use
===

Add subcamps, groups and patrols using the Django management interface.
Let the scout masters login via Facebook, Google (depending on your
social auth configuration), give them the rights to add points (again,
in the Django mangement interface) and you are ready to go.

Configuration
=============

Add the following to your config.py:
- SOCIAL_AUTH_FACEBOOK_KEY = XXX - your Facebook application key - XXX
- SOCIAL_AUTH_FACEBOOK_SECRET = XXX - your Facebook application secret - XXX

- SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = XXX - your Google application key - XXX
- SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = XXX - your Google application secret - XXX

# You can add more addresses to this array
- ADMIN_USERS = ['XXX - your@mail.address.tld - XXX']

Documentation
=============

There's not too much documentation, I'm afraid. However, it's a simple
Django application that you can easily deploy locally (using SQLite
database) or in the Amazon cloud using AWS Elastic Beanstalk. A simple
eb deploy (and depending on your choice the options to add an RDS
database - MySQL only).

Testing
=======

Yes, that's something that is definitely missing...
