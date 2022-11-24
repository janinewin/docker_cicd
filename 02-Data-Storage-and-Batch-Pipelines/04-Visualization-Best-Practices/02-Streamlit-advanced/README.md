## Engineering context - real life use
Often times, as a data engineer, you need to present data and summarize your results in a human readable way. Most people won't be able to read your dataframes straight from the console.
This is why creating simple apps to summarize data in an interactive ways using dashboards, graphs and texts is important (it's also fun for some).
Having such apps will help you highlight your findings and establish a baseline of common knowledge for your peers.
You want your app to be adopting as much clean code principles as possible so that the code is easily readable, maintainable and extensible.
Leveraging dependency injections and the single responsibility principle sets you up for success.

## Background
This exercise aims at teaching you the fundamentals to create a functional streamlit app.
You will:
- Set up a clean architecture for the streamlit app
- Discover the principle of dependency injection,
- Implement components use the single responsibilty principle
- Write unit tests
- Write documentation using docstring, restructured text and sphinx
- Add theming and various configs
- Implement a UI based on a mock

## End goal
At the end of this exercise you should:
- Have a solid base to implement any UI using streamlit
- Feel comfortable with some clean code notions
- Understand basic unit tests methodology
- Understand how to write proper documentation


## Setup
Please do the setup exercise first!

## Mocks and UI
### Basic UX
![Link to UI mock](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D5/F1%20Dashboard%20Mock.jpg)

### Welcome page
![welcome Page](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D5/dashboard-launch.png)

### Selected race
![selected race](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D5/dashboard-race-selected.png)

## Task 1: Secrets configuration
Before we can implement our UI, we need to add a secrets file for streamlit to store our credentials to connect to the database. Secrets files are never committed to git and should always be private or very well secured. The secret file for streamlit is a simple `.toml` file that streamlit automatically loads and parses at run time if in the correct location. Simply put, it is equivalent to `.env` file.

1. In the `.streamlit` folder there is an existing config file responsible for the configuration of a few key elements in streamlit. In the same folder add a `secrets.toml` file

2. In the `secrets.toml` file add the required credentials to connect to the PostgresSQL instance
    ```toml
    [postgres]

    drivername = "postgresql"
    host = "database"
    port = 5432
    database = "f1db"
    username = "postgres"
    password = "postgres"
    ```
You are now ready to go with the UI implementation.

## Task 2: Layout and Static UI

For this task we'll create the basic layout for the app UI, populate it with some data, add some theming for the looks.

Please refer to streamlit's documentation to for the widget and their calling conventions
[Streamlit API reference](https://docs.streamlit.io/library/api-reference)

1. Implement the `layoutHeader` method in `main.py` using `st.title`
2. Implement `layoutTopContainer` to display the contrustor and driver championships. This container is composed of two columns in which you present tables
    - Call from the module `F1Queries`  the method `getConstructorStandingsForRace` to get the constructor championship data
    - Call from the module `F1Queries`  the method `getDriverStandingsForRace` to get the constructor championship data
    - using this pseudo code
        ```python
        if not launched:
            # Display constructor standings season's result (you can display the data using the last race_id of the year)
            # Display driver standings season's result (you can display the data using the last race_id of the year)
        else:
            # Display the current constructor standing
            # Display the current driver standing
        ```
3. Implement `layoutSideBar` to display a sidebar composed of a title and buttons for each races with the race name as text
    - Call from the module `F1 Queries` the method `getRacesForYear`
4. Implement `clickSideBarButton` to push to our cache the selected race_id and update the is_launched boolean
    - Use the constants `F1Constants.IS_LAUNCHED: Bool`
    - Use the constants `F1Constants.SELECTED_RACE: Int`
    - Call from the module `F1Cache` the method `cacheKeyValue`

We now have laid out basic components for our UI and are presenting static data. However nothing is interactive yet, we need to add some actions and introduce the concept of state into the app.

## Task 3: Data transforms, unit tests and documentation

In this task we'll focus on:
- Writing unit tests for our transformation data
- Transforming the input data we get from our F1 database in order to get better insights and situational data

We are using pytest as a testing framework, refer to the documentation if you want to get more knowledge [pytest documentation](https://docs.pytest.org/en/7.1.x/contents.html)

We'll do some test-driven development here (TDD)

1. Let's extract the race name for a given race_id from the dataFrame containing all the races in the year.
    - Implement the `F1Transforms` unit tests in the module `app.tests.test_f1_transforms`.
    - Here you want to call the method `getRaceName` from the module `F1Transforms` and pass in the fixture parameters
    - Use the `assert` method to compare your method results with the expected result
    - For the sake of this exercise please return the results of your method - **this is only for testing purposes**
        ```python
        res = <my_method_here>
        [...]
        return res
        ```
    - Now that our test is implemented we can implement the actual method body. Head to the file `f1_transforms.py` and implement the method `getRaceName`.
        ```python
        """From the dataframe race_df containing all the races for a given year and the race_id of a given race. Return the string `race_name` matching the race_id"""
        ```
    - Run tests they should pass
    - Write a simple docstring for this method using the numpy format:
        ```python
        """
        Method description....
        Parameters
        ----------
        my_param_1: type
            description of parameters
        my_param_2: type
            description of parameters

        Returns
        -------
        my_return: type
            description of parameters

        """
        ```
    - run `make doc` it should open the freshly compiled documentation using sphinx

2. Using the same methodology as above, extract the fastest laps for a given race, by implementing the method `getBestTimePerLap`
    ```python
    """For all the laps in given race compute extract for each lap the fastest lap and return a dataframe containing the fastest laps for each lap"""
    ```

## Task 4: Interactivity and advanced layouts

Now that we have all the data necessary for our dashboard and the first simple layout let's add some interactivity and some more widgets.
For this exercise we'll first add some state into our app so we can get some interactivity going, then we'll add more widgets (tables, strings, graphs)

1. Update the method `layoutHeader` using the method implemented `F1Transform.getRaceName`
    ```python
    if not launched:
        # Display some generic title
        # Display some subtitle
    else:
        # Display title
        # Display race name
    ```
2. Implement the `layoutMiddleContainer` method. The container is based on 2 columns
- Display fastest pitstop for a given race using `F1Queries.getFastestPitStopForRace` and using a `st.text` widget that you can format the way you want
- Display the fastest lap for a given race using `F1Queries.getFastestLapTimeForRace` and using a `st.text` widget
- Implement an early exit condition to not display this container if `F1Constants.IS_LAUNCHED` is False

3. Implement the `layoutBottomContainer` method to diplay a graph of the evolution of the fastest lap for a given race over time.
- Implement an early exit condition to not display this container if `F1Constants.IS_LAUNCHED` is False
- Get the all the laps for a race using `F1Queries.getLapTimesForRace`
- Compute the fastest laps using your newly implement method `F1Transforms.getBestTimePerLap`
- A graph should now appear when you refresh

4. Play with your app colors by updating the `config.toml` theme section as mentionned in the docs [theming docs](https://docs.streamlit.io/library/advanced-features/theming)


You should have now a fully functionning dashboard covered with some unit tests and documentation.

## Useful links
- [Sphinx kick off](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html)
- [Sphinx Theme](https://sphinx-rtd-theme.readthedocs.io/en/stable/index.html)
- [Sphinx docs](https://www.sphinx-doc.org/en/master/index.html)
