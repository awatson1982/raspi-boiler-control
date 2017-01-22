from bottle import route, redirect, request, run, \
                     static_file, response, template, error

from get_props import prop
from session import get_sessionid, set_session, check_session
import psycopg2
from override import set_override
import auth
import logging 
import check_temp

logtype = prop('logtype')
if logtype == 'file':
    logFile = prop('loglocation')
    logging.basicConfig(format='%(asctime)s: %(message)s ',filename=logFile, filemode='a', level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.DEBUG)

@route('/')
def login():
    pysessionid = get_sessionid()
    response.set_cookie('pysessionid', pysessionid, secret=prop('cookieSecret'), httponly=True)
    return template('login')

@route('/main', method=['POST', 'GET'])
def main():
    try:
        try:
            rqstSession = request.get_cookie('pysessionid', secret=prop('cookieSecret'))
        except:
            pass
        if check_session(rqstSession) is True:
            try:
                roomTemp = check_temp.temp('room').get_temp()
                radTemp = check_temp.temp('rad').get_temp()
                outsideTemp = check_temp.temp('outside').get_temp()
                if request.forms.get('override','').strip():
                    logging.debug('override')
                    set_override()
                    return template('main', roomTemp=roomTemp, radTemp=radTemp, outsideTemp=outsideTemp)
            except:
                pass
            return template('main', roomTemp=roomTemp, radTemp=radTemp, outsideTemp=outsideTemp)
        elif request.forms.get('override','').strip() is '':
            rqstSession = request.get_cookie('pysessionid', secret=prop('cookieSecret'))
            username = request.forms.get('username').upper()
            password = request.forms.get('password').strip()
            logging.debug(password)
            if auth.passwd(username, password).check_password() == True:
                set_session(rqstSession)
                roomTemp = check_temp.temp('room').get_temp()
                radTemp = check_temp.temp('rad').get_temp()
                outsideTemp = check_temp.temp('outside').get_temp()            
                return template('main', roomTemp=roomTemp, radTemp=radTemp, outsideTemp=outsideTemp)           
            else:
                return template('login')
    except Exception as e:
        logging.debug('exception in main: %s' % e)
        return '<p>Error</p>'

@route('/getschedule', method=['GET', 'POST'])
def get_schedule():
    try:
        rqstSession = request.get_cookie('pysessionid', secret=prop('cookieSecret'))
        if check_session(rqstSession) is True:
            try:
                delete = request.query['delete']
            except:
                delete = False
            try:
                select = request.forms.get('select')
            except:
                select = None
            if delete is not False:
                id_shed = request.query['id_shed']
                conn_string = prop('database')
                conn = psycopg2.connect(conn_string)
                cursor = conn.cursor()
                sql =   """
                        delete from schedule where id_shed = %(id_shed)s
                        """
                cursor.execute(sql, {'id_shed':id_shed})
                conn.commit()
                cursor.close()
                
                return template('scheduleConf')
            
            elif select is not None:
                tmpl = request.forms.get('tmpl')
                conn_string = prop('database')
                conn = psycopg2.connect(conn_string)
                cursor = conn.cursor()
                sql =   """
                        select s.id_shed, s.day, s.time, s.state, t.template_name 
                        from schedule s join template t on (s.id_tmpl = t.id_tmpl) 
                        where t.template_name = %(tmpl)s  order by s.seq, s.time
                        """
                cursor.execute(sql, {'tmpl':tmpl})
                result = cursor.fetchall()
                
                sql =   """
                        update template set selected = 'N'
                        """
                cursor.execute(sql)
                conn.commit()
                sql =   """
                        update template set selected = 'Y' where template_name = %(tmpl)s
                        """
                cursor.execute(sql, {'tmpl':tmpl})
                conn.commit()
                sql =   """
                        select template_name from template
                        """
                cursor.execute(sql)
                rows = cursor.fetchall()
                cursor.close()
                tmpl = []
                for row in rows:
                    tmpl.append(row[0])
                
                return template('sched_table', rows=result, tmpl=tmpl)                

            else:
                conn_string = prop('database')
                conn = psycopg2.connect(conn_string)
                cursor = conn.cursor()
                sql =   """
                        select s.id_shed, s.day, s.time, s.state, t.template_name from schedule s join template t on (s.id_tmpl = t.id_tmpl) where t.selected = 'Y'  order by seq, time
                        """
                cursor.execute(sql)
                result = cursor.fetchall()
                
                sql =   """
                        select template_name, (select count(1) from template) as count from template
                        """
                cursor.execute(sql)
                rows = cursor.fetchall()
                cursor.close()
                tmpl = []
                count = 0
                for row in rows:
                    count = row[1]
                    tmpl.append(row[0])
                
                return template('sched_table', rows=result, tmpl=tmpl, count=count)
        else:
            pysessionid = ''
            response.set_cookie('pysessionid', pysessionid, secret=prop('cookieSecret'), Expires='Thu, 01-Jan-1970 00:00:10 GMT', httponly=True)
            redirect('/login')
    except Exception as e:
        logging.debug(e)
        return '<p>Error</p>'



