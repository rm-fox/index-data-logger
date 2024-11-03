# index-data-logger

Application to:
- log all available compute datapoints to database.
- log specific indices as timeseries appends to databases.

#### High Level Structure

One class for logging all data:
- Initially uses gpu hunt, then append further sources to df before pushing to db.
    - add_gpu_hunt
    - add_additional_source
- May want to only push price updates to save space.

One class for index:
- function for each new index, where a formula is defined (could be graph)

Main:
- Calls both all_logger and index_logger
