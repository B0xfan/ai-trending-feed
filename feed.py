#!/usr/bin/env python3
"""Build the AI Trending repo RSS feed from items.json.

Usage: python3 feed.py  (reads items.json in this dir, writes feed.xml)
Item fields: repo, link, date (YYYY-MM-DD), stars, description, usage.
Stars are a snapshot from the day the item was added; RSS readers cache
items, so counts are not refreshed on older entries.
"""
import html
import json
import os
from datetime import datetime, timezone
from email.utils import format_datetime

HERE = os.path.dirname(os.path.abspath(__file__))


def rfc822(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return format_datetime(dt)


def main():
    with open(os.path.join(HERE, "items.json")) as f:
        items = json.load(f)
    items = sorted(items, key=lambda i: i["date"], reverse=True)

    out = []
    out.append('<?xml version="1.0" encoding="UTF-8"?>')
    out.append('<rss version="2.0">')
    out.append("  <channel>")
    out.append("    <title>AI Trending</title>")
    out.append("    <link>https://github.com/trending</link>")
    out.append(
        "    <description>One item per repo from the daily AI Trending report: "
        "what it does, how many stars it has, and how you would actually use it.</description>"
    )
    out.append("    <language>en</language>")
    out.append(
        "    <lastBuildDate>%s</lastBuildDate>"
        % format_datetime(datetime.now(timezone.utc))
    )
    for it in items:
        body = (
            "<p>%s</p>\n<p><strong>Stars:</strong> %s</p>\n"
            "<p><strong>Practical use:</strong> %s</p>"
            % (
                html.escape(it["description"]),
                html.escape(str(it["stars"])),
                html.escape(it["usage"]),
            )
        )
        out.append("    <item>")
        out.append("      <title>%s</title>" % html.escape(it["repo"]))
        out.append("      <link>%s</link>" % html.escape(it["link"]))
        out.append(
            "      <guid isPermaLink=\"true\">%s</guid>" % html.escape(it["link"])
        )
        out.append("      <pubDate>%s</pubDate>" % rfc822(it["date"]))
        out.append("      <description><![CDATA[%s]]></description>" % body)
        out.append("    </item>")
    out.append("  </channel>")
    out.append("</rss>")
    with open(os.path.join(HERE, "feed.xml"), "w") as f:
        f.write("\n".join(out) + "\n")
    print(f"wrote feed.xml with {len(items)} items")


if __name__ == "__main__":
    main()
