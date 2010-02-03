django-ban
----------

This is a simple application to restrict access to site by IP.

Installation
============

* Install *ipcalc* library (`pip install ipcalc`).
* Add `ban` in you INSTALLED_APPS.
* Add `'ban.middleware.DenyMiddleware'` to your `MIDDLEWARE_CLASSES` to deny
users on the Denied IP list.
* Add `'ban.middleware.AllowMiddleware'` to your `MIDDLEWARE_CLASSES` to only allow
users on the Allowed IP list.
* Run ./manage.py syncdb, to create necessary tables.
* Add one or more entries to the Allow or Deny lists in the admin
  interface. You can just enter a single IP or use a network mask,
  like this: 213.67.43.0/24

Dependencies
============

* `ipcalc >= 0.1`
