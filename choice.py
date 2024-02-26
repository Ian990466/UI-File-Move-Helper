import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import json

class ImageOrganizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Organizer")

        # 初始設定視窗
        self.setup_frame = tk.Frame(root)
        self.setup_frame.pack()

        tk.Label(self.setup_frame, text="請選擇圖片所在路徑：").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Label(self.setup_frame, text="請選擇目標文件夾所在路徑：").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Label(self.setup_frame, text="請輸入目標文件夾名稱（空格分隔）：").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Label(self.setup_frame, text="預覽圖片高度：").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)

        self.image_path_entry = tk.Entry(self.setup_frame)
        self.image_path_entry.grid(row=0, column=1, padx=5, pady=5)
        self.target_path_entry = tk.Entry(self.setup_frame)
        self.target_path_entry.grid(row=1, column=1, padx=5, pady=5)
        self.target_folders_entry = tk.Entry(self.setup_frame)
        self.target_folders_entry.grid(row=2, column=1, padx=5, pady=5)
        self.preview_height_entry = tk.Entry(self.setup_frame)
        self.preview_height_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(self.setup_frame, text="選擇圖片路徑", command=self.browse_image_path).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(self.setup_frame, text="選擇目標文件夾路徑", command=self.browse_target_path).grid(row=1, column=2, padx=5, pady=5)

        tk.Button(self.setup_frame, text="開始", command=self.start).grid(row=4, column=0, columnspan=3, pady=10)

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
        self.preview_height = preview_height  # 將 preview_height 存為 self 的屬性

        self.current_image_index = 0

        self.work_frame = tk.Frame(self.root)
        self.work_frame.pack()

        # 預覽圖片
        self.show_image()

        # 在工作視窗底部排列資料夾名稱的Button
        button_row = tk.Frame(self.work_frame)
        button_row.grid(row=1, column=0, sticky='w')

        for i, folder in enumerate(target_folders):
            button = tk.Button(button_row, text=folder, command=lambda f=folder: self.move_to_folder(f), width=15, anchor='w')
            button.grid(row=0, column=i, padx=5, pady=5, sticky='w')


    def show_image(self):
        if self.current_image_index < len(self.image_list):
            # 刪除先前的 Label
            if hasattr(self, 'image_label'):
                self.image_label.destroy()

            image_path = self.image_list[self.current_image_index]
            img = Image.open(image_path)
            img.thumbnail((self.preview_height, self.preview_height))
            img = ImageTk.PhotoImage(img)

            self.image_label = tk.Label(self.work_frame, image=img)
            self.image_label.image = img
            self.image_label.grid(row=0, column=0, padx=10, pady=10)  # 使用 grid 佈局
    
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

            # 檢查是否處理完所有圖片，是的話關閉程式
            if self.current_image_index == len(self.image_list):
                self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageOrganizer(root)
    root.mainloop()
