# reddit-seller-block

Browsing Reddit isn't same as before. Too many OnlyFans.

`reddit-seller-block` is simple Python program to clean up feed, it will try to detect seller and block them.

## Usage

First, make Oauth scripting app, like in instruction below.

https://redditclient.readthedocs.io/en/latest/oauth/

Now, run the app.

First need Python3. Then:

```
$ pip install praw
```

now run: (change out vars for your user/pass/id/secret)

```
$ python main.py $USERNAME $PASSWORD $CLIENT_ID $CLIENT_SECRET
```

There are many sellers, more than ever thought. Might want to run the program in a loop, every 30 min or so like this:

```
$ while true; do python main.py $USERNAME $PASSWORD $CLIENT_ID $CLIENT_SECRET; sleep 1800; done
```
