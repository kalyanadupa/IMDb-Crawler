import sys 
import requests 
import lxml.html 
from datetime import date, datetime
import MySQLdb


db = MySQLdb.connect('localhost','root','satyakala','imdb')
cursor = db.cursor()

langL = []
genreL = []
countryL = []
locationL = []
personL = []
directorL = []



def createTab():
    global db
    global cursor

    try:

    # cursor.execute("drop table if exists country")
        COUNTRY = """create table country (
            CID int(11) not null AUTO_INCREMENT,
            name varchar(50) not null,
            primary key (CID)
            )"""
        cursor.execute(COUNTRY)
    except Exception as Ex:
        print Ex
        pass

    try:
    # cursor.execute("drop table if exists genre")
        GENRE = """create table genre (
            GID int(11) not null AUTO_INCREMENT,
            name varchar(50) not null,
            primary key (GID)
            )"""
        cursor.execute(GENRE)    
    except Exception as Ex:
        print Ex
        pass

    try:
    # cursor.execute("drop table if exists language")
        LANGUAGE = """create table language (
            LAID int(11) not null AUTO_INCREMENT,
            name varchar(50) not null,
            primary key (LAID)
            )"""
        cursor.execute(LANGUAGE)    
    except Exception as Ex:
        print Ex
        pass

    try:
    # cursor.execute("drop table if exists location")
        LOCATION = """create table location (
            LID int(11) not null AUTO_INCREMENT,
            name varchar(50) not null,
            primary key (LID)
            )"""
        cursor.execute(LOCATION)
    except Exception as Ex:
        print Ex
        pass
    
    
        try:
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
        except Exception as Ex:
            print Ex
            pass

    try:
    # cursor.execute("drop table if exists person")
        PERSON = """create table person (
            PID char(9) not null,
            name varchar(100) not null,
            dob date default null,
            primary key (PID)
            )"""
        cursor.execute(PERSON)
    except Exception as Ex:
        print Ex
        pass
    

    # cursor.execute("drop table if exists m_cast")
    try:
        MCast = """create table m_cast (
            MID char(9) not null,
            PID char(9) not null,
            constraint fhg primary key (MID,PID),
            constraint hdb foreign key (MID) references movie (MID),
            constraint hdlkn  foreign key (PID) references person (PID)
            )"""
        cursor.execute(MCast)
    except Exception as Ex:
        print Ex
        pass

    # cursor.execute("drop table if exists m_country")
    try:
        MCountry = """create table m_country (
            MID char(9) not null,
            CID int(11) not null,
            primary key (MID,CID),
            foreign key (MID) references movie (MID),
            foreign key (CID) references country (CID)
            )"""
        cursor.execute(MCountry)
    except Exception as Ex:
        print Ex
        pass

    try:    
    # cursor.execute("drop table if exists m_director")
        MDirector = """create table m_director (
            MID char(9) not null,
            PID char(9) not null,
            primary key (MID,PID),
            foreign key (MID) references movie (MID),
            foreign key (PID) references person (PID)
            )"""
        cursor.execute(MDirector)
    except Exception as Ex:
        print Ex
        pass

    try:    
    # cursor.execute("drop table if exists m_genre")
        MGenre = """create table m_genre (
            MID char(9) not null,
            GID int(11) not null,
            primary key (MID,GID),
            foreign key (MID) references movie (MID),
            foreign key (GID) references genre (GID)
            )"""
        cursor.execute(MGenre)
    except Exception as Ex:
        print Ex
        pass

    try:    
    # cursor.execute("drop table if exists m_language")
        MLanguage = """create table m_language (
            MID char(9) not null,
            LAID int(11) not null,
            primary key (MID,LAID),
            foreign key (MID) references movie (MID),
            foreign key (LAID) references language (LAID)
            )"""
        cursor.execute(MLanguage)
    except Exception as Ex:
        print Ex
        pass

    try:
    # cursor.execute("drop table if exists m_location")
        MLocation = """create table m_location (
            MID char(9) not null,
            LID int(11) not null,
            primary key (MID,LID),
            foreign key (MID) references movie (MID),
            foreign key (LID) references location (LID)
            )"""
        cursor.execute(MLocation)    
    except Exception as Ex:
        print Ex
        pass

    try:
    # cursor.execute("drop table if exists m_director")
        MProducer = """create table m_producer (
            MID char(9) not null,
            PID char(9) not null,
            primary key (MID,PID),
            foreign key (MID) references movie (MID),
            foreign key (PID) references person (PID)
            )"""
        cursor.execute(MProducer)
    except Exception as Ex:
        print Ex
        pass




def dropTab():
    cursor.execute('DROP TABLE if exists m_director, m_producer, m_cast, m_genre, m_country, m_language, m_location')
    cursor.execute('DROP TABLE if exists movie, person, genre, country, language, location')

