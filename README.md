# Flask-Large-Application-Example
This is how I structure my large Flask applications.

## Guide
패키지는 `app/`, `config/`, `migrations/`, `tests/`, `utils/`로 나뉘어 있습니다.

### app/
`docs/`, `models/`, `views/` 패키지로 나뉘어 있고 웹 서버 개발 시 필요한 템플릿과 정적 파일을 위해 static, templates 디렉토리가 구성되어 있습니다. docs에는 Swagger doc 관리, models에는 SQLAlchemy나 MongoEngine을 이용해 설계된 스키마 관리, views에는 API를 작성하는 방식입니다. flask-restful.Api와 flask.Blueprint를 적극적으로 사용하는, 개인적으로 이상적이라 생각하는 방식으로 샘플(app/views/sample.py)을 만들어 두었습니다.

`models/\_\_init\_\_.py`에 Mongo, `views/\_\_init\_\_.py`에 Router 클래스가 있으며 각각 서버 시작 전 DB Connect, 라우팅을 담당합니다. `views/\_\_init\_\_.py`의 BaseResource 클래스는 view function에서 쓸만한 helper function들을 classmethod로 관리하기 좋습니다. SQLAlchemy, MongoEngine과 WTForms 사이의 연동이 굉장히 좋으니, Model만 만들고 combine하는 것도 생산성을 높이는 하나의 방법입니다.

### config/
Config, DevConfig, ProductionConfig 클래스가 각각 `\_\_init\_\_.py`, `dev.py`, `production.py` 모듈에 나뉘어 서버 구성에 필요한 설정 값들을 다룹니다.

### migrations/
Alembic이나 Flask-migrate로 데이터베이스 마이그레이션 시 사용 가능한 패키지입니다. 세분화는 되어 있지 않습니다.

### tests/
Model이나 API에 대한 테스트 케이스를 작성하는 패키지입니다. `\_\_init\_\_.py`에 `TCBase` 클래스가 있으며, 모든 테스트 케이스에 적용되어야 할 initialize와 exit 패턴을 여기서 관리하면 좋습니다.

### utils/
mongo_to_dict, merge_dict 등과 같은 헬퍼 모듈/함수를 해당 패키지에서 다루면 좋습니다.

### Swagger를 쓰지 않을거라면
1. `app/docs/` 패키지를 제거합니다.
2. `app/\_\_init\_\_.py`에서 `flasgger`와 관련된 구문을 모두 지웁니다.
3. config/\_\_init\_\_.py에서 `SWAGGER` 필드를 제거합니다.

### MongoEngine을 쓰지 않을거라면
1. `app/models/\_\_init\_\_.py`에서 Mongo 클래스를 기호에 맞게(SQLAlchemy 등) 커스텀하거나, `app/models/` 패키지를 제거합니다.
2. `app/\_\_init\_\_.py`에서 `Mongo`와 관련된 구문을 모두 지웁니다.
3. config/dev.py와 config/production.py에서 `MONGODB_SETTINGS` 필드를 제거합니다.

## I Referred
### People
<a href="https://github.com/JungWinter">존경하는 정겨울님</a>
### Repository
<a href="https://github.com/yoshiya0503/Flask-Best-Practices">Flask Best Practice에 관한 일본어 Repository</a>  
<a href="https://github.com/miguelgrinberg/flasky">O'Reilly의 'Flask Web Development' 예제 코드 모음</a>  
<a href="https://github.com/JackStouffer/Flask-Foundation">JackStouffer / Flask-Foundation</a>  
<a href="https://github.com/realpython/flask-skeleton/blob/master/manage.py">realpython / flask-skeleton</a>  
<a href="https://github.com/swaroopch/flask-boilerplate/tree/master/flask_application">swaroopch / flask-boilerplate</a>
### Website
<a href="https://exploreflask.com/en/latest/">Explore Flask - Explore Flask 1.0 documentation</a>  
<a href="http://exploreflask.com/en/latest/organizing.html">Organizing your project - Explore Flask 1.0 documentation</a>  
<a href="http://flask.pocoo.org/docs/0.12/patterns/">Patterns of Flask - Flask Documentation (0.12)</a>  
<a href="http://flask.pocoo.org/docs/0.12/patterns/packages/">Larger Applications - Flask Documentation (0.12)</a>  
<a href="https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications">How To Structure Large Flask Applications | DigitalOcean</a>  
<a href="http://flask.pocoo.org/snippets/category/application-structure/">Application Structure | Flask(A Python Microframework)</a>  
<a href="https://www.gitbook.com/book/ecod/flask-large-app-how-to/details">Flask Large App How to - GitBook</a>  
<a href="https://libsora.so/posts/flask-project-structure/">Flask Project 구조 예제 - /usr/lib/libsora.so</a>  
<a href="https://stackoverflow.com/questions/14415500/common-folder-file-structure-in-flask-app">StackOverflow - Common folder/file structure in Flask app</a>
### Presentation
<a href="http://slides.skien.cc/flask-hacks-and-best-practices/">Flask Hacks and Best Practices</a>

## API Security Checklist
### 인증 (Authentication)
- [ ] `Basic Auth`를 사용하지 말고 표준 인증방식을 사용하세요. (예로, JWT, OAuth 등)
- [ ] `인증`, `토큰 생성`, `패스워드 저장`은 직접 개발하지 말고 표준을 사용하세요.
- [ ] 로그인에서 `Max Retry`와 격리 기능을 사용하세요.
- [ ] 민감한 데이터는 암호화하세요.

