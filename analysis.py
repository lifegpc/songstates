import sys
import os
import XMLParser
import json
import time
import xlwt
h="""useage:
\tanalysis.py [-h] [-a] inputfile outputfile
choice:
\t-h\t显示帮助
\t-a\t分析所有时间的数据
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
    if os.path.exists(filen2) :
        removedir(filen2)
    os.mkdir(filen2)
    if 'a' in settings:
        fn:str="%s\\all.xls"%(filen2)
        w=xlwt.Workbook(encoding='utf8')
        t:xlwt.Worksheet=w.add_sheet('每首歌听歌时间')
        w.save(fn)
def getchoice(settings:dict,i:str):
    "解析是否为选项，不是选项返回0，是选项但解析失败返回1"
    if len(i)>=1 and i[0]=='-':
        if i=='-a' :
            settings['a']=True
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
if __name__=="__main__" :
    if len(sys.argv)>1 :
        name=""
        name2=""
        settings={}
        m=0
        for i in sys.argv[1:] :
            if i=='-h' :
                print(h)
                exit(0)
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
        if m==2 :
            main(name,name2,settings)
        else :
            print('参数不足')
            print(h)
            exit(-1)
