import RPi.GPIO as GPIO #서보모터 사용을 위해 불러옴
import firebase_admin #파이어베이스 sdk 불러오기
#라즈베리파이 현재시간을 불러오기 위해 사용
import time
import datetime


from firebase_admin import credentials  #파이어베이스 sdk 불러오기
from firebase_admin import db  #파이어베이스 sdk 불러오기
from time import sleep

#서보모터 GPIO 보드번호
pin = 18 # PWM pin num 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings (False)
GPIO.setup(pin, GPIO.OUT)
p = GPIO.PWM(pin, 50)
p.start(0) # 서보모터 duty 값 0으로 초기화

#Firebase database 인증
#Firebase에서 생성한 인증키를 통하여 서비스계정 인증
#automatic-feeder.json 파일에는 firebase 서비스 계정과 관련된 모든 정보 포함 (프로젝트id,프로젝트keyid,클라이언트id,email,인증uri,토큰uri 등..)
cred = credentials.Certificate('automatic-feeder.json')
#Firebase database 앱 초기화
firebase_admin.initialize_app(cred,{'databaseURL':'https://automatic-feeder-f3230.firebaseio.com/'})

cnt2 = db.reference('Feeder/count') #서버의 카운트값을 불러옴
cnt=cnt2.get()  #해당 카운트값을 cnt에 저장
print (cnt) #카운트값 화면에 출력 (정상실행 확인용)
cnt1 = int(cnt) #카운트값은 스트링 형식으로 불러오므로 값 비교를 위해 int값으로 변경함 (cnt1에 저장)

#while문을 통해 파이어베이스 서버의 값을 라즈베리파이에 실시간 연동 및 실시간 모터 구동 (무한루프)
while True :
    now= datetime.datetime.now() #datetime 함수를 통해 현재 라즈베리파이의 시간을 불러옴
    nowTime= now.strftime('%H%M%S') #불러온 시간에서 시간/분/초를 nowTime에 저장

    #파이어베이스 서버에 있는 Time1 Time2 Time3 값을 불러온다
    time1_1 = db.reference('Feeder/Time1')
    time1=time1_1.get()
    time2_2 = db.reference('Feeder/Time2')
    time2=time2_2.get()
    time3_3 = db.reference('Feeder/Time3')
    time3=time3_3.get()

    #만약 time1,time2,time3 값이 현재 라즈베리파이의 시간과 일치하면 커맨드값을 1로 변경함
    if nowTime==time1:
        command1 = db.reference('Feeder')
        command1.update({'command':'1'})
    
    if nowTime==time2:
        command1 = db.reference('Feeder')
        command1.update({'command':'1'})
        
    if nowTime==time3:
        command1 = db.reference('Feeder')
        command1.update({'command':'1'})

    #라즈베리파이 서버에서 커맨드값을 불러온다
    ref = db.reference('Feeder/command')
    lc=ref.get()
    #만약 불러온 커맨드값이 1일경우 서보모터를 회전시킴
    if '1'==lc:
                p.start(7.5) #서보모터 duty값 7.5로 변경

                p.ChangeDutyCycle(1) #duty값을 1로 변경(이에따라 모터가 작동함)
                print ("angle : 0") #디버깅용 출력
                time.sleep(1) #인터벌을 준다

                p.ChangeDutyCycle(9) #duty값을 9로 변경
                print ("angle : 180")
                time.sleep(1) #인터벌을 준다 // 적정시간을 입력하지 않으면 사료가 너무 많이 배급됨

                p.ChangeDutyCycle(1) #duty 값을 다시 1로 변경(사료 배급을 끝내고 원위치)
                print ("angle : 0")
                time.sleep(1)

                #모터 동작 (1회)를 마치면 무한동작을 막기 위해 서버의 커맨드값을 다시 0으로 바꾼다
                ref = db.reference('Feeder')
                ref.update({'command':'0'})

                #모터 동작을 1회 완료시 서버의 카운트값(모터 동작 횟수)를 1 늘린다
                cnt1+=1
                ref = db.reference('Feeder')
                ref.update({'count': str(cnt1)}) #서버에는 스트링으로 저장해야 하므로 다시 스트링 값으로 변경
                print(cnt1) #디버깅용 출력