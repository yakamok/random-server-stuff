def check_loadavg():
	#get load average
	with open("/proc/loadavg","r") as handle:
		loadavg = handle.read().split()
	#get number of CPU's
	with open("/proc/cpuinfo","r") as handle:
		cpuinfo = [x for x in handle.readlines() if "processor" in x]

	#figure out if CPU usage is too high or not
	for x in range(1,3):
		if float(loadavg[x]) < (len(cpuinfo) * 0.925):
			return None
		elif float(loadavg[x]) > (len(cpuinfo) * 0.925):
			if x == 2:
				return "CPU usage has been High for Too long check ASAP!!!"
			else:
				return "CPU usage is a little high, might be worth having a check"

#send an email if CPU usage is too high
status = check_loadavg()
if status != None:
	msgbody = status
	import smtplib
	from email.mime.text import MIMEText

	msg = MIMEText(msgbody)
	msg['Subject'] = "CPU Usage Alert!!"
	msg['From'] = 'servername'
	msg['To'] = 'alert@address.com'

	s = smtplib.SMTP('smtp.gmail.com','')
	s.starttls()
	s.login("usernamehere@gmail.com","password")
	s.sendmail(me, [you], msg.as_string())
	s.quit()
