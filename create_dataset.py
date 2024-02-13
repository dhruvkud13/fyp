import cv2
import os
import glob

def start_capture(name):
    path = "./data/" + name
    num_of_images = 0
    detector = cv2.CascadeClassifier("./data/haarcascade_frontalface_default.xml")
    try:
        os.makedirs(path)
    except:
        print('Directory Already Created')
    vid = cv2.VideoCapture(0)
    while True:
        ret, img = vid.read()
        new_img = None
        grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = detector.detectMultiScale(image=grayimg, scaleFactor=1.1, minNeighbors=5)
        for x, y, w, h in face:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 0), 2)
            cv2.putText(img, "Face Detected", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            cv2.putText(img, str(str(num_of_images)+" images captured"), (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            new_img = img[y:y+h, x:x+w]
        cv2.imshow("Face Detection", img)
        key = cv2.waitKey(1) & 0xFF
        try :
            cv2.imwrite(str(path+"/"+str(num_of_images)+name+".jpg"), new_img)
            num_of_images += 1
        except :
            pass
        if key == ord("q") or key == 27 or num_of_images > 300: #take 300 frames
            break
    cv2.destroyAllWindows()
    return num_of_images

def take_video(name, video):
    path = "./data/" + name
    num_of_images = 0
    detector = cv2.CascadeClassifier("./data/haarcascade_frontalface_default.xml")
    try:
        os.makedirs(path)
    except:
        print('Directory Already Created')
    vid = cv2.VideoCapture(video)
    if not vid.isOpened():
        print("Error: Could not open video file.")
        exit()
    num_of_images = 0
    while True:
        ret, img = vid.read()
        new_img = None
        grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = detector.detectMultiScale(image=grayimg, scaleFactor=1.1, minNeighbors=5)
        if not ret:
            break  # Break the loop if no more frames are available
        for x, y, w, h in face:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 0), 2)
            cv2.putText(img, "Face Detected", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            cv2.putText(img, str(str(num_of_images)+" images captured"), (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            new_img = img[y:y+h, x:x+w]
        cv2.imshow("Face Detection", img)
        key = cv2.waitKey(1) & 0xFF
        try :
            cv2.imwrite(str(path+"/"+str(num_of_images)+name+".jpg"), new_img)
            num_of_images += 1
        except :
            pass
        if key == ord("q") or key == 27 or num_of_images > 300: #take 300 frames
            break
    vid.release()
    cv2.destroyAllWindows()
    return num_of_images

def augment_captured_images(name, path):
    num_of_images = 301
    output_folder = "./data/" + name
    detector = cv2.CascadeClassifier("./data/haarcascade_frontalface_default.xml")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    scale_factors = [0.9, 1.1]  # Scaling factors
    rotations = [-10, 10]  # Rotation angles in degrees
    flips = [0, 1]  # Flip options: 0 for no flip, 1 for horizontal flip
    brightness_factors = [0.8, 1.2]  # Brightness adjustment factors
    # images = glob.glob(os.path.join(path, "*.jpg"))
    image = cv2.imread(path)
    # for image_path in images:
    #     image = cv2.imread(image_path)
    count = 0
    while count < num_of_images:
        augmented_image = image.copy()
        scale_factor = scale_factors[count % len(scale_factors)]
        augmented_image = cv2.resize(augmented_image, None, fx=scale_factor, fy=scale_factor)
        rotation_angle = rotations[count % len(rotations)]
        rotation_matrix = cv2.getRotationMatrix2D((augmented_image.shape[1] / 2, augmented_image.shape[0] / 2), rotation_angle, 1)
        augmented_image = cv2.warpAffine(augmented_image, rotation_matrix, (augmented_image.shape[1], augmented_image.shape[0]))
        flip_option = flips[count % len(flips)]
        augmented_image = cv2.flip(augmented_image, flip_option)
        brightness_factor = brightness_factors[count % len(brightness_factors)]
        augmented_image = cv2.convertScaleAbs(augmented_image, alpha=brightness_factor, beta=0)
        output_path = os.path.join(output_folder, f"{count}{name}.jpg")
        cv2.imwrite(output_path, augmented_image)
        count += 1
    print(f"{num_of_images} images generated and saved in {output_folder}")
    return num_of_images