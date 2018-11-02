from email.utils import formatdate


def after_request(response):
    try:
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'deny'
        response.headers['Date'] = formatdate(timeval=None, localtime=False, usegmt=True)
    finally:
        return response
