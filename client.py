#!/usr/bin/env python

"""Example implementation of the ArcSight Logger SDK."""

import time
import json
from datetime import datetime
from datetime import timedelta
import loggersdk


# This is a basic example showing how you can import and utilize the
# ArcSight Logger SDK. This is installed with "pip install loggersdk"
# The script itself is not meant for production, but rather only for
# documentation and learning material on utilization of the SDK itself.
# The package itself is not part of any official product.


# Starting with creating variables for information that will be reused
# to make the rest of the script cleaner.
# Please change minimum the HOST, USERNAME and PASSWORD to its correct values
HOST = '10.0.0.0.1:9000'
USERNAME = 'admin'
PASSWORD = 'PASSWORD'
QUERY = 'deviceVendor CONTAINS "ArcSight"'
CHART_QUERY = 'deviceVendor CONTAINS "ArcSight" | sort Time'

# Please leave this entry alone, it is only to generate a unique search_id
SEARCH_ID = int(round(time.time() * 1000))

# Making an example script timezone aware and in very specific ISO format
# supported by the logger is not fun, please ignore this mess, but feel
# free to make it better/cleaner with a PR. The biggest issue is that
# the ISO format actually uses microseconds, and to make it worse there is
# a timezone added at the last part, so we can't just strip the last chars
# to keep the script timezone and package independent.
# By default it sets start_time to now minus 40 minutes,
# and end_time by now minus 10 minutes
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'
CURRENT_TIMEZONE = datetime.utcnow().astimezone().tzinfo
CURRENT_TIME = datetime.now(tz=CURRENT_TIMEZONE)
DRILLDOWN_START = CURRENT_TIME - timedelta(minutes=40)
DRILLDOWN_START = DRILLDOWN_START.isoformat(timespec='milliseconds')
DRILLDOWN_END = CURRENT_TIME - timedelta(minutes=10)
DRILLDOWN_END = DRILLDOWN_END.isoformat(timespec='milliseconds')


# All error handling is done by the SDK for this example, if an API call fail
# the script will exit, which is why additional error checking is
# not implemented here.

# Logging in the user, saving the response in a variable.
print("Trying to login to " + HOST)
authtoken = loggersdk.login(HOST, USERNAME, PASSWORD)
print("Login Successful")

# While it can be done with one line, this is just to show that we only
# want to store the actual authentication token, and not the whole array
authtoken = authtoken['log.loginResponse']['log.return']

# We then continue with initializing a search, providing the host/IP,
# the authtoken that was retrieved from the login request,
# a query in the same format as on the ArcSight Logger, and a search_id.
print("Creating a search with ID " + str(SEARCH_ID))
loggersdk.search(HOST, authtoken, QUERY, SEARCH_ID)

# Checking the status of the search we just triggered
status = loggersdk.status(HOST, authtoken, SEARCH_ID)
print("Current status of the search is: " + status['status'])

# This is a custom function in the SDK and not part of the API itself.
# It runs a status check every 5 seconds, until the status changes to complete.
print("Waiting for search to finish")
loggersdk.wait(HOST, authtoken, SEARCH_ID)
print("Search finished")

# Retriving and printing the full results after the search is finished
print("Printing out a copy of the results")
events = loggersdk.events(HOST, authtoken, SEARCH_ID)
print(json.dumps(events, indent=10))

# We can shrink the time range for a finished search, the example itself
# only adds 10 minutes to START_TIME, and removes 10 minutes from END_TIME
print("Drilling down the timeframe for " + str(SEARCH_ID))
loggersdk.drilldown(HOST, authtoken, SEARCH_ID, DRILLDOWN_START, DRILLDOWN_END)
print("Drilldown successful")

# After retrieving the events using the normal event function,
# we can collect the row_id from the returning results,
# it is the first value in each results array,
# example format would be CC-0@Local
print("Getting raw events from drilldowned search and prints them")
raw_events = loggersdk.raw_events(HOST, authtoken, SEARCH_ID, [events['results'][0][0]])
print(raw_events)

# Shows an example of histogram output with default bucket configs
print("Retriving an histogram version of the event and prints it")
histogram = loggersdk.histogram(HOST, authtoken, SEARCH_ID)
print(json.dumps(histogram, indent=10))

# Stopping a search, keeping the search results available until its timeout
print("Stopping the search, normally only done when finished")
loggersdk.stop(HOST, authtoken, SEARCH_ID)
print("Stop successful")

# Closes the search, no reason to stop it first,
# this is just for example purposes
print("Closing search with id " + str(SEARCH_ID))
loggersdk.close(HOST, authtoken, SEARCH_ID)


# For testing charts, we need a second search, as you need to format
# your query specifically to allow for chart_data usage.
# New search_ID generated first
SEARCH_ID = int(round(time.time() * 1000))
print("Creating new search for charts")
loggersdk.search(HOST, authtoken, CHART_QUERY, SEARCH_ID)
print("New search created")

# Now lets wait again for the search to finish
print("Waiting for search to finish")
loggersdk.wait(HOST, authtoken, SEARCH_ID)
print("Search finished")

# And last we can retrieve the values in a format commonly used for charts
print("Getting chart data and printing the output,\
      this example includes utilizing optional arguments")
# This is the additional optional arguments we want to append right after
# the mandatory options
kwargs = {
    'length': 30,
    'offset': 2
}

chart_data = loggersdk.chart_data(HOST, authtoken, SEARCH_ID, **kwargs)
print(json.dumps(chart_data, indent=10))

# Get the type of the search, this should now be aggregated
print("Getting type of search")
status = loggersdk.status(HOST, authtoken, SEARCH_ID)
print("Search type is " + status['result_type'])
print("This is different from a normal search which uses type histogram, it's only because our search query included a sort action")

# Now that all functions have been created let's close down this last search
print("Closing search with id " + str(SEARCH_ID))
loggersdk.close(HOST, authtoken, SEARCH_ID)

# Always remember to log out at the end, or you will end up overloading
# the ArcSight Logger with sessions, making you unable to login again
# until sessions has timed out manually, especially during development
# this can be quite dangerous.
print("Logging out")
loggersdk.logout(HOST, authtoken)
print("Logout successful, thanks for testing!")
