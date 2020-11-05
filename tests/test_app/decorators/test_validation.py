import json
from typing import Type

from pydantic import BaseModel, ValidationError, constr

from app.context import context_property
from app.decorators.validation import validate_with_pydantic, PayloadLocation
from tests import BaseTestCase


class TestValidateWithPydantic(BaseTestCase):
    """
    validate_with_schematics로 데코레이팅된 함수를 만들고,
    요청 데이터와 함께 request context를 열어서 이를 호출하는 방식으로 테스트를 진행합니다.
    """

    class TestSchema(BaseModel):
        foo: constr(min_length=1)

    def setUp(self):
        """
        Override this method to true.

        Args:
            self: (todo): write your description
        """
        super(TestValidateWithPydantic, self).setUp()

    def initialize_function_and_call(
        self,
        payload_location: PayloadLocation,
        schema: Type[BaseModel] = TestSchema,
        json_force_load: bool = False,
    ):
        """
        인자 정보를 통해 `validate_with_pydantic`으로 데코레이팅된 함수를 생성하고, 호출합니다.
        """

        @validate_with_pydantic(
            payload_location=payload_location,
            model=schema,
            json_force_load=json_force_load,
        )
        def handler():
            """
            Decorator to register a handler.

            Args:
            """
            pass

        handler()

    def test_validation_pass_with_payload_location_args(self):
        """
        Validate the test payload payload payload payload with validator.

        Args:
            self: (todo): write your description
        """
        with self.app.test_request_context(query_string={"foo": "bar"}):
            self.initialize_function_and_call(PayloadLocation.ARGS)

    def test_validation_pass_with_payload_location_json(self):
        """
        Validate payload payload payload payload payload payload payload. json payload.

        Args:
            self: (todo): write your description
        """
        with self.app.test_request_context(json={"foo": "bar"}):
            self.initialize_function_and_call(PayloadLocation.JSON)

    def test_validation_error_with_payload_location_args(self):
        """
        Validate the test payload payload is valid.

        Args:
            self: (todo): write your description
        """
        with self.app.test_request_context(query_string={"foo": ""}):
            with self.assertRaises(ValidationError) as e:
                self.initialize_function_and_call(PayloadLocation.ARGS)

    def test_validation_error_with_payload_location_json(self):
        """
        Validate the test payload against the test payload.

        Args:
            self: (todo): write your description
        """
        with self.app.test_request_context(json={"foo": ""}):
            with self.assertRaises(ValidationError):
                self.initialize_function_and_call(PayloadLocation.JSON)

    def test_context_property_binding_with_payload_location_args(self):
        """
        Test if the test binding binding.

        Args:
            self: (todo): write your description
        """
        with self.app.test_request_context(query_string={"foo": "bar"}):
            self.initialize_function_and_call(PayloadLocation.ARGS)
            self.assertEqual(
                self.TestSchema(foo="bar"), context_property.request_payload
            )

    def test_context_property_binding_with_payload_location_json(self):
        """
        Test if the test context with the test context payload.

        Args:
            self: (todo): write your description
        """
        with self.app.test_request_context(json={"foo": "bar"}):
            self.initialize_function_and_call(PayloadLocation.JSON)
            self.assertEqual(
                self.TestSchema(foo="bar"), context_property.request_payload
            )

    def test_json_force_load(self):
        """
        : parameter test test test test test

        Args:
            self: (todo): write your description
        """
        with self.app.test_request_context(data=json.dumps({"foo": "bar"})):
            # TODO
            # self.initialize_function_and_call(
            #     PayloadLocation.JSON, json_force_load=False
            # )
            # print(context_property.request_payload)

            self.initialize_function_and_call(
                PayloadLocation.JSON, json_force_load=True
            )
            self.assertEqual(
                self.TestSchema(foo="bar"), context_property.request_payload
            )
