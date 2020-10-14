# Flask-Large-Application-Example 
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/JoMingyu/Flask-Large-Application-Example/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/JoMingyu/Flask-Large-Application-Example/?branch=master) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/5df22321aa484650abb918f7a512274a)](https://www.codacy.com/app/JoMingyu/Flask-Large-Application-Example?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=JoMingyu/Flask-Large-Application-Example&amp;utm_campaign=Badge_Grade)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

This is how I structure my large Flask applications.

## About
마이크로 웹 프레임워크인 Flask는 항상 개발자에게 구조에 대한 고민을 하게 만듭니다. 이 저장소는 제가 Flask를 배우기 시작했던 고등학교 1학년 때부터 지금까지의 시간동안 Flask 어플리케이션의 구조에 대해 고민한 흔적입니다. 근데 뭐 계속 개선하다 보니까 Flask에게만 특별히 적용할 수 있는 구조라기 보단 다른 웹 프레임워크들에서도 써먹을 수 있는 기반이 될 수도 있을 것 같네요.

구조가 막 빡세다고 좋아지는 건 아닌 것 같아서, 조금 편하려고 복잡도를 높여버리는 모습은 지양했습니다. 이 레포의 '최신 버전'은 항상 제 기준에선 가장 편한 구조인데, 모두에게 그렇지도 않고 저도 자주 마음이 바뀝니다. 별거 아닌 코드에 커밋이 백단위인 게 이런 이유니까, 그냥 이거 가져가서 본인한테 맞게 커스텀하시면 좋을 것 같습니당 ㅎㅎ

## 컨셉
### application factory가 필요하다.([app/\_\_init\_\_.py](app/__init__.py))
local에서 실행해보는 용도, 테스트 클라이언트를 얻는 용도, 배포 단에서 사용하는 용도 등으로 app 객체가 필요한데, 그들은 모두 extension 초기화 - view들 라우팅 - hook 달아주는 것은 똑같고, 단지 주입되는 config가 다른 것밖에 차이가 없습니다. create_app에서 config class들을 받도록 했습니다.

### extension들은 lazy하게 초기화한다.([app/extensions.py](app/extensions.py), [app/\_\_init\_\_.py의 register_extensions](app/__init__.py#L7-L10))
어떤 config를 주입할지는 create_app 함수가 호출된 후 정해지므로, config에 의해 초기화가 진행되는 extension들은 lazy하게 초기화하도록 했습니다. 

### config를 따로 패키지화해서, 선택지를 두어 관리한다.([config/](config))
1. Flask에서 config는 class로 다루는 게 가장 좋다고 생각합니다.
2. Config는 정적이어야 합니다. Config class 내에서 if절이 있는 형태는 좋지 않다고 생각합니다. 환경 변수에 따라 서로 다른 config를 주입해야 한다면, 각각에 맞게 class를 나누어 준비한 후 create_app을 호출하는 단에서 config를 상황에 맞게 전달하도록 만드는 게 좋다고 봅니다. 
3. 선택지마다 모듈을 만들어 두었습니다. 예를 들어, Local DB를 바라보도록 하는 config/Remote DB를 바라보도록 하는 config를 db_config라는 모듈에 LocalDBConfig, RemoteDBConfig 클래스로 준비한다.

### 상수 config는 따로 관리되어야 한다.([constants/](constants))
DRY한 코드를 작성하기 위해 리터럴을 지양해야 합니다. 게시글 목록 API에서 반환해주는 게시글 기본 갯수나, 특정 API의 사용 가능 시간같은 것들을 예로 들 수 있습니다. 이런 상수 config들은 따로 관리해야 하는 것은 맞지만, 굳이 app 객체에 주입할 필요가 없습니다. 따로 모듈만 만들어 두면 됨.

### blueprint와 flask_restful이 필요하다.([app/views/\__init\__.py](app/views/__init__.py))
다른 복잡한 이유가 아니라, 더 구조적인 라우팅을 위해 blueprint의 url prefix, [flask_restful의 MethodView 확장](app/views/sample/sample.py)이 도움을 주기 때문입니다.

### context-dependent한 데이터는 따로 property class화 시킨다.([app/context.py](app/context.py))
request, g 처럼 contenxt-dependent한 객체는 attribute가 dynamic하기 때문에, known attribute를 가지는 객체를 만들어 중계해주는 게 좋습니다. 휴먼 에러 예방에 도움이 되더라구요.

### request context를 hook하는 친구들은 hook 패키지에 따로 관리한다.([app/hooks/](app/hooks))
### view function이 호출되기 전의 전처리는 view decorator가 하는 것이 맞다.([app/decorators/](app/decorators))

## I Referred
### People
<a href="https://github.com/JungWinter">정겨울님</a>

### Repository
- https://github.com/imwilsonxu/fbone
- https://github.com/cookiecutter-flask/cookiecutter-flask
- https://github.com/JackStouffer/Flask-Foundation
- https://github.com/alexandre-old/flask-rest-template
- https://github.com/dpgaspar/Flask-AppBuilder
- https://github.com/hack4impact/flask-base
- https://github.com/gothinkster/flask-realworld-example-app
- https://github.com/alexandre-old/flask-rest-template
- https://github.com/JoMingyu/Flask-Large-Application-Example
- https://github.com/yoshiya0503/Hermetica
- https://github.com/realpython/cookiecutter-flask-skeleton
- https://github.com/swaroopch/flask-boilerplate

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
