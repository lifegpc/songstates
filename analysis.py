import sys
import os
import XMLParser
import json
import time
import xlwt
import dataqc
import time
h="""useage:
\tanalysis.py [-h] [-a] [-y <year>|all] [-ya] [-m <year><month>|all]
 [-ym] [-q] [-hid] [-hp] [-p] [-dp] <inputfile> <outputfile>
choice:
\t-h\t显示帮助
\t-a\t分析所有时间的数据
\t-y\t分析指定年份的数据
\t\t可以输入多个年份，中间用","隔开
\t\t例如：2019,2020,2021
\t\t可以用"all"选择所有存在的年份
\t-ya\t相当于"-y all"
\t-m\t分析指定年月的数据
\t\t可以输入多个年月，中间用","隔开
\t\t例如：201902,201905,202001
\t\t可以用"all"选择所有存在的年月
\t-ma\t相当于"-m all"
\t-q\t歌曲去重
\t-hid\t分析每日听歌时间时输出详细信息
\t-hp\t每日听歌时间按播放时间降序（详细信息不受此影响）
\t-p\t计算播放时间百分比
\t-dp\t发行年份听歌时间按播放时间降序
inputfile:支持XML和JSON文件
outputfile:输出文件夹名称
"""
def main(filen:str,filen2:str,settings:dict) :
    try :
        re=XMLParser.loadXML(filen)
    except:
        f=open(filen2,'r',encoding='utf8')
        re=json.load(f)
        f.close()
    if 'q' in settings :
        re=dataqc.qc(re)
    if os.path.exists(filen2) :
        removedir(filen2)
    os.mkdir(filen2)
    def writexls(fn:str,settings:dict,re:list):
        w=xlwt.Workbook(encoding='utf8')
        t:xlwt.Worksheet=w.add_sheet('每首歌听歌时间')
        t.set_panes_frozen('1')
        t.set_vert_split_pos(1)
        t.set_horz_split_pos(1)
        ti=['排名','播放时间(s)','播放时间','占比','播放次数','标题','艺术家','专辑','轨道艺术家','专辑艺术家','年份','光盘编号','轨道编号','编码','编码扩展','扩展名','比特率','采样频率','声道数','长度','长度(s)','上次播放']
        ti2=['playcount','title','artist','album','trackartist','albumartist','date','discnumber','tracknumber','codec','codecprofile','ext','bitrate','samplerate','channels','length','lengthseconds','lastplayed']
        ti3=[0.35,0.9,1,0.7,0.7,2.8,2,3.6,1,2,0.4,0.7,0.7,0.5,0.7,0.5,0.5,0.7,0.5,0.5,0.7,1.5]#宽度
        if not 'p' in settings :
            ti=ti[:3]+ti[4:]
            ti3=ti3[:3]+ti3[4:]
        k=0
        for i in ti:
            t.write(0,k,i)
            rr:xlwt.Column=t.col(k)
            rr.width=int(rr.width*ti3[k])
            k=k+1
        if 'p' in settings:
            s=xlwt.XFStyle()
            s.num_format_str='0.00%'
        r=re
        sort(r,'playtime')
        k=1
        tt=0
        tk=1
        for i in r :
            if i['playtime']!=tt :
                tt=i['playtime']
                tk=k
            t.write(k,0,tk)
            t.write(k,1,i['playtime'])
            t.write(k,2,getlengthstr(i['playtime']))
            n=3
            if 'p' in settings :
                t.write(k,3,xlwt.Formula('B%s/SUM(B2:B%s)'%(k+1,len(r)+1)),s)
                n=4
            for j in ti2 :
                if j in i :
                    t.write(k,n,i[j])
                n=n+1
            k=k+1
        t:xlwt.Worksheet=w.add_sheet('艺术家听歌时间')
        t.set_panes_frozen('1')
        t.set_vert_split_pos(1)
        t.set_horz_split_pos(1)
        ti=['排名','播放时间(s)','播放时间','占比','艺术家']
        ti3=[0.35,0.9,1,0.7,2]
        if not 'p' in settings :
            ti=ti[:3]+ti[4:]
            ti3=ti3[:3]+ti3[4:]
        k=0
        for i in ti :
            t.write(0,k,i)
            rr:xlwt.Column=t.col(k)
            rr.width=int(rr.width*ti3[k])
            k=k+1
        r=getartistplaytimelist(re)
        sort(r,'playtime')
        k=1
        tt=0
        tk=1
        for i in r :
            if i['playtime']!=tt :
                tt=i['playtime']
                tk=k
            t.write(k,0,tk)
            t.write(k,1,i['playtime'])
            t.write(k,2,getlengthstr(i['playtime']))
            if 'p' in settings :
                t.write(k,3,xlwt.Formula('B%s/SUM(B2:B%s)'%(k+1,len(r)+1)),s)
                t.write(k,4,i['artist'])
            else :
                t.write(k,3,i['artist'])
            k=k+1
        t:xlwt.Worksheet=w.add_sheet('专辑听歌时间')
        t.set_panes_frozen('1')
        t.set_vert_split_pos(1)
        t.set_horz_split_pos(1)
        ti=['排名','播放时间(s)','播放时间','占比','专辑','专辑艺术家']
        ti3=[0.35,0.9,1,0.7,3.6,2]
        if not 'p' in settings :
            ti=ti[:3]+ti[4:]
            ti3=ti3[:3]+ti3[4:]
        k=0
        for i in ti :
            t.write(0,k,i)
            rr:xlwt.Column=t.col(k)
            rr.width=int(rr.width*ti3[k])
            k=k+1
        r=getalbumplaytimelist(re)
        sort(r,'playtime')
        k=1
        tt=0
        tk=1
        for i in r :
            if i['playtime']!=tt :
                tt=i['playtime']
                tk=k
            t.write(k,0,tk)
            t.write(k,1,i['playtime'])
            t.write(k,2,getlengthstr(i['playtime']))
            if 'p' in settings :
                t.write(k,3,xlwt.Formula('B%s/SUM(B2:B%s)'%(k+1,len(r)+1)),s)
                t.write(k,4,i['album'])
                t.write(k,5,i['albumartist'])
            else :
                t.write(k,3,i['album'])
                t.write(k,4,i['albumartist'])
            k=k+1
        t:xlwt.Worksheet=w.add_sheet('专辑-艺术家听歌时间')
        t.set_panes_frozen('1')
        t.set_vert_split_pos(1)
        t.set_horz_split_pos(1)
        ti=['排名','播放时间(s)','播放时间','占比','艺术家','专辑','专辑艺术家']
        ti3=[0.35,0.9,1,0.7,2,3.6,2]
        if not 'p' in settings :
            ti=ti[:3]+ti[4:]
            ti3=ti3[:3]+ti3[4:]
        k=0
        for i in ti :
            t.write(0,k,i)
            rr:xlwt.Column=t.col(k)
            rr.width=int(rr.width*ti3[k])
            k=k+1
        r=getalbumartistplaytimelist(re)
        sort(r,'playtime')
        k=1
        tt=0
        tk=1
        for i in r :
            if i['playtime']!=tt :
                tt=i['playtime']
                tk=k
            t.write(k,0,tk)
            t.write(k,1,i['playtime'])
            t.write(k,2,getlengthstr(i['playtime']))
            if 'p' in settings :
                t.write(k,3,xlwt.Formula('B%s/SUM(B2:B%s)'%(k+1,len(r)+1)),s)
                t.write(k,4,i['artist'])
                t.write(k,5,i['album'])
                t.write(k,6,i['albumartist'])
            else :
                t.write(k,3,i['artist'])
                t.write(k,4,i['album'])
                t.write(k,5,i['albumartist'])
            k=k+1
        if 'hid' in settings :
            r=geteverydayplaytimelist(re,True)
        else :
            r=geteverydayplaytimelist(re)
        if 'hp' in settings :
            sort(r['r'],'playtime')
        t:xlwt.Worksheet=w.add_sheet('每日听歌时间')
        t.set_panes_frozen('1')
        t.set_vert_split_pos(1)
        t.set_horz_split_pos(1)
        ti=['序号','日期','播放时间(s)','播放时间','占比']
        ti3=[0.35,1.5,0.9,1,0.7]
        if not 'p' in settings :
            ti=ti[:-1]
            ti3=ti3[:-1]
        k=0
        for i in ti :
            t.write(0,k,i)
            rr:xlwt.Column=t.col(k)
            rr.width=int(rr.width*ti3[k])
            k=k+1
        k=1
        for i in r['r'] :
            t.write(k,0,k)
            t.write(k,1,i['timestr'])
            t.write(k,2,i['playtime'])
            t.write(k,3,getlengthstr(i['playtime']))
            if 'p' in settings :
                t.write(k,4,xlwt.Formula('C%s/SUM(C2:C%s)'%(k+1,len(r['r'])+1)),s)
            k=k+1
        if 'hid' in settings :
            if 'hp' in settings :
                sort(r['r'],'time',False)
            t:xlwt.Worksheet=w.add_sheet('每日听歌时间(详细记录)')
            t.set_panes_frozen('1')
            t.set_vert_split_pos(1)
            t.set_horz_split_pos(1)
            ti=['序号','播放时间','播放次数','标题','艺术家','专辑','轨道艺术家','专辑艺术家','年份','光盘编号','轨道编号','编码','编码扩展','扩展名','比特率','采样频率','声道数','长度','长度(s)']
            ti2=['playcount','title','artist','album','trackartist','albumartist','date','discnumber','tracknumber','codec','codecprofile','ext','bitrate','samplerate','channels','length','lengthseconds']
            ti3=[0.5,1.5,0.7,2.8,2,3.6,1,2,0.4,0.7,0.7,0.5,0.7,0.5,0.5,0.7,0.5,0.5,0.7]
            k=0
            for i in ti :
                t.write(0,k,i)
                rr:xlwt.Column=t.col(k)
                rr.width=int(rr.width*ti3[k])
                k=k+1
            k=1
            for i in r['r']:
                for j in r['d'][i['timestr']]:
                    t.write(k,0,k)
                    t.write(k,1,j['ts'])
                    n=2
                    for m in ti2:
                        if m in re[j['i']] :
                            t.write(k,n,re[j['i']][m])
                        n=n+1
                    k=k+1
        t:xlwt.Worksheet=w.add_sheet('发行年份听歌时间')
        t.set_panes_frozen('1')
        t.set_vert_split_pos(1)
        t.set_horz_split_pos(1)
        ti=['序号','年份','播放时间(s)','播放时间','占比']
        ti3=[0.35,0.4,0.9,1,0.7]
        if not 'p' in settings :
            ti=ti[:-1]
            ti3=ti3[:-1]
        k=0
        for i in ti :
            t.write(0,k,i)
            rr:xlwt.Column=t.col(k)
            rr.width=int(rr.width*ti3[k])
            k=k+1
        r=getdateplaytimelist(re)
        if 'dp' in settings :
            sort(r,'playtime')
        else :
            sort(r,'date',False)
        k=1
        for i in r :
            t.write(k,0,k)
            t.write(k,1,i['date'])
            t.write(k,2,i['playtime'])
            t.write(k,3,getlengthstr(i['playtime']))
            if 'p' in settings :
                t.write(k,4,xlwt.Formula('C%s/SUM(C2:C%s)'%(k+1,len(r)+1)),s)
            k=k+1
        w.save(fn)
    getlength(re)
    if 'a' in settings:
        writexls("%s\\all.xls"%(filen2),settings,re)
    if 'y' in settings and 'm' in settings and settings['y']=='all' and settings['m']=='all' :
        temp=autogetyearormonth(re,True,True)
        settings['y']=temp['y']
        settings['m']=temp['m']
    elif 'y' in settings and settings['y']=='all' :
        temp=autogetyearormonth(re)
        settings['y']=temp['y']
    elif 'm' in settings and settings['m']=='all' :
        temp=autogetyearormonth(re,False,True)
        settings['m']=temp['m']
    elif 'y' in settings :
        sorttimestruct(settings['y'],False)
    elif 'm' in settings :
        sorttimestruct(settings['m'],False)
    if 'y' in settings :
        for i in settings['y'] :
            writexls('%s\\%s.xls'%(filen2,time.strftime('%Y',i)),settings,gettimelist(re,i))
    if 'm' in settings :
        for i in settings['m'] :
            writexls('%s\\%s.xls'%(filen2,time.strftime('%Y%m',i)),settings,gettimelist(re,i,False,True))
