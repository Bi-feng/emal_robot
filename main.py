from src import send_email

if __name__ == '__main__':
    email_recipient = 'bifeng_zhe@outlook.com'
    send_email('Test Email', 'This is a test email', email_recipient)
