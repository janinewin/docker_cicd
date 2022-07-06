# Image transformation with Python

## Set up Streamlit with image upload

See [file upload](https://docs.streamlit.io/library/api-reference/widgets/st.file_uploader)


## Extract the face using Scikit-image

Use the [face detection module](https://scikit-image.org/docs/stable/auto_examples/applications/plot_face_detection.html#sphx-glr-auto-examples-applications-plot-face-detection-py)


## Display the image back on the page

Just `st.image`

## Separation of concerns in the code

- Detail where to put the Streamlit code, where to put the transformation code.
- Add a test for each part


## Build a v2 of the app using a Pytorch model

- Let's use an open source deep learning model, [Yolov5](https://github.com/ultralytics/yolov5)
- Get the basics of Pytorch and deep learning
- Write the function fo load and test the model

## Pimp the app, real-time face detection using Streamlit

- Code [here](https://github.com/nicolalandro/yolov5_streamlit)
- Demo [here](https://share.streamlit.io/nicolalandro/yolov5_streamlit/main)

