django-ban
----------

This is a simple application to restrict access to site by IP.

Installation
============

* Install *ipcalc* library.
* Add ban in you INSTALLED_APPS.
* Add option **BAN_POLICY**:  
  `BAN_POLICY = 'deny,allow'` or `BAN_POLICY = 'allow,deny'`.

  In first case it means that all users are allowed by default,
  second case restricts access to all users who not in *allow* list

  **Default value is 'allow,deny'**

* Add `'ban.middleware.BanningMiddleware'` to your `MIDDLEWARE_CLASSES`.
* Run ./manage.py syncdb, to create necessary tables.
* Add one or more entries to the Allow or Deny lists in the admin
  interface. You can just enter a single IP or use a network mask,
  like this: 213.67.43.0/24

Dependencies
============

* ipcalc >= 0.1 -- http://pypi.python.org/pypi/ipcalc/  
  `easy_install install ipcalc`

TODO
===

* Add a text description to the list items.
