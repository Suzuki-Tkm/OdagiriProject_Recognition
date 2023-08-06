import cv2

try:
    camera = cv2.VideoCapture(0)
    QRCD = cv2.QRCodeDetector()
            
    while True:

        ret, img = camera.read()
        cv2.imshow('Camera',img)
        data,points,b_img = QRCD.detectAndDecode(img)
        key = cv2.waitKey(10)
        if key == 27:
            break
        if data !='':
            print(data)
            break
    cv2.destroyAllWindows()
    camera.release()

except FileNotFoundError as e:
    print(e)