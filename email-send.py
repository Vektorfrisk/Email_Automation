import smtplib
from email.message import EmailMessage
import pandas as pd
import math

EMAIL_ADDRESS = 'apps-test@ptc.com'

# --- Defining Email function ---
def send_email():
    msg = EmailMessage()
    msg['Subject'] = 'This is a test email'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_RECIPIENT

    msg.set_content('This is a plain text email')

    msg.add_alternative("""\
    <!DOCTYPE html>
    <html>
        <body>
            <h1 style="color:SlateGray;">This is an HTML Email!</h1>
        </body>
    </html>
    """, subtype='html')

    #with smtplib.SMTP('ptcpo', 25) as smtp:
        #smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    #    smtp.send_message(msg)

    with smtplib.SMTP('localhost', 1025) as smtp:
        smtp.send_message(msg)

# --- Load recipients from CSV ---
RECIPIENTS_FILE = 'recipients.csv'
 
df = pd.read_csv(RECIPIENTS_FILE)
 
recipients = []
for cell in df['Email'].dropna():
    # A cell may hold several addresses separated by ; or ,
    for address in str(cell).replace(',', ';').split(';'):
        address = address.strip()
        if address and address not in recipients:   # skip blanks and duplicates
            recipients.append(address)
    
    if not recipients:
        raise SystemExit(f'No email addresses found in {RECIPIENTS_FILE}')

    EMAIL_RECIPIENT = ', '.join(recipients)
    send_email()       #send email per cell (1 cell should be all emailID of 1 customer)
    recipients.clear()  #reset recipients so next cell ids can be added in for loop
 

    print(f'Sending to: {EMAIL_RECIPIENT}')

