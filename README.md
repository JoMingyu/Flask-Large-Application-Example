# Flask-Large-Application-Example
This is how I structure my large Flask applications.  

## Guide
패키지는 app/, config/, migrations/, tests/, utils/로 나뉘어 있습니다.

### app/
docs/, models/, views/ 패키지로 나뉘어 있고 웹 서버 개발 시 필요한 템플릿과 정적 파일을 위해 static, templates 디렉토리가 구성되어 있습니다. docs에는 Swagger doc, models에는 SQLAlchemy나 MongoEngine을 이용해 설계된 스키마, views에는 API를 작성하는 방식입니다. flask-restful.Api와 flask.Blueprint를 적극적으로 사용하는, 개인적으로 이상적이라 생각하는 방식으로 샘플(app/views/sample.py)을 만들어 두었습니다.

models/\_\_init\_\_.py에 Mongo, views/\_\_init\_\_.py에 ViewInjector 클래스가 있으며 각각 서버 시작 전 DB Connect, 라우팅을 담당합니다. views/\_\_init\_\_.py의 BaseResource 클래스는 view function에서 쓸만한 helper function들을 classmethod로 관리하기 좋습니다.

### config/
Config, DevConfig, ProductionConfig 클래스가 각각 \_\_init\_\_.py, dev.py, production.py 모듈에 나뉘어 서버 구성에 필요한 설정 값들을 다룹니다.

### migrations/
Alembic이나 Flask-migrate로 데이터베이스 마이그레이션 시 사용 가능한 패키지입니다. 세분화는 되어 있지 않습니다.

### tests/
Model이나 API에 대한 테스트 케이스를 작성하는 패키지입니다. \_\_init\_\_.py에 TCBase 클래스가 있으며, 모든 테스트 케이스에 적용되어야 할 initialize와 exit 패턴을 여기서 관리하면 좋습니다.

### utils/
mongo_to_dict, merge_dict 등과 같은 헬퍼 모듈/함수를 해당 패키지에서 다루면 좋습니다.

### Swagger를 쓰지 않을거라면
1. app/docs/ 패키지를 제거합니다.
2. app/\_\_init\_\_.py에서 flasgger와 관련된 구문을 모두 지웁니다.
3. config/\_\_init\_\_.py에서 SWAGGER 필드를 제거합니다.

### MongoEngine을 쓰지 않을거라면
1. app/models/\_\_init\_\_.py에서 Mongo 클래스를 기호에 맞게(SQLAlchemy 등) 커스텀하거나, app/models/ 패키지를 제거합니다.
2. app/\_\_init\_\_.py에서 Mongo와 관련된 구문을 모두 지웁니다.
3. config/dev.py와 config/production.py에서 MONGODB_SETTINGS 필드를 제거합니다.

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
