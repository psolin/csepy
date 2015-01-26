#csepy

Google Custom Search Engine API Python Wrapper

##Before you start:

* [Turn on Custom Search API by agreeing to the terms](https://console.developers.google.com/).  Note the API key.

* [Create a custom search engine that works the way that you want it to work](https://www.google.com/cse/all).  Note its ID in the URL.

##Usage:

Import the module
    from csepy import googlecse

Use your secret key and custom search engine ID:
    x = googlecse(SECRET_KEY='YOUR_SECRET_KEY', CSE_ID='YOUR_CSE_ID')

Grab the JSON results
    y = x.results(query='test')

You can use a host of other parameters, but 'query' is required.  Check them out here: https://developers.google.com/custom-search/json-api/v1/reference/cse/list

In case something went wrong, you view the URL that is generated:
    z = x.url(query='test')