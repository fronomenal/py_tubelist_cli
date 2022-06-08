import os
from googleapiclient.discovery import build
import typer
import re
from datetime import timedelta
from dotenv import load_dotenv

app = typer.Typer()

load_dotenv("./secrets/.env")
yt = build("youtube", "v3", developerKey=os.environ["YT_API_KEY"])


def main():

    h_pattern = re.compile(r"(\d+)H")
    m_pattern = re.compile(r"(\d+)M")
    s_pattern = re.compile(r"(\d+)S")

    runtime = 0

    npt = None
    while True:
        pl_req = yt.playlistItems().list(
            part="contentDetails",
            playlistId="PLNF8K9Ddz0kKfujG6blfAxngYh_C66C_q",
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

    print(f"Total playtime is {hrs}:{mins}:{secs}")
    # app()


@app.command()
def playtime():
    pass


@app.command()
def popular():
    pass


if __name__ == '__main__':
    main()
