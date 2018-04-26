import feedparser
import datetime
import os
import random
from BeautifulSoup import BeautifulSoup

def dt_cov(year,month,day):
	return datetime.date(int(year),int(month_alpha_to_numera(month)),int(day))

def month_alpha_to_numera(month_A_1):
	if month_A_1.isalpha():
		my_date = datetime.datetime.strptime(month_A_1, "%b")
		return my_date.strftime("%m")
	else:
		return month_A_1

with open("websites.txt","r") as handle:
	sites = handle.readlines()
data_poop = []
data_poop2 = []

#get stats for month
now = datetime.datetime.now()
this_month = now.strftime("%b")
this_year = now.strftime("%Y")

for x in sites:

	data = feedparser.parse(x)
	date_from_first_post = data['entries'][0].published.split()
	page_title = data['entries'][0].title
	#print data['entries'][0].content
	finaly_count = 0
	for v in range(0,len(data['entries'])):
		cleantext = BeautifulSoup(str(data['entries'][v].content)).text.split()
		for_count = []
		for d in cleantext:
			if "http" not in d and "\\n" not in d:
				for_count.append(d)
				print d

		finaly_count += len(for_count)
	#print "total posts" + str(len(data['entries']))
	#print date_from_first_post

	todays_date = str(datetime.date.today())
	todays_date2 = todays_date.replace('-',' ').split()

	#print todays_date2

	my_date = datetime.datetime.strptime(date_from_first_post[2], "%b")
	month = my_date.strftime("%m")

	a = datetime.date(int(date_from_first_post[3]),int(month),int(date_from_first_post[1]))
	b = datetime.date(int(todays_date2[0]),int(todays_date2[1]),int(todays_date2[2]))
	days_since_last_login = (b-a).days

	dates = []

	for c in range(0,len(data['entries'])):
		temp_date = data['entries'][c].published.split()
		dates.append(dt_cov(temp_date[3],temp_date[2],temp_date[1]))

	dates.sort()
	dates.reverse()

	streak_len = 0

	if (dt_cov(todays_date2[0],todays_date2[1],todays_date2[2])-dates[0]).days <= 7:
		for alg in range(0,len(dates)):
			z = alg + 1
			if z != len(dates):
				if (dates[alg]-dates[z]).days <= 7:
					streak_len += 1
				else:
					break

	with open("insults-list.txt") as handle:
		insults_list = handle.readlines()


	if streak_len <= 2:

		if days_since_last_login <= 7:
			verdict = "<div class='blogg'>"
			verdy = "not a lazy fuck"
		elif days_since_last_login > 7 and days_since_last_login <= 14:
			verdict = "<div class='blogb'>"
			verdy = "a bit behind"
		elif days_since_last_login > 14 and days_since_last_login <= 30:
			verdict = "<div class='blogp'>"
			verdy = "procrastinating"
		elif days_since_last_login > 30 and days_since_last_login <= 60:
			verdict = "<div class='blogl'>"
			verdy = "lazy fuck"
		elif days_since_last_login > 60 and days_since_last_login <= 90:
			verdict = "<div class='blogsl'>"
			verdy = "Blogging maybe isnt your thing"
		else:
			verdict = "<div class='blogdl'>"
			verdy = "Time to give up on blogging"
	else:
		verdict = "<div class='blogg'>"
		verdy = insults_list[random.randint(0,len(insults_list) -1)]
		print verdy

	count = 0 
	total_for_month = 0
	for b  in range(0,len(data['entries'])):
		if str(this_year).strip() in str(data['entries'][b].published.strip()):
			if str(this_month).strip() in str(data['entries'][b].published).strip():
				month_content = BeautifulSoup(str(data['entries'][b].content)).text.split()
				month_count = []
				for d in month_content:
					if "http" not in d:
						month_count.append(d)
				#print len(month_count)

				total_for_month += len(month_count)

				count += 1
	#print "total for month" + str(total_for_month) + " and post count " + str(count)
	posts_this_month = "<strong>Posts this month:</strong> " + str(count) + "<br />"
	most_recent_post = "<strong>Most recent post:</strong> <a href='" + data['entries'][0].link + "'>" + data['entries'][0].title + "</a><br />"

	if days_since_last_login < 60:
		data_poop.append(verdict + "<div class='httpclass'>" + x.strip() + ":</div> " + most_recent_post +  posts_this_month + str(days_since_last_login) + " days since last post<br />" +  "Total Word Count: " + str(finaly_count) + "<br />" +  "Total Word Count This month: " + str(total_for_month) + "<br />" + "Average word count per Post: " + str(finaly_count / len(data['entries'])) + "<br />" + verdy + "<br />Streak: " + str(streak_len) + "<br /></div>")
	else:
		data_poop2.append(verdict + "<div class='httpclass'>" + x.strip() + ":</div> " + most_recent_post +  posts_this_month + str(days_since_last_login) + " days since last post<br />" + "Total Word Count: " + str(finaly_count) + "<br />" +  "Total Word Count This month: " + str(total_for_month) + "<br />" + "Average word count per Post: " + str(finaly_count / len(data['entries'])) + "<br />" + verdy + "<br />Streak: " + str(streak_len) + "<br /></div>")

	x2 = x[x.index("//"):].replace("//","")
	xclean = x2[:x2.index("/")]

	if os.path.exists(xclean) == True:
		with open(xclean,"r") as handle:
			check_exists_in = handle.read()
		if page_title.strip() not in str(check_exists_in):
			with open(xclean, "a") as handle:
				handle.write(page_title + " ### " + str(date_from_first_post[3]) + " " + str(month) + " " + str(date_from_first_post[1]))
 	else:
		with open(xclean, "w") as handle:
			handle.write(page_title + " ### " + str(date_from_first_post[3]) + " " + str(month) + " " + str(date_from_first_post[1]))



#write to a static html file here

with open("index.html","w") as handle:
	handle.write("<html>")
	handle.write("<head>")
	handle.write("<title>Lazy Fuck Alert</title>")
	handle.write("<link rel='stylesheet' type='text/css' href='style.css'/>")
	handle.write("</head>")
	handle.write("<body>")
	handle.write("<div id='wrapper'>")
	handle.write("<div id='header'>")
	handle.write("<div id='title'>Lazy fuck Alert</div>")
	handle.write("<strong>" + str(now) + "</strong>")
	handle.write("</div>")
	for x in data_poop:
		handle.write(x)
	for x in data_poop2:
		handle.write(x)
	#handle.write("last update: " + )
	handle.write("</div>")
	handle.write("</body>")
	handle.write("</html>")
