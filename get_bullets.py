#!/usr/bin/env python

import imaplib
import email
import getpass
import local_settings
from time import localtime, strftime

class Bullets(object):
    """ Someone who sending bullets and their bullets
    """

    def __init__(self, msg):
        """ parse the message and create Bullets object"""
        pass

    @property
    def name(self):
        """ Return presentation name:
        like "Allison" or "Matt Dabrowski"
        """
        return self.name

    @property
    def email(self):
        """ The email we expect this user to send bullets from and also to
        receive bullet reminders at e.g. mgreenway@uchicago.edu """
        return self.email

    @property
    def text(self):
        """ The users bullets example:
        some text blob. """
        return self.text



def sent_today(msg):
    """ Return True if the message was sent today
    """
    return strftime("%a, %d %b %Y", localtime()) == msg["Date"][:-15]


def messages_with(field, search):
    """ Get messages with "bullet" in the subject """

    host = getattr(local_settings, "host", "xmail.uchicago.edu")
    port = getattr(local_settings, "port", 993)

    server = imaplib.IMAP4_SSL(host, port)

    password = getattr(local_settings, "password", None)
    if password is None:
        password = getpass.getpass()

    username = getattr(local_settings, "username", None)
    if username is None:
        username = getpass.getuser()

    server.login(username, password)
    server.select()

    stat, mail = server.search(None, field, search)

    return [email.message_from_string(
        server.fetch(n, '(RFC822)')[1][0][1]) for n in mail[0].split()]


def main():
    """
    Run the main bullet fetch loop
    """
    daily_bullets = []

    for msg in messages_with("subject", "bullet"):
        if sent_today(msg):
            payload = msg.get_payload()
            if not isinstance(payload, basestring):
                payload = payload[0]

            email = msg["From"].split()[-1].strip("<>")
            print email
            daily_bullets.append("%s:\n%s\n" % (local_settings.folks[email], payload))
    print "\n".join(daily_bullets)

if __name__ == "__main__":
    main()
