from bottle import route, redirect, request, run, jinja2_template, \
                    debug, static_file, response, template
import hashlib
import uuid
from password import check_password

@route('/')
def get_details():
    pysessionid = sessionid()
    response.set_cookie('pysessionid', pysessionid)
    return template('login')
    
@route('/setshedule', method='POST')
def set_schedule():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_password(password) is True:
        state = 'valid'
        pysessionid = request.get_cookie('pysessionid')
        set_session(state, pysessionid )
        return template('output')
    else:
        return "Password Incorrect"

@route('/newuser', method='POST')
def new_user():
    

def sessionid():
    seed = str(uuid.uuid4().hex)
    pysessionid = hashlib.md5(seed.encode(encoding='utf_8')).hexdigest()
    return pysessionid
    

    
def set_session(state, pysessionid):
    if state == 'valid':
        valid_sessions.append(pysessionid)

run(host='192.168.0.5', port=99, debug=True)