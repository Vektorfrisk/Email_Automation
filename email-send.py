import smtplib
from email.message import EmailMessage
import pandas as pd

EMAIL_ADDRESS = 'apps-test@ptc.com'

# --- Load recipients from Excel ---
RECIPIENTS_FILE = 'recipients.csv'
 
df = pd.read_csv(RECIPIENTS_FILE)
 
recipients = []
for cell in df['Email'].dropna():
    # A cell may hold several addresses separated by ; or ,
    for addr in str(cell).replace(',', ';').split(';'):
        addr = addr.strip()
        if addr and addr not in recipients:   # skip blanks and duplicates
            recipients.append(addr)
 
if not recipients:
    raise SystemExit(f'No email addresses found in {RECIPIENTS_FILE}')
 
EMAIL_RECIPIENT = ', '.join(recipients)
print(f'Sending to: {EMAIL_RECIPIENT}')

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


with smtplib.SMTP('ptcpo', 25) as smtp:
    #smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)