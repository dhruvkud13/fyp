# import cv2
# from time import time
# from PIL import Image
# from tkinter import messagebox

# def main_app(name, timeout = 5):
        
#         face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
#         recognizer = cv2.face.LBPHFaceRecognizer_create()
#         print(f"name is: {name}")
#         recognizer.read(f"./data/classifiers/{name}_classifier.xml")
#         cap = cv2.VideoCapture(0)
#         pred = False
#         start_time = time()
#         while True:
#             ret, frame = cap.read()
#             #default_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             faces = face_cascade.detectMultiScale(gray,1.3,5)

#             for (x,y,w,h) in faces:


#                 roi_gray = gray[y:y+h,x:x+w]

#                 id,confidence = recognizer.predict(roi_gray)
#                 confidence = 100 - int(confidence)
#                 if confidence > 50:
#                     #if u want to print confidence level
#                             #confidence = 100 - int(confidence)
#                         pred = True
#                         text = f'Recognized: {name.upper()} - Confidence: {confidence}%'
#                         font = cv2.FONT_HERSHEY_PLAIN
#                         frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#                         frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                       
                       
#                 else:   
#                         pred = False
#                         text = f'Unknown Face - Confidence: {confidence}%'
#                         font = cv2.FONT_HERSHEY_PLAIN
#                         frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
#                         frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 0,255), 1, cv2.LINE_AA)
                       
                        
#             cv2.imshow("image", frame)

#             '''
#             if cv2.waitKey(20) & 0xFF == ord('q'):
#                 print(pred)
#                 if pred == True :
                    
#                     dim =(124,124)
#                     img = cv2.imread(f".\\data\\{name}\\{pred}{name}.jpg", cv2.IMREAD_UNCHANGED)
#                     resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
#                     cv2.imwrite(f".\\data\\{name}\\50{name}.jpg", resized)
#                     Image1 = Image.open(f".\\2.png") 
                      
#                     # make a copy the image so that the  
#                     # original image does not get affected 
#                     Image1copy = Image1.copy() 
#                     Image2 = Image.open(f".\\data\\{name}\\50{name}.jpg") 
#                     Image2copy = Image2.copy() 
                      
#                     # paste image giving dimensions 
#                     Image1copy.paste(Image2copy, (195, 114)) 
                      
#                     # save the image  
#                     Image1copy.save("end.png") 
#                     frame = cv2.imread("end.png", 1)
#                     cv2.imshow("Result",frame)
#                     cv2.waitKey(5000)
                
#                     messagebox.showinfo('Congrat', 'You have already checked in')
#                 else:
#                     messagebox.showerror('Alert', 'Please check in again')
#                 break
#         '''
#             elapsed_time = time() - start_time
#             if elapsed_time >= timeout:
#                 print(pred)
#                 if pred:
#                     messagebox.showinfo('Congrat', 'You have already checked in')
#                 else:
#                     messagebox.showerror('Alert', 'Please check in again')
#                 break

#             if cv2.waitKey(20) & 0xFF == ord('q'):
#                 break
#         cap.release()
#         cv2.destroyAllWindows()
        

import cv2
from time import time
from PIL import Image
from tkinter import messagebox
from tkinter import filedialog

def main_app(name, timeout=5, image_path=None, video_path=None):
    face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    print(f"name is: {name}")
    recognizer.read(f"./data/classifiers/{name}_classifier.xml")

    if image_path:
        # Perform recognition on the uploaded image
        image = cv2.imread(image_path)
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        print(f"Number of faces detected: {len(faces)}")
        print('before for loop')
        for (x, y, w, h) in faces:
            print('in for loop')
            roi_gray = gray[y:y + h, x:x + w]
            id, confidence = recognizer.predict(roi_gray)
            confidence = 100 - int(confidence)
            if confidence > 50:
                pred = True
                text = f'Recognized: {name.upper()} - Confidence: {confidence}%'
                print(f"text is: {text}")
                font = cv2.FONT_HERSHEY_PLAIN
                image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                image = cv2.putText(image, text, (x, y - 4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
            else:
                pred = False
                text = f'Unknown Face - Confidence: {confidence}%'
                print(f"text is: {text}")
                font = cv2.FONT_HERSHEY_PLAIN
                image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                image = cv2.putText(image, text, (x, y - 4), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
        if len(faces) == 0:
            print("No faces detected in the uploaded image")

        cv2.imshow("image", image)


    else:
        # Start the camera for live recognition
        # cap = cv2.VideoCapture(0)
        # pred = False
        # start_time = time()

        # while True:
        #     ret, frame = cap.read()
        #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #     faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        #     for (x, y, w, h) in faces:
        #         roi_gray = gray[y:y + h, x:x + w]
        #         id, confidence = recognizer.predict(roi_gray)
        #         confidence = 100 - int(confidence)
        #         if confidence > 50:
        #             pred = True
        #             text = f'Recognized: {name.upper()} - Confidence: {confidence}%'
        #             print(f"text is: {text}")
        #             font = cv2.FONT_HERSHEY_PLAIN
        #             frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #             frame = cv2.putText(frame, text, (x, y - 4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
        #         else:
        #             pred = False
        #             text = f'Unknown Face - Confidence: {confidence}%'
        #             print(f"text is: {text}")
        #             font = cv2.FONT_HERSHEY_PLAIN
        #             frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        #             frame = cv2.putText(frame, text, (x, y - 4), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

        #     cv2.imshow("image", frame)

        #     elapsed_time = time() - start_time
        #     if elapsed_time >= timeout:
        #         print(pred)
        #         if pred:
        #             messagebox.showinfo('Congrats', 'You have already checked in')
        #         else:
        #             messagebox.showerror('Alert', 'Please check in again')
        #         break

        #     if cv2.waitKey(20) & 0xFF == ord('q'):
        #         break

        # cap.release()
        # cv2.destroyAllWindows()
        if video_path:
            cap = cv2.VideoCapture(video_path)
        else:
            cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Video file or camera not opened")
            return

        pred = False
        start_time = time()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x:x + w]
                id, confidence = recognizer.predict(roi_gray)
                confidence = 100 - int(confidence)
                if confidence > 50:
                    pred = True
                    text = f'Recognized: {name.upper()} - Confidence: {confidence}%'
                    font = cv2.FONT_HERSHEY_PLAIN
                    frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    frame = cv2.putText(frame, text, (x, y - 4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                else:
                    pred = False
                    text = f'Unknown Face - Confidence: {confidence}%'
                    font = cv2.FONT_HERSHEY_PLAIN
                    frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    frame = cv2.putText(frame, text, (x, y - 4), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

            cv2.imshow("video", frame)

            elapsed_time = time() - start_time
            if elapsed_time >= timeout:
                if pred:
                    messagebox.showinfo('Congrats', 'You have already checked in')
                else:
                    messagebox.showerror('Alert', 'Please check in again')
                break

            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


# Example usage:
# To perform recognition on an uploaded image
# main_app("John", image_path="path_to_uploaded_image.jpg")

# To start live camera recognition
# main_app("John")

