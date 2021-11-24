
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests, datetime
from bs4 import BeautifulSoup #To install: pip3 install beautifulsoup4

    
# email_sender_account = input("email_sender_account: ")
# email_sender_username = input("email_sender_username: ")
# email_sender_password = input("email_sender_password: ")

def SendEmail (data, time, url):
	email_sender_account = "newstufflover@gmail.com"
	email_sender_username = "Kane Nguyen"
	email_sender_password = "@kien12a99"

	#change if not gmail.
	email_smtp_server = "smtp.gmail.com" 
 
	# smtp port 
	email_smtp_port = 587 
	email_recepients = ["cudayanh@gmail.com"] #your receipts
    
    # body cua mail 
	email_subject = f"new notices from {url} - {time}"
	email_body = f'<html><head></head>'

	email_body += "<body><h2 style='color: rgb(86, 0, 251)'>Newly Updated</h2>"
	email_body += f"<h2 style='color: rgb(9, 179, 223)'>Total notices: {len(data)}</h2>"	

	# table 
	email_body += "<br/><table style='border: 1px solid #96D4D4l; border-spacing: 20px;'>"

	for val in data:
		email_body += str(val) 
	
	email_body += "</table>"

	email_body += "</body></html>"
	
	#footer
	email_body += f"<br><h3>Click <a href={url}>here</a> for more details.<h3>"

	# send/receive mails o day
	print(f"\n-> Logging in to {email_sender_account}")
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		server.login(email_sender_account, email_sender_password)
		for recipient in email_recepients:
			print("-> start sending mail...")
			print(f"-> Sending email to {recipient}")
			message = MIMEMultipart('alternative') 
			message['From'] = email_sender_account 
			message['To'] = recipient 
			message['Subject'] = email_subject 
			message.attach(MIMEText(email_body, 'html')) 
			server.sendmail(email_sender_account,recipient,message.as_string())
		server.quit()
	print("-> sending mail completed")


# target url m? mh mu?n monitor
# url = "https://cs.kw.ac.kr:501/department_office/lecture.php"

def dataPulling():
    pass 


url = "http://ncov.mohw.go.kr/en/"

# make a request 
req = requests.get(url, verify=False)
# use beautifulSoup to scap data
bsObj = BeautifulSoup(req.text, "html.parser")
# print data as format 
# print(bsObj.prettify())

# data = bsObj.find_all("tr", class_ = "class_name")
# find all tag <tr> in received data (chu y cho nay)
# data = bsObj.find_all("tr")
data = bsObj.find_all("div", class_ = "occurrenceStatus")

TimeNow = datetime.datetime.now()
if (data):
	SendEmail(data, TimeNow, url)
else:
    print("data is null")

if __name__ == "__main__":
    pass


# relevant references 
# 1. https://hackersandslackers.com/scraping-urls-with-beautifulsoup/
# 2. https://realpython.com/python-send-email/
# 3. https://beautiful-soup-4.readthedocs.io/en/latest/
