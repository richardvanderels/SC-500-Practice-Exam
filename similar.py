"""List cross-objective question pairs that look alike (TF-IDF cosine > 0.30). Review the top ones by hand."""
import json,glob,re,math
from collections import Counter
qs=[]
for f in sorted(glob.glob('data/[0-9]*.json')): qs+=json.load(open(f,encoding='utf-8'))
stop=set("the a an of to and or in for is that be by with on must should you which what your agent agents uses use each are it as this from not can when at its inc ltd company".split())
def toks(q):
    if q['type']=='dropdown': key=" ".join(t['options'][a] for t,a in zip(q['targets'],q['answer']))
    else: key=" ".join(q['choices'][i] for i in q['answer'])
    t=q['stem']+" "+key+" "+key
    return [w for w in re.findall(r"[a-z_][a-z0-9_.\-]+",t.lower()) if w not in stop and len(w)>2]
docs=[Counter(toks(q)) for q in qs]
df=Counter(w for d in docs for w in d)
N=len(qs)
vec=[]
for d in docs:
    v={w:c*math.log(N/df[w]) for w,c in d.items()}
    n=math.sqrt(sum(x*x for x in v.values())) or 1
    vec.append({w:x/n for w,x in v.items()})
pairs=[]
for i in range(N):
    for j in range(i+1,N):
        if qs[i]['obj'][:3]==qs[j]['obj'][:3] and qs[i]['obj']==qs[j]['obj']: continue
        a,b=vec[i],vec[j]
        s=sum(x*b.get(w,0) for w,x in a.items())
        if s>0.30: pairs.append((s,qs[i]['id'],qs[j]['id']))
for s,a,b in sorted(pairs,reverse=True)[:90]: print(f"{s:.2f} {a} {b}")
