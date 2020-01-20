# 歌曲信息整理
## 简介
由于[foobar2000](https://www.foobar2000.org/)的高度可定制性，因此可以采取定制copycommand，然后利用copyname来复制歌曲信息甚至播放数据。
然后对复制的内容稍加处理可以得到xml文件，在通过分析内容得到音乐播放的数据。
## 使用前准备
### 使用前foobar2000的配置
获取播放次数以及上次播放时间需要[Playback Statistics](https://www.foobar2000.org/components/view/foo_playcount)插件，获取历史播放时间需要[Enhanced Playback Statistics](https://www.foobar2000.org/components/view/foo_enhanced_playcount)插件。  
需要在Preferences内，在左侧选择Display-->Context Menu，在右侧启用 Copy name(s)。   
然后在左侧选择Advanced，在右侧选择Display-->Legacy title formatting settings (deprecated, provided for compatibility with old components only)，修改里面的Copy command为   
```txt
<song><title>$replace(%title%,&,&amp;)</title>$if(%artist%,<artist>$replace(%artist%,&,&amp;)</artist>,)$if(%track artist%,<trackartist>$replace(%track artist%,&,&amp;)</trackartist>,)$if(%album%,<album>$replace(%album%,&,&amp;)</album>,)$if(%album artist%,<albumartist>$replace(%album artist%,&,&amp;)</albumartist>,)$if(%date%,<date>%date%</date>,)$if(%discnumber%,<discnumber>%discnumber%</discnumber>,)$if(%tracknumber%,<tracknumber>%tracknumber%</tracknumber>,)<codec>%codec%</codec>$if(%codec_profile%,<codecprofile>%codec_profile%</codecprofile>,)<ext>$ext(%filename_ext%)</ext><bitrate>%bitrate%</bitrate><samplerate>%samplerate%</samplerate><channels>%channels%</channels><length>%length%</length><lengthseconds>%length_seconds%</lengthseconds><playcount>%play_count%</playcount>$if($strcmp(%last_played%,N/A),,<lastplayed>%last_played%</lastplayed>)$if($strcmp(%play_count%,0),,<playedtimes>%played_times%</playedtimes>)</song>
```
**注：这里只处理了特殊符号&，当歌曲信息内含有&lt;、&gt;等时，并没有做相应的处理，因此可能产生错误。**<br/>   
这样，便可以在歌曲的右键菜单中看到Copy name(s)，通过这个可以快速复制歌曲的信息，下面就是一个例子：   
```xml
<song><title>I LOVE NEW DAY!</title><artist>花澤香菜</artist><album>Blue Avenue</album><albumartist>花澤香菜</albumartist><date>2015</date><discnumber>1</discnumber><tracknumber>01</tracknumber><codec>PCM</codec><ext>aif</ext><bitrate>1411</bitrate><samplerate>44100</samplerate><channels>stereo</channels><length>5:37</length><lengthseconds>337</lengthseconds><playcount>5</playcount><lastplayed>2020-01-12 07:52:37</lastplayed><playedtimes>["2020-01-02 16:18:53", "2020-01-02 16:56:35", "2020-01-10 17:52:21", "2020-01-11 08:47:02", "2020-01-12 07:52:37"]</playedtimes></song>
```
由于复制多首歌曲时，复制出来的内容会有多个根节点，所以需要在两头增加&lt;playlist&gt;标签。   
就像这样：
```xml
<playlist>
<song><title>错错错</title><artist>六哲</artist><album>伤感情歌对唱</album><albumartist>六哲</albumartist><discnumber>1</discnumber><tracknumber>01</tracknumber><codec>FLAC</codec><ext>flac</ext><bitrate>921</bitrate><samplerate>44100</samplerate><channels>stereo</channels><length>4:49</length><lengthseconds>289</lengthseconds><playcount>5</playcount><lastplayed>2020-01-16 08:13:07</lastplayed><playedtimes>["2020-01-02 15:11:11", "2020-01-05 19:25:29", "2020-01-12 18:20:33", "2020-01-14 17:48:29", "2020-01-16 08:13:07"]</playedtimes></song>
<song><title>only my railgun</title><artist>fripSide (フリップサイド)</artist><album>Only My Railgun (とある科学の超电磁炮OP)</album><albumartist>fripSide (フリップサイド)</albumartist><discnumber>1</discnumber><tracknumber>01</tracknumber><codec>FLAC</codec><ext>flac</ext><bitrate>1174</bitrate><samplerate>44100</samplerate><channels>stereo</channels><length>4:17</length><lengthseconds>257</lengthseconds><playcount>3</playcount><lastplayed>2020-01-16 10:35:08</lastplayed><playedtimes>["2020-01-12 16:28:43", "2020-01-13 14:45:26", "2020-01-16 10:35:08"]</playedtimes></song>
</playlist>
```
[这里](https://kanahanazawa.com/tools/foobarxml/)是一个可以加上根节点的小工具。
## 程序部分
### 转换部分
#### XMLToJSON
该程序将XML转换成JSON。使用时直接在命令行输入输入文件名和输出文件名即可。   
例如将out.xml转换为out.json，可以使用下面的命令行
```bash
python XMLToJSON.py out.xml out.json
```
#### XMLToXLS
该程序将XML转换为XLS。可以使用选项"-h"将歌曲历史播放记录专门写入"History"表。   
**注：现在输入文件也可以是JSON文件**   
将out.xml转换成out.xls，示例：
```bash
python XMLToJSON.py out.xml out.xls #简单转换
python XMLToJSON.py -h out.xml out.xls #将歌曲历史播放记录写入"History"表，"-h"可以放在任一位置
```
