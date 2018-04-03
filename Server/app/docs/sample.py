SAMPLE_POST = {
    'tags': ['Some Tag'],
    'description': '요청 JSON payload를 그대로 응답',
    'parameters': [
        {
            'name': 'name',
            'description': '이름',
            'in': 'json',
            'type': 'str',
            'required': True
        },
        {
            'name': 'age',
            'description': '나이',
            'in': 'json',
            'type': 'int',
            'required': True
        }
    ],
    'responses': {
        '201': {
            'description': '성공',
            'examples': {
                '': {
                    'name': '조민규',
                    'age': 19
                }
            }
        }
    }
}
