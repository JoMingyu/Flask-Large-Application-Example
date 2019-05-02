from app.context import context_property
from app.decorators.validation import validate_with_pydantic, PayloadLocation
from app.views.base import BaseResource
from app.views.sample.schema import Post


class SampleAPI(BaseResource):
    @validate_with_pydantic(PayloadLocation.JSON, Post)
    def post(self):
        payload = context_property.request_payload

        return payload.dict(), 201
