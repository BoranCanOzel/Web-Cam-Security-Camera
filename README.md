
# 📸 WebCamSecurityCamera

A project for capturing video frames from a webcam and uploading them to a server. The web application displays the recorded videos.

## Project Structure

```
WebCamSecurityCamera/
├── client/
│   ├── client.py
├── server/
│   ├── upload.php
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   └── recordings/  # Make sure this directory exists
```

## 🛠️ Setup and Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)
- OpenCV
- requests
- aiohttp (for asynchronous requests)
- FFmpeg

### 🛠️ FFmpeg Setup

If you want to use FFmpeg for any video processing tasks, follow these steps to install it:

1. **Download FFmpeg**:
   - Go to the [FFmpeg download page](https://ffmpeg.org/download.html).
   - Download the appropriate version for your operating system.

2. **Install FFmpeg**:
   - Follow the installation instructions for your operating system.

   **Windows**:
   - Extract the downloaded zip file.
   - Add the `bin` folder to your system PATH.

   **macOS**:
   ```bash
   brew install ffmpeg
   ```

   **Linux**:
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

3. **Verify Installation**:
   - Open a terminal or command prompt and run:
   ```bash
   ffmpeg -version
   ```
   - You should see the FFmpeg version information if the installation was successful.

### 📦 Client Setup

1. Navigate to the `client` directory:
    ```bash
    cd client
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the `client.py` script to start capturing and uploading frames:
    ```bash
    python client.py
    ```

### 🌐 Server Setup

1. Ensure the `recordings` directory exists and is writable by the web server:

2. Deploy the contents of the `server` directory to your web server.

### 🖥️ Viewing Recordings

Open `index.html` in a web browser to view the recorded videos. The page will fetch and display the videos from the `recordings` directory.

## 📝 Notes

- The `client.py` script captures frames from the webcam and recordings them as JPEG images to the server every second.
- The `upload.php` script handles the uploaded images and saves them in the `recordings` directory.
- The web application (served by `index.html`, `script.js`, and `style.css`) displays the recorded videos.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📧 Contact

If you have any questions, feel free to open an issue or contact me directly at [your-email@example.com](mailto:your-email@example.com).

Enjoy using WebCamSecurityCamera! 🎉
