from random import random
from tqdm import tqdm
import threading
import os
import cv2
import numpy as np
import math
import timeit
import argparse
from PIL import Image, ImageDraw

# Setup
videopath = "video.mp4"
num_threads = os.cpu_count()

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--threads', type=int, help="The number of running threads. Defaults as the number of threads in your CPU (currently " + str(num_threads)+").", default=num_threads)
parser.add_argument('-p', '--path', type=str, help="The path of the video file you want to compute. Defaults to video.mp4 contained in the folder.", default=videopath)
args=parser.parse_args()
num_threads, videopath = vars(args).values()
print("About to analyze file at \""+videopath+"\".\nRunning threads: "+str(num_threads)+".\n")

vidcap = cv2.VideoCapture(videopath)
length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
start = timeit.default_timer()

def dowork(initial_frame, frames, tn):
	# Initial loop setup
	count = 0
	w, h = int(2000 / num_threads), 200
	r_w = w / frames
	canvas = Image.new("RGB", (w, h))
	# Create the directory
	current_directory = os.getcwd()
	final_directory = os.path.join(current_directory, str(tn))
	if not os.path.exists(final_directory):
   		os.makedirs(final_directory)
	# Set the first frame
	vidcap = cv2.VideoCapture(videopath)
	vidcap.set(cv2.CAP_PROP_POS_FRAMES, initial_frame-1)
	success, img = vidcap.read()
	for i in tqdm(range(frames), leave=False): 
	    cv2.imwrite("./"+str(tn)+"/frame.jpg", img)     # save frame as JPEG file    
	    success,img = vidcap.read()
	    if not success: 
	        break
	    # Calculate average color
	    average = img.mean(axis=0).mean(axis=0)
	    col = (int(average[2]), int(average[1]), int(average[0]))
	    # Draw the stripe
	    img1 = ImageDraw.Draw(canvas)
	    shape = (int(count * r_w), 0, int((count + 1) * r_w), h)  
	    img1.rectangle(shape, fill = col, outline = col)
	    # Remove the temp frame, repeat
	    os.remove("./"+str(tn)+"/frame.jpg")
	    count += 1
	#canvas.show()
	canvas.save("%d.jpg" % tn)
	os.rmdir(str(tn))

# Calculate the initial frames for each thread
start_frames = []
frames = int(length / num_threads)
for i in range(num_threads):
	start_frames.append(i * frames)

# Initialize threads
threads = []
for i in range(num_threads):
	t = threading.Thread(target=dowork, args=[start_frames[i], frames, i])
	t.daemon=True
	threads.append(t)

for t in threads:
	t.start()

# Wait for all the threads to finish
for t in threads:
	t.join()

# Load images
images = []
for i in range(num_threads):
	tmp = Image.open(str(i)+".jpg")
	images.append(tmp)

# Stitch them together
final_img = Image.new("RGB", (images[0].width * num_threads, images[0].height))
for i in range(num_threads):
	final_img.paste(images[i], ((images[0].width * i), 0)) 
final_img.show()
final_img.save("output_" + str(random()) +".jpg")

# Clean up the temporary jpgs
for i in range(num_threads):
	os.remove(str(i) + ".jpg")

# Stop timer and print runtime
stop = timeit.default_timer()
elapsed = (stop - start) +1
print("\nFinished execution in %d seconds." % elapsed)
