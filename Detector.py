import cv2
import cv2
import pyodbc

server = 'rgg165.database.windows.net'
database = 'RGG'
authentication = 'ActiveDirectoryPassword'
username = 'CloudSA4a9cebf1'
password = '{Psadhjuh8}'
driver = '{ODBC Driver 17 for SQL Server}'

connection_string = 'DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password

def main_app(name):
        
        face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        #solo tengo que cambiar el nombre aquí!!!
        recognizer.read(f"./data/classifiers/{name}_classifier.xml")
        text = name.upper()
        loanGranted = grantLoan(text)
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            #default_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray,1.3,5)

            for (x,y,w,h) in faces:


                roi_gray = gray[y:y+h,x:x+w]

                id,confidence = recognizer.predict(roi_gray)
                confidence = 100 - int(confidence)

                print(text + ' ' + str(confidence) + ' ' + str(loanGranted))
                #confidence = 100 - int(confidence)

                if confidence > 40:
                    if loanGranted:
                    #TODO: if u have the money
                        text = name.upper()
                        font = cv2.FONT_HERSHEY_PLAIN
                        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                    else:
                        #TODO: if u don't have the money
                        text = name.upper()
                        font = cv2.FONT_HERSHEY_PLAIN
                        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 0,255), 1, cv2.LINE_AA)
                else:
                    text = "UnknownFace"
                    font = cv2.FONT_HERSHEY_PLAIN
                    frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 0,255), 1, cv2.LINE_AA)


            cv2.imshow("image", frame)


            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

#TODO: grant loan if money > 20% total price of cars 
def grantLoan(name):
    with pyodbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Bank")
            rows = cursor.fetchall()
            for row in rows:
                print('---------------')
                print (str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
                if str(row[1]) == name and float(str(row[2])) > 500000:
                    return True
            return False