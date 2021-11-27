import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests, datetime
from bs4 import BeautifulSoup 
import typing 

def SendEmail(data: any, time, url: str, email_sender_acc: str, email_sender_pass: str, email_recepients: list, mail_smtp_type: str):
	if (email_sender_acc is None or email_sender_pass is None or email_recepients is None or mail_smtp_type is None):
		raise Exception("email_sender_acc && email_sender_pass && email_recepients && mail_type values should not be null.")
	
	email_subject = f"New notices from {url} - {time}"
	email_body = f'<html><head></head>'

	email_body += "<body><h2 style='color: rgb(86, 0, 251)'>Newly Updated</h2>"
	email_body += f"<h2 style='color: rgb(9, 179, 223)'>Total notices: {len(data)}</h2>"	

	email_body += "<br/><table style='border: 1px solid #96D4D4l; border-spacing: 20px;'>"

	for val in data:
		email_body += str(val) 
	
	email_body += "</table>"

	email_body += "</body></html>"
	
	email_body += f"<br><h3>Click <a href={url}>here</a> for more details.<h3>"

	print(f"\n-> Logging in to {email_sender_acc}")
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(mail_smtp_type, 465, context=context) as server:
		server.login(email_sender_acc, email_sender_pass)
		for recipient in email_recepients:
			print("-> start sending mail...")
			print(f"-> Sending email to {recipient}")
			message = MIMEMultipart('alternative') 
			message['From'] = email_sender_acc
			message['To'] = recipient 
			message['Subject'] = email_subject 
			message.attach(MIMEText(email_body, 'html')) 
			server.sendmail(email_sender_acc,recipient,message.as_string())
		server.quit()
	print("-> sending mail completed")

def dataPulling(url: str):
	req = requests.get(url, verify=False)
	bsObj = BeautifulSoup(req.text, "html.parser")
	data = bsObj.find_all("div", class_="occurrenceStatus")
	TimeNow = datetime.datetime.now()
	if (data):
		email_sender_acc = input("email_sender_account: ")
		email_sender_pass = input("email_sender_password: ")
		N = int(input("enter number of recipients: "))
		email_recepients = [""]*N 
		for i in range(N):
			email_recepients[i] = input(f"enter recipient {i+1}: ")
		mail_smtp_type = input("mail_smtp_type (ex: smtp.gmail.com): ")
		SendEmail(data, TimeNow, url, email_sender_acc, email_sender_pass, email_recepients, mail_smtp_type)
	else:
		print("data is null")

if __name__ == "__main__":
	# url = "http://ncov.mohw.go.kr/en/"
	url = input("enter url: ")
	dataPulling(url)
	