import sys
import os
import XMLParser
import json
import xlwt
def main(filen,filen2,settings) :
    re=XMLParser.loadXML(filen)
    if os.path.exists(filen2) :
        os.remove(filen2)
    w=xlwt.Workbook()
    a=w.add_sheet('Source Data')
    t=['id','title','artist','trackartist','album','albumartist','date','discnumber','tracknumber','codec','codecprofile','ext','bitrate','samplerate','channels','length','lengthseconds','playcount','lastplayed','playedtimes']
    j=0
    for i in t :
        a.write(0,j,i)
        j=j+1
    j=1
    for i in re :
        a.write(j,0,j)
        k=1
        for ii in t[1:] :
            if ii in i:
                a.write(j,k,i[ii])
            k=k+1 
        j=j+1
    w.save(filen2)
if __name__=="__main__" :
    if len(sys.argv)>1 :
        m=0
        name=""
        name2=""
        settings={}
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
            main(name,name2,settings)
        else :
            print('参数不足')
            exit(-1)
