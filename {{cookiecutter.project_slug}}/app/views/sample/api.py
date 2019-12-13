from http import HTTPStatus

from flask_restful import Resource

from app.context import context_property
from app.decorators.validation import validate_with_pydantic, PayloadLocation
from app.views.sample.schema import Post


class SampleAPI(Resource):
    @validate_with_pydantic(
        payload_location=PayloadLocation.JSON, model=Post, json_force_load=True
    )
    def post(self):
        payload: Post = context_property.request_payload

        return {"msg": f"hello {payload.name}"}, HTTPStatus.CREATED
