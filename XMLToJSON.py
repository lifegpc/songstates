import sys
import os
import XMLParser
import json
def main(filen,filen2) :
    re=XMLParser.loadXML(filen)
    if os.path.exists(filen2) :
        os.remove(filen2)
    f=open(filen2,'w',encoding='utf8')
    json.dump(re,f)
    f.close()
if __name__=="__main__" :
    if len(sys.argv)>1 :
        m=0
        name=""
        name2=""
        for i in sys.argv[1:] :
            if m==0 :
                if os.path.exists(i) and os.path.isfile(i) :
                    name=i
                    m=m+1
                else :
                    print('"%s"文件不存在或是一个文件夹'%(i))
                    exit(-1)
            elif m==1 :
                name2=i
                m=m+1
                break
        if m==2 :
            main(name,name2)
        else :
            print('参数不足')
            exit(-1)
