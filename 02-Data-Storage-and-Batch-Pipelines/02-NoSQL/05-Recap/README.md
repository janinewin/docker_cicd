# Team work!

Two teams work together on a project:
- Team machine learning. It provides a service that takes as input an image and returns the list of coordinates of the center of the faces that are found in the image.
- Team app. This team provides a web application on which you can upload a picture, and it will draw on the picture a red dot every time a face is found.

## Flow

- [App team] User logs into the app
- [App team] User uploads an image
- [App -> ML] Image is sent to the ML team's service
- [ML] Process the image and get the faces' coordinates
- [ML -> App] Coordinates are sent back to the App team
- [App] Draws a red dot for each coordinate and displays back to the user
- [User] Is happy
