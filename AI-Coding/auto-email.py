import smtplib
import email
import datetime
import schedule
import time

def send_email():
    msg = email.message.EmailMessage()
    msg["From"] = "Your-mail@AAA.com"
    msg["To"] = "send-to@CCC.com"
    msg["Subject"] = datetime.date.today().strftime("%Y-%m-%d") + "打卡"
    msg.set_content(datetime.date.today().strftime("%Y-%m-%d") + "打卡")
    server = smtplib.SMTP("smtp.AAA.com", 25)
    server.login("AAA@AAA.com", "Password")
    server.send_message(msg)
    server.quit()
    print("邮件已发送")

schedule.every().day.at("07:00").do(send_email)
while True:
    schedule.run_pending()
    time.sleep(1)