#### JWT (JSON Web Token)
- [ ] 무작위 대입 공격을 어렵게 하기 위해 랜덤하고 복잡한 키값 (`JWT Secret`)을 사용하세요.
- [ ] 요청 페이로드에서 알고리즘을 가져오지 마세요. 알고리즘은 백엔드에서 강제로 적용하세요. (`HS256` 혹은 `RS256`)
- [ ] 토큰 만료 기간 (`TTL`, `RTTL`)은 되도록 짧게 설정하세요.
- [ ] JWT 페이로드는 [디코딩이 쉽기](https://jwt.io/#debugger-io) 때문에 민감한 데이터는 저장하지 마세요.

#### OAuth
- [ ] 허용된 URL만 받기 위해서는 서버 단에서 `redirect_uri`가 유효한지 항상 검증하세요.
- [ ] 토큰 대신 항상 코드를 주고받으세요. (`response_type=token`을 허용하지 마세요)
- [ ] OAuth 인증 프로세스에서 CSRF를 방지하기 위해 랜덤 해쉬값을 가진 `state` 파라미터를 사용하세요.
- [ ] 디폴트 스코프를 정의하고 각 애플리케이션마다 스코프 파라미터의 유효성을 검증하세요.

### 접근 (Access)
- [ ] DDoS나 무작위 대입 공격을 피하려면 요청 수를 제한하세요. (Throttling)
- [ ] MITM (중간자 공격)을 피하려면 서버 단에서 HTTPS를 사용하세요.
- [ ] SSL Strip 공격을 피하려면 `HSTS` 헤더를 SSL과 함께 사용하세요.
- [ ] 비밀번호 각각 다른 salt를 적용하세요.

### 입력 및 요청 (Input)
- [ ] 각 요청 연산에 맞는 적절한 HTTP 메서드를 사용하세요. `GET (읽기)`, `POST (생성)`, `PUT (대체/갱신)`, `DELETE (삭제)`
- [ ] 서버에서 지원하는 포맷 (예를 들어 `application/xml`이나 `application/json` 등)만을 허용하기 위해 요청의 Accept 헤더의 `content-type`을 검증하여 매칭되는 게 없을 경우엔 `406 Not Acceptable`로 응답하세요.
- [ ] 요청받은 POST 데이터의 `content-type`을 검증하세요. (예를 들어 `application/x-www-form-urlencoded`나 `multipart/form-data` 또는 `application/json` 등)
- [ ] 일반적인 취약점(`XSS`, `SQL-Injection`, `Remote Code Execution` 등)들을 피하기 위해선 사용자 입력의 유효성을 검증하세요.
- [ ] URL에는 그 어떤 민감한 데이터(`자격 인증 (crendentials)`, `패스워드`, `보안 토큰` 또는 `API 키`)도 포함하고 있어서는 안 되며 이러한 것들은 표준 인증 방식의 헤더를 사용하세요.
- [ ] 캐싱과 속도 제한 정책을 제공하는 API 게이트웨이 서비스(`Quota`, `Spike Arrest`, `Concurrent Rate Limit` 등)를 사용하세요.

### 서버 처리
- [ ] 잘못된 인증을 피하기 위해 모든 엔드포인트가 인증 프로세스 뒤에서 보호되고 있는지 확인하세요.
- [ ] 사용자의 리소스 식별자를 사용하는 건 지양하세요. `/user/654321/orders` 대신 `/me/orders`를 사용하세요.
- [ ] 자동 증가 (auto-increment) 식별자 대신 `UUID`를 사용하세요.
- [ ] XML 파일을 파싱하고 있다면, `XXE` (XML external entity attack)를 피하기 위해 엔티티 파싱을 비활성화하세요.
- [ ] XML 파일을 파싱하고 있다면, 지수적 엔티티 확장 공격을 통한 빌리언 러프/XML 폭탄을 피하기 위해 엔티티 확장을 비활성화하세요.
- [ ] 파일 업로드에는 CDN을 사용하세요.
- [ ] 거대한 양의 데이터를 다루고 있다면, HTTP 블로킹을 피하고 응답을 빠르게 반환하기 위해 워커나 큐를 사용하세요.
- [ ] 디버그 모드를 꺼놓는 일을 절대 잊지 마세요.

### 반환 및 응답 (Output)
- [ ] `X-Content-Type-Options: nosniff` 헤더를 반환하세요.
- [ ] `X-Frame-Options: deny` 헤더를 반환하세요.
- [ ] `Content-Security-Policy: default-src 'none'` 헤더를 반환하세요.
- [ ] `X-Powered-By`, `Server`, `X-AspNet-Version` 등의 fingerprinting 성격의 헤더는 제거하세요.
- [ ] 응답에 `content-type`을 강제하세요. 만약 `application/json` 데이터를 반환하고 있다면 응답의 `content-type`은 `application/json`입니다.
- [ ] `자격 인증 (crendentials)`, `패스워드`, `보안 토큰`과 같은 민감한 데이터는 반환하지 마세요.
- [ ] 각 연산에 맞는 적절한 상태 코드를 반환하세요. (예를 들어 `200 OK`, `400 Bad Request`, `401 Unauthorized`, `405 Method Not Allowed` 등)

### CI & CD
- [ ] 단위/통합 테스트로 설계 및 구현을 검토하세요.
- [ ] 모든 API를 테스트하세요.
- [ ] 배포를 자동화하세요.
- [ ] 코드 리뷰 절차를 사용하고 자체 승인을 무시하세요.
- [ ] 배포에 대한 롤백 솔루션을 설계하세요.

### 관례
- [ ] JSON request/response payload의 각 요소에 대한 네이밍 프로토콜은 camel case로 구성하세요.
- [ ] 데이터베이스의 모든 row/document/key-value pair에 대해 타임스탬핑하세요.
