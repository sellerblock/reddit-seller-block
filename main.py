import praw
import platform
import sys

USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]
CLIENT_ID = sys.argv[3]
CLIENT_SECRET = sys.argv[4]

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    username=USERNAME,
    password=PASSWORD,
    user_agent=f"{platform.system()} {platform.release()} {platform.version()}:{CLIENT_ID}:0 (by u/{USERNAME})",
    read_only=False,
)
blocked = {}


def seller(u):
    if u.name in blocked:
        return blocked[u.name]
    is_seller = False
    description = u.subreddit.public_description

    # A few redeemables, if they say they are not selling, we take their
    # word for it.
    #
    # TODO: I know of at least one false negative here since she wrote
    # "Don't message me, onlyfans at: blah"
    if "don't sell" in description or "not selling" in description or \
        "No O" in description or \
        "don't" in description.lower() and "onlyfans" in description.lower() or \
        "don't" in description.lower() and "sell" in description.lower() or \
            "don't" in description.lower() and "money" in description.lower():
        return False

    # Look for trigger words
    block_words = [
        "OF",
        "onlyfans",
        "Onlyfans",
        "OnlyFans",
        "𝐎𝐧𝐥𝐲𝐅𝐚𝐧𝐬",
        "ONLYFANS",
        "videos",  # rare to mention videos
        "OnlyF ans",
        "snap",
        "Snap",
        "SNAP",
        "sext",
        "Hutt",
        "hutt",
        "linktr.ee",
        "links",
        "fansly",
        "clips4sale",
    ]
    for word in block_words:
        is_seller = is_seller or word in description
        if is_seller:
            return True
    for u_sub in u.submissions.new():
        for word in block_words:
            is_seller = is_seller or word in u_sub.title or word in u_sub.url
            # or word in u_sub.subreddit.name # TODO: shit performance

            if is_seller:
                return True

    blocked[u.name] = is_seller
    return is_seller


def scan_submissions(listing, total_blocked):
    for sub in listing:
        try:
            author = sub.author
            desc = author.subreddit.public_description.replace("\n", " ")
            is_seller = seller(author)
            if is_seller:
                total_blocked += 1
            print(
                f"🟥 BLOCKED! total_blocked={total_blocked} user={author.name:20}description=\"{desc}\" " if is_seller else
                f"✅ OK       user={author.name:20} description=\"{desc}\"")
            if is_seller:
                author.block()
        except Exception as e:
            print(e)

    return total_blocked


total_blocked = 0
for multireddit in reddit.user.me().multireddits():
    listings = [multireddit.new(), multireddit.top()]
    for listing in listings:
        total_blocked = scan_submissions(listing, total_blocked)

listings = [reddit.front.new(), reddit.front.best(), reddit.front.top()]
for listing in listings:
    total_blocked = scan_submissions(listing, total_blocked)
