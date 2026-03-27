# 🛡️ Media Encryptor Pro
Securely encrypt and decrypt your images and videos using custom cryptographic pixel manipulation.
code
Markdown
# 🛡️ Media Encryptor Pro

**Media Encryptor Pro** is a sleek, modern Python desktop application that securely encrypts and decrypts your personal images and videos using advanced cryptographic pixel manipulation. 

In an era where data privacy is paramount, this tool empowers you to take full control of your personal media. It securely scrambles the underlying pixel data, rendering your files entirely unreadable to unauthorized viewers. Your media remains safe, completely offline, and accessible only to those who possess the exact cryptographic integer key.

---

## ✨ Features

- **🖼️ Image Encryption & Decryption:** Secure your photos by shifting pixel color values using a custom key.
- **🎥 Video Encryption & Decryption:** Scramble video files frame-by-frame without losing the video format.
- **🔀 Pixel Swapping:** Add an extra layer of obfuscation to images by structurally swapping pixel columns.
- **🚀 Modern UI:** Built with `customtkinter` featuring Dark, Light, and System themes.
- **⚡ Multithreaded Processing:** Ensures the application remains fast and responsive without freezing during heavy video processing.
- **📊 Live Progress Tracking:** Real-time progress bars and status updates tell you exactly what frame or column is currently being processed.
- **🛑 Safe Cancel Operation:** Quickly abort long video processing tasks cleanly without corrupting your files.

---

## 👨‍💻 Created & Developed By

- **Prem Ghayal**
- **Om Sapkal**

---

## ⚙️ Prerequisites

Before you begin, ensure you have **Python 3.x** installed on your system. 
You will also need to install the required third-party libraries: `customtkinter`, `opencv-python`, `Pillow`, and `numpy`.

---

## 📥 How to Download and Install

Follow these steps in your terminal or command prompt to get the project up and running:

### 1. Clone the Repository
Download the project to your local machine using Git:
```bash
git clone https://github.com/shadow-fighter666/Media-Encryptor-Pro.git
```
### 2. Navigate to the Project Folder
code
```Bash
cd Media-Encryptor-Pro
```
### 3. Install the Required Libraries
Install the necessary Python dependencies using pip.
For Windows / Mac:
code
```Bash
pip install customtkinter opencv-python pillow numpy
```
For Linux (Kali / Ubuntu / Debian):
(Note: Modern Linux environments use PEP 668. It is recommended to use a virtual environment or the break-system-packages flag).
code
# Option A: Using the flag directly
```bash
pip3 install customtkinter opencv-python pillow numpy --break-system-packages
```
# Option B: Using a Virtual Environment (Recommended)
```bash
python3 -m venv myenv
source myenv/bin/activate
pip install customtkinter opencv-python pillow numpy
```
### ▶️ How to Run the Application
Once everything is installed, simply run the Python script to launch the GUI:
code
```bash
python MediaEncryptorPro.py
```
(Use python3 MediaEncryptorPro.py if you are on Linux or macOS).
💡 How to Use
Select a File: Click the Browse button to select an Image (.jpg, .png, etc.) or Video (.mp4, .avi, etc.).
Choose Operation: Use the dropdown menu to select whether you want to Encrypt, Decrypt, or Swap Pixels.
Enter Key: Type in an integer (number) key. (Remember this key! You will need the exact same number to decrypt the file later).
Process: Click Start Processing. The new secured file will be saved in the exact same folder as your original file with encrypted_ or decrypted_ added to the filename!
📝 License
This project is open-source and available for educational and personal privacy purposes.