@route('/edit/<id_shed>', method=['POST', 'GET'])
def edit_item(id_shed):
    try:
        rqstSession = request.get_cookie('pysessionid', secret=prop('cookieSecret'))
        if check_session(rqstSession) is True:
            if request.forms.get('save','').strip():
                id_shed = request.forms.get('id_shed','').strip()
                state = request.forms.get('state','').strip()
                time = request.forms.get('time','').strip()
            
                conn_string = prop('database')
                conn = psycopg2.connect(conn_string)
                cursor = conn.cursor()
                sql =   """
                        update schedule set time = %(time)s, state = %(state)s where id_shed = %(id_shed)s
                        """
                cursor.execute(sql, {'time':time, 'state':state, 'id_shed':id_shed})
                conn.commit()
                return template('scheduleConf')
            else:
                conn_string = prop('database')
                conn = psycopg2.connect(conn_string)
                cursor = conn.cursor()
                sql =   """
                        select id_shed, day, time, state from schedule where id_shed = %(id_shed)s
                        """
                cursor.execute(sql, {'id_shed':id_shed})
                cur_data = cursor.fetchone()
         
                return template('edit_schedule', old=cur_data, id_shed=id_shed)
        else:
            pysessionid = ''
            response.set_cookie('pysessionid', pysessionid, secret=prop('cookieSecret'), Expires='Thu, 01-Jan-1970 00:00:10 GMT', httponly=True)
            redirect('/login')
    except Exception as e:
        logging.debug(e)
        return '<p>Error</p>'

@route('/newschedule', method='any')
def new_schedule():
    try:
        rqstSession = request.get_cookie('pysessionid', secret=prop('cookieSecret'))
        if check_session(rqstSession) is True:
            if request.forms.get('save','').strip():
                day = request.forms.get('day', '').strip()
                state = request.forms.get('state','').strip()
                time = request.forms.get('time','').strip()
                tmpl = request.forms.get('tmpl','').strip()
                seq_dict={'MONDAY':1, 'TUESDAY':2, 'WEDNESDAY':3, 'THURSDAY':4, 'FRIDAY':5, 'SATURDAY':6, 'SUNDAY':7}
                seq=seq_dict[day]
                conn_string = prop('database')
                conn = psycopg2.connect(conn_string)
                cursor = conn.cursor()
                
                sql =   """
                        insert into schedule (id_shed, day, time, state, seq, id_tmpl) values (nextval('schedule_id_shed_seq'), %(day)s, %(time)s, %(state)s, %(seq)s, (select id_tmpl from template where template_name = %(tmpl)s))
                        """
                cursor.execute(sql, {'time':time, 'state':state, 'day':day, 'seq':seq, 'tmpl':tmpl})
                conn.commit()
                cursor.close()
                return template('scheduleConf')
            else:
                conn_string = prop('database')
                conn = psycopg2.connect(conn_string)
                cursor = conn.cursor()
                sql =   """
                        select template_name from template
                        """
                cursor.execute(sql)
                rows = cursor.fetchall()
                cursor.close()
                tmpl = []
                for row in rows:
                    tmpl.append(row[0])
                return template('new_schedule', tmpl=tmpl)
        else:
            pysessionid = ''
            response.set_cookie('pysessionid', pysessionid, secret=prop('cookieSecret'), Expires='Thu, 01-Jan-1970 00:00:10 GMT', httponly=True)
            redirect('/login')
    except Exception as e:
        logging.debug(e)
        return '<p>Error</p>'
            
