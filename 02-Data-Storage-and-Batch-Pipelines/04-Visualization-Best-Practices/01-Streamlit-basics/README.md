## Data
We are going to use real Formula 1 data. The goal of this exercise is to get you familiar with the basic functionality of Streamlit, while exploring the Formula 1 dataset.

## Streamlit basics
In the `app` folder there is a file called `main.py`. It is already
partly filled with code, but your goal is to enhance the main Streamlit page
with the following:
- Add the right caching decorator to the `load_data` function
- Create a Streamlit title, subheader on the main page. Do the same in the sidebar
- The data that is loaded needs to be saved into the session state for it
to be reusable across different pages in Streamlit
- In the pages subdirectory, create two Python files. See the Streamlit documentation
for more info on how this works. Create one file for doing descriptive
statistics, and another one for visualizing the data. It is up to you to decide
on the data that you want to visualize. Create something cool!
