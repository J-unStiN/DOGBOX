DOGBOX
=============

개발환경: Rasberry PI Zero W
개발언어: Python

## 설명
GPIO를 통해 소리감지센서모듈을 제어하고 소리를 감지하면 카메라가 작동하여 영상을 녹화 및 영상캡쳐 후 저장
저장된 영상의 객체를 확인하고 사용자에게 이메일로 전송합니다.


now = datetime.datetime.now()
filename = now.strftime('/home/pi/Videos/%Y-%m-%d-%H:%M:%S') 
코드를 통해 촬영한 영상의 파일이름을 현재시간으로 저장하였습니다.

개발시 라즈베리파이 제로W의 H/W 한계로 인해 Tensorflow가 작동되지 않아 객체 인식을 하기 위하여 OpenCV DNN을 사용하였습니다.

SMTP을 통해 구글의 SMTP 서버에 접속하여 메일을 보내고 MIMEBase 을 통하여 메일 규격에 맞는 메시지를 작성했습니다.


## 영상링크
https://youtu.be/uOoeQZHqrQ0