def getDOB(CID):
    doco = lxml.html.document_fromstring(requests.get("http://www.imdb.com/name/" + CID).content)
    try:
        dob = doco.xpath('//time[@itemprop = "birthDate"]/@datetime')[0]
    except IndexError:
        dob = ""    
    return dob        

def getName(eachCast):
    doco = lxml.html.document_fromstring(requests.get("http://www.imdb.com/name/" + eachCast).content)
    try:
        dob = doco.xpath('//td[@id = "overview-top"]/h1/span/text()')[0]
    except IndexError:
        try:
            dob = doco.xpath('//div[@class = "no-pic-text-column"]/h1/span/text()')[0]
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
    movie['titleID'] = id[7:16]
    try:
        movie['title'] = hxs.xpath('//*[@id="overview-top"]/h1/span[1]/text()')[0].strip()
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
        lol = lxml.html.document_fromstring(requests.get("http://www.imdb.com" + id+"fullcredits").content)
        count = len(lol.xpath('//div[@id="fullcredits_content"]/h4'))
        while count != 1:
            tmp = lol.xpath('//div[@id="fullcredits_content"]/h4[{0}]/text()'.format(count-1))[0].strip().encode('utf-8')
            if 'Directed by' in tmp:
                movie['Rdirector'] = [i.strip().encode('utf-8') for i in lol.xpath('//div[@id="fullcredits_content"]/table[{0}]/tbody/tr/td/a/text()'.format(count-1))]
                movie['RdirectorID'] = [i.strip().encode('utf-8') for i in lol.xpath('//div[@id="fullcredits_content"]/table[{0}]/tbody/tr/td/a/@href'.format(count-1))]
                    
            elif 'Produced by' in tmp:
                movie['producer'] = [i.strip().encode('utf-8') for i in lol.xpath('//div[@id="fullcredits_content"]/table[{0}]/tbody/tr/td/a/text()'.format(count-1))]
                dummy = [i.strip().encode('utf-8') for i in lol.xpath('//div[@id="fullcredits_content"]/table[{0}]/tbody/tr/td/a/@href'.format(count-1))]              
                movie['producerID'] = [i[6:15] for i in dummy]    
            count -= 1
    except Exception, e:
        print e    
    
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
        print id
        coco = lxml.html.document_fromstring(requests.get("http://www.imdb.com" + id+"fullcredits").content)
        # movie['cast'] = coco.xpath('//tr[@class = "odd"]/td/a/span/text()') + coco.xpath('//tr[@class = "even"]/td/a/span/text()')
        movie['castID'] = [i[6:15] for i in coco.xpath('//tr[@class = "odd"]/td[@class = "itemprop"]/a/@href')] + [i[6:15] for i in coco.xpath('//tr[@class = "even"]/td[@class = "itemprop"]/a/@href')]
        movie['cast'] = coco.xpath('//tr[@class = "odd"]/td/a/span/text()') + coco.xpath('//tr[@class = "even"]/td/a/span/text()')
        movie['director'] = [i[:-1] for i in coco.xpath('//table[@class = "simpleTable simpleCreditsTable"]/tbody/tr/td/a/text()')] [0]
        movie['directorID'] = [i[6:15] for i in coco.xpath('//table[@class = "simpleTable simpleCreditsTable"]/tbody/tr/td/a/@href')] [0]
        # datLoop = coco.xpath('//div[@id= "fullcredits_content"/h4/text()')
        # for heading in datLoop:
            
    except IndexError:
        movie['cast'] = ""    

    return movie

# //span[@class="pagination"]/a/@href


