def qc(l:list):
    m=1
    r=[]
    for i in l[:-1] :
        for j in l[m:]:
            if not (isin(i) and isin(j) and iseq(i,j)) :
                r.append(i)
    r.append(l[len(l)])
    return r
def isin(d:dict) :
    "检查信息"
    if 'artist' in d and 'album' in d :
        return True
    else :
        return False
def iseq(d:dict,d2:dict):
    "去重"
    if d['artist']==d2['artist'] and d['title']==d2['title'] and d['album']==d2['album']:
        return True
    else :
        return False