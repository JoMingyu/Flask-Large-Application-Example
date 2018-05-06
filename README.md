# Flask-Large-Application-Example
This is how I structure my large Flask applications.

## About
Flask는 마이크로 웹 프레임워크입니다. Django처럼 정해져 있는 구조가 없어 항상 개발자에게 구조에 대한 고민을 하게 만듭니다. 이 저장소는 제가 Flask를 배우기 시작했던 때부터, 1년 가까이의 시간동안 Flask 어플리케이션의 구조에 대해 고민한 흔적입니다.

## 기준
API 문서화에 Swagger(flasgger), 데이터베이스에 MongoDB(MongoEngine), 인증 처리에 JWT(flask-jwt-extended), 데이터 압축에 gzip, 테스트에 unittest를 사용한다고 가정합니다.

## 요소
### server.py
```
if __name__ == '__main__':
    app = create_app(DevConfig)

    ...

    app.run(**app.config['RUN_SETTING'])
```
Application factory에 Config 클래스를 전달하여 Flask 인스턴스를 얻고, 해당 객체에 정의된 config를 이용해 Flask 어플리케이션을 실행합니다. Argument parser를 이용해 포트를 받거나, secret_key가 환경변수에 없는 경우 warning을 띄우는 간단한 로직들도 함께 정의되어 있습니다.

### config/\_\_init\_\_.py & config/\*\*\*.py
#### Class based config management
```
class Config:
    SERVICE_NAME = 'Flask_Large_Application_Example'
    REPRESENTATIVE_HOST = None

    RUN = {
        'threaded': True
    }

    SECRET_KEY = os.getenv('SECRET_KEY', '85c145a16bd6f6e1f3e104ca78c6a102')

    ...

class DevConfig(Config):
    HOST = 'localhost'
    PORT = 5000
    DEBUG = True

    RUN = dict(Config.RUN, **{
        'host': HOST,
        'port': PORT,
        'debug': DEBUG
    })

    ...
```

Flask에서 설정을 다루기 위한 방법은, config 프로퍼티가 dict-like 객체인 점을 이용한 `app.config[]`, `app.config.update()`나 해당 객체가 재정의한 메소드인 `app.config.from_envvar()`, `app.config.from_pyfile()` 등을 사용할 수 있습니다. 한가지 흥미로운 패턴은, 설정에 대해서도 클래스를 사용할 수 있으며 상속 구조도 가능하다는 것입니다. 설정 파일을 어떻게 관리하길 원하는가에 따라 다르지만, 저는 클래스 상속 구조 형태로 설정 값들을 다룰 경우 간결하고 이상적이라고 보고 있습니다.

### app/\_\_init\_\_.py
#### Application Factory
```
def create_app(*config_cls):
    """
    Creates Flask instance & initialize

    Returns:
        Flask
    """
    app_ = Flask(
        __name__,
        ...
    )

    for config in config_cls:
        app_.config.from_object(config)

    ...

    return app_
```

일반적인 Flask의 패턴은 `Blueprint를 가져오며 Flask 객체를 만드는 것`입니다. 그러나 이 객체의 생성을 함수 형태로 만들어 두면, 나중에 이 Flask 어플리케이션의 여러 인스턴스를 만들 수 있습니다.

1. 테스트 : Flask 어플리케이션의 인스턴스를 다른 설정으로 지정하여 모든 경우를 테스트할 수 있습니다.
2. 여러 인스턴스 : 동알한 Flask 어플리케이션의 서로 다른 버전을 실행시킨다고 가정한다면, 웹 서버에 다른 설정을 가진 다중 인스턴스를 가지도록 하는 것보다 application factory 패턴을 이용해 같은 어플리케이션의 여러 인스턴스를 편하게 사용할 수 있게 됩니다.

### app/views/sample.py
#### flask-restful의 pluggable view-like resource routing
Flask 튜토리얼 등에서 사용하는 건 함수 기반의 라우팅입니다.

```
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'hello'
```

위의 코드는 간단하지만, 다른 모델이나 템플릿에도 적용 가능한 방식으로 뷰를 제공하고 싶다면 더 유연한 구조가 필요할 수 있습니다. Flask 0.7에 추가된 Pluggable View는 Django의 Generic View에 영향을 받았습니다. Flask는 Pluggable View를 위해 `flask.views.View`와 `flask.view.MethodView` 클래스를 제공하며, 여기서는 MethodView를 이용한 `메소드 기반 디스패치`를 사용하고, flask-restful의 도움을 받아 Blueprint 기반으로 라우팅을 더욱 직관적으로 진행합니다.

```
from flask import Blueprint
from flask_restful import Api, Resource

api = Api(Blueprint('sample_api', __name__))
api.prefix = '/prefix'


@api.resource('/sample')
class Sample(Resource):
    def get(self):
        return {
            'msg': 'hello!'
        }
```

### app/views/\_\_init\_\_.py
#### Router
위에서 정의한 블루프린트 기반의 리소스들을 Flask 인스턴스에 할당합니다.

