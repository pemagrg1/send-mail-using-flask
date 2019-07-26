from flask import Flask, render_template, request
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('home.html')

@app.route('/get_details', methods=['GET', 'POST'])
def get_csv():
    all_values = request.form.to_dict()
    receiver_email = all_values["receiver"]
    sender_email = all_values["sender"]
    password = all_values["password"]
    subject = all_values["subject"]
    body = all_values["message"]

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=00, use_reloader=False)
