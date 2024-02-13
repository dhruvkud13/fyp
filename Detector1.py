import cv2
import numpy as np
from time import time
from tkinter import messagebox
import os
from sklearn.decomposition import PCA

def main_app(name, timeout=5, image_path=None):
    def compute_eigenfaces(data_dir, num_components=100):
        # Step 1: Collect a dataset of face images
        images = []
        for filename in os.listdir(data_dir):
            img = cv2.imread(os.path.join(data_dir, filename), cv2.IMREAD_GRAYSCALE)
            images.append(img.flatten())

        # Step 2: Build a data matrix
        data_matrix = np.array(images)

        # Step 3: Compute the mean face
        mean_face = np.mean(data_matrix, axis=0)

        # Step 4: Subtract the mean face
        centered_data = data_matrix - mean_face

        # Step 5: Perform PCA
        pca = PCA(n_components=num_components)
        pca.fit(centered_data)

        # Step 6: Select top eigenfaces
        eigenfaces = pca.components_

        # Step 7: Save eigenfaces
        np.save('./data/eigenfaces.npy', eigenfaces)

        return eigenfaces

    def compute_known_weights(data_dir, eigenfaces):
        known_weights = {}

        for filename in os.listdir(data_dir):
            # Load face image
            img = cv2.imread(os.path.join(data_dir, filename), cv2.IMREAD_GRAYSCALE)

            # Flatten the image and subtract the mean face
            flattened_img = img.flatten() - eigenfaces.mean(axis=0)

            # Project the image onto eigenfaces to obtain weights
            weights = np.dot(flattened_img, eigenfaces.T)

            # Extract the person's name or ID from the filename (assuming filename contains label)
            name = filename.split('.')[0]

            # Save the weights for this person
            known_weights[name] = weights

        # Save known weights to file
        np.save('./data/known_weights.npy', known_weights)

    def recognize_faces(eigenfaces, name, timeout=5, image_path=None):
        if image_path:
            # Perform recognition on the uploaded image
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            image = cv2.resize(image, (100, 100))  # Resize image to match eigenfaces size

            # Flatten the image into a 1D array
            flattened_image = image.flatten()

            # Subtract mean face
            flattened_image -= eigenfaces.mean(axis=0)

            # Project the image onto eigenfaces
            weights = np.dot(flattened_image, eigenfaces.T)

            # Load known weights for comparison
            known_weights = np.load('./data/known_weights.npy', allow_pickle=True).item()

            # Compare with known weights
            min_distance = float('inf')
            recognized_name = None
            for known_name, known_weight in known_weights.items():
                distance = np.linalg.norm(weights - known_weight)
                if distance < min_distance:
                    min_distance = distance
                    recognized_name = known_name

            if min_distance < threshold:  # Adjust threshold as needed
                messagebox.showinfo('Recognition', f'Welcome back, {recognized_name}!')
            else:
                messagebox.showerror('Recognition', 'Unauthorized access!')

            # Display the image with recognized faces (if any)
            cv2.imshow("image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        else:
            # Start the camera for live recognition
            cap = cv2.VideoCapture(0)
            start_time = time()

            while True:
                ret, frame = cap.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.resize(gray, (100, 100))  # Resize frame to match eigenfaces size

                # Flatten the frame into a 1D array
                flattened_frame = gray.flatten()

                # Subtract mean face
                flattened_frame -= eigenfaces.mean(axis=0)

                # Project the frame onto eigenfaces
                weights = np.dot(flattened_frame, eigenfaces.T)

                # Load known weights for comparison
                known_weights = np.load('./data/known_weights.npy', allow_pickle=True).item()

                # Compare with known weights
                min_distance = float('inf')
                recognized_name = None
                for known_name, known_weight in known_weights.items():
                    distance = np.linalg.norm(weights - known_weight)
                    if distance < min_distance:
                        min_distance = distance
                        recognized_name = known_name

                if min_distance < threshold:  # Adjust threshold as needed
                    messagebox.showinfo('Recognition', f'Welcome back, {recognized_name}!')
                else:
                    messagebox.showerror('Recognition', 'Unauthorized access!')

                # Display the frame with recognized faces (if any)
                cv2.imshow("frame", gray)

                elapsed_time = time() - start_time
                if elapsed_time >= timeout:
                    messagebox.showerror('Alert', 'Timeout reached. Please try again.')
                    break

                if cv2.waitKey(20) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

    # Parameters
    threshold = 100  # Adjust as needed

    # Step 1: Compute eigenfaces
    eigenfaces = compute_eigenfaces('./data/faces')

    # Step 2: Compute and save known weights
    compute_known_weights('./data/faces', eigenfaces)

    # Step 3: Recognize faces using eigenfaces
    recognize_faces(eigenfaces, name, timeout, image_path)

# Example usage:
# To perform recognition on an uploaded image
# main_app("John", image_path="path_to_uploaded_image.jpg")

# To start live camera recognition
# main_app("John")
