import numpy as np
import cv2
import os
cap = cv2.VideoCapture(0)
classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

name = input("Enter your name: ")
count = int(input("Enter number of pics: "))
images = []

while True:
    ret,image = cap.read()
    if ret:
        faces = classifier.detectMultiScale(image)
        cv2.imshow("My First Camera", image)

        if len(faces) > 0:
            sorted_faces = sorted(faces,key=lambda item:item[2]*item[3])
            x,y,w,h = sorted_faces[-1]
            cut = image[y:y+h,x:x+w]

            resized = cv2.resize(cut,(100,100))

            cv2.imshow("Chopped", resized)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    elif key == ord("c"):
        images.append(resized.mean(axis=2).flatten())
        count -= 1
        print(count)

        if count == 0:
            break

cap.release()
cv2.destroyAllWindows()

X = np.array(images)
y = np.full((X.shape[0],1),name)

data = np.hstack([y,X])

if os.path.exists("faces.npy"):
    old = np.load("faces.npy")
    data = np.vstack([old,data])


np.save("faces.npy",data)