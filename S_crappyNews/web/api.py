import os
import yaml
import json
import bottle
import pymongo
import argparse
from ssl import CERT_NONE
from bson import json_util
from bottle import response

# Init bottle
app = bottle.Bottle()

# Load yaml config file
config = yaml.load(open(os.path.join(os.path.dirname(__file__), "config.yml")))

# Init mongodb
client = pymongo.MongoClient(config["mongo"]["uri"], ssl_cert_reqs=CERT_NONE)
db = client[config["mongo"]["db"]]


@app.route("/news")
def get_all():
    """
    Get all news in the collection
    :return: json => [{"url": "xxx", "body": "xxx", "title": "xxx"}]
    """
    news = [news for news in db.news.find()]

    response.content_type = "application/json"
    return json.dumps(news, default=json_util.default)


@app.route("/news/<keyword>")
def get_news(keyword):
    """
    Get news based on keyword searched
    :param keyword: String
    :return: json => [{"url": "xxx", "body": "xxx", "title": "xxx"}]
    """
    query = {"body": {"$regex": keyword, "$options": "i"}}
    news = [news for news in db.news.find(query)]

    response.content_type = "application/json"
    return json.dumps(news, default=json_util.default)


def main():
    """
    Start bottle web server
    """
    parser = argparse.ArgumentParser(description="Start web server")
    parser.add_argument("--host", help="Web server host address. (default: 127.0.0.1)")
    parser.add_argument("--port", help="Web server port. (default: 8080)")
    args = parser.parse_args()

    app.run(host="127.0.0.1" if not args.host else args.host, port="8080" if not args.port else args.port)


if __name__ == "__main__":
    main()
