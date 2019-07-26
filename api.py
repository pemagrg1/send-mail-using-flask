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
    filename = request.files['file']
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    attachment = open(filename,
                      'rb')  # for opening file, file is open in read mode
    part = MIMEBase('application', 'octet_stream')
    part.set_payload((attachment).read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header('Content-Disposition',
                    "attachment; filename= " + "test.csv")  # add the file to the header

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

    return render_template('test_csv_caremethod.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=00, use_reloader=False)
