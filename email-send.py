import smtplib
from email.message import EmailMessage
from pandas import read_csv as pd_read_csv
from string import Template

EMAIL_ADDRESS = 'apps-test@ptc.com'
#Email_Body = open('email-body.html', 'r').read()  # Load the HTML email body from a file

# --- Defining Email function ---
def send_email(Subject, Address, Recipient, Name, Environment, Date, Time):
    msg = EmailMessage()
    msg['Subject'] = Subject
    msg['From'] = Address
    msg['To'] = Recipient

    msg.set_content('This is a plain text email')

    with open('email-body.html', 'r') as html:
        template = Template(html.read())

    html_body = template.safe_substitute(
        client_name = Name,
        environment = Environment,
        date = Date,
        time = Time
    )
    msg.add_alternative(html_body, subtype='html')

    #with smtplib.SMTP('ptcpo', 25) as smtp:
        #smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    #    smtp.send_message(msg)

    with smtplib.SMTP('localhost', 1025) as smtp:
        smtp.send_message(msg)

# --- Load recipients from CSV ---
RECIPIENTS_FILE = 'recipients.csv'
 
df = pd_read_csv(RECIPIENTS_FILE)



for name_cell, env_cell, date_cell, time_cell, email_cell in zip(df['Company'], df['Environment'], df['Date'], df['Time'], df['Email'].dropna()):
    recipients = []
    SUBJECT = f"[System Maintenance] :: {str(date_cell).strip()} {str(time_cell).strip()} || {str(name_cell).strip()} | Servigistics | {str(env_cell).strip()}"
    # A cell may hold several addresses separated by ; or ,
    for address in str(email_cell).replace(',', ';').split(';'):
        address = address.strip()
        if address and address not in recipients:   # skip blanks and duplicates
            recipients.append(address)
    
    if not recipients:
        raise SystemExit(f'No email addresses found in {RECIPIENTS_FILE}')

    EMAIL_RECIPIENT = ', '.join(recipients)
    send_email(SUBJECT, EMAIL_ADDRESS, EMAIL_RECIPIENT, name_cell, env_cell, date_cell, time_cell)      #send email per cell (1 cell should be all emailID of 1 customer)
 

    print(f'Sending to: {EMAIL_RECIPIENT}')

