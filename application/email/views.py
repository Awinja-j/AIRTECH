import os
import smtplib

login = os.environ.get("LOGIN")
password = os.environ.get("PASSWORD")
from_addr = os.environ.get("FROM_ADDRESS")
smtpserver ='smtp.gmail.com:587'

def email_type(type, customer, date, seat):
      if type is 'reminder':
        return 'Dear {}'.format(customer)
      else:
        return 'Dear {}'.format(customer)

def sendemail(to_addr_list, subject, date, seat):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + email_type(subject, to_addr_list, date, seat )

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems
