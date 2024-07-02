import cv2
import numpy as np
import collections
import time
import subprocess
import os
import requests
from datetime import datetime  # Import datetime module

# Adjustable parameters
PRE_RECORD_SECONDS = 5
RECORD_SECONDS = 2

# Initialize the camera
cap = cv2.VideoCapture(1)
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Calculate the number of frames to keep in the buffer
buffer_size = PRE_RECORD_SECONDS * fps

# Circular buffer to store frames
frame_buffer = collections.deque(maxlen=buffer_size)

# Initialize variables
recording = False
start_time = None
out = None
filename = None

# Read the first frame
ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():
    # Calculate the difference between the current frame and the previous frame
    diff = cv2.absdiff(frame1, frame2)

    # Convert the difference to grayscale
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Blur the grayscale image
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply thresholding to the blurred image
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # Dilate the thresholded image to fill in holes
    dilated = cv2.dilate(thresh, None, iterations=3)

    # Find contours in the dilated image
    contours, _ = cv2.findContours(
        dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Check for significant movement
    movement_detected = False
    for contour in contours:
        area = cv2.contourArea(contour)
        if area >= 1000:  # Lower the threshold to detect smaller movements
            movement_detected = True
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            print(f"Movement detected with contour area: {area}")
            break

    if movement_detected:
        if not recording:
            # Start recording
            recording = True
            start_time = time.time()

            # Create a video writer
            # Using 'XVID' codec for AVI files
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = f'movement_{current_time}.avi'
            out = cv2.VideoWriter(filename, fourcc, fps,
                                  (frame1.shape[1], frame1.shape[0]))

            # Write the buffered frames to the video file
            print(f"Starting recording from {PRE_RECORD_SECONDS} seconds ago.")
            for buffered_frame in frame_buffer:
                out.write(buffered_frame)

        # Reset the timer
        start_time = time.time()

    if recording:
        # Write the current frame to the video file
        out.write(frame1)

        # Stop recording after RECORD_SECONDS if no movement is detected
        if time.time() - start_time >= RECORD_SECONDS:
            print(
                f"Stopped recording after {RECORD_SECONDS} seconds of no movement.")
            recording = False
            out.release()

            # Convert the recorded AVI file to MP4
            mp4_filename = filename.replace('.avi', '.mp4')
            # Update this path to your FFmpeg installation
            ffmpeg_path = r'C:\ffmpeg\bin\ffmpeg.exe'
            ffmpeg_command = [
                ffmpeg_path, '-i', filename, '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental', '-b:a', '192k', '-y', mp4_filename
            ]
            subprocess.run(ffmpeg_command)
            os.remove(filename)

            # Verify that the file was saved correctly
            if os.path.exists(mp4_filename):
                print(f"File {mp4_filename} saved successfully.")

                # Upload the video file to the server
                try:
                    with open(mp4_filename, 'rb') as f:
                        files = {'file': (mp4_filename, f, 'video/mp4')}
                        response = requests.post(
                            'https://YOURWEBSITE/securitycamera/upload.php', files=files)
                        print("Upload response:", response.text)
                except Exception as e:
                    print(f"Failed to upload the file: {e}")
            else:
                print(f"File {mp4_filename} was not saved correctly.")

    # Add the current frame to the buffer
    frame_buffer.append(frame1)

    # Display the result
    cv2.imshow("feed", frame1)

    # Update the frames
    frame1 = frame2
    ret, frame2 = cap.read()

    # Break the loop if 'q' is pressed
    if cv2.waitKey(10) == ord('q'):
        break

# Release the camera and destroy all windows
cap.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()
