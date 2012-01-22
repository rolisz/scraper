__author__ = 'Roland'
import argparse
import urllib.request
import urllib.parse
import re

parser = argparse.ArgumentParser(description = 'A simple Web Scraper for 50apps Challenge')
parser.add_argument('url',metavar = 'u',help ='The URL to start searching on')
parser.add_argument('depth',metavar = 'd', help = 'The depth to search in')
parser.add_argument('search', metavar = 's', help = 'The search term')

args = vars(parser.parse_args())


visited = set()
urls = set([('',args['url'].encode(),'')])

depth = 0
results = []
while urls and depth < int(args['depth']):
  for url in urls.copy():
    sUrl = urllib.parse.urljoin(args['url'],url[1].decode('utf-8'))
    if not sUrl in visited:
      visited.add(sUrl)
      try:
        f = urllib.request.urlopen(sUrl)
        site = f.read()
        if args['search'] in site.decode('utf-8'):
            results.append(sUrl)
        prog = re.compile(b'<a (.*?)href="([^"]+?)"(.*?)>')
        nUrls = prog.findall(site)
        urls.update(set(nUrls))
        urls.difference_update(visited)
        urls.remove(url)
      except Exception as e:
        print(e)
    else:
      urls.remove(url)
  depth += 1
print(results)
