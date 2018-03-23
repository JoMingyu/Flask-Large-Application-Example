# Flask-Large-Application-Example
This is how I structure my large Flask applications.

## About
'나중에 쓰려고' 만든 Flask 어플리케이션 예제이자 보일러플레이트입니다. 따라서 Swagger, MongoDB + MongoEngine, JWT, unittest와 같이 지극히 개인 취향인 기능들이 많아 일반화되어있지 않고 복잡할 수 있습니다. Flask의 설계 원칙(micro)에 맞는 간단하고, 일반화된 Flask 어플리케이션의 예제를 보려면 <a href="https://github.com/JoMingyu/Flask-Large-Application-Example-Simplified">Flask Large Application Example - Simplified</a>를 참고하시기 바랍니다.

## 요소
### Application Factory(app/\_\_init\_\_.py)
```
def create_app(dev=True):
    """
    Creates Flask instance & initialize

    :rtype: Flask
    """
    app_ = Flask(__name__)

    ...
```
일반적인 Flask의 패턴은 Blueprint를 가져오며 Flask 객체를 만드는 것입니다. 그러나 이 객체의 생성을 함수 형태로 만들어 두면, 나중에 이 Flask 어플리케이션의 여러 인스턴스를 만들 수 있습니다.

1. 테스트 : Flask 어플리케이션의 인스턴스를 다른 설정으로 지정하여 모든 경우를 테스트할 수 있습니다.
2. 여러 인스턴스 : 동알한 Flask 어플리케이션의 서로 다른 버전을 실행시킨다고 가정한다면, 웹 서버에 다른 설정을 가진 다중 인스턴스를 가지도록 하는 것보다 application factory 패턴을 이용해 같은 어플리케이션의 여러 인스턴스를 편하게 사용할 수 있게 됩니다.

### Class based config(config/)
```
class Config(object):
    REPRESENTATIVE_HOST = None
    PORT = 3000

    ...

class DevConfig(Config):
    HOST = 'localhost'

    if not Config.REPRESENTATIVE_HOST:
        Config.SWAGGER['host'] = '{}:{}'.format(HOST, Config.PORT)

    DEBUG = True

    ...
```
Flask에서 설정을 다루기 위한 방법은 `app.config[]`, `app.config.update()`, `app.config.from_envvar()`, `app.config.from_pyfile()` 등이 있습니다. 한가지 흥미로운 패턴은, 설정에 대해서도 클래스를 사용할 수 있으며 상속 구조도 가능하다는 것입니다. 설정 파일을 어떻게 관리하길 원하는가에 따라 다르지만, 저는 클래스 상속 구조 형태로 설정 값들을 다룰 경우 간결하고 이상적이라고 보고 있습니다.

### 플러거블 뷰(app/views/sample.py)
Flask 튜토리얼 등에서 사용하는 건 함수 기반의 라우팅입니다.
```
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'hello'
```

위의 코드는 간단하고 유연하지만, 다른 모델이나 템플릿에도 적용 가능한 방식으로 뷰를 제공하고 싶다면 더 유연한 구조가 필요할 수 있습니다. Flask 0.7에 추가된 Pluggable View는 Django의 Generic View에 영향을 받았습니다. Flask는 Pluggable View를 위해 `flask.views.View`와 `flask.view.MethodView` 클래스를 제공하며, 여기서는 MethodView를 이용한 `메소드 기반 디스패치`를 사용하고, flask-restful의 도움을 받아 Blueprint 기반으로 라우팅을 더욱 직관적으로 진행합니다.

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

이와 같이 각 모듈에서 블루프린트 기반으로 리소스를 정의해 두고, 아래처럼 Flask 인스턴스에 블루프린트를 할당하는 방식입니다.

```
class Router(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        from app.views import sample
        app.register_blueprint(sample.api.blueprint)
```

