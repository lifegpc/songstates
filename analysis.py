import sys
import os
def main(filen) :
    pass
if __name__=="__main__" :
    if len(sys.argv)>1 :
        for i in sys.argv[1:] :
            if os.path.exists(i) and os.path.isfile(i) :
                main(i)
            else :
                print('"%s"文件不存在或是一个文件夹'%(i))
