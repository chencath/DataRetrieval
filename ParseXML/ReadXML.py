"""
Description:
 - A simple demo to get XML data.

Author:
 - Cathy Chen
Last modified date: 3-18-2021
"""

import requests
import xml.dom.minidom


document = """\
<slideshow>
<title>Demo slideshow</title>
<slide><title>Slide title</title>
<point>This is a demo</point>
<point>Of a program for processing slides</point>
</slide>

<slide><title>Another demo slide</title>
<point>It is important</point>
<point>To have more than</point>
<point>one slide</point>
</slide>
</slideshow>
"""

# parsing xml   https://docs.python.org/3/library/xml.dom.minidom.html
dom = xml.dom.minidom.parseString(document)

dom.getElementsByTagName("title")[0].childNodes
# Out[13]: [<DOM Text node "'Demo slide'...">]
dom.getElementsByTagName("title")[1].childNodes
# [<DOM Text node "'Slide titl'...">]
dom.getElementsByTagName("title")[2].childNodes
# [<DOM Text node "'Another de'...">]
dom.getElementsByTagName("title")[0].childNodes[0]
# Out[14]: <DOM Text node "'Demo slide'...">
dom.getElementsByTagName("title")[1].childNodes[0]
# Out[15]: <DOM Text node "'Demo slide'...">
dom.getElementsByTagName("title")[0].childNodes[0].data
# Out[16]: 'Demo slideshow'


response = requests.get(
    "https://news.google.com/news/rss/headlines/section/q/finance%20news/finance%20news?ned=us&hl=en")
content = response.content
news_dom = xml.dom.minidom.parseString(content)
news_dom.getElementsByTagName()
news_dom.getElementsByTagName("title")[0].childNodes
# <DOM Text node "'"finance n'...">
news_dom.getElementsByTagName("title")[1].childNodes
# [<DOM Text node "'Stock mark'...">]
news_dom.getElementsByTagName("link")[1].childNodes
# [<DOM Text node "'https://fi'...">]


response = requests.get(
    "https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Datasets/daily_treas_bill_rates.xml")
content = response.content
dataDOM = xml.dom.minidom.parseString(content)