```
class Router(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        from app.views import sample
        app.register_blueprint(sample.api.blueprint)
```
#### BaseResource
flask-restful.Resource(flask.views.MethodView) 클래스를 상속받은 클래스입니다. 파이썬이 유니코드 형태로 문자열을 다루기 때문에 생기는 문제 등을 해결하고 몇가지 유의미한 인스턴스 변수들을 제공합니다. view function에서 자주 사용할만한 기능들을 여기에 메소드화하여 API 리소스를 재사용성 높게 설계할 수 있습니다.

```
class BaseResource(Resource):
    def __init__(self):
        self.now = time.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def unicode_safe_json_dumps(cls, data, status_code=200, **kwargs):
        return Response(
            ujson.dumps(data, ensure_ascii=False),
            status_code,
            content_type='application/json; charset=utf8',
            **kwargs
        )
```

#### auth_required & json_required & gzipped & ...
[뷰 데코레이터](http://flask-docs-kr.readthedocs.io/ko/latest/patterns/viewdecorators.html)는 각 뷰 함수에 추가적인 기능을 주입하는 데 사용될 데코레이터입니다. 이들은 application context와 request context에 모두 접근할 수 있어, g나 current_app을 활용한 유연한 비즈니스 로직을 작성하기에 유리합니다.

```
def auth_required(model):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            ...

            return fn(*args, **kwargs)
        return wrapper
    return decorator

def json_required(*required_keys):
    def decorator(fn):
        if fn.__name__ == 'get':
            print('[WARN] JSON with GET method? on "{}()"'.format(fn.__qualname__))

        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                abort(406)

            for required_key in required_keys:
                if required_key not in request.json:
                    abort(400)

            return fn(*args, **kwargs)
        return wrapper
    return decorator
```

#### Error handler, request context callback
API 보안을 위한 헤더 설정을 위해 request context callback인 `after_request`와 서버에서 발생하는 오류를 잡아 특정 로직을 수행하기 위한 보일러플레이트인 `exception_handler`를 정의하였습니다.

```
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'deny'

    return response

def exception_handler(e):
    # TODO

    return '', 500
```

### tests/views/\_\_init\_\_.py
#### TCBase
unittest로 테스트 시, test fixture의 중복을 제거하기 위해 만들어 둔 베이스 클래스입니다. 테스트 작성 시 request 코드를 짧게 작성하고 response 데이터를 쉽게 가공하기 위한 헬퍼 메소드 몇가지도 정의되어 있습니다. 이전에는 json_request 메소드도 함께 존재하였으나, Flask 1.0에선 Flask test client의 요청 메소드에서 json 파라미터를 제공하기 때문에 제거하였습니다.

```
class TCBase(TC):
    def __init__(self, *args, **kwargs):
        self.client = app.test_client()
        self.today = datetime.now().strftime('%Y-%m-%d')

        super(TCBase, self).__init__(*args, **kwargs)

    def setUp(self):
        ...

    def tearDown(self):
        ...

    def request(self, method, target_url_rule, token=None, *args, **kwargs):
        ...

    def decode_response_data(self, resp):
        return resp.data.decode()

    def get_response_data_as_json(self, resp):
        return ujson.loads(self.decode_response_data(resp))
```

## I Referred
### People
<a href="https://github.com/JungWinter">존경하는 정겨울님</a>

### Repository
<a href="https://github.com/yoshiya0503/Flask-Best-Practices">Flask Best Practice에 관한 일본어 Repository</a>  
<a href="https://github.com/miguelgrinberg/flasky">flasky - O'Reilly의 'Flask Web Development' 예제 코드 모음</a>  
<a href="https://github.com/JackStouffer/Flask-Foundation">JackStouffer / Flask-Foundation</a>  
<a href="https://github.com/realpython/flask-skeleton">realpython / flask-skeleton</a>  
<a href="https://github.com/swaroopch/flask-boilerplate">swaroopch / flask-boilerplate</a>

### Website
<a href="https://exploreflask.com/en/latest/">Explore Flask - Explore Flask 1.0 documentation</a>  
<a href="http://exploreflask.com/en/latest/organizing.html">Organizing your project - Explore Flask 1.0 documentation</a>  
<a href="http://flask.pocoo.org/docs/0.12/patterns/">Patterns of Flask - Flask Documentation (0.12)</a>  
<a href="http://flask.pocoo.org/docs/0.12/patterns/packages/">Larger Applications - Flask Documentation (0.12)</a>  
<a href="http://flask.pocoo.org/snippets/category/application-structure/">Application Structure | Flask(A Python Microframework)</a>  

<a href="https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications">How To Structure Large Flask Applications | DigitalOcean</a>  
<a href="https://damyanon.net/post/flask-series-structure/">How to Structure a Flask Application</a>  
<a href="https://www.gitbook.com/book/ecod/flask-large-app-how-to/details">Flask Large App How to - GitBook</a>  
<a href="https://libsora.so/posts/flask-project-structure/">Flask Project 구조 예제 - /usr/lib/libsora.so</a>  
<a href="https://stackoverflow.com/questions/14415500/common-folder-file-structure-in-flask-app">StackOverflow - Common folder/file structure in Flask app</a>

### Presentation
<a href="http://slides.skien.cc/flask-hacks-and-best-practices/">Flask Hacks and Best Practices</a>
