import feedparser

d = feedparser.parse('htttp://b.hatena.ne.jp/hotentry/it.rss')

for entry in d.entries:
    print(entry.link, entry.title)
