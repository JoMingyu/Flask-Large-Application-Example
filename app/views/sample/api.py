from http import HTTPStatus

from flask_restful import Resource

from app.context import context_property
from app.decorators.validation import validate
from app.views.sample.schema import PostJson


class SampleAPI(Resource):
    @validate(
        json=PostJson
    )
    def post(self):
        payload: PostJson = context_property.request_json

        return {"msg": f"hello {payload.name}"}, HTTPStatus.CREATED
