import os
from googleapiclient.discovery import build
import typer
import re
from datetime import timedelta
from dotenv import load_dotenv

app = typer.Typer()

yt = None


def gauth():
    global yt
    load_dotenv("./secrets/.env")
    yt = build("youtube", "v3", developerKey=os.environ["YT_API_KEY"])


@app.command()
def playtime(plid: str):
    """
    Get an aggregate of all the playtime of each video in a playlist

    :param plid: The id of the playlist. Can be obtained from the list query string of playlist urls

    :return: A runtime sum of every video in the list
    """

    gauth()

    h_pattern = re.compile(r"(\d+)H")
    m_pattern = re.compile(r"(\d+)M")
    s_pattern = re.compile(r"(\d+)S")

    runtime = 0

    npt = None
    while True:
        pl_req = yt.playlistItems().list(
            part="contentDetails",
            playlistId=plid,
            maxResults=30,
            pageToken=npt
        )
        pl_res = pl_req.execute()

        npt = pl_res.get("nextPageToken")

        vids = []
        for item in pl_res["items"]:
            vids.append(item["contentDetails"]["videoId"])

        vid_ids = ",".join(vids)

        vd_req = yt.videos().list(part="contentDetails", id=vid_ids)

        vd_res = vd_req.execute()

        for item in vd_res["items"]:
            duration = item["contentDetails"]["duration"]

            hrs = h_pattern.search(duration)
            mins = m_pattern.search(duration)
            secs = s_pattern.search(duration)

            h = int(hrs.group(1)) if hrs else 0
            m = int(mins.group(1)) if mins else 0
            s = int(secs.group(1)) if secs else 0

            seconds = timedelta(hours=h, minutes=m, seconds=s).total_seconds()

            runtime += seconds

        if not npt:
            break

    runtime = int(runtime)
    mins, secs = divmod(runtime, 60)
    hrs, mins = divmod(mins, 60)

    print(f"Total playtime is {hrs:02d}h:{mins:02d}m:{secs:02d}s")


@app.command()
def popular(plid: str, start: int = 1, end: int = -1):
    """
    Get a list of all links in a playlist sorted by view count

    :param plid: The id of the playlist. Can be obtained from the list query string of playlist urls

    :param start: Limit the number of displayed videos from a start position

    :param end: Limit the number of displayed videos by a cutoff end

    :return: View count sorted videos
    """

    gauth()

    pl = []

    npt = None
    while True:
        pl_req = yt.playlistItems().list(
            part="contentDetails",
            playlistId=plid,
            maxResults=30,
            pageToken=npt
        )
        pl_res = pl_req.execute()

        npt = pl_res.get("nextPageToken")

        vids = []
        for item in pl_res["items"]:
            vids.append(item["contentDetails"]["videoId"])

        vid_ids = ",".join(vids)

        vd_req = yt.videos().list(part="statistics", id=vid_ids)

        vd_res = vd_req.execute()

        for item in vd_res["items"]:
            link = f"https://www.youtube.com/watch?v={item['id']}"
            views = int(item["statistics"]["viewCount"])

            pl.append({"link": link, "views": views})

        pl.sort(key=lambda vid: vid["views"], reverse=True)

        if not npt:
            break

    if start > len(pl) or end > len(pl):
        print("start/end option values out of range")
        exit(1)

    for i, v in enumerate(pl[start-1:end]):
        print("{:d} -> {:s} \n     {:,d}".format(i+start, v['link'], v['views']))
        # print("{0: >42} {1:21}".format(v['link'], v['views']))


@app.command()
def init():

    fpath = "./secrets/.env"
    os.makedirs(os.path.dirname(fpath), exist_ok=True)
    with open(fpath, "w") as f:
        api_key = typer.prompt("What's your google youtube api key?")
        typer.echo(f"Initializing script with key: {api_key}")
        f.write(f"YT_API_KEY = {api_key}")
        typer.echo("Success. You can now use either the Popular or Playtime command")


if __name__ == '__main__':
    app()