@route('/newuser', method='any')
def new_user():
    try:
        rqstSession = request.get_cookie('pysessionid', secret=prop('cookieSecret'))
    except:
        pass
    if check_session(rqstSession) is True:
        if request.forms.get('save','').strip():
            userid = request.forms.get('userid', '').upper()
            password = request.forms.get('password').strip()
            confpassword = request.forms.get('confpassword').strip()
            logging.debug('new user password = %s' % password)
            if password is not '' and password == confpassword and userid is not '':
                hashed_password = auth.passwd(userid, password).hash_password()
            
                conn_string = prop('database')
                conn = psycopg2.connect(conn_string)
                cursor = conn.cursor()
            
                sql =   """
                        insert into users (id_usrr, userid, password) values (nextval('users_id_usrr_seq'), %(userid)s, %(password)s)
                        """
                cursor.execute(sql, {'userid':userid, 'password':hashed_password})
                conn.commit()
                cursor.close()
                redirect("/main")
    
            else:
                return template('newuser')
        else:
            return template('newuser')
    else:
        pysessionid = ''
        response.set_cookie('pysessionid', pysessionid, secret=prop('cookieSecret'), Expires='Thu, 01-Jan-1970 00:00:10 GMT', httponly=True)
        return template('login') 


@route('/settemp', method=['GET', 'POST'])
def set_temp():
    rqstSession = request.get_cookie('pysessionid', secret=prop('cookieSecret'))
    if check_session(rqstSession) is True:
        if request.forms.get('save','').strip():
            target_temp = request.forms.get('temp').strip()
            logging.debug('target temp = %s' % target_temp)
            conn_string = prop('database')
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
        
            sql =   """
                    update target_temp set target_temp = %(target_temp)s
                    """
            cursor.execute(sql, {'target_temp':target_temp})
            conn.commit()
            cursor.close()
            redirect("/main")
        else:
            logging.debug('set temp page')
            conn_string = prop('database')
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
        
            sql =   """
                    select target_temp from target_temp
                    """
            cursor.execute(sql)
            curr_temp = cursor.fetchone()
            logging.debug('current target temp = %s' % curr_temp)
            cursor.close()
            return template('set_temp', curr_temp=curr_temp)
    else:
        pysessionid = ''
        response.set_cookie('pysessionid', pysessionid, secret=prop('cookieSecret'), Expires='Thu, 01-Jan-1970 00:00:10 GMT', httponly=True)
        return template('main')

@route('/newtemplate', method=['GET', 'POST'])
def new_template():
    rqstSession = request.get_cookie('pysessionid', secret=prop('cookieSecret'))
    if check_session(rqstSession) is True:
        if request.forms.get('save','').strip():
            name = request.forms.get('name').strip()
            conn_string = prop('database')
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
        
            sql =   """
                    insert into template (id_tmpl, template_name) values (nextval('template_id_tmpl_seq'), %(name)s)
                    """
            cursor.execute(sql, {'name':name})
            conn.commit()
            cursor.close()
            return template('new_template')
        else:
            return template('new_template')
    else:
        pysessionid = ''
        response.set_cookie('pysessionid', pysessionid, secret=prop('cookieSecret'), Expires='Thu, 01-Jan-1970 00:00:10 GMT', httponly=True)
        return template('main')

    
@error(404)
def error404(error):
    return 'Nothing here, sorry'

@route('<path:path>')
def server_static(path):
    static = prop('static')
    return static_file(path, root=static)
##########



host = prop('host')
port = prop('port')

run(host=host, port=port, debug=True)
