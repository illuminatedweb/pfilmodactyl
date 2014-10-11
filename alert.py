#!/usr/bin/python

import MySQLdb
import smtplib
import logging
import datetime

logging.basicConfig(filename="alerts.log", level=logging.DEBUG)
now = datetime.datetime.now()

def getalerts ():
	try:
		db = MySQLdb.connect(host="localhost", user="pfilmoda_ctyl", passwd="o7RosPb8Z1pxIoU6b", db="pfilmoda_ctyl")
		cur = db.cursor() 
		cur.execute("SELECT DISTINCT TRIM(email), TRIM(title) FROM alerts WHERE DATE(date) = DATE(NOW()) ORDER BY email, title")
		for row in cur.fetchall():
			email = row[0]
			title = row[1]
			mailsend (email, 'alerts@pfilmodactyl.com', 'Movie Released: ' + title, title + ' has been released! Thanks for using pfilmodactyl.com.') 
	except Exception, e:
		log ("error", "getalerts", str(e))
		
def mailsend (toaddress, fromaddress, subject, message):
	header = 'To:' + toaddress + '\n' + 'From:' + fromaddress + '\n' + 'Subject:' + subject + '\n'
	msg = header + '\n' + message
	log ("info", "mailsend", msg)
	smtpserver = smtplib.SMTP("mail.pfilmodactyl.com", 25)
	try:
		smtpserver.login("alerts@pfilmodactyl.com", "alertme")
		smtpserver.sendmail(fromaddress, toaddress, msg)
	except Exception, e:
		log ("error", "mailsend", str(e))
	smtpserver.quit()
					  
def log (level, function, message):
	tolog = " " + str(now) + " [" + function + "]:\n----------------------------------------------\n" + message + "\n----------------------------------------------"
	if level == "info":
		logging.info(tolog)
	elif level == "error":
		logging.error(tolog)
					  
getalerts()
