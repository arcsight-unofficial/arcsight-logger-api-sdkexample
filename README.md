# Arcsight Logger REST Development SDK Implementation Example

This is a basic script implementing all the different functionality of the ArcSight Logger SDK

### Installation:

Download or clone the git repository:

```sh
$ git clone https://github.com/arcsight-unofficial/arcsight-logger-api-sdkexample
```

Install library with pip from the newly created folder:

```sh
$ cd arcsight-logger-api-sdkexample
$ pip install -r requirements.txt
```

Open up client.py with your faviourite editor, and ensure you change the first variables at the top:

```sh
$ vi client.py
$ Change HOST, USERNAME and PASSWORD to fit your environment
```

Run the test with your python binary (minimum python3)
This will run different searches and show how each function in the SDK works. Feel free to change values or implementations to test the parts you want before running the basic script.

```sh
$ python3 ./client.py
```

### Other related resources:

There is now new unofficial documentation for utilizing the ArcSight Logger API:

[ArcSight Logger API Documentation, web based](https://github.com/arcsight-unofficial/arcsight-logger-api-documentation)

[ArcSight Logger API Examples using Postman](https://github.com/arcsight-unofficial/arcsight-logger-api-examples)

[ArcSight Logger API SDK](https://github.com/arcsight-unofficial/arcsight-logger-api-sdk)

### Optional Parameters for API requests:
Only the mandatory options is implemented for each function call, all optional arguments for each API call can be found in the above web based documentation and can be supplied as the last arguments when creating an instance of the function.
This is because each function with optional parameters also accepts unlimited kwargs as the last scope item.
An example of this integration can be found in the SDK implementation of chart_data in this script.

### Support:
This SDK and example is not officially supported by Micro Focus, for any issues please post a issue on the github issue page or ask on the [ArcSight Community forums](https://community.softwaregrp.com/t5/ArcSight-User-Discussions/bd-p/arcsight-discussions)