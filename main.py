import os
from dotenv import load_dotenv


def init():
    load_dotenv("./secrets/.env")


def print_hi():
    print(os.environ["YT_API_KEY"])


if __name__ == '__main__':
    init()
    print_hi()
