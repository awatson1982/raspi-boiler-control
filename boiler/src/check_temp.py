import psycopg2
from get_props import prop
import logging
import requests



class temp:
    
    def __init__(self, sensor):
        logtype = prop('logtype')
        if logtype == 'file':
            logFile = prop('loglocation')
            logging.basicConfig(format='%(asctime)s: %(message)s ',filename=logFile, filemode='a', level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.DEBUG)
        
        self.sensor = sensor
        
    def get_temp(self):
        sensor = self.sensor
        if sensor == 'room':
            Probe = prop('roomProbe')
        elif sensor == 'rad':
            Probe = prop('radProbe')
        elif sensor == 'outside':
            Probe = prop('outsideProbe')
        if sensor in ('rad', 'outside'):
            try: 
                f=open(Probe, 'r')
                for l in f:
                        if 't=' in l:
                                temp=(float(l.split('=',1)[1].strip().replace('\n', '')))/1000
                f.close()
            except Exception as e:
                logging.debug(e)
        else:
            try:
                tempAPI = requests.get(Probe)
                if tempAPI.status_code != 200:
                    raise Exception('GET /temp/ {}'.format(tempAPI.status_code) )
                temp = tempAPI.json()['temp'] 
            except Exception as e:
                logging.debug(e)
        
        
        return temp 
            

    def check_temp(self):
        logtype = prop('logtype')
        if logtype == 'file':
            logFile = prop('loglocation')
            logging.basicConfig(format='%(asctime)s: %(message)s ',filename=logFile, filemode='a', level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.DEBUG)
        
        roomTemp = temp.get_temp(self)
        
        try:
            tolerance = int(prop('tolerance'))
            
            conn_string = prop('database')
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
            
            sql =   """
                    select target_temp from target_temp
                    """
            cursor.execute(sql)
            
            target_temp = cursor.fetchone()
            cursor.close()
            try:
                target_temp = target_temp[0]
                logging.debug(target_temp)
            except:
                target_temp = None
        
            if target_temp is None:
                logging.debug('No target temp set, setting default to 21')
                target_temp = 21
            
            upper = target_temp + tolerance
            lower = target_temp - tolerance
            logging.debug('lower = %s' % lower)
            logging.debug('upper = %s' % upper)
            if roomTemp >= lower and roomTemp <= upper:
                logging.debug('temp within range')
                return 'WITHIN'
            elif roomTemp >= upper:
                logging.debug('HIGH')
                return 'HIGH'
            elif roomTemp <= lower:
                logging.debug('LOW')
                return 'LOW'
               
        except Exception as e:
            logging.debug(e) 