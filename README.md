# Flask-Server-Quickstart
내가 Flask 서버를 만들 때 쓸 퀵스타트

### 필요 모듈
	flask
	flask-restful
	pymysql
	pyfcm
	cryptography

### 구현되어 있는 기반 모듈
#### main.py
Flask의 객체를 생성하고 flask_restful의 Api의 객체를 생성하여 sample 모듈의 Sample 클래스를 /test URI에 라우팅한 예.
app.secret_key 변수는 서버에서 세션을 사용할 경우 채워주어야 함(Flask는 세션을 시큐어 쿠키를 통해 제공함)
### support 패키지
#### crypto.py
Fernet을 이용한 양방향 암호화와 sha를 이용한 SHA512 단방향 암호화 함수 지원

	from support import crypto
	encrypted_text = crypto.fernet_encrypt(‘plain text’)
	decrypted_text = crypto.fernet_decrypt(encrypted_text)
Fernet 사용 시 key 필드에 ‘=’로 끝나는 44자리의 영어 알파벳, 숫자로 이루어진 bytes 값 입력 필요

	key = b'wWX4VyWSzKifCA-kZ_9j4y9LjRc5iGxVH_6AgDUBQXs='
generate_key 함수를 호출하면 key에 맞는 랜덤 bytes 값을 출력함

	from support import crypto
	crypto.generate_key()
	> b'wWX4VyWSzKifCA-kZ_9j4y9LjRc5iGxVH_6AgDUBQXs='

#### mysql.py
pymysql을 이용한 MySQL 데이터베이스 접근 모듈
모듈 사용 시 user, password, db 필드에 각각 사용자 이름, 비밀번호, 테이블 이름 입력 필요

	from support import mysql
	result = mysql.execute(“SELECT * FROM table WHERE col=’”, “value”, “’”)

#### mail.py
Smtplib을 이용한 SMTP 이메일 전송 모듈
모듈 사용 시 from_email, smtp_host, smtp_port, smtp_id, smtp_pw 필드에 데이터 입력 필요

	from support import mail
	mail.send(‘someemail@google.com’, ‘제목’, ‘내용’)

#### firebase.py
pyfcm을 이용한 Firebase 푸쉬 알림 모듈
모듈 사용 시 FCMNotifiaction 객체 생성 구문의 api_key 매개변수에 데이터 입력 필요

	from support import firebase
	result = firebase.notify_topic_subscribers(‘제목’, ‘내용’, ‘topic_name’)
	result = firebase.notify_single_device(‘제목’, ‘내용’, ‘registration_id’)

### restful 패키지
#### sample.py
flask_restful을 활용하여 Sample 클래스를 만들어 둔 샘플 모듈
