#wordpress export xml parsers to markdown files

from bs4 import BeautifulSoup

with open('/path/to/files/postexport.xml') as handle:
	dataa = BeautifulSoup(handle)

title = dataa.findAll('title')
published = dataa.findAll('wp:post_date')
content = dataa.findAll('content:encoded')
status = dataa.findAll('wp:status')

combined_data = {}

title_md = []
published_md = []
content_md = []
status_md = []

for x in title:
	title_md.append(str(x).replace("<title>","# ").replace("</title>",""))

for x in published:
	published_md.append(str(x).replace("<wp:post_date>","").replace("</wp:post_date>",""))

for x in content:
	content_md.append(str(x).replace("<pre class=\"toolbar:2 lang:sh decode:true \">","<pre>").replace("[bash]","<pre>").replace("[/bash]","</pre>").replace("<strong>","__").replace("</strong>","__").replace("<content:encoded>","").replace("</content:encoded>","").replace("<!--more-->","").replace("","").replace("<pre class=\"toolbar:2 lang:c decode:true \">","<pre>").replace("<pre class=\"toolbar:2 lang:python decode:true  \">","<pre>"))

for x in status:
	status_md.append(str(x))

for x in range(0,len(title_md)):
	combined_data[x] = [title_md[x], published_md[x], content_md[x], status_md[x]]
