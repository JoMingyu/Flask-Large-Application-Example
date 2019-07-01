import arrow
from flask_restful import Resource


class BaseResource(Resource):
    def __init__(self):
        self.utcnow = arrow.utcnow()
        self.kstnow = self.utcnow.to("Asia/Seoul")
        self.iso8601_formatted_utcnow = self.utcnow.isoformat()
        self.iso8601_formatted_kstnow = self.kstnow.isoformat()
