import psycopg2
import time as TIME
import datetime
from datetime import timedelta
import logging
from get_props import prop
from override import check_override
from switch import switch_boiler
import check_temp

logtype = prop('logtype')
if logtype == 'file':
    logFile = prop('loglocation')
    logging.basicConfig(format='%(asctime)s: %(message)s ',filename=logFile, filemode='a', level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.DEBUG)

def get_schedule():
    while True:
        conn_string = prop('database')
        
        logging.debug("Connecting to database ->%s" % (conn_string))
        
        try:
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
        except Exception as e:
            logging.debug("failed to connect to database -> %s" (e))
        
    
        try:
            #get current time and day of week
            day = datetime.date.today()
            time = datetime.datetime.now().time()
            dayOfWeek = datetime.date.strftime(day, '%A')
            
            logging.debug(dayOfWeek)
            
            #get schedule rows from database
            sql = """
                  select s.id_shed, s.day, s.time, s.state 
                  from schedule s 
                  join template t on t.id_tmpl = s.id_tmpl 
                  where upper(s.day) = upper(%(day)s) 
                  and s.time <= %(curr_time)s 
                  and t.selected = 'Y'
                  order by s.time desc
                  """
                    
            cursor.execute(sql, {'day':dayOfWeek, 'curr_time':time})
            shed_row = cursor.fetchone()
            shed_row_str = str(shed_row)
            logging.debug('current schedule row = %s' % shed_row_str)
            
            while shed_row is None:
                pre_day = day-timedelta(days=1) 
                dayOfWeek = datetime.date.strftime(pre_day, '%A')
                            
                cursor.execute(sql, {'day':dayOfWeek, 'curr_time':time})
                shed_row = cursor.fetchone()
                shed_row_str = str(shed_row)
                logging.debug('current schedule row = %s' % shed_row_str)
            
            id_shed = shed_row[0]
            shed_day = shed_row[1]
            shed_time = shed_row[2]
            shed_state = shed_row[3]
            
        except Exception as e:
            logging.debug(e)
        
        try:
            sql = """
                  select state from current_state
                  """
            cursor.execute(sql)
            
            row = cursor.fetchone()
            curr_state = row[0]
        except Exception as e:
            logging.debug(e)
            curr_state = 'OFF'
        try:
            temp = check_temp.temp('room').check_temp()
            logging.debug('temp is: %s' % temp)
            logging.debug('checking override')
            override = check_override(id_shed)
            
            #ON    0    low    on
            #off    1    low    on
        except Exception as e:
            logging.debug('error in temp or override %s' % e)
        try:
            if shed_state == 'ON' and override == '0' and temp == 'LOW' and curr_state == 'OFF':
                switch_boiler('ON')
                logging.info('switching boiler on \n schedule state = on /n Override = false, temp =  low')        
            elif shed_state == 'OFF' and override == '1' and temp == 'LOW' and curr_state == 'OFF':
                switch_boiler('ON')
                logging.info('switching boiler on \n schedule state = off /n Override = true, temp =  low')
            else:
                switch_boiler('OFF')
                logging.info('switching boiler off \n schedule state = %s /n Override = %s, temp =  %s' % (shed_state, override, temp))
            
        except Exception as e:
            logging.debug('error in switch section: %s' % e)
        
        t = float(prop('loopsleep'))
        logging.debug('sleeping for = %s seconds' % t)
        TIME.sleep(t)

get_schedule()
