import re
import nltk
import json
import gzip
from collections import defaultdict

porter = nltk.PorterStemmer()

del_non_letters = re.compile(ur'[^a-z ]')

persons = list(l.strip().decode('utf-8') for l in open('persons.txt'))

def norm_name(name):
    return frozenset(sorted(del_non_letters.sub(u'', porter.stem(w)) for w in nltk.word_tokenize(name)))
persons_norm = list(norm_name(n) for n in persons)

unique_names = set()
srt_persons_norm = sorted(persons_norm, key=lambda x : len(x), reverse=True)

for i, p in enumerate(srt_persons_norm):
    repeated = False
    for s in unique_names:
        if s > p:
            repeated = True
            break
    if not repeated:
        unique_names.add(p)


f = gzip.open('kaggle_f_n_t_sentences.txt.gz')
uuid = None
persons_dict = defaultdict(float)
uuid_features = []

all_persons_words = set()
for p in unique_names:
    all_persons_words.update(p)

unique_names_cache = {}
def get_unique_name(name):
    if name in unique_names_cache:
        return unique_names_cache.get(name)
    n_name = norm_name(name)
    for w in n_name:
        if w not in all_persons_words:
            return None
    for s in unique_names:
        if s >= n_name:
            unique_names_cache[name] = s
            return s
    return None

uuid_pos, uuid_neg = 0.0, 0.0
for i, l in enumerate(f):
    cur_uuid, sent_type, sent_num, sent, names, sntm = l.strip('\n').split('\t')
    sntm = json.loads(sntm)
    if cur_uuid != uuid:
        if uuid:
            print("\t".join((uuid, str(uuid_pos), str(uuid_neg), json.dumps(dict((' '.join(k), v) for k, v in persons_dict.iteritems())))))
            # uuid_features.append((uuid, uuid_pos, uuid_neg, persons_dict))
            uuid_pos, uuid_neg = 0.0, 0.0
            persons_dict = defaultdict(float)
        uuid = cur_uuid
    uuid_pos += sntm['pos']
    uuid_neg += sntm['neg']
    for nm, tp in json.loads(names):
        if tp == u"PERSON":
            uname = get_unique_name(nm)
            if uname:
                persons_dict[uname] += sntm['pos'] - sntm['neg']
if uuid:
    print("\t".join((uuid, str(uuid_pos), str(uuid_neg), json.dumps(dict((' '.join(k), v) for k, v in persons_dict.iteritems())))))
    # uuid_features.append((uuid_pos, uuid_neg, persons_dict))
