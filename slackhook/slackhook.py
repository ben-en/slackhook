#!/usr/bin/env python

import json
import argparse
from urllib.request import urlopen, Request


class Slack:
    def __init__(self, url, token, channel):
        self.url = url
        self.token = token
        self.channel = channel

    def build_request(self, info):
        """
        Takes the dict `info` and turns it into a json dump. Uploads with
        requests module, and returns the response.
        """
        params = json.dumps(info).encode('utf8')
        req = Request(
                      self.url,
                      data=params,
                      headers={'content-type': 'application/json'},
                     )
        return req

    def send_message(self, text, username, icon_url, attachments=None):
        """ text and username should not be None, but icon_url may be None. """
        info = {
            "text": text,
            "token": self.token,
            "channel": self.channel,
            "username": username,
        }
        if icon_url:
            info['icon_url'] = icon_url
        if attachments:
            info['attachments'] = attachments
        req = self.build_request(info)
        response = urlopen(req)
        return response


def main():
    """ Creates a one shot message to slack. """
    parser = argparse.ArgumentParser(description='Message slack.')
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
    s = Slack(args.url, args.token, args.channel)
    resp = s.send_message(args.text, args.username, args.icon_url)
    print(resp.read().decode('utf8'))


if __name__ == "__main__":
    main()
