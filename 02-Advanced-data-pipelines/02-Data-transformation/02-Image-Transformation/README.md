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

Use the Streamlit documentation on [file upload](https://docs.streamlit.io/library/api-reference/widgets/st.file_uploader) to fill the `def streamlit_read_uploaded_file()` function. **This should return the uploaded file**.

<details>
  <summary markdown='span'>💡 Hint</summary>

  Notice that the Streamlit example gives you many ways to load and then convert the `uploaded_file`, we only care about the file loading part.
</details>

## Find the face patches on the uploaded image

In the main function, called `def streamlit_app()`, we want to build the image with embedded face patches on it, like in the Scikit image tutorial (see the red square around the face).

<img src="https://scikit-image.org/docs/stable/_images/sphx_glr_plot_face_detection_001.png" width=400>

We've written the function `def apply_face_patches_to_original_image(...)` for you, it's just a matter of applying it to the right inputs to get the image with face patches. **Can you do it?**

<details>
  <summary markdown='span'>💡 Hint</summary>

  The function `apply_face_patches_to_original_image` has two inputs.
  
  - `img` of type `np.ndarray`
  - `face_patches` of type `List[Patch]`

  Use the types to find the right values to plug in as inputs, from what has already been calculated in this function `def streamlit_app()`
</details>

## Display the image back on the page

Now that we have:

- Uploaded an image
- Applied the face recognition onto it
- Embedded the face patches on the original image

**Let's display that image with face patches in the webapp**

<details>
  <summary markdown='span'>💡 Hint</summary>

  Look at the [official documentation](https://docs.streamlit.io/library/api-reference/media/st.image) from Streamlit.
</details>

## Deploy to the cloud this first version of the app

Congratulations, you've built a fun webapp to detect faces. Let's share it with the world 🌏.

**Step 1**

Regardless of your cloud provider, we'll need to **package the app within a Docker image**. We've already written the `Dockerfile` for you. We've left a lot of comments in it. Please take a moment to read through it and follow the instruction at the end.

### GCP

We assume below that you have followed the first exercise setup instructions, and now have a working Google "Cloud Artifact Registry" Docker repository. If not, please go back to that exercise 👈.

**Step 2**

Open Google Cloud Artifact Registry. Tag the image with your remote Docker repository prefix.

Set the value of `REGISTRYPREFIX` in your `Makefile`, at the top.

**Step 3**

👉 Now you can re-tag the image with `make tag`. **We highly encourage you to read carefully through the commented Makefile, it should be instructive 🔓.**

**Step 4**

👉 Finally, let's push it to the cloud with `make push`.

**Go to your cloud console, Artifact Registry and look for this newer version, can you find it?**

**Step 5**

Deploy it!

Go to Cloud Run and create a new service: click `CREATE SERVICE`.

- `Deploy one revision from an existing container image`, click `SELECT` and in the tab `Artifact Registry`, look for your image
- Give it the service name `lwface`
- Pick the closest region, if you're in Europe, pick `europe-west` for instance.
- CPU allocation: `CPU is only allocated during request processing`
- Autoscaling: Minimum of 0 and Maximum of 5
- Open `Container, Variables & Secrets, Connections, Security`
  - What's the container port? Hint 💡: look in the `CMD` of the `Dockerfile`
  - Up the memory to 1 GiB
  - Keep the CPU at 1
  - Maximum requests per container: 5
- Click `CREATE` 🚀

Once deployed, your app should be live with a URL, try it, share it with your peers!

## Pimp the app, real-time face detection using Streamlit

- Code [here](https://github.com/nicolalandro/yolov5_streamlit)
- Demo [here](https://share.streamlit.io/nicolalandro/yolov5_streamlit/main)

## Build a v2 of the app using a Pytorch model

- Let's use an open source deep learning model, [Yolov5](https://github.com/ultralytics/yolov5)
- Get the basics of Pytorch and deep learning
- Write the function fo load and test the model

## Deploy the newer version to the cloud

Ready to show your app to the world? Follow the same steps as earlier to deploy the newer version to the cloud.
