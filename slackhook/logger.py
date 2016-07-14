import sys
import logging

from slackhook import Slack


class SlackLog(logging.StreamHandler):
    """ Custom logger to message slack

    ***Note***
    All messages require a pipe ('|') character on which to split. Putting this
    character at the end of the line seems to only result in a blank new line
    following the message, useful for readability.
    """
    def __init__(self, url, token, channel):
        logging.Handler.__init__(self)
        self.slack = Slack(url, token, channel)

    def flush(self):
        """ Since slack messages are atomic, pass when the buffer tries to clear
        """
        pass

    def emit(self, record):
        try:
            msg = self.format(record)
            attach = None
            if msg.find('|') != -1:
                msg, attachment = msg.split('|')
                attach = [{"text": attachment}]
            self.slack.send_message(msg, attachments=attach)
        except Exception:
            self.handleError(record)


def new_excepthook(log):
    def excepthook(type, value, traceback):
        log.error("Uncaught exception", exc_info=(type, value, traceback))
    return excepthook


def add_slacklog(url, token, channel):
    log = logging.getLogger('slackhook')
    log.setLevel(logging.DEBUG)
    sys.excepthook = new_excepthook(log)

    # create a console handler
    ch = logging.StreamHandler()
    ch_formatter = \
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - '
                          '%(message)s')
    ch.setFormatter(ch_formatter)

    # create a slack handler
    sh = SlackLog(url, token, channel)
    sh_formatter = \
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - '
                          '%(message)s')
    sh.setFormatter(sh_formatter)

    log.addHandler(ch)
    log.addHandler(sh)
