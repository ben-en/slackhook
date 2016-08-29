#!/usr/bin/env python

import json
import argparse
from urllib.request import urlopen, Request


class Slack:
    """ Holds url, token, channel and optionally username or icon_url for ease
    of messaging on slack.
    """
    def __init__(self, url, token, channel, username=None, icon_url=None):
        self.url = url
        self.token = token
        self.channel = channel
        if username:
            self.username = username
        if icon_url:
            self.icon_url = icon_url

    def assemble_url(self, info_json):
        """ Using urllib.request.Request, create a url to open """
        return Request(self.url, data=info_json,
                       headers={'content-type': 'application/json'})

    def send_message(self, text, username=self.username,
                     icon_url=self.icon_url, attachments=None):
        """ Send a message to slack """
        # Create the data that will be used in the message
        info = {
            # From args
            "text": text,
            # From args or class
            "username": username,
            # From class
            "token": self.token,
            "channel": self.channel,
        }
        if icon_url:
            info['icon_url'] = icon_url
        if attachments:
            info['attachments'] = attachments

        # Encode the data, create a url, open it, and return the raw response
        return urlopen(assemble_url(encode_data(info)))


def encode_data(d):
    """ Takes a dictionary and returns a utf8 encoded json string. """
    return json.dumps(d).encode('utf8')


def main():
    """ Creates a one shot message to slack. """
    parser = argparse.ArgumentParser(description='Create a one shot message to slack.')
    parser.add_argument('token', metavar='TOKEN', help='your private token')
    parser.add_argument('channel', metavar='CHANNEL', help='channel to '
                        'message.')
    parser.add_argument('url', metavar='URL', help='slack endpoint to access')
    parser.add_argument('text', metavar='TEXT', help='message text')
    parser.add_argument('--username', metavar='USER', default="slackhookbot",
                        help='user to message as')
    parser.add_argument('--icon_url', metavar="URL", help="optional url to "
                        "an image that is used as the icon")
    args = parser.parse_args()

    # Initialize the slack object and print the response from the message
    s = Slack(args.url, args.token, args.channel)
    resp = s.send_message(args.text, args.username, args.icon_url)
    print(resp.read().decode('utf8'))


if __name__ == "__main__":
    main()
