create table schedule 
(
	id_shed	SERIAL	PRIMARY KEY,
	day	VARCHAR(9) not null,
	time	TIME without time zone	not null,
	state	VARCHAR(3) not null
);

create table override
(
	id_over	SERIAL PRIMARY KEY,
	id_shed	SERIAL references schedule(id_shed),
	starttime	TIME without time zone not null,
	state VARCHAR(3) not null
);

create table target_temp
(
	id_targ	SERIAL PRIMARY KEY,
	id_shed	SERIAL references schedule(id_shed),
	target_temp int not null
);

create table template 
(
	id_tmpl	SERIAL	PRIMARY KEY,
	template_name	VARCHAR(20)	not null
);

create table current_state 
(
	state	VARCHAR(3)	not null
);

CREATE TABLE users
(
  id_usrr serial PRIMARY KEY,
  userid character varying(20) NOT NULL,
  password character varying(128) NOT NULL,
  salt character varying(32) NOT NULL
);

CREATE TABLE log
(
	outside_temp numeric,
	rad_temp numeric,
	room_temp numeric,
	datestamp timestamp,
	state VARCHAR(3)
);
