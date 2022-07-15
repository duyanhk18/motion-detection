import cv2 as cv
import time
from pygame import mixer

mixer.init()
sound=mixer.Sound("Alert.wav")

delay = 2

# ip = input('IP address: ')
# port = input('Port: ')
# user = input('User: ')
# password = input('Password: ')
# channel = input('Camera: ')

ip = ''
port = ''
user = ''
password = ''
channel = ''

if len(ip) < 5:
    ip = '192.168.9.100'

if port == '':
    port = '554'

if user == '':
    user = 'admin'

if password == '':
    password = 'admin'

if channel == '':
    channel = '1'

# cap = cv.VideoCapture('rtsp://admin:admin@192.168.9.100:554/cam/realmonitor?channel=1&subtype=1')

cap = cv.VideoCapture('rtsp://'+user+':'+password+'@'+ip+':'+port+'/cam/realmonitor?channel='+channel+'&subtype=1')

ret, frame1 = cap.read()
print("Image Dimension before crop: ", frame1.shape)
height = frame1.shape[0]
width  = frame1.shape[1]

# h1 = int(height/2.5)
# h2 = int(height)
# w1 = int(width/3)
# w2 = int(width/2)

h1 = int(height*0.42)
h2 = int(height)
w1 = int(width*0.33)
w2 = int(width*0.5)

frame1 = frame1[h1:h2,w1:w2]
print("Image Dimension after crop: ", frame1.shape)
frame2 = frame1
last = time.time()
while cap.isOpened():


    diff = cv.absdiff(frame1, frame2)
    diff_gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(diff_gray, (5, 5), 0)
    _, thresh = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)
    dilated = cv.dilate(thresh, None, iterations=3)
    contours, _ = cv.findContours(
        dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv.boundingRect(contour)
        if cv.contourArea(contour) < int(frame1.shape[0]*frame1.shape[1]*0.02):
            continue
        cv.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 1)
        if round(time.time() - last) >= delay:
            sound.play()
            print('Motion detected')
            last = time.time()

    # cv.drawContours(frame1, contours, -1, (0, 255, 0), 2)

    # cv.imshow("Video", frame1)

    frame1 = frame2

    ret, frame2 = cap.read()
    frame2 = frame2[h1:h2,w1:w2]

    if cv.waitKey(1)&0xff == ord('q'):
        break

cap.release()
cv.destroyAllWindows()