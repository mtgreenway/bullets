#!/usr/bin/env python

import imaplib
import email
import getpass
import local_settings
from time import localtime, strftime
import smtplib
import sys
from email.mime.text import MIMEText
import html2text


def today():
    return strftime("%a, %d %b %Y", localtime())

def today_():
    return strftime("%d-%b-%Y", localtime())


def sent_today(msg):
    """ Return True if the message was sent today
    """
    return today() == msg["Date"][:-15]


def messages_with(search):
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
    server.select("bullets")

    stat, mail = server.search(None, search)

    return [email.message_from_string(
        server.fetch(n, '(RFC822)')[1][0][1]) for n in mail[0].split()]

def trim_message(msg):
    """ Remove certain patterns from the email """
    if not isinstance(msg, basestring):
        msg = msg[0]
        msg = msg.as_string()

    if msg.startswith("<html>"):
        msg = html2text.html2text(msg)
    msg = msg.replace("\r", "")

    explode = msg.split("\n")
    for i, val in enumerate(explode):
        for ign in ["From nobody", "Content-Type:",
                "Content-Transfer-Encoding:"]:
            if val.startswith(ign):
                explode[i] = ""
        if val == '':
            break
    for _ in range(explode.count("")):
        explode.remove("")

    return "\n".join(explode)

def fetch_bullets():
    """
    Run the main bullet fetch loop
    """
    daily_bullets = []
    senders = set()

    #for msg in messages_with("(senton %s) (subject bullet)" % today_()):
    for msg in messages_with("(senton %s) (subject bullet)" % today_()):
    #for msg in messages_with("(subject bullet)" ):
        if sent_today(msg):
            payload = trim_message(msg.get_payload())

            email = msg["From"].split()[-1].strip("<>")
            if email in local_settings.folks:
                senders.add(email)
                daily_bullets.append("%s:\n%s\n" % (local_settings.folks[email], payload))

    return  "\n".join(daily_bullets), set(local_settings.folks.keys()) - senders


def main():
    #bullets, didnt_send = fetch_bullets()
    bullets, _ = fetch_bullets()
    if len(sys.argv) == 2 and sys.argv[1] == "-r":
        didnt_send = set(["mgreenway@uchicago.edu"])
        msg = MIMEText("Please send me your bullets")
        msg['Subject'] = 'Bullets'
        msg['From'] = "<%s>" % local_settings.sender
        msg['To'] = ", ".join(list(didnt_send))
        server = smtplib.SMTP_SSL(host="authsmtp.uchicago.edu", port=465)
        server.login(local_settings.username, local_settings.password)
        server.sendmail("mgreenway@uchicago.edu", list(didnt_send), msg.as_string())
    else:
        print bullets

if __name__ == "__main__":
    main()