def insertValues(movie):
    global db
    global cursor
    global langL
    global countryL
    global genreL
    global locationL
    global directorL
    global personL
    cursor.execute('insert into movie values  ("{0}","{1}","{2}","{3}","{4}")'.\
         format( movie['titleID'], movie['title'],movie['year'],movie['rating'],movie['numVotes'].replace(",", "")))
    db.commit()
    # for eachCast in movie['castID'] :
    #     cursor.execute('insert into person values  ("{0}","{1}","{2}")'.\
    #          format( eachCast, getName(eachCast),getDOB(eachCast)))
    
    castL = movie['cast']
    castIDL = movie['castID']
    x = len(castL)

    for i in range(0,x):
        cName = castL.pop()
        cID = castIDL.pop()
        cDob = getDOB(cID)
        print "Inserting " + cName + " " + cID   
        if cName in personL:
            cursor.execute('insert into m_cast values ("{0}","{1}")'.\
                format( movie['titleID'],cID ))
            db.commit()
        else:
            personL.append(cName)
            cursor.execute('insert into person values  ("{0}","{1}","{2}")'.\
                     format( cID, cName,cDob))    
            db.commit()
            cursor.execute('insert into m_cast values ("{0}","{1}")'.\
                format( movie['titleID'],cID ))
            db.commit()


    producerL = movie['producer']
    producerIDL = movie['producerID']
    x = len(producerL)

    for i in range(0,x):
        cName = producerL.pop()
        cID = producerIDL.pop()
        cDob = getDOB(cID)
        print "Inserting " + cName + " " + cID   
        if cName in personL:
            cursor.execute('insert into m_producer values ("{0}","{1}")'.\
                format( movie['titleID'],cID ))
            db.commit()
        else:
            personL.append(cName)
            cursor.execute('insert into person values  ("{0}","{1}","{2}")'.\
                     format( cID, cName,cDob))    
            db.commit()
            cursor.execute('insert into m_producer values ("{0}","{1}")'.\
                format( movie['titleID'],cID ))
            db.commit()       



    if movie['director'] in personL:
        cursor.execute('insert into m_director values ("{0}","{1}")'.\
            format( movie['titleID'],movie['directorID'] ))
        db.commit()
    else:
        personL.append(movie['director'])
        cursor.execute('insert into person values  ("{0}","{1}","{2}")'.\
                 format( movie['directorID'], movie['director'],getDOB(movie['directorID'])))    
        db.commit()
        cursor.execute('insert into m_director values ("{0}","{1}")'.\
            format( movie['titleID'],movie['directorID'] ))
        db.commit()    

    

    if movie['country'] in countryL:
        x =  countryL.index(movie['country'])
        x = x+1
        cursor.execute('insert into m_country values ("{0}","{1}")'.\
            format( movie['titleID'],x ))
        db.commit()
    else:
        countryL.append(movie['country'])
        x =  countryL.index(movie['country'])
        x = x+1
        cursor.execute('insert into country values ("{0}","{1}")'.\
            format( x,movie['country'] ))    
        db.commit()
        cursor.execute('insert into m_country values ("{0}","{1}")'.\
            format( movie['titleID'],x ))    
        db.commit()


    for eachGenre in movie['genre']:
        if eachGenre in genreL:
            x =  genreL.index(eachGenre)
            x = x+1
            cursor.execute('insert into m_genre values ("{0}","{1}")'.\
                format( movie['titleID'],x))
            db.commit()
        else:
            genreL.append(eachGenre)
            x =  genreL.index(eachGenre)
            x = x+1
            cursor.execute('insert into genre values ("{0}","{1}")'.\
                format( x,eachGenre))    
            db.commit()
            cursor.execute('insert into m_genre values ("{0}","{1}")'.\
                format( movie['titleID'],x ))    
            db.commit()    
    
    for eachLang in movie['language']:
        if eachLang in langL:
            x =  langL.index(eachLang)
            x = x+1
            cursor.execute('insert into m_language values ("{0}","{1}")'.\
                format( movie['titleID'],x))
            db.commit()
        else:
            langL.append(eachLang)
            x =  langL.index(eachLang)
            x = x+1
            cursor.execute('insert into language values ("{0}","{1}")'.\
                format( x,eachLang))
            print eachLang +" -> "
            print type(eachLang)        
            db.commit()
            cursor.execute('insert into m_language values ("{0}","{1}")'.\
                format( movie['titleID'],x ))    
            db.commit()    

    for eachLoc in movie['locations']:
        if eachLoc in locationL:
            if isinstance(eachLoc,str):
                x =  locationL.index(eachLoc)
                x = x+1
                cursor.execute('insert into m_location values ("{0}","{1}")'.\
                    format( movie['titleID'],x))
                db.commit()
        else:
            if isinstance(eachLoc,str):
                locationL.append(eachLoc)
                x =  locationL.index(eachLoc)
                x = x+1
                print eachLoc +" -> " 
                print type(eachLoc)
                cursor.execute('insert into location values ("{0}","{1}")'.\
                    format( x,eachLoc))    
                db.commit()
                cursor.execute('insert into m_location values ("{0}","{1}")'.\
                    format( movie['titleID'],x ))    
                db.commit()            
            


if __name__ == '__main__':
    alltitles = []
    # dropTab()
    # createTab()
    address = "/search/title?languages=hi|1&title_type=feature&num_votes=50,&sort=user_rating,desc"
    # for num in range(5):
    #     address, tmp = getList( address)
    #     alltitles += tmp
    
    # print alltitles
    #FnF
    # title = "/title/tt1905041/"
    #Baby
    # title = "/title/tt3848892/"
    # movie = getMovie(title)
    # print movie
    # insertValues(movie)
    title = "/title/tt3848892/"
    movie = getMovie(title)
    print movie
    insertValues(movie)
    # for title in alltitles:
        # print getMovie(title)


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
