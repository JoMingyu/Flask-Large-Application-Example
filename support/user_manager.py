from flask import make_response
from support import mysql, crypto


def get_encrypted_id_from_session(request, session, key):
    session_id = ''

    if request.cookies.get(key):
        # Cookie exists
        session_id = request.cookies.get(key)
    elif key in session:
        # Session exists
        session_id = session[key]

    # Session id : plain text

    result = mysql.execute("SELECT id FROM account WHERE session_id='", crypto.sha512_encrypt(session_id), "'")
    # Encrypted session id

    return result[0]['id']


def remove_session(request, session, key):
    response = make_response('', 201)
    # Make response to access cookie and return

    encrypted_id = get_encrypted_id_from_session(request, session, key)
    # Get encrypted id to remove session from database

    if request.cookies.get(key):
        # Cookie exists
        response.set_cookie(key, '', expires=0)
    elif key in session:
        # Session exists
        session.pop(key, None)

    mysql.execute("UPDATE account SET session_id=null WHERE id='", encrypted_id, "'")

    return response
