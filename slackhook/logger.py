import sys
import logging

from slackhook import Slack


class SlackLog(logging.StreamHandler):
    """ Custom logger to message slack based on standard logger API

    ***Note***
    All messages require a pipe ('|') character on which to split. Putting this
    character at the end of the line seems to only result in a blank new line
    following the message, useful for readability.
    """
    def __init__(self, url, token, channel):
        # Initialize the current instance as a logging handler
        logging.Handler.__init__(self)
        # Initialize the slack object
        self.slack = Slack(url, token, channel)

    def flush(self):
        """
        As slack messages are atomic, pass when the logger tries to clear
        the buffer.
        """
        pass

    def emit(self, record):
        """ Write log message to slack """
        try:
            msg = self.format(record) # Apply the log format to the record

            # Find a '|' and split it into an attachment
            attach = None
            if msg.find('|') != -1:
                msg, attachment = msg.split('|')
                attach = [{"text": attachment}]
            self.slack.send_message(msg, attachments=attach)
        except Exception:
            self.handleError(record)


def new_excepthook(log):
    """ When called, returns a function that can be used to replace
    sys.excepthook. See add_slacklog() for usage.
    """
    def excepthook(type, value, traceback):
        log.error("Uncaught exception", exc_info=(type, value, traceback))
    return excepthook


def add_slacklog(url, token, channel):
    """ Demo function for adding a slack logger to a program """
    # Name the logger
    log = logging.getLogger('slackhook')
    # Set the desired global logging level
    log.setLevel(logging.DEBUG)
    # Implement a new hook for uncaught exceptions, directing them through the
    # slack logger
    sys.excepthook = new_excepthook(log)

    # Create two handlers, each with specific formats and conventions. See the
    # standard library for examples of how crazy you can get.

    # Create a handler that logs specifically to stdout
    console_handler = logging.StreamHandler()
    console_handler_formatter = \
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - '
                          '%(message)s')
    console_handler.setFormatter(console_handler_formatter)

    # Create a handler that logs specifically to slack
    slack_handler = SlackLog(url, token, channel)
    # We only want ERROR level messages
    slack_handler.setLevel(logging.ERROR)
    # No need for time (slack has that) or level (only getting one level)
    slack_handler_formatter = logging.Formatter('%(name)s - %(message)s')
    slack_handler.setFormatter(slack_handler_formatter)

    # Add each handler to our logger "log"
    log.addHandler(console_handler)
    log.addHandler(slack_handler)
