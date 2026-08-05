#!/usr/bin/env python3
import json
import sys
from datetime import datetime, timezone
from urllib.request import Request, urlopen

URLS = [
    'https://sp12.iidx.app/api/v1/sheets',
    'https://sp12.iidx.app/api/v1/sheets/list',
    'https://api-sp12.iidx.app/sheets',
]

def get_json(url):
    req = Request(url, headers={
        'User-Agent': 'farewell2236/naide GitHub Actions',
        'Accept': 'application/json',
    })
    with urlopen(req, timeout=30) as r:
        if r.status != 200:
            raise RuntimeError(f'HTTP {r.status}')
        return json.load(r)

def pick(obj, names):
    for name in names:
        if isinstance(obj, dict) and obj.get(name) is not None:
            return obj[name]
    return None

def clean(value):
    return ' '.join(str(value or '').split())

def normalize_rank(value):
    s = clean(value)
    if not s or s in ('null', '-'):
        return '未分類'
    # APIの文字列は原則そのまま利用
    return s.replace('難易度未定', '未定')

def transform(raw):
    if isinstance(raw, list):
        arr = raw
    elif isinstance(raw, dict):
        arr = raw.get('sheets') or raw.get('data') or raw.get('songs') or []
    else:
        arr = []

    rows = []
    seen = set()
    for x in arr:
        if not isinstance(x, dict):
            continue
        title = clean(pick(x, ['title', 'music_title', 'name', 'song_name']))
        if not title:
            continue
        ver = clean(pick(x, ['version', 'ver', 'series'])) or '-'
        normal = normalize_rank(pick(x, ['n_clear_string', 'normal_string', 'normal', 'normal_rank']))
        hard = normalize_rank(pick(x, ['hard_string', 'hard', 'hard_rank']))
        key = (title, ver)
        if key in seen:
            continue
        seen.add(key)
        rows.append({
            'title': title,
            'chart': 'SP☆12',
            'ver': ver,
            'normal': normal,
            'hard': hard,
            'level': 12,
            'source': 'sp12.iidx.app',
        })
    return rows

def main():
    errors = []
    for url in URLS:
        try:
            rows = transform(get_json(url))
            if len(rows) < 100:
                raise RuntimeError(f'取得件数不足: {len(rows)}')
            out = {
                'updatedAt': datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds'),
                'sourceUrl': url,
                'data': rows,
            }
            with open('songs.json', 'w', encoding='utf-8') as f:
                json.dump(out, f, ensure_ascii=False, indent=2)
                f.write('\n')
            print(f'取得成功: {url} / {len(rows)}譜面')
            return
        except Exception as e:
            errors.append(f'{url}: {e}')
    print('\n'.join(errors), file=sys.stderr)
    raise SystemExit(1)

if __name__ == '__main__':
    main()
