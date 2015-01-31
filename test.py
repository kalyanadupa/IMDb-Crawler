import sys 
import requests 
import lxml.html 
from bs4 import BeautifulSoup


# respond = requests.get("http://www.imdb.com/search/title?languages=hi|1&title_type=feature&num_votes=50,&sort=user_rating,desc")
# hxs = lxml.html.document_fromstring(requests.get("http://www.imdb.com/search/title?languages=hi|1&title_type=feature&num_votes=50,&sort=user_rating,desc").content)
# #".//*[@id='content-primary']/table[3]/tbody/tr[%d]/td[2]/a/text()"
# movie = {}

# xyz = hxs.xpath('//td[@class="image"]/a/@href')
# print xyz

# nextPage = hxs.xpath('//span[@class="pagination"]/a/@href')[1]
# print nextPage
def getDOB(CID)
	doco = lxml.html.document_fromstring(requests.get("http://www.imdb.com/name/" + CID).content)
	try:
		dob = doco.xpath('//time[@itemprop = "birthDate"]/@datetime')[0]
	except IndexError:
		dob = ""	
	return dob	

def getList(address):
	hxs = lxml.html.document_fromstring(requests.get("http://www.imdb.com"+address).content)
	alltitles = hxs.xpath('//td[@class="image"]/a/@href')
	# print alltitles
	ret = hxs.xpath('//span[@class="pagination"]/a/@href')[1]
	return ret, alltitles

def getMovie(id): 
	hxs = lxml.html.document_fromstring(requests.get("http://www.imdb.com" + id).content)
	
	movie = {}
	try:
		movie['title'] = hxs.xpath('//*[@id="overview-top"]/h1/span[1]/text()')[0].strip()
		print movie['title']
	except IndexError:
		movie['title']
	try:
		movie['year'] = hxs.xpath('//*[@id="overview-top"]/h1/span[2]/a/text()')[0].strip()
	except IndexError:
		try:
			movie['year'] = hxs.xpath('//*[@id="overview-top"]/h1/span[3]/a/text()')[0].strip()
		except IndexError:
			movie['year'] = ""
	try:
		movie['rating'] = hxs.xpath('//*[@id="overview-top"]/div[3]/div[3]/strong/span/text()')[0]
	except IndexError:
		movie['rating'] = ""		
	try:
		movie['numVotes'] = hxs.xpath('//*[@id="overview-top"]/div[3]/div[3]/a[1]/span/text()')[0].strip()
	except IndexError:
		movie['numVotes'] = ""
	try:
		movie['genre'] = hxs.xpath('//*[@id="overview-top"]/div[2]/a/span/text()')
	except IndexError:
		movie['genre'] = []
	#language
	#casting
	#location	

	try:
		movie['certification'] = hxs.xpath('//*[@id="overview-top"]/div[2]/span[1]/@title')[0].strip()
	except IndexError:
		movie['certification'] = ""
	try:
		movie['running_time'] = hxs.xpath('//*[@id="overview-top"]/div[2]/time/text()')[0].strip()
	except IndexError:
		movie['running_time'] = ""
	
	try:
		movie['release_date'] = hxs.xpath('//*[@id="overview-top"]/div[2]/span[3]/a/text()')[0].strip()
	except IndexError:
		try:
			movie['release_date'] = hxs.xpath('//*[@id="overview-top"]/div[2]/span[4]/a/text()')[0].strip()
		except Exception:
			movie['release_date'] = ""
	
	try:
		movie['metascore'] = hxs.xpath('//*[@id="overview-top"]/div[3]/div[3]/a[2]/text()')[0].strip().split('/')[0]
	except IndexError:
		movie['metascore'] = 0

	try:
		movie['director'] = hxs.xpath('//*[@id="overview-top"]/div[4]/a/span/text()')[0].strip()
	except IndexError:
		movie['director'] = ""
	try:
		movie['stars'] = hxs.xpath('//*[@id="overview-top"]/div[6]/a/span/text()')
	except IndexError:
		movie['stars'] = ""
	try:
		movie['poster'] = hxs.xpath('//*[@id="img_primary"]/div/a/img/@src')[0]
	except IndexError:
		movie['poster'] = ""
	
	#Language
	try: 
		for i in xrange(4):
			lang = hxs.xpath('//div[@id = "titleDetails"]/div[{0}]/h4/text()'.format(i))
			if 'Language:' in lang:
				movie['language'] = hxs.xpath('//div[@id = "titleDetails"]/div[{0}]/a/text()'.format(i))
	except IndexError:
		movie['language'] = ""			

	#Country
	try:
		for i in xrange(4):
			lang = hxs.xpath('//div[@id = "titleDetails"]/div[{0}]/h4/text()'.format(i))
			if 'Country:' in lang:
				movie['country'] = hxs.xpath('//div[@id = "titleDetails"]/div[{0}]/a/text()'.format(i))[0]
	except IndexError:
		movie['country'] = ""			
	#location
	try:
		loco = lxml.html.document_fromstring(requests.get("http://www.imdb.com" + id+"locations?ref_=tt_dt_dt").content)
		movie['locations'] = [i[:-1] for i in loco.xpath('//div[@class = "soda sodavote odd"]/dt/a/text()')]
		dummy = [i[:-1] for i in loco.xpath('//div[@class = "soda sodavote even"]/dt/a/text()')]	
		movie['locations'] = movie['locations']+dummy
	except IndexError:
		movie['locations'] = ""

	#Cast
	try:
		DOB = {}
		coco = lxml.html.document_fromstring(requests.get("http://www.imdb.com" + id+"fullcredits").content)
		movie['cast'] = coco.xpath('//tr[@class = "odd"]/td/a/span/text()') + coco.xpath('//tr[@class = "even"]/td/a/span/text()')
		movie['castID'] = [i[6:15] for i in coco.xpath('//tr[@class = "odd"]/td[@class = "itemprop"]/a/@href')] + [i[6:15] for i in coco.xpath('//tr[@class = "even"]/td[@class = "itemprop"]/a/@href')]
		movie['director'] = [i[:-1] for i in coco.xpath('//table[@class = "simpleTable simpleCreditsTable"]/tbody/tr/td/a/text()')] [0]
		movie['directorID'] = [i[6:15] for i in coco.xpath('//table[@class = "simpleTable simpleCreditsTable"]/tbody/tr/td/a/@href')] [0]
		datLoop = coco.xpath('//div[@id= "fullcredits_content"/h4/text()')
		# for heading in datLoop:
			
	except IndexError:
		movie['cast'] = ""	

	#Director
	
	return movie

# //span[@class="pagination"]/a/@href

if __name__ == '__main__':
	alltitles = []

	address = "/search/title?languages=hi|1&title_type=feature&num_votes=50,&sort=user_rating,desc"
	# for num in range(5):
	# 	address, tmp = getList( address)
	# 	alltitles += tmp
	
	# print alltitles
	#FnF
	# title = "/title/tt1905041/"
	#Baby
	title = "/title/tt3848892/"
	print getMovie(title)
	# for title in alltitles:
	# 	print getMovie(title)


	#coco = lxml.html.document_fromstring(requests.get("http://www.imdb.com/title/tt1905041/fullcredits").content)
	#/name/nm7061978/?ref_=ttfc_fc_cl_i