### BaseResource(app/views/\_\_init\_\_.py)
flask-restful.Resource(flask.views.MethodView) 클래스를 상속받은 클래스입니다. 파이썬이 유니코드 형태로 문자열을 다루기 때문에 생기는 문제 등을 해결합니다. 현재는 `unicode_safe_json_dumps` 메소드와 `self.now` 인스턴스 필드만을 가지고 있습니다. `self.` 형태로 접근할 만한 헬퍼 함수를 정의하는 경우, 여기에 선언해서 사용하면 좋습니다.

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

### 뷰 데코레이터(app/views/\_\_init\_\_.py)
<a href="http://flask-docs-kr.readthedocs.io/ko/latest/patterns/viewdecorators.html">뷰 데코레이터</a>는 각 뷰 함수에 추가적인 기능을 주입하는 데 사용될 데코레이터입니다. 여기서는 API 보안을 위한 헤더 설정을 위해 `@app.after_request` 데코레이터를 설정했고, `@json_required`, `@auth_required` 데코레이터를 만들어 두었습니다.

```
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'deny'

    return response

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

### mongo_to_dict(app/views/models/support/mongo_helper.py)

### TCBase(tests/views/\_\_init\_\_.py)

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

## API Checklist
### API Spec
- [ ] Swagger나 Redoc 등을 사용해 API를 문서화하세요.
- [ ] 표준화된 API 설계 원칙을 따르세요. (REST, GraphQL 등)
### 관례
- [ ] JSON request/response payload의 각 요소에 대한 네이밍 프로토콜은 camel case로 구성하세요.
- [ ] 데이터베이스의 모든 row/document/key-value pair에 대해 타임스탬핑하세요.
### CI & CD
- [ ] 단위/통합 테스트로 설계 및 구현을 검토하세요.
- [ ] 모든 API를 테스트하세요.
- [ ] 배포를 자동화하세요.
- [ ] 코드 리뷰 절차를 사용하고 자체 승인을 무시하세요.
- [ ] 배포에 대한 롤백 솔루션을 설계하세요.

## API Security Checklist
### 인증 (Authentication)
- [ ] `Basic Auth`를 사용하지 말고 표준 인증방식을 사용하세요. (예로, JWT, OAuth 등)
- [ ] `인증`, `토큰 생성`, `패스워드 저장`은 직접 개발하지 말고 표준을 사용하세요.
- [ ] 로그인에서 `Max Retry`와 격리 기능을 사용하세요.
- [ ] 민감한 데이터는 모두 암호화하세요.

#### JWT (JSON Web Token)
- [ ] 무작위 대입 공격을 어렵게 하기 위해 랜덤하고 복잡한 키값 (`JWT Secret`)을 사용하세요.
- [ ] 요청 페이로드에서 알고리즘을 가져오지 마세요. 알고리즘은 백엔드에서 강제로 적용하세요. (`HS256` 혹은 `RS256`)
- [ ] 토큰 만료 기간 (`TTL`, `RTTL`)은 되도록 짧게 설정하세요.
- [ ] JWT 페이로드는 [디코딩이 쉽기](https://jwt.io/#debugger-io) 때문에 민감한 데이터는 저장하지 마세요.

#### OAuth
- [ ] 허용된 URL만 받기 위해서는 서버 단에서 `redirect_uri`의 유효성을 항상 검증하세요.
- [ ] 항상 토큰 대신 코드를 주고받으세요. (`response_type=token`을 허용하지 마세요)
- [ ] OAuth 인증 프로세스에서 CSRF를 방지하기 위해 랜덤 해쉬값을 가진 `state` 파라미터를 사용하세요.
- [ ] 디폴트 스코프를 정의하고 각 애플리케이션마다 스코프 파라미터의 유효성을 검증하세요.

### 접근 (Access)
- [ ] DDoS나 무작위 대입 공격을 피하려면 요청 수를 제한하세요. (Throttling)
- [ ] MITM (중간자 공격)을 피하려면 서버 단에서 HTTPS를 사용하세요.
- [ ] SSL Strip 공격을 피하려면 `HSTS` 헤더를 SSL과 함께 사용하세요.

### 입력 및 요청 (Input)
- [ ] 각 요청의 연산에 맞는 적절한 HTTP 메서드를 사용하세요. `GET (읽기)`, `POST (생성)`, `PUT (대체/갱신)`, `DELETE (삭제)`. 그리고 요청 메소드가 리소스에 적합하지 않은 경우 `405 Method Not Allowed`로 응답하세요.
- [ ] 여러분이 지원하는 포맷 (예를 들어 `application/xml`이나 `application/json` 등)만을 허용하려면 요청의 Accept 헤더에서 `content-type`의 유효성을 검사하고 일치하지 않으면 `406 Not Acceptable`로 응답하세요.
- [ ] 요청받은 POST 데이터의 `content-type`을 검증하세요. (예를 들어 `application/x-www-form-urlencoded`나 `multipart/form-data` 또는 `application/json` 등)
- [ ] 일반적인 취약점들을 피하기 위해선 사용자 입력의 유효성을 검증하세요. (예를 들어 `XSS`, `SQL-Injection` 또는 `Remote Code Execution` 등)
- [ ] URL에는 그 어떤 민감한 데이터 (`자격 인증 (crendentials)`, `패스워드`, `보안 토큰` 또는 `API 키`)도 포함하고 있어서는 안 되며 이러한 것들은 표준 인증 방식의 헤더를 사용하세요.
- [ ] 캐싱과 속도 제한 정책을 제공하는 API 게이트웨이 서비스 (예를 들어 `Quota`, `Spike Arrest`, `Concurrent Rate Limit`)를 사용하고, API 리소스를 동적으로 배포하세요.

### 서버 처리
- [ ] 인증 프로세스가 손상되는 것을 피하기 위해 모든 엔드포인트가 인증 프로세스 뒤에서 보호되고 있는지 확인하세요.
- [ ] 사용자 소유의 리소스 식별자는 피해야 합니다. `/user/654321/orders` 대신 `/me/orders`를 사용하세요.
- [ ] 자동 증가 (auto-increment) 식별자 대신 `UUID`를 사용하세요.
- [ ] XML 파일을 파싱하고 있다면, `XXE` (XML 외부 엔티티 공격, XML external entity attack)를 피하기 위해 엔티티 파싱을 비활성화하세요.
- [ ] XML 파일을 파싱하고 있다면, 지수적 엔티티 확장 공격을 통한 빌리언 러프/XML 폭탄을 피하기 위해 엔티티 확장을 비활성화하세요.
- [ ] 파일 업로드에는 CDN을 사용하세요.
- [ ] 거대한 양의 데이터를 다루고 있다면, 워커나 큐를 사용하여 가능한 한 백그라운드에서 처리하고, HTTP 블로킹을 피하기 위해 응답을 빠르게 반환하세요.
- [ ] 디버그 모드를 꺼놓는 일을 절대 잊지 마세요.

### 반환 및 응답 (Output)
- [ ] `X-Content-Type-Options: nosniff` 헤더를 반환하세요.
- [ ] `X-Frame-Options: deny` 헤더를 반환하세요.
- [ ] `Content-Security-Policy: default-src 'none'` 헤더를 반환하세요.
- [ ] `X-Powered-By`, `Server`, `X-AspNet-Version` 등의 디지털 지문 (fingerprinting) 성격의 헤더는 제거하세요.
- [ ] 응답에 `content-type`을 강제하세요. 만약 `application/json` 데이터를 반환하고 있다면 응답의 `content-type`은 `application/json`입니다.
- [ ] `자격 인증 (crendentials)`, `패스워드`, `보안 토큰`과 같은 민감한 데이터는 반환하지 마세요.
- [ ] 각 작업에 맞는 적절한 상태 코드를 반환하세요. (예를 들어 `200 OK`, `400 Bad Request`, `401 Unauthorized`, `405 Method Not Allowed` 등)
