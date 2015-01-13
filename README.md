Twitter Sort
==========

Twitter Sort is a sorting algorithm that takes advantage of the Twitter API.
You pass the script the numbers you would like sorted and it will tweet
a request asking for somebody to sort them. When someone replies with
a sorted version of the numbers, it will print them to the console 
and return.

Setup
-----
Ensure you have the `tweepy` module installed:

    pip install tweepy

Or clone from the Git repository:

    git clone https://github.com/tweepy/tweepy.git
    cd tweepy
    python setup.py install

Rename `settings_template.py` to `settings.py` and fill the API_KEY and
API_SECRET with your own key.

Usage
-----

```shell
$ python main.py 1,2,3,4
```
