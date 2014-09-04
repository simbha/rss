#!/usr/bin/env python

# Written by Gem Newman. This work is licensed under a Creative Commons         
# Attribution-NonCommercial-ShareAlike 3.0 Unported License.                    


import requests, re, datetime, os.path, dateutil.parser, PyRSS2Gen
from bs4 import BeautifulSoup


RSS_DIR = os.path.dirname(os.path.realpath(__file__))
RSS_FILE = "WritingExcusesRSS.xml"
RSS_IMAGE = "http://www.writingexcuses.com/wp-content/uploads/2014/04/"       \
            "WX-banner.jpg"
RSS_PATH = os.path.join(RSS_DIR, RSS_FILE)
RSS_LINK = "http://savage.startleddisbelief.com/rss/" + RSS_FILE
RSS_TITLE = "Writing Excuses Archive"
RSS_WEBSITE = "http://www.writingescuses.com/"
RSS_DESCRIPTION = "Fifteen minutes long, because you're in a hurry, and we're"\
                  " not that smart."
RSS_TYPE = "audio/mpeg"

# Include all ways of representing nonbreaking space characters.
DATE_FORMAT = r"^\d+( |&nbsp;|\xc2?\xa0)\w+( |&nbsp;|\xc2?\xa0)\d+"
TIME_FORMAT = r"\d+:\d+"

RETRIES = 10
TIMEOUT = 5     # Timeout value for requests, in seconds.


def init():
    items = find_items()
    rss = create_rss(
        title=RSS_TITLE, website=RSS_WEBSITE, image=RSS_IMAGE,
        description=RSS_DESCRIPTION, items=items
    )
    rss.write_xml(open(RSS_PATH, "w"))


def find_items():
    items = []

    for p in page_generator():
        print "Retrieving episode information from {}...".format(p)

        response = requests.get(p, timeout=TIMEOUT)
        soup = BeautifulSoup(response.text.encode("utf8"))

        for e in soup.find_all("ul", class_="epinfo"):
            item = {}

            try:
                notes_tag = e.find("a")
                item["title"] = " ".join([s for s in notes_tag.strings])
                item["description"] = ""
                item["guid"] = notes_tag.get("href")
                item["file"] = e.find("a", text="Download").get("href")

                date_tag = e.find("li", text=re.compile(DATE_FORMAT))
                if date_tag:
                    d = date_tag.string.replace(u"\xa0", " ")
                    item["date"] = dateutil.parser.parse(d)
                else:
                    print "No date tag found: {}".format(e)
                    item["date"] = None

                time_tag = e.find("li", text=re.compile(TIME_FORMAT))
                if time_tag:
                    t = time_tag.string.split(":")
                    item["length"] = (int(t[0]) * 60 + int(t[1])) * 1000
                else:
                    item["length"] = None

                items.append(item)

            except Exception as e:
                print "Error: {}".format(repr(e))
                print item
                print "Skipping this element."

    return items


def create_rss(title, website, description, items, image):
    print "Creating RSS file..."

    rss = PyRSS2Gen.RSS2(
        title=title,
        link=website,
        description=description,
        image=PyRSS2Gen.Image(url=image, title=title, link=website),
        lastBuildDate=datetime.datetime.now(),

        items = [PyRSS2Gen.RSSItem(
            title = i["title"],
            link = RSS_LINK,
            description = i["description"],
            guid = PyRSS2Gen.Guid(i["guid"]),
            enclosure = PyRSS2Gen.Enclosure(i["file"], i["length"], RSS_TYPE),
            pubDate = i["date"],
        ) for i in items]
    )

    return rss


def page_generator():
    r = requests.get("http://www.writingexcuses.com", timeout=TIMEOUT)
    m = re.findall("Season (\d+)", r.text)

    if not m:
        print "Unable to determine current season. Assuming 20. Why not?"
        current_season = 20
    else:
        current_season = int(m[0])

    for i in range(1, current_season + 1):
        if i < 8:
            yield("http://www.writingexcuses.com/season{:03d}/".format(i))
        else:
            yield("http://www.writingexcuses.com/category/season/season-{}/"
                  .format(i))


if __name__ == "__main__":
    init()
#    if os.path.isfile(RSS_PATH):
#        update()
#    else:
#        init()

