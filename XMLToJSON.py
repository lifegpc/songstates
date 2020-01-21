import sys
import os
import XMLParser
import json
import dataqc
def main(filen:str,filen2:str,settings:dict) :
    re=XMLParser.loadXML(filen)
    if 'q' in settings :
        re=dataqc.qc(re)
    if os.path.exists(filen2) :
        os.remove(filen2)
    f=open(filen2,'w',encoding='utf8')
    json.dump(re,f)
    f.close()
def getchoice(settings:dict,i:str):
    "解析是否为选项，不是选项返回0，是选项但解析失败返回1"
    if len(i)>=1 and i[0]=='-' :
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
