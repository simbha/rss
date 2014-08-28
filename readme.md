Overview
========

Creates and maintains an RSS feed for a podcast that I like to listen to (but that doesn't have a full historical RSS feed).

Installation
============

Instructions
------------

Just run `rss.py` whenever you want the feed to update (via cron or whatever), ensure that the target RSS file is network-accessible, then point your feed reader to it.

Requirements
------------

* requests
* PyRSS2Gen
* Beautiful Soup 4

Bugs and Feature Requests
=========================

Feature Requests
----------------

* Does not yet support updating the feed. (It needs to be regenerated from scratch each time.)

Known Bugs
----------

None.

License Information
===================

Written by Gem Newman. [GitHub](https://github.com/spurll/) | [Blog](http://www.startleddisbelief.com) | [Twitter](https://twitter.com/spurll)

This work is licensed under Creative Commons [BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/).
