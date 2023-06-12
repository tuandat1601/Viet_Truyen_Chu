import smtplib
from email.message import EmailMessage
import ssl
# Thông tin tài khoản email
email = 'nguyentuandat1601@gmail.com'
password = 'jdnfitzzxcbhzlxd'
em  = EmailMessage()
# Thông tin người nhận và nội dung email
recipient = '6051071029@st.utc2.edu.vn'
subject = 'Subject of the Email'
message = 'Content of the Email'

port = 465  # For starttls
smtp_server = "smtp.gmail.com"
em['From'] = email
em['To'] = recipient
em['Subject'] = subject
em.set_content(message)

context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context = context) as smtp:
    smtp.login(email,password=password)
    smtp.sendmail(email,recipient,em.as_string())

