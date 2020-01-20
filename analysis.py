import sys
import os
h="""useage:
\tanalysis.py [-h] [-a] inputfile outputfile
choice:
\t-h\t显示帮助
\t-a\t分析所有时间的数据
"""
def main(filen:str,filen2:str,settings:dict) :
    pass
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
                name2=i
                m=m+1
        if m==2 :
            main(name,name2,settings)
        else :
            print('参数不足')
            print(h)
            exit(-1)
