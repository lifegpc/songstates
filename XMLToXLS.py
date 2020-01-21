import sys
import os
import XMLParser
import json
import xlwt
import dataqc
def main(filen:str,filen2:str,settings:dict) :
    try :
        re=XMLParser.loadXML(filen)
    except :
        f=open(filen,'r',encoding='utf8')
        re=json.load(f)
        f.close()
    if 'q' in settings :
        re=dataqc.qc(re)
    if os.path.exists(filen2) :
        os.remove(filen2)
    w=xlwt.Workbook()
    a=w.add_sheet('Source Data')
    t=['id','title','artist','trackartist','album','albumartist','date','discnumber','tracknumber','codec','codecprofile','ext','bitrate','samplerate','channels','length','lengthseconds','playcount','lastplayed','playedtimes']
    if 'h' in settings :
        t2=['id','time']
        b=w.add_sheet('History')
        j=0
        for i in t2 :
            b.write(0,j,i)
            j=j+1
        t=t[:-1]
        k2=1
    j=0
    for i in t :
        a.write(0,j,i)
        j=j+1
    j=1
    if 'h' in settings :
        t.append('playedtimes')
    for i in re :
        a.write(j,0,j)
        k=1
        for ii in t[1:] :
            if ii in i:
                if 'h' in settings and ii=='playedtimes' :
                    for iii in i[ii] :
                        b.write(k2,0,j)
                        b.write(k2,1,iii)
                        k2=k2+1
                else:
                    a.write(j,k,i[ii])
            k=k+1 
        j=j+1
    w.save(filen2)
def getchoice(settings:dict,i:str):
    "解析是否为选项，不是选项返回0，是选项但解析失败返回1"
    if len(i)>=1 and i[0]=='-' :
        if i=='-h' :
            settings['h']=True
            return 2
        if i=='-q' :
            settings['q']=True
            return 2
        else :
            return 1
    else :
        return 0
if __name__=="__main__" :
    if len(sys.argv)>1 :
        m=0
        name=""
        name2=""
        settings={}
        for i in sys.argv[1:] :
            read=getchoice(settings,i)
            if m==0 and read==0 :
                if os.path.exists(i) and os.path.isfile(i) :
                    name=i
                    m=m+1
                else :
                    print('"%s"文件不存在或是一个文件夹'%(i))
                    exit(-1)
            elif m==1 and read==0 :
                name2=i
                m=m+1
            if read==1 :
                print('"%s"不是有效的选项'%(i))
        if m==2 :
            main(name,name2,settings)
        else :
            print('参数不足')
            exit(-1)
