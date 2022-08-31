# FrameBars
Convert a video in a picture showing the average color for each frame.

| ![FrameBars of the first episode of The Simpsons.](https://i.imgur.com/vpB2pjk.jpeg "FrameBars of the first episode of The Simpsons.") |
|:--:|
|FrameBars of the first episode of The Simpsons.|


## Installation & Usage
Download the project from the git page or execute the command ```git clone https://github.com/giuliosmedile/FrameBars.git```.

Install the required packages with the command ```pip3 install -r requirements.txt```

Run the program with the command ```python3 ./framebars.py```


## Options

The program supports two command-line arguments:
- ```-t [THREADS]``` to specify the number of concurrent threads. Default to the CPU's number of threads.
- ```-p [PATH]``` to specify the input file. Supports various kinds of video formats. Defaults to *video.mp4* included in the project.

Additionally ```-h``` or ```--help``` can be called at runtime to see this explanation.
