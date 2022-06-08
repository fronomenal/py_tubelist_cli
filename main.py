import os
from googleapiclient.discovery import build
from dotenv import load_dotenv


def init():
    load_dotenv("./secrets/.env")


def main():
    yt = build("youtube", "v3", developerKey=os.environ["YT_API_KEY"])

    req = yt.channels().list(part="statistics", id="UCNYi_zGmR519r5gYdOKLTjQ")

    res = req.execute()

    print(res["items"][0]["statistics"])


if __name__ == '__main__':
    init()
    main()
