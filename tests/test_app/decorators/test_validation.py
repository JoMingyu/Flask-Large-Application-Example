import json

from pydantic import BaseModel, ValidationError, constr

from app.context import context_property
from app.decorators.validation import validate
from tests import BaseTestCase


class TestValidate(BaseTestCase):
    """
    validate로 데코레이팅된 함수를 만들고,
    요청 데이터와 함께 request context를 열어서 이를 호출하는 방식으로 테스트를 진행합니다.
    """

    class TestSchema(BaseModel):
        foo: constr(min_length=1)

    def setUp(self):
        super(TestValidate, self).setUp()

    def initialize_function_and_call(
        self,
        decorator_kwargs: dict = None,
        handler_kwargs: dict = None
    ):
        """
        인자 정보를 통해 `validate_with_pydantic`으로 데코레이팅된 함수를 생성하고, 호출합니다.
        """

        if decorator_kwargs is None:
            decorator_kwargs = {}

        if handler_kwargs is None:
            handler_kwargs = {}

        @validate(
            **decorator_kwargs
        )
        def handler(**kwargs):
            pass

        handler(**handler_kwargs)

    def test_path_params_validation(self):
        with self.app.test_request_context():
            self.initialize_function_and_call(
                decorator_kwargs={'path_params': self.TestSchema},
                handler_kwargs={'foo': 'bar'}
            )
            self.assertEqual(self.TestSchema(foo='bar'), context_property.request_path_params)

    def test_path_params_validation_error(self):
        with self.app.test_request_context():
            with self.assertRaises(ValidationError):
                self.initialize_function_and_call(
                    decorator_kwargs={'path_params': self.TestSchema},
                    handler_kwargs={'foo': ''}
                )

            self.assertIsNone(context_property.request_path_params)

    def test_query_params_validation(self):
        with self.app.test_request_context(query_string={'foo': 'bar'}):
            self.initialize_function_and_call(
                decorator_kwargs={'query_params': self.TestSchema},
            )
            self.assertEqual(self.TestSchema(foo='bar'), context_property.request_query_params)

    def test_query_params_validation_error(self):
        with self.app.test_request_context(query_string={'foo': ''}):
            with self.assertRaises(ValidationError):
                self.initialize_function_and_call(
                    decorator_kwargs={'query_params': self.TestSchema},
                )

            self.assertIsNone(context_property.request_query_params)

    def test_json_validation(self):
        with self.app.test_request_context(json={'foo': 'bar'}):
            self.initialize_function_and_call(
                decorator_kwargs={'json': self.TestSchema},
            )
            self.assertEqual(self.TestSchema(foo='bar'), context_property.request_json)

    def test_json_validation_error(self):
        with self.app.test_request_context(json={'foo': ''}):
            with self.assertRaises(ValidationError):
                self.initialize_function_and_call(
                    decorator_kwargs={'json': self.TestSchema},
                )

            self.assertIsNone(context_property.request_query_params)

    def test_json_without_content_type(self):
        with self.app.test_request_context(data=json.dumps({"foo": "bar"})):
            with self.assertRaises(ValidationError):
                self.initialize_function_and_call(
                    decorator_kwargs={'json': self.TestSchema},
                )

            self.assertIsNone(context_property.request_query_params)

    def test_json_without_content_type__with_json_force_load(self):
        with self.app.test_request_context(data=json.dumps({"foo": "bar"})):
            self.initialize_function_and_call(
                decorator_kwargs={'json': self.TestSchema, 'json_force_load': True},
            )
            self.assertEqual(self.TestSchema(foo='bar'), context_property.request_json)
