# Flask-Large-Application-Example
This is how I structure my large Flask applications.

Google과 GitHub의 수많은 Best Practice들과 예제들을 분석하고, 직접 서버를 만들며 고민한 Flask 어플리케이션 예제입니다.

## Diff
현재 repository의 변화 과정은 다음과 같습니다.
### Start
Quickstart라는 이름으로 레포를 시작했습니다. 서드파티로 Flask-restful을 사용하고 main.py에서 리소스를 모아주는 구조였습니다. Config를 다루는 부분도 없었고, DB를 MySQL로 한정지었던 점과 과도한 기반 모듈들 탓에 개인화 시키거나 큰 프로젝트를 진행하기엔 다소 무리가 있었습니다.
### Refactor(~ commit #ae163e3)
기존에 작성해 두었던 Quickstart는 문제가 많았습니다. Flask를 이용해 프로젝트를 진행하며 구조에 대한 고민을 많이 하게 되어 리팩토링을 진행했습니다. Application factory(create_app())와 같은 best practice들을 적용하고, app 객체의 before_first_request()같은 데코레이터를 통해 logging 수행부를 추가했습니다. Config 관리도 클래스 단위로 움직이도록 했습니다.

다만 API의 자동 라우팅을 위해 기반 모듈로 사용했던 blueprints.py는 범용적으로 사용하기에 무리가 있었고, 서브파티 라이브러리로 사용했던 flask-restful-swagger-2는 확장성이 부족한 Swagger UI 빌더였습니다. 또한 logger도 유의미한(분석 가능한) JSON 형태의 logging이 더 낫습니다.
### Change structure(~ commit #f2d564a)
타 Best practice들을 참고하며 구조를 크게 바꿨습니다. __init__.py를 적극적으로 활용하고, models, views 패키지를 분리했습니다. 구조적으론 발전했으나, 기존의 blueprints.py나 flask-restful-swagger-2같이 문제될 수 있는 부분은 그대로 남아 있었습니다. config를 다루는 부분을 클래스 기반/모듈 상수 기반 중 고민했으나 후자로 결정했습니다.
### Generalization 1(~ commit #3de1af5)
현재 레포를 참고해서 프로젝트를 진행하고 있는 Flask 입문자들이 많아 누가 보기에도 합당한 구조의 Flask 어플리케이션을 고민했습니다. 먼저 확장성에 무리가 있는 blueprints.py를 제거하고, Swagger doc 딕셔너리를 관리하기 위한 docs/ 패키지 추가, 403, 404, 500 에러 핸들링을 추가했습니다.
### Generalization 2(~ commit #181e157)
API 테스팅을 위한 tests/ 패키지 추가, Swagger API documentation을 지원하기 위한 라이브러리를 flask-restful-swagger-2에서 flasgger로 바꿨습니다. 그로 인해 필요없어진 CORS support도 동시에 제거했습니다.

flask-restful로 API를 만들기 위한 BaseResource 클래스가 추가되고, blueprint 기반의 API register 구조를 고안했습니다.

## I Referred
### People
<a href="https://github.com/JungWinter">존경하는 정겨울님</a>
### Repository
<a href="https://github.com/yoshiya0503/Flask-Best-Practices">Flask Best Practice에 관한 일본어 Repository</a>  
<a href="https://github.com/miguelgrinberg/flasky">O'Reilly의 'Flask Web Development' 예제 코드 모음</a>  
<a href="https://github.com/JackStouffer/Flask-Foundation">JackStouffer / Flask-Foundation</a>  
<a href="https://github.com/codecool/flask-app-structure">codecool / flask-app-structure</a>
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
