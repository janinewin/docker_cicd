# Image transformation with Python

In this exercise, we'll build a cool real-time face detection app, step by step!

As a bonus, for the bravest, you'll have the opportunity to deploy it to your cloud provider and show it to the world 😎.

The exercise is broken down into the following bits:

1. Build a function that detects faces from images
2. Hook this function to a simple Streamlit app. Images will be uploaded to the app, faces detected using the function in step 1, and results displayed back on the Streamlit app.
3. Enhance the Streamlit app and hook it to your webcam 📹.
4. Enhance the image detection module with a deep learning model 🧮.
5. Deploy the app to the cloud.

**Note** All functions have been written to `lwface/face.py`, that's the only file to work on throughout this exercise.

## Dive into the Python libraries

Let's look into our `pyproject.toml` file to understand which libraries we've installed and why.

### Image analysis

- [Matplotlib](https://matplotlib.org/) is the most used data visualization / plotting library in Python.
- [Pillow](https://pillow.readthedocs.io/en/stable/) is the Python Imaging Library, you'll find it used everywhere images are loaded and transformed. It is compatible with Numpy, images are "just" arrays of integers at the end of the day. **Ask your TA for more details about this if you're curious as to why**.
- [Scikit-Image](https://scikit-image.org/) is a collection of algorithms for image processing, highly compatible with the Numpy ecosystem and Pillow.
- [Torch](https://pytorch.org/), developed by Facebook Research, is one of the three most popular deep learning frameworks. We use it to enhance our face detection algorithm.
- [Numpy](https://numpy.org/), the fundamental package for scientific computing with Python. As images are just Numpy arrays for the computer, all packages above use Numpy for processing.


### Server

- [Streamlit](https://streamlit.io/) which you've seen previously, is a simple yet powerful way to build data apps.
- [Watchdog](https://pypi.org/project/watchdog/) when combined with Streamlit, allows us to run the app while working on the code. Just run `poetry run streamlit lwface/face.py` to run the app, then work on the code and just reload the page in your browser for changes to take effect. Magic 🎂!
- [Streamlit WebRTC](https://github.com/whitphx/streamlit-webrtc) to hook your camera to a Streamlit application using [WebRTC](https://webrtc.org/).
- [av](https://pypi.org/project/av/) is used to convert the WebRTC video frames to Python-friendly data structures that can be fed to our image processing algorithms.


## Extract faces using Scikit-image

We'll start by building the simpler face detection function `def detect_face(...)`.

Use the [face detection module](https://scikit-image.org/docs/stable/auto_examples/applications/plot_face_detection.html#sphx-glr-auto-examples-applications-plot-face-detection-py).

Only accept JPEG images of type `jpeg` or `jpg`.

<details>
  <summary markdown='span'>💡 Hint</summary>

  - If you struggle finding the right bits to use, try running the example.
  - Then import the right libraries.
  - Use the function signature to understand the right input and output types.
  - Then only keep the bits needed in `detect_face`, given an image, to return the detected patches.
</details>


## Set up Streamlit with image upload

Use the Streamlit documentation on [file upload](https://docs.streamlit.io/library/api-reference/widgets/st.file_uploader) to fill the `def streamlit_file_upload()` function. **We want to read the file as `bytes`**.

<details>
  <summary markdown='span'>💡 Hint</summary>

  Notice that the Streamlit example gives you many ways to convert the `uploaded_file`, we only care about the one to read the file as bytes.
</details>


## Display the image back on the page

TODO @selim

Just `st.image`


## Deploy to the cloud this first version of the app

- Use the Dockerfile provided.
- Build the Docker image.
- Tag the Docker image with your remote repository prefix.
- Push the Docker image to your remote repository.
- Deploy the Docker image as an application (in Cloud Run for GCP users).

## Pimp the app, real-time face detection using Streamlit

- Code [here](https://github.com/nicolalandro/yolov5_streamlit)
- Demo [here](https://share.streamlit.io/nicolalandro/yolov5_streamlit/main)

## Build a v2 of the app using a Pytorch model

- Let's use an open source deep learning model, [Yolov5](https://github.com/ultralytics/yolov5)
- Get the basics of Pytorch and deep learning
- Write the function fo load and test the model

## Deploy the newer version to the cloud

Ready to show your app to the world? Follow the same steps as earlier to deploy the newer version to the cloud.
