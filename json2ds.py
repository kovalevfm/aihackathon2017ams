#!/usr/bin/env python

import json
import os
import sys


header = [
    "uuid",
    "ord_in_thread",
    "author",
    "published",
    "title",
    "text",
    "language",
    "crawled",
    "site_url",
    "country",
    "domain_rank",
    "thread_title",
    "spam_score",
    "main_img_url",
    "replies_count",
    "participants_count",
    "likes",
    "comments",
    "shares",
    "type",
]


def get_value(d, k):
    if k == 'site_url':
        return d['url']
    elif k == 'country':
        return d['thread']['country']
    elif k == 'domain_rank':
        return d['thread']['domain_rank']
    elif k == 'thread_title':
        return d['thread']['title'].replace('"', '').replace('\n', ' ')
    elif k == 'spam_score':
        return d['thread']['spam_score']
    elif k == 'main_img_url':
        return d['thread']['main_image']
    elif k == 'replies_count':
        return d['thread']['replies_count']
    elif k == 'participants_count':
        return d['thread']['participants_count']
    elif k == 'likes':
        return d['social']['facebook']['likes']
    elif k == 'comments':
        return d['social']['facebook']['comments']
    elif k == 'shares':
        return d['social']['facebook']['shares']
    elif k == 'type':
        return 'ok'
    elif k == 'text':
        return d[k].replace('"', '').replace('\n', ' ')
    elif k == 'title':
        return d[k].replace('"', '').replace('\n', ' ')
    else:
        return d[k]


def main():

    dirname = sys.argv[1]
    interesting_persons = []
    with open('persons.txt') as ps:
        interesting_persons = set(p.strip() for p in ps)
    sys.stdout.write(','.join(header) + '\n')
    idx = 0
    # files = ['news/news_0000058.json', 'news/news_0000061.json', 'news/news_0000063.json', 'news/news_0000067.json']
    # for _, __, files in os.walk(dirname):
    for _, __, files in os.walk(dirname):
        for f in files:
            if f.find('json') == -1:
                continue
            with open(os.path.join(_, f)) as input:
                # with open(f) as input:
                try:
                    data = json.loads(input.read().decode('utf-8'))
                except:
                    continue
                persons_emotions = data['entities']['persons']
                if not persons_emotions:
                    continue
                persons = set(p['name'] for p in persons_emotions)
                matched = persons & interesting_persons
                if not matched:
                    continue
                idx += 1
                # sys.stderr.write('{}\t{}\n'.format(idx, f))
                fields = [get_value(data, k) for k in header]
                sys.stdout.write((u','.join(u'"{}"'.format(val) for val in fields) + u'\n').encode('utf-8'))
                # if idx == 100:
                #     break

if __name__ == '__main__':
    main()
