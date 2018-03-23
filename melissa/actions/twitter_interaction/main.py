import tweepy

# Melissa
from melissa.profile import data

WORDS = {'post_tweet': {'groups': ['tweet']}}


class TwitterInteraction():

    def post_tweet(self, text):
        if data['twitter']['consumer_key'] == "xxxx" \
                or data['twitter']['consumer_secret'] == "xxxx" \
                or data['twitter']['access_token'] == "xxxx" \
                or data['twitter']['access_token_secret'] == "xxxx":
            msg = "Twitter requires a consumer key and secret," \
                  " and an access token and token secret."
            print msg
            return msg

        words_of_message = text.split()
        words_of_message.remove('tweet')
        cleaned_message = ' '.join(words_of_message).capitalize()

        auth = tweepy.OAuthHandler(
            data['twitter']['consumer_key'],
            data['twitter']['consumer_secret']
        )

        auth.set_access_token(
            data['twitter']['access_token'],
            data['twitter']['access_token_secret']
        )

        api = tweepy.API(auth)
        api.update_status(status=cleaned_message)

        return 'Your tweet has been posted'
