import xml.sax
import json
def loadXML(filen) :
    "加载XML文件"
    p=xml.sax.make_parser()
    p.setFeature(xml.sax.handler.feature_namespaces, 0)
    h=Hander()
    p.setContentHandler(h)
    p.parse(filen)
    return p.getContentHandler().sb
class Hander(xml.sax.ContentHandler) :
    istag=0
    sa={}
    sb=[]
    def startDocument(self) :
        self.sa={}
        self.sb=[]
        self.istag=0
    def startElement(self,tag,attributes) :
        if tag=='song' :
            self.sa={}
            self.istag=0
        elif tag=='title':
            self.istag=1
        elif tag=='artist' :
            self.istag=2
        elif tag=='trackartist' :
            self.istag=3
        elif tag=='album' :
            self.istag=4
        elif tag=='albumartist':
            self.istag=5
        elif tag=='date':
            self.istag=6
        elif tag=='discnumber' :
            self.istag=7
        elif tag=='tracknumber' :
            self.istag=8
        elif tag=='codec' :
            self.istag=9
        elif tag=='codecprofile' :
            self.istag=10
        elif tag=='ext' :
            self.istag=11
        elif tag=='bitrate' :
            self.istag=12
        elif tag=='samplerate' :
            self.istag=13
        elif tag=='channels' :
            self.istag=14
        elif tag=='length' :
            self.istag=15
        elif tag=='lengthseconds' :
            self.istag=16
        elif tag=='playcount' :
            self.istag=17
        elif tag=='lastplayed' :
            self.istag=18
        elif tag=='playedtimes' :
            self.istag=19
    def endElement(self,tag) :
        if tag=='song' :
            self.sb.append(self.sa)
            self.sa={}
        self.istag=0
    def characters(self,context) :
        if self.istag==1 :
            self.sa['title']=context
        elif self.istag==2 :
            self.sa['artist']=context
        elif self.istag==3 :
            self.sa['trackartist']=context
        elif self.istag==4 :
            self.sa['album']=context
        elif self.istag==5 :
            self.sa['albumartist']=context
        elif self.istag==6 :
            try :
                self.sa['date']=int(context)
            except :
                if 'date' in self.sa :
                    self.sa.pop('date')
        elif self.istag==7 :
            self.sa['discnumber']=int(context)
        elif self.istag==8 :
            self.sa['tracknumber']=int(context)
        elif self.istag==9 :
            self.sa['codec']=context
        elif self.istag==10 :
            self.sa['codecprofile']=context
        elif self.istag==11 :
            self.sa['ext']=context
        elif self.istag==12 :
            self.sa['bitrate']=int(context)
        elif self.istag==13 :
            self.sa['samplerate']=int(context)
        elif self.istag==14 :
            self.sa['channels']=context
        elif self.istag==15 :
            self.sa['length']=context
        elif self.istag==16 :
            self.sa['lengthseconds']=int(context)
        elif self.istag==17 :
            self.sa['playcount']=int(context)
        elif self.istag==18 :
            self.sa['lastplayed']=context
        elif self.istag==19 :
            self.sa['playedtimes']=json.loads(context)
    def endDocument(self) :
        pass
