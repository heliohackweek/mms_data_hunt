# MMS Data Hunt Project

This Helio HackWeek project aims at finding events within observational data from Scientists in the Loop (SITL) reports to better equip researchers of finding overlooked or similar events by extending the requested functionality.

Challenges/Tasks:

1. SITL Reports Web Search

    a. Building the database.

        - Retrieve ASCII reports from [Berkely](https://www.ssl.berkeley.edu/~moka/eva/sitl_report.html) hopefully from some type of RESTful API.
        - Parse through reports to create a language learning set to pick up on mispelled events, case sensitivity, and typographic errors.
        - Find occurances of reported BBF and DF events.
        - Store results in a SQL-less database for future use.
        - Automate process for future reports as well as process all remaining reports.
        - _out of scope:_ create a standardized reporting mechanism or format
    b. Frontend work

        - Website with search that queries database base upon event type, date range, or latest N events.
        - API underneath website so researchers can grab data from database using HTTP methods
        - Visually map events to xy and yz planes for further research
        - Add functionality of mapping/visualizations to show data layers or with slight transparency
        - _out of scope:_ extend to produce a catalog of all events reported
2. Event Finder

  a. Build a Python package to search MMS data for specific events (BBF & DF)

    - Use pyspedas to retrieve/stream data for specific dates and times reported from sample CSV files from database of SITL reports
    - Unsure about specific types of observations needed to identify these events
    - Data format retrieved? Is is a Pandas dataframe?
    - Manipulate to identify event duration, magnatude, location, and observational files used.
    - Add event information to database as well as references to data, imagery, and other information (metadata or resources)

  b. Use ML to find similar events

    - Once a small subset of events have been confirmed from the data, a training set will be created for each event type
    - Use of tensorflow to produce similar events within the spanse of observational records
    - Optimize algorithm used to optimize resource use

  c. Use GPU processing to optimize ML techniques

    - Use RAPIDS on NVIDIA resources to expedite processing of data for events
    - Build optimized algorithms to sift through large amounts of data for analysis