def getchoice(settings:dict,i:str):
    "解析是否为选项，不是选项返回0，是选项但解析失败返回1"
    if len(i)>=1 and i[0]=='-':
        if i=='-a' :
            settings['a']=True
            settings['ok']=True
            return 2
        elif i=='-q' :
            settings['q']=True
            return 2
        elif i=='-hid' :
            settings['hid']=True
            return 2
        elif i=='-p' :
            settings['p']=True
            return 2
        elif i=='-hp' :
            settings['hp']=True
            return 2
        elif i=='-dp' :
            settings['dp']=True
            return 2
        elif i=='-y' :
            return 3
        elif i=='-m' :
            return 4
        elif i=='-ya' :
            if 'y' in settings :
                if settings['y']!='all' :
                    print('-y 选项出现混用all和年份')
                    print(h)
                    exit(-1)
            else :
                settings['y']='all'
                settings['ok']=True
            return 2
        elif i=='-ma' :
            if 'm' in settings :
                if settings['m']!='all' :
                    print('-m 选项出现混用all和年月')
                    print(h)
                    exit(-1)
            else :
                settings['m']='all'
                settings['ok']=True
            return 2
        else :
            return 1
    else:
        return 0
def removedir(f:str) :
    "删除文件夹"
    fl=os.listdir(f)
    for i in fl :
        i='%s\\%s'%(f,i)
        if os.path.isdir(i) :
            removedir(i)
        else:
            os.remove(i)
    try :
        os.removedirs(f)
    except :
        pass
