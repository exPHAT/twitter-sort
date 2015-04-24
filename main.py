# Twitter-Sort
# main.py
# Aaron Taylor
#
# This sorting technique allows a program to pass this script a list of
# numbers, and be returned the sorted version of them. This works by tweeting
# the list to Twitter asking for them to be sorted, and when there is a
# reply, we check to ensure they're sorted. If they are, we return.

import tweepy
import sys
import os
from webbrowser import open as site  # For the auth token
import settings

keysPath = "keys.txt"
if len(sys.argv) == 1:
    print("Arguments required!")
    sys.exit()

numbers = eval("".join(sys.argv[1:]))

auth = tweepy.OAuthHandler(settings.API_KEY, settings.API_SECRET)

if os.path.exists(keysPath):
    keysFile = open(keysPath, "r+")
else:
    keysFile = open(keysPath, "a+")
    keysFile.seek(0)

if len(keysFile.read()) == 0:
    authUrl = auth.get_authorization_url()
    site(authUrl)
    authPIN = input("Enter your auth PIN: ")
    try:
        auth.get_access_token(str(authPIN))
    except tweepy.TweepErrori as e:
        print("Error: Getting access token failed: " + e.message)
        sys.exit()
    # Save for next call
    keysFile.write(auth.access_token + " " + auth.access_token_secret)
else:
    keysFile.seek(0)
    keys = keysFile.read().split(" ")
    if len(keys) == 2:
        auth.set_access_token(keys[0], keys[1])
    else:
        # The file is set up incorrectly
        print("Error: Something is wrong with", keysPath)
        sys.exit()

api = tweepy.API(auth)

tweetID = api.update_status(status="Can you sort these numbers? " + str(numbers)).id


class ReplyListener(tweepy.StreamListener):

    def on_status(self, status):
        # There is a status tweeted tagging the user

        if status.in_reply_to_status_id == tweetID:
            # There was a reply to the aaron-sort tweet
            parsedNumbers = "".join(status.text.split(" ")[1:])\
                .replace(" ", "")\
                .replace("[", "")\
                .replace("]", "")\
                .replace("(", "")\
                .replace(")", "").split(",")
            givenNumbers = list(map(int, parsedNumbers))

            # Ensure the given numbers are sorted

            areSorted = True
            if len(givenNumbers) != len(numbers):
                areSorted = False
            for n in givenNumbers:
                if givenNumbers.count(n) != numbers.count(n):
                    areSorted = False
                    break
            for i in range(len(givenNumbers)):
                if i > 0:
                    if not givenNumbers[i] >= givenNumbers[i - 1]:
                        areSorted = False
                        break

            if areSorted:
                print(givenNumbers)  # Print the sorted numbers to the console
                api.update_status(
                    "@" + status.author.screen_name + " Awesome! Thanks!",
                    in_reply_to_status_id=status.id)
                return False
            else:
                api.update_status(
                    "@" + status.author.screen_name +
                    " Those numbers aren't sorted!",
                    in_reply_to_status_id=status.id)
                return True
        else:
            # They did not reply to the aaron-sort tweet
            return True

    def on_error(self, statusCode):
        # There was a listener error

        print("There was a listener error with the code", statusCode)
        return True

    def on_timeout(self):
        # There was a listener timeout

        print("There was a listener timeout")
        return True

listener = tweepy.streaming.Stream(auth, ReplyListener())
# Listen for a response to the user
listener.filter(track=["@" + api.me().screen_name])
