import sys 
import requests 
import lxml.html 
from bs4 import BeautifulSoup
import MySQLdb


db = MySQLdb.connect('10.5.18.67','12CS30001','dual12','12CS30001')
cursor = db.cursor()

	

def createTab():
	global db
	global cursor
	# cursor.execute("drop table if exists country")
	COUNTRY = """create table country (
		CID int(11) not null AUTO_INCREMENT,
		name varchar(50) not null,
		primary key (CID)
		)"""
	
	cursor.execute(COUNTRY)

	# cursor.execute("drop table if exists genre")
	GENRE = """create table genre (
		GID int(11) not null AUTO_INCREMENT,
		name varchar(50) not null,
		primary key (GID)
		)"""
	cursor.execute(GENRE)	

	# cursor.execute("drop table if exists language")
	LANGUAGE = """create table language (
		LAID int(11) not null AUTO_INCREMENT,
		name varchar(50) not null,
		primary key (LAID)
		)"""
	cursor.execute(LANGUAGE)	

	# cursor.execute("drop table if exists location")
	LOCATION = """create table location (
		LID int(11) not null AUTO_INCREMENT,
		name varchar(50) not null,
		primary key (LID)
		)"""
	cursor.execute(LOCATION)

	# cursor.execute("drop table if exists movie")
	MOVIE = """create table movie (
		MID char(9) not null,
		title varchar(100) not null,
		year year(4) default null,
		rating float(3,1)default null,
		num_votes int(11) default null,
		primary key (MID)
		)"""
	cursor.execute(MOVIE)	

	# cursor.execute("drop table if exists person")
	PERSON = """create table person (
		PID char(9) not null,
		name varchar(100) not null,
		dob date default null,
		primary key (PID)
		)"""
	cursor.execute(PERSON)		

	# cursor.execute("drop table if exists m_cast")
	MCast = """create table m_cast (
		MID char(9) not null,
		PID char(9) not null,
		constraint fhg primary key (MID,PID),
		constraint hdb foreign key (MID) references movie (MID),
		constraint hdlkn  foreign key (PID) references person (PID)
		)"""
	cursor.execute(MCast)

	# cursor.execute("drop table if exists m_country")
	MCountry = """create table m_country (
		MID char(9) not null,
		CID char(9) not null,
		primary key (MID,CID),
		foreign key (MID) references movie (MID),
		foreign key (CID) references country (CID)
		)"""
	cursor.execute(MCountry)

	# cursor.execute("drop table if exists m_director")
	MDirector = """create table m_director (
		MID char(9) not null,
		PID char(9) not null,
		primary key (MID,PID),
		foreign key (MID) references movie (MID),
		foreign key (PID) references person (PID)
		)"""
	cursor.execute(MDirector)

	# cursor.execute("drop table if exists m_genre")
	MGenre = """create table m_director (
		MID char(9) not null,
		GID char(9) not null,
		primary key (MID,GID),
		foreign key (MID) references movie (MID),
		foreign key (PID) references genre (GID)
		)"""
	cursor.execute(MGenre)

	# cursor.execute("drop table if exists m_language")
	MLanguage = """create table m_language (
		MID char(9) not null,
		LAID char(9) not null,
		primary key (MID,LAID),
		foreign key (MID) references movie (MID),
		foreign key (LAID) references language (LAID)
		)"""
	cursor.execute(MLanguage)

	# cursor.execute("drop table if exists m_location")
	MLocation = """create table m_location (
		MID char(9) not null,
		LID char(9) not null,
		primary key (MID,LID),
		foreign key (MID) references movie (MID),
		foreign key (LID) references location (LID)
		)"""
	cursor.execute(MLocation)	

	# cursor.execute("drop table if exists m_producer")
	MProducer = """create table m_producer (
		MID char(9) not null,
		PID char(9) not null,
		primary key (MID,PID),
		foreign key (MID) references movie (MID),
		foreign key (PID) references person (PID)
		)"""
	cursor.execute(MDirector)
	
	

def dropTab():
	cursor.execute(DROP TABLE IF EXISTS m_director)
	cursor.execute(DROP TABLE m_director, m_producer, m_cast, m_genre, m_country, m_language, m_location)
	cursor.execute(DROP TABLE movie, person, genre, country, language, location)

def getDOB(CID):
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
	createTab()
	dropTab()
	address = "/search/title?languages=hi|1&title_type=feature&num_votes=50,&sort=user_rating,desc"
	# for num in range(5):
	# 	address, tmp = getList( address)
	# 	alltitles += tmp
	
	# print alltitles
	#FnF
	# title = "/title/tt1905041/"
	#Baby
	title = "/title/tt3848892/"
	# print getMovie(title)
	# for title in alltitles:
	# 	print getMovie(title)


	#coco = lxml.html.document_fromstring(requests.get("http://www.imdb.com/title/tt1905041/fullcredits").content)
	#/name/nm7061978/?ref_=ttfc_fc_cl_i

	# respond = requests.get("http://www.imdb.com/search/title?languages=hi|1&title_type=feature&num_votes=50,&sort=user_rating,desc")
	# hxs = lxml.html.document_fromstring(requests.get("http://www.imdb.com/search/title?languages=hi|1&title_type=feature&num_votes=50,&sort=user_rating,desc").content)
	# #".//*[@id='content-primary']/table[3]/tbody/tr[%d]/td[2]/a/text()"
	# movie = {}

	# xyz = hxs.xpath('//td[@class="image"]/a/@href')
	# print xyz

	# nextPage = hxs.xpath('//span[@class="pagination"]/a/@href')[1]
	# print nextPage
