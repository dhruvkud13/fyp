import cv2
import os
import tkinter as tk
from tkinter import filedialog

def upload_image():
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select Image File", filetypes=(("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"), ("All files", "*.*")))
    input_image_path.set(root.filename)

def augment_image():
    input_path = input_image_path.get()
    if input_path == "":
        print("Please select an image first.")
        return

    output_folder = "augmented_images"
    num_images = 300

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_prefix = output_prefix_entry.get()  # Get the output prefix from the entry widget

    # Load the input image
    image = cv2.imread(input_path)

    # Define augmentation parameters
    # You can adjust these parameters based on your requirements
    scale_factors = [0.9, 1.1]  # Scaling factors
    rotations = [-10, 10]  # Rotation angles in degrees
    flips = [0, 1]  # Flip options: 0 for no flip, 1 for horizontal flip
    brightness_factors = [0.8, 1.2]  # Brightness adjustment factors

    count = 0
    while count < num_images:
        augmented_image = image.copy()

        # Apply random scaling
        scale_factor = scale_factors[count % len(scale_factors)]
        augmented_image = cv2.resize(augmented_image, None, fx=scale_factor, fy=scale_factor)

        # Apply random rotation
        rotation_angle = rotations[count % len(rotations)]
        rotation_matrix = cv2.getRotationMatrix2D((augmented_image.shape[1] / 2, augmented_image.shape[0] / 2), rotation_angle, 1)
        augmented_image = cv2.warpAffine(augmented_image, rotation_matrix, (augmented_image.shape[1], augmented_image.shape[0]))

        # Apply random flip
        flip_option = flips[count % len(flips)]
        augmented_image = cv2.flip(augmented_image, flip_option)

        # Apply random brightness adjustment
        brightness_factor = brightness_factors[count % len(brightness_factors)]
        augmented_image = cv2.convertScaleAbs(augmented_image, alpha=brightness_factor, beta=0)

        # Save the augmented image
        output_path = os.path.join(output_folder, f"{count}{output_prefix}.jpg")
        cv2.imwrite(output_path, augmented_image)

        count += 1

    print(f"{num_images} images generated and saved in {output_folder}")

# Create the GUI
root = tk.Tk()
root.title("Image Augmentation")
root.geometry("400x200")

input_image_path = tk.StringVar()

input_label = tk.Label(root, text="Upload Image:")
input_label.pack()

upload_button = tk.Button(root, text="Upload", command=upload_image)
upload_button.pack()

input_entry = tk.Entry(root, textvariable=input_image_path, state='readonly')
input_entry.pack()

output_prefix_label = tk.Label(root, text="Output Prefix:")
output_prefix_label.pack()

output_prefix_entry = tk.Entry(root)
output_prefix_entry.pack()

augment_button = tk.Button(root, text="Augment Image", command=augment_image)
augment_button.pack()

root.mainloop()
