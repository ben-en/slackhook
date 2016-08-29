Slackhook
=========

A library for messaging slack from the command line or as a python logger.

Usage
=====

General usage can be found with the -h flag::

    usage: slackhook [-h] [--username USER] [--icon_url URL]
                     TOKEN CHANNEL URL TEXT

    Message slack.

    positional arguments:
      TOKEN            your private token
      CHANNEL          channel to message.
      URL              slack endpoint to access
      TEXT             message text

    optional arguments:
      -h, --help       show this help message and exit
      --username USER  user to message as
      --icon_url URL   optional url to an image that is used as the icon

Example usage::

    slackhook --username ben.ennis ABC23478DEF82 #general <slack url> "My Message"

Current Features
================

Can be used to 1) message users/channels from the command line, 2) message 
users/channels from python programs, or 3) log a given set of messages to a 
user/channel with the standard library logger.

Planned Features
================

- Useful documentation
- Cleaner code
- Inline documentation
- A more intuitive set of arguments
- Tests
