"""Authenticate to Twitter and announce tagged release."""

import os

import tweepy
from ghapi.all import context_github


def twitter_api():
    """Connect to Twitter API."""
    consumer_key,consumer_secret,access_token,access_token_secret = context_secrets.TWITTER.split()
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    return tweepy.API(auth)


def tweet_text(payload):
    """Compile Tweet."""
    def_tmpl = "New #{repo} release: v{tag_name}. {html_url}\n\n{body}"
    tweet_tmpl = os.getenv('TWEETREL_TEMPLATE', def_tmpl)
    rel_blank = {
        "html_url": "NO RELEASE INFO",
        "tag_name": "NO RELEASE INFO",
        "body": "NO RELEASE INFO"
    }
    rel = payload.get("release", rel_blank)
    repo = payload.repository.full_name.split('/')[1]
    res = tweet_tmpl.format(repo=repo, tag_name=rel.tag_name, html_url=rel.html_url, body=rel.body)
    return res if len(res)<=280 else (res[:279] + "…")


def send_tweet():
    """Tweet release."""
    payload = context_github.event
    return twitter_api().update_status(tweet_text(payload))


send_tweet()