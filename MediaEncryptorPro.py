import customtkinter as ctk
import tkinter.messagebox as messagebox
from tkinter import filedialog
import threading
import os
from PIL import Image
import cv2
import numpy as np

# Configure the global appearance
ctk.set_appearance_mode("Dark")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

class ModernCryptoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Media Encryptor Pro")
        self.geometry("650x550")
        self.resizable(False, False)

        # State variable for canceling processes
        self.cancel_flag = False

        # Build UI
        self.create_widgets()

    def create_widgets(self):
        # Header Label
        self.header_label = ctk.CTkLabel(self, text="Media Encryptor Pro", font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.pack(pady=(20, 10))

        # Tabview for organizing sections
        self.tabview = ctk.CTkTabview(self, width=600, height=400)
        self.tabview.pack(padx=20, pady=10, fill="both", expand=True)

        self.tab_main = self.tabview.add("Main")
        self.tab_settings = self.tabview.add("Settings")
        self.tab_about = self.tabview.add("About")

        self.setup_main_tab()
        self.setup_settings_tab()
        self.setup_about_tab()

    def setup_main_tab(self):
        # -- File Selection --
        file_frame = ctk.CTkFrame(self.tab_main, fg_color="transparent")
        file_frame.pack(pady=15, fill="x", padx=20)

        ctk.CTkLabel(file_frame, text="Select Media File:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        
        browse_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
        browse_frame.pack(fill="x", pady=5)
        
        self.filepath_var = ctk.StringVar()
        self.file_entry = ctk.CTkEntry(browse_frame, textvariable=self.filepath_var, state="readonly", width=380)
        self.file_entry.pack(side="left", padx=(0, 10))
        
        self.browse_btn = ctk.CTkButton(browse_frame, text="Browse", width=100, command=self.browse_file)
        self.browse_btn.pack(side="left")

        # -- Operation Selection --
        op_frame = ctk.CTkFrame(self.tab_main, fg_color="transparent")
        op_frame.pack(pady=10, fill="x", padx=20)
        
        ctk.CTkLabel(op_frame, text="Select Operation:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        
        self.operation_var = ctk.StringVar(value="Encrypt Image")
        operations =[
            "Encrypt Image", 
            "Decrypt Image", 
            "Swap Image Pixels", 
            "Encrypt Video", 
            "Decrypt Video"
        ]
        self.op_dropdown = ctk.CTkComboBox(op_frame, values=operations, variable=self.operation_var, width=250, command=self.toggle_key_entry)
        self.op_dropdown.pack(anchor="w", pady=5)

        # -- Key Input --
        key_frame = ctk.CTkFrame(self.tab_main, fg_color="transparent")
        key_frame.pack(pady=10, fill="x", padx=20)

        ctk.CTkLabel(key_frame, text="Encryption/Decryption Key (Integer):", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        
        self.key_var = ctk.StringVar()
        self.key_entry = ctk.CTkEntry(key_frame, textvariable=self.key_var, width=150)
        self.key_entry.pack(anchor="w", pady=5)

        # -- Action Buttons --
        action_frame = ctk.CTkFrame(self.tab_main, fg_color="transparent")
        action_frame.pack(pady=20)

        self.process_btn = ctk.CTkButton(action_frame, text="Start Processing", fg_color="#28a745", hover_color="#218838", font=ctk.CTkFont(weight="bold"), command=self.start_processing)
        self.process_btn.pack(side="left", padx=10)

        self.cancel_btn = ctk.CTkButton(action_frame, text="Cancel", fg_color="#dc3545", hover_color="#c82333", state="disabled", command=self.cancel_processing)
        self.cancel_btn.pack(side="left", padx=10)

        # -- Progress Bar & Status --
        self.progress_bar = ctk.CTkProgressBar(self.tab_main, width=450)
        self.progress_bar.pack(pady=(10, 5))
        self.progress_bar.set(0.0)

        self.status_var = ctk.StringVar(value="Ready")
        self.status_label = ctk.CTkLabel(self.tab_main, textvariable=self.status_var, text_color="gray")
        self.status_label.pack()

    def setup_settings_tab(self):
        ctk.CTkLabel(self.tab_settings, text="Application Settings", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)

        # Theme Toggle
        theme_frame = ctk.CTkFrame(self.tab_settings)
        theme_frame.pack(pady=10, padx=50, fill="x")

        ctk.CTkLabel(theme_frame, text="Appearance Mode:").pack(side="left", padx=20, pady=20)
        
        self.theme_selector = ctk.CTkOptionMenu(theme_frame, values=["Dark", "Light", "System"], command=self.change_theme)
        self.theme_selector.pack(side="right", padx=20, pady=20)
        self.theme_selector.set("Dark")

    def setup_about_tab(self):
        # About content
        ctk.CTkLabel(self.tab_about, text="Media Encryptor Pro", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(30, 5))
        
        ctk.CTkLabel(self.tab_about, text="Version 2.0", font=ctk.CTkFont(size=12), text_color="gray").pack(pady=(0, 20))

        ctk.CTkLabel(self.tab_about, text="Securely encrypt and decrypt your images and videos\nusing custom cryptographic pixel manipulation.", justify="center").pack(pady=10)

        # Creators Section
        creators_frame = ctk.CTkFrame(self.tab_about, corner_radius=10)
        creators_frame.pack(pady=20, padx=50, fill="x")

        ctk.CTkLabel(creators_frame, text="Created & Developed By:", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 5))
        ctk.CTkLabel(creators_frame, text="👨‍💻 Prem Ghayal", font=ctk.CTkFont(size=14)).pack(pady=2)

    # --- UI Interactions ---

    def change_theme(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def browse_file(self):
        operation = self.operation_var.get()
        
        # ERROR FIXED HERE: Changed ';' to spaces for Linux compatability and added "All Files" fallback
        if "Image" in operation:
            filetypes =[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp"),
                ("All Files", "*.*")
            ]
        else:
            filetypes =[
                ("Video Files", "*.mp4 *.avi *.mov *.mkv"),
                ("All Files", "*.*")
            ]

        filename = filedialog.askopenfilename(title="Select Media File", filetypes=filetypes)
        if filename:
            self.filepath_var.set(filename)

    def toggle_key_entry(self, choice):
        # Disable key input if swapping pixels
        if choice == "Swap Image Pixels":
            self.key_entry.configure(state="disabled")
            self.key_var.set("")
        else:
            self.key_entry.configure(state="normal")
        
        # Clear filepath to prevent using wrong file types
        self.filepath_var.set("")

    def update_status(self, msg, progress=None):
        self.status_var.set(msg)
        if progress is not None:
            self.progress_bar.set(progress)

    def cancel_processing(self):
        self.cancel_flag = True
        self.update_status("Canceling... please wait.")

    def reset_gui(self):
        self.process_btn.configure(state="normal", text="Start Processing")
        self.cancel_btn.configure(state="disabled")
        self.browse_btn.configure(state="normal")
        self.cancel_flag = False

    def start_processing(self):
        filepath = self.filepath_var.get()
        operation = self.operation_var.get()
        
        if not filepath:
            messagebox.showerror("Error", "Please select a file first.")
            return

        key = 0
        if operation != "Swap Image Pixels":
            try:
                key = int(self.key_var.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid integer for the key.")
                return

        # Lock UI
        self.process_btn.configure(state="disabled", text="Processing...")
        self.cancel_btn.configure(state="normal")
        self.browse_btn.configure(state="disabled")
        self.progress_bar.set(0)
        self.cancel_flag = False

        # Run in thread
        thread = threading.Thread(target=self.run_operation, args=(filepath, operation, key))
        thread.daemon = True
        thread.start()

    # --- Core Processing Logic ---

    def run_operation(self, filepath, operation, key):
        dirname = os.path.dirname(filepath)
        basename = os.path.basename(filepath)
        name_without_ext = os.path.splitext(basename)[0]

        out = ""
        try:
            if operation == "Encrypt Image":
                out = os.path.join(dirname, "encrypted_" + basename)
                self.process_image(filepath, out, key, mode="encrypt")
                
            elif operation == "Decrypt Image":
                out = os.path.join(dirname, "decrypted_" + basename)
                self.process_image(filepath, out, key, mode="decrypt")
                
            elif operation == "Swap Image Pixels":
                out = os.path.join(dirname, "swapped_" + basename)
                self.swap_pixels(filepath, out)
                
            elif operation == "Encrypt Video":
                out = os.path.join(dirname, "encrypted_" + name_without_ext + ".avi")
                self.process_video(filepath, out, key, mode="encrypt")
                
            elif operation == "Decrypt Video":
                out = os.path.join(dirname, "decrypted_" + name_without_ext + ".avi")
                self.process_video(filepath, out, key, mode="decrypt")

            if self.cancel_flag:
                self.after(0, lambda: self.update_status("Operation Canceled.", 0))
                self.after(0, lambda: messagebox.showwarning("Canceled", "The operation was canceled by the user."))
            else:
                self.after(0, lambda: self.update_status("Complete!", 1.0))
                self.after(0, lambda: messagebox.showinfo("Success", f"Operation successful!\nSaved to:\n{out}"))

        except Exception as e:
            self.after(0, lambda: self.update_status("Error occurred.", 0))
            self.after(0, lambda: messagebox.showerror("Error", str(e)))

        finally:
            self.after(0, self.reset_gui)

    def process_image(self, image_path, output_path, key, mode="encrypt"):
        img = Image.open(image_path).convert("RGB")
        pixels = img.load()
        width, height = img.size

        for i in range(width):
            if self.cancel_flag: break
            
            # Update Progress Bar
            if i % 10 == 0: 
                self.after(0, self.update_status, f"{mode.capitalize()}ing Image... ({i}/{width} cols)", i / width)

            for j in range(height):
                r, g, b = pixels[i, j]
                if mode == "encrypt":
                    pixels[i, j] = ((r + key) % 256, (g + key) % 256, (b + key) % 256)
                else:
                    pixels[i, j] = ((r - key) % 256, (g - key) % 256, (b - key) % 256)
                key += 1

        if not self.cancel_flag:
            img.save(output_path)

    def swap_pixels(self, image_path, output_path):
        img = Image.open(image_path).convert("RGB")
        pixels = img.load()
        width, height = img.size

        for i in range(0, width - 1, 2):
            if self.cancel_flag: break
            
            if i % 10 == 0:
                self.after(0, self.update_status, f"Swapping Pixels... ({i}/{width} cols)", i / width)

            for j in range(height):
                pixels[i, j], pixels[i + 1, j] = pixels[i + 1, j], pixels[i, j]

        if not self.cancel_flag:
            img.save(output_path)

    def process_video(self, input_video, output_video, key, mode="encrypt"):
        cap = cv2.VideoCapture(input_video)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Failsafe if video file is missing fps metadata
        if fps == 0 or fps != fps: 
            fps = 30.0

        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

        frame_count = 0
        while True:
            if self.cancel_flag: break

            ret, frame = cap.read()
            if not ret: break
                
            frame_count += 1
            progress = frame_count / total_frames if total_frames > 0 else 0
            
            # Update UI safely
            self.after(0, self.update_status, f"{mode.capitalize()}ing Video... Frame {frame_count}/{total_frames}", progress)

            frame = frame.astype(np.int16)
            temp_key = key

            # Pixel by pixel math
            for i in range(frame.shape[0]):
                for j in range(frame.shape[1]):
                    b, g, r = frame[i, j]
                    
                    if mode == "encrypt":
                        frame[i, j] = ((b + temp_key) % 256, (g + temp_key) % 256, (r + temp_key) % 256)
                    else:
                        frame[i, j] = ((b - temp_key) % 256, (g - temp_key) % 256, (r - temp_key) % 256)
                        
                    temp_key = (temp_key + 1) % 256

            processed_frame = frame.astype(np.uint8)
            out.write(processed_frame)

        cap.release()
        out.release()
        
        # Delete corrupted/half-finished file if canceled
        if self.cancel_flag and os.path.exists(output_video):
            os.remove(output_video)

if __name__ == "__main__":
    app = ModernCryptoApp()
    app.mainloop()
