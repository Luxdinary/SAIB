import json,urllib.request,os
names=list(json.load(open('thumb_prompts.json',encoding='utf-8')).keys())
jobs=dict(l.split() for l in open('jobs_thumbs.txt'))
for l in open('thumb_urls.txt'):
    i,ts=l.split(); n=names[int(i)]
    if os.path.exists(n+'.png'): continue
    urllib.request.urlretrieve(f"https://d8j0ntlcm91z4.cloudfront.net/user_3Ffs1RmQOHi0bbSM6jmwxmZG7oG/hf_20261102_{ts}_{jobs[i]}.png", n+'.png')
    print(n)
