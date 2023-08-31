import tkinter as tk
from tkinter import filedialog, Scale
from PIL import Image, ImageTk, ImageEnhance

class ImageProcessor:
    def __init__(self):

        self.original_img = None
        self.img = None


    def load_image(self, path):
            self.original_img = Image.open(path)
            
            # Scale image if necessary
            max_size = (1000, 1000)
            if self.original_img.size[0] > max_size[0] or self.original_img.size[1] > max_size[1]:
                self.original_img.thumbnail(max_size, Image.Resampling.LANCZOS)

            self.img = self.original_img.copy()

    def to_grayscale(self):
        self.img = self.original_img.convert('L')

    def adjust_brightness(self, factor):
        enhancer = ImageEnhance.Brightness(self.original_img)
        self.img = enhancer.enhance(factor)

    def adjust_contrast(self, factor):
        enhancer = ImageEnhance.Contrast(self.original_img)
        self.img = enhancer.enhance(factor)

    def save(self, path):
        if self.img:
            self.img.save(path)


class ImageManipulator:
    def __init__(self, root, processor):
        self.root = root
        self.processor = processor

        # Load image button
        self.load_btn = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_btn.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")])
        if file_path:
            self.processor.load_image(file_path)
            self.display_image_controls()


    def display_image_controls(self):
        # Remove the Load Image button to make space for image and controls
        self.load_btn.pack_forget()

        # Display image
        self.image_tk = ImageTk.PhotoImage(self.processor.img)
        self.image_label = tk.Label(self.root)
        self.image_label.pack()
        self.update_image()


        # Grayscale button
        self.grayscale_btn = tk.Button(self.root, text="Convert to Grayscale", command=self.to_grayscale)
        self.grayscale_btn.pack()

        # Brightness control
        self.brightness_scale = Scale(self.root, from_=0.5, to_=2.0, resolution=0.1, orient=tk.HORIZONTAL, label="Brightness")
        self.brightness_scale.set(1.0)
        self.brightness_scale.bind("<ButtonRelease-1>", self.adjust_brightness)
        self.brightness_scale.pack()

        # Contrast control
        self.contrast_scale = Scale(self.root, from_=0.5, to_=2.0, resolution=0.1, orient=tk.HORIZONTAL, label="Contrast")
        self.contrast_scale.set(1.0)
        self.contrast_scale.bind("<ButtonRelease-1>", self.adjust_contrast)
        self.contrast_scale.pack()

        # Save button
        self.save_btn = tk.Button(self.root, text="Save Image", command=self.save_image)
        self.save_btn.pack()

    def update_image(self):
        self.image_tk = ImageTk.PhotoImage(self.processor.img)
        self.image_label['image'] = self.image_tk
        # keep a reference to the image object to prevent garbage collection
        self.image_label.image = self.image_tk

    def to_grayscale(self):
        self.processor.to_grayscale()
        self.update_image()

    def adjust_brightness(self, event):
        factor = self.brightness_scale.get()
        self.processor.adjust_brightness(factor)
        self.update_image()

    def adjust_contrast(self, event):
        factor = self.contrast_scale.get()
        self.processor.adjust_contrast(factor)
        self.update_image()

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"),
                                                                                    ("JPEG files", "*.jpg"),
                                                                                    ("All files", "*.*")])
        if file_path:
            self.processor.save(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Image Manipulator")

    processor = ImageProcessor()
    app = ImageManipulator(root, processor)

    root.mainloop()
