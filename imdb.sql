
DROP TABLE if exists m_director, m_producer, m_cast, m_genre, m_country, m_language, m_location;
DROP TABLE if exists movie, person, genre, country, language, location;


create table country (
CID int(11) not null AUTO_INCREMENT,
name varchar(50) not null,
primary key (CID)
);

create table genre (
GID int(11) not null AUTO_INCREMENT,
name varchar(50) not null,
primary key (GID)
);

create table language (
LAID int(11) not null AUTO_INCREMENT,
name varchar(50) not null,
primary key (LAID)
);

create table location (
LID int(11) not null AUTO_INCREMENT,
name varchar(50) not null,
primary key (LID)
);

create table movie (
MID char(9) not null,
title varchar(100) not null,
year year(4) default null,
rating float(3,1)default null,
num_votes int(11) default null,
primary key (MID)
);

create table person (
PID char(9) not null,
name varchar(100) not null,
dob date default null,
primary key (PID)
);


create table m_cast (
MID char(9) not null,
PID char(9) not null,
constraint fhg primary key (MID,PID),
constraint hdb foreign key (MID) references movie (MID),
constraint hdlkn  foreign key (PID) references person (PID)
);

create table m_country (
MID char(9) not null,
CID int(11) not null,
primary key (MID,CID),
foreign key (MID) references movie (MID),
foreign key (CID) references country (CID)
);

create table m_director (
MID char(9) not null,
PID char(9) not null,
primary key (MID,PID),
foreign key (MID) references movie (MID),
foreign key (PID) references person (PID)
);

create table m_genre (
MID char(9) not null,
GID int(11) not null,
primary key (MID,GID),
foreign key (MID) references movie (MID),
foreign key (GID) references genre (GID)
);

create table m_language (
MID char(9) not null,
LAID int(11) not null,
primary key (MID,LAID),
foreign key (MID) references movie (MID),
foreign key (LAID) references language (LAID)
);

create table m_location (
MID char(9) not null,
LID int(11) not null,
primary key (MID,LID),
foreign key (MID) references movie (MID),
foreign key (LID) references location (LID)
);

create table m_producer (
MID char(9) not null,
PID char(9) not null,
primary key (MID,PID),
foreign key (MID) references movie (MID),
foreign key (PID) references person (PID)
);



