import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import json

class ImageOrganizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Organizer")

        # Initial setup window
        self.setup_frame = tk.Frame(root)
        self.setup_frame.pack()

        tk.Label(self.setup_frame, text="Select the path of the images:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Label(self.setup_frame, text="Select the path of the target folder:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Label(self.setup_frame, text="Enter the names of target folders (separated by spaces):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Label(self.setup_frame, text="Preview image height:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)

        self.image_path_entry = tk.Entry(self.setup_frame)
        self.image_path_entry.grid(row=0, column=1, padx=5, pady=5)
        self.target_path_entry = tk.Entry(self.setup_frame)
        self.target_path_entry.grid(row=1, column=1, padx=5, pady=5)
        self.target_folders_entry = tk.Entry(self.setup_frame)
        self.target_folders_entry.grid(row=2, column=1, padx=5, pady=5)
        self.preview_height_entry = tk.Entry(self.setup_frame)
        self.preview_height_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(self.setup_frame, text="Choose image path", command=self.browse_image_path).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(self.setup_frame, text="Choose target folder path", command=self.browse_target_path).grid(row=1, column=2, padx=5, pady=5)

        tk.Button(self.setup_frame, text="Start", command=self.start).grid(row=4, column=0, columnspan=3, pady=10)

    def browse_image_path(self):
        path = filedialog.askdirectory()
        self.image_path_entry.delete(0, tk.END)
        self.image_path_entry.insert(0, path)

    def browse_target_path(self):
        path = filedialog.askdirectory()
        self.target_path_entry.delete(0, tk.END)
        self.target_path_entry.insert(0, path)

    def start(self):
        image_path = self.image_path_entry.get()
        target_path = self.target_path_entry.get()
        target_folders = self.target_folders_entry.get().split()
        preview_height = int(self.preview_height_entry.get())

        self.setup_frame.destroy()

        self.image_list = [os.path.join(image_path, file) for file in os.listdir(image_path)
                        if file.lower().endswith(('.png', '.jpg', '.bmp'))]
        self.target_path = target_path
        self.preview_height = preview_height  # Store preview_height as a class attribute

        self.current_image_index = 0

        self.work_frame = tk.Frame(self.root)
        self.work_frame.pack()

        # Display preview image
        self.show_image()

        # Arrange folder names' buttons at the bottom of the working window
        button_row = tk.Frame(self.work_frame)
        button_row.grid(row=1, column=0, sticky='w')

        for i, folder in enumerate(target_folders):
            button = tk.Button(button_row, text=folder, command=lambda f=folder: self.move_to_folder(f), width=15, anchor='w')
            button.grid(row=0, column=i, padx=5, pady=5, sticky='w')


    def show_image(self):
        if self.current_image_index < len(self.image_list):
            # Delete the previous Label if it exists
            if hasattr(self, 'image_label'):
                self.image_label.destroy()

            image_path = self.image_list[self.current_image_index]
            img = Image.open(image_path)
            img.thumbnail((self.preview_height, self.preview_height))
            img = ImageTk.PhotoImage(img)

            self.image_label = tk.Label(self.work_frame, image=img)
            self.image_label.image = img
            self.image_label.grid(row=0, column=0, padx=10, pady=10)  # Use grid layout
    
    def move_to_folder(self, folder):
        if self.current_image_index < len(self.image_list):
            image_path = self.image_list[self.current_image_index]
            target_folder_path = os.path.join(self.target_path, folder)
            os.makedirs(target_folder_path, exist_ok=True)
            new_image_path = os.path.join(target_folder_path, os.path.basename(image_path))
            os.rename(image_path, new_image_path)
            self.current_image_index += 1
            self.image_label.destroy()
            self.show_image()

            # Check if all images have been processed, if yes, close the program
            if self.current_image_index == len(self.image_list):
                self.generate_json()  # Call the function to generate JSON
                self.root.destroy()

    def generate_json(self):
        # Create a dictionary to store information
        data = {}
        for folder in os.listdir(self.target_path):
            folder_path = os.path.join(self.target_path, folder)
            if os.path.isdir(folder_path):
                files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
                data[folder] = {'num_files': len(files), 'files': files}

        # Write the dictionary to a JSON file
        with open('output.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageOrganizer(root)
    root.mainloop()