def getlength(l:list) :
    "获得每首歌的播放时间（秒）"
    for i in l:
        i['playtime']=i['lengthseconds']*i['playcount']
def sort(l:list,k:str,p:bool=True):
    "根据k的关键字排序,false升序,true降序"
    m=1
    while m<len(l) :
        n=m
        while n<len(l) :
            if p and l[m-1][k]<l[n][k] :
                t=l[m-1]
                l[m-1]=l[n]
                l[n]=t
            if not p and l[m-1][k]>l[n][k] :
                t=l[m-1]
                l[m-1]=l[n]
                l[n]=t
            n=n+1
        m=m+1
def getlengthstr(i:int) :
    "获取长度 day h m s"
    if i>=(3600*24) :
        return "%s天 %.2d:%.2d:%.2d"%(i//(3600*24),(i%(3600*24))//3600,(i%3600)//60,i%60)
    elif i>=3600 :
        return "%.2d:%.2d:%.2d"%(i//3600,(i%3600)//60,i%60)
    elif i>=0 :
        return "%.2d:%.2d"%(i//60,i%60)
    else :
        return ""
def getartistplaytimelist(l:list):
    "获取艺术家播放时间列表"
    r=[]
    def isin(d:dict,r:list) :
        "判断d是否存在于r"
        k=0
        for i in r:
            if d['artist']==i['artist'] :
                return k
            k=k+1
        return -1
    for i in l :
        if 'artist' in i :
            k=isin(i,r)
            if k >-1:
                r[k]['playtime']=r[k]['playtime']+i['playtime']
            else :
                r.append({'artist':i['artist'],'playtime':i['playtime']})
    return r
def getalbumplaytimelist(l:list) :
    "获取专辑播放时间列表"
    r=[]
    def isin(d:dict,r:list) :
        "判断d是否存在于r"
        k=0
        for i in r:
            if d['album']==i['album'] and d['albumartist']==i['albumartist'] :
                return k
            k=k+1
        return -1
    for i in l :
        if 'album' in i and 'albumartist' in i :
            k=isin(i,r)
            if k >-1:
                r[k]['playtime']=r[k]['playtime']+i['playtime']
            else :
                r.append({'album':i['album'],'playtime':i['playtime'],'albumartist':i['albumartist']})
    return r
def getalbumartistplaytimelist(l:list):
    "获取专辑-艺术家播放时间列表"
    r=[]
    def isin(d:dict,r:list) :
        "判断d是否存在于r"
        k=0
        for i in r:
            if d['album']==i['album'] and d['albumartist']==i['albumartist'] and d['artist']==i['artist'] :
                return k
            k=k+1
        return -1
    for i in l :
        if 'album' in i and 'albumartist' in i and 'artist' in i :
            k=isin(i,r)
            if k >-1:
                r[k]['playtime']=r[k]['playtime']+i['playtime']
            else :
                r.append({'album':i['album'],'playtime':i['playtime'],'albumartist':i['albumartist'],'artist':i['artist']})
    return r
def geteverydayplaytimelist(l:list,s:bool=False) :
    "获取每天的播放时间，s为True返回详细信息"
    d={}
    r=[]
    def getstr(t:str):
        return time.strftime('%Y-%m-%d',time.strptime(t,'%Y-%m-%d %H:%M:%S'))
    def isin(t:str,r:list):
        ts=getstr(t)
        k=0
        for i in r :
            if i['timestr']==ts :
                return k
            k=k+1
        return -1
    m=0
    for i in l :
        if 'playedtimes' in i:
            for j in i['playedtimes'] :
                k=isin(j,r)
                if k>-1 :
                    r[k]['playtime']=r[k]['playtime']+i['lengthseconds']
                    if s:
                        d[getstr(j)].append({'i':m,'t':time.strptime(j,'%Y-%m-%d %H:%M:%S'),'ts':j})
                else :
                    r.append({'playtime':i['lengthseconds'],'time':time.strptime(getstr(j),'%Y-%m-%d'),'timestr':getstr(j)})
                    if s:
                        d[getstr(j)]=[{'i':m,'t':time.strptime(j,'%Y-%m-%d %H:%M:%S'),'ts':j}]
        m=m+1
    sort(r,'time',False)
    if s:
        for i in r:
            sort(d[i['timestr']],'t',False)
    return {'r':r,'d':d}
def getdateplaytimelist(l:list) :
    "获取发行年份的播放时间"
    r=[]
    def isin(d:dict,r:list):
        k=0
        for i in r:
            if d['date']==i['date'] :
                return k
            k=k+1
        return -1
    for i in l:
        if 'date' in i:
            k=isin(i,r)
            if k>-1 :
                r[k]['playtime']=r[k]['playtime']+i['playtime']
            else :
                r.append({'date':i['date'],'playtime':i['playtime']})
    return r
def getyearormonth(s:str,settings:dict,b:str='y'):
    "获取year或month的参数，y year,m month"
    def getc(s:str,b:str='y') -> list :
        "获取年份参数"
        r=s.split(',')
        l=[]
        for i in r :
            if b=='y':
                t=time.strptime(i,'%Y')
            else :
                t=time.strptime(i,'%Y%m')
            l.append(t)
        return l
    def merge(l:list,l2:list) -> list:
        "将两个列表去重合并"
        r=[]
        for i in l+l2 :
            o=True
            for j in r :
                if i==j :
                    o=False
                    break
            if o:
                r.append(i)
        return r
    if b in settings :
        if settings[b]=='all' :
            if s!='all' :
                return -1
        else :
            if s=='all' :
                return -1
            else :
                c=getc(s,b)
                settings[b]=merge(c,settings[b])
    else :
        if s=='all' :
            settings[b]='all'
        else :
            settings[b]=getc(s,b)
    settings['ok']=True
    return 0
def autogetyearormonth(l:list,y:bool=True,m:bool=False)->dict:
    "获取所有时间段"
    yr=[]
    mr=[]
    def getyear(s:str) -> time.struct_time:
        return time.strptime(time.strftime('%Y',time.strptime(s,"%Y-%m-%d %H:%M:%S")),'%Y')
    def getmonth(s:str) -> time.struct_time:
        return time.strptime(time.strftime('%Y%m',time.strptime(s,'%Y-%m-%d %H:%M:%S')),'%Y%m')
    def isin(t:time.struct_time,l:list) -> bool :
        for i in l :
            if i==t :
                return False
        return True
    if y or m :
        for i in l :
            if 'playedtimes' in i :
                for j in i['playedtimes'] :
                    if y and isin(getyear(j),yr) :
                        yr.append(getyear(j))
                    if m and isin(getmonth(j),mr) :
                        mr.append(getmonth(j))
    if y :
        sorttimestruct(yr,False)
    if m :
        sorttimestruct(mr,False)
    return {'y':yr,'m':mr}
def sorttimestruct(l:list,b:bool=True):
    "对时间结构元组进行排序,True降序,False升序"
    t=[]
    for i in l:
        t.append({'s':i,'t':time.mktime(i)})
    sort(t,'t',b)
    k=0
    for i in t :
        l[k]=i['s']
        k=k+1
def gettimelist(l:list,t:time.struct_time,y:bool=True,m:bool=False) -> list :
    "根据时间结构元组获得相应时间内歌曲数据"
    r=[]
    def getyear(s:str) -> time.struct_time:
        return time.strptime(time.strftime('%Y',time.strptime(s,"%Y-%m-%d %H:%M:%S")),'%Y')
    def getmonth(s:str) -> time.struct_time:
        return time.strptime(time.strftime('%Y%m',time.strptime(s,'%Y-%m-%d %H:%M:%S')),'%Y%m')
    def getnewlist(l:list,t:time.struct_time,y:bool,m:bool) -> list :
        r=[]
        for i in l :
            if y and getyear(i)==t :
                r.append(i)
            if m and getmonth(i)==t :
                r.append(i)
        return r
    for i in l :
        if 'playedtimes' in i :
            te=getdictcopy(i)
            te['playedtimes']=getnewlist(te['playedtimes'],t,y,m)
            te['playcount']=len(te['playedtimes'])
            if te['playcount'] ==0 :
                te.pop('playedtimes')
            r.append(te)
        else :
            r.append(i)
    getlength(r)
    return r
def getdictcopy(d:dict)-> dict :
    re={}
    for i in d.keys():
        if type(d[i])==list :
            re[i]=getlistcopy(d[i])
        elif type(d[i])==dict :
            re[i]=getdictcopy(d[i])
        else :
            re[i]=d[i]
    return re
def getlistcopy(l:list) -> list :
    re=[]
    for i in l:
        if type(i)==list :
            re.append(getlistcopy(i))
        elif type(i)==dict :
            re.append(getdictcopy(i))
        else :
            re.append(i)
    return re
if __name__=="__main__" :
    if len(sys.argv)>1 :
        name=""
        name2=""
        settings={}
        m=0
        read=0
        for i in sys.argv[1:] :
            if i=='-h' :
                print(h)
                exit(0)
            if read==3 :
                re=getyearormonth(i,settings)
                if re==-1 :
                    print('-y 选项出现混用all和年份')
                    print(h)
                    exit(-1)
                read=0
                continue
            elif read==4 :
                re=getyearormonth(i,settings,'m')
                if re==-1 :
                    print('-m 选项出现混用all和年月')
                    print(h)
                    exit(-1)
                read=0
                continue
            read=getchoice(settings,i)
            if m==0 and read==0 :
                if os.path.exists(i) and os.path.isfile(i) :
                    name=i
                    m=m+1
                else :
                    print('"%s"文件不存在或是一个文件夹'%(i))
                    exit(-1)
            elif m==1 and read==0 :
                if not os.path.exists(i) or (os.path.exists(i) and os.path.isdir(i)) :
                    name2=i
                    m=m+1
                else :
                    print('"%s"文件已存在'%(i))
                    exit(-1)
        if m==2 and 'ok' in settings :
            main(name,name2,settings)
        else :
            if m==1:
                print('参数不足:缺少输出文件夹参数')
            elif m==0 :
                print('参数不足:缺少输入文件和输出文件夹参数')
            else :
                print('-a -y -m选项至少需要有一个')
            print(h)
            exit(-1)
    else :
        print('需要参数')
        print(h)
        exit(-1)
