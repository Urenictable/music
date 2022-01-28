import os
import time
import json
import requests
from easy_pack import Easy as Fc
from color_print import Color as Cp

class Music():
    def __init__(self, keyword):
        #初始化函数
        self.num = 1
        #初始化自定义包
        self.Fc = Fc()
        self.Cp = Cp()
        self.keyword = keyword
        if self.keyword == "":
            pass
        else:
            try:
                self.parser()
                self.combination()
                self.song_datas_dic()
            except:
                self.Cp.print_green_text(print_text="网络错误，请检查网络链接！")

    def parser(self):
        ''' 解析音乐url '''
        try:
            #one在这里是转dict必须输入的，指定转换几个
            #headers = dict(one=random.choice(self.requests_headers))
            head_url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w="+self.keyword
            print(head_url)
            response = requests.get(head_url, headers=self.Fc.Agents()).text
            response = response.strip('callback()')
            #print(response)
            #解析json
            json_data = json.loads(response)
            json_data1 = json_data['data']['song']['list']
            json_data2 = json_data['data']['zhida']['zhida_singer']['singerPic']
            #print(json_data2)
            #创造列表
            self.song_Name = []
            #歌名
            self.song_Singer = []
            #歌手
            self.song_AlbumName = []
            #专辑
            self.AlbumId = []
            #歌曲号，用于拼接歌手图片
            self.song_StrMediaMid = []
            #拼接音乐连接时使用

            #获取并添加值
            try:
                for data in json_data1:
                    self.song_Name.append(data['songname'])
                    self.song_Singer.append(data['singer'][0]['name'])
                    self.song_AlbumName.append(data['albumname'])
                    self.song_StrMediaMid.append(data['strMediaMid'])
                    self.AlbumId.append(data['albumid'])
            except:
                self.Cp.print_green_text(print_text="数据获取失败！")
            #print(self.song_Name, self.song_Singer, self.song_AlbumName, self.song_Img, self.song_StrMediaMid)
        except:
            self.Cp.print_green_text(print_text="获取数据失败！")

    def combination(self):
        """ combination:组合，组合音乐url """
        try:
            self.song_Url = []
            for song in range(0, len(self.song_StrMediaMid)):
                #音乐json请求网页
                url2 = 'https://u.y.qq.com/cgi-bin/musicu.fcg?data={"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"7208009084","songmid":["%s"],"songtype":[0],"uin":"2883","loginflag":1,"platform":"20"}}}'
                #格式化写入url2
                purl = url2 % self.song_StrMediaMid[song]
                print(purl)
                resp = requests.get(purl, headers=self.Fc.Agents())
                # 对结果进行解码
                ret_json = resp.content.decode()
                # 转化为字典
                ret_dict = json.loads(ret_json)
                purl = ret_dict["req_0"]["data"]["midurlinfo"][0]["purl"]
                #这是最终的歌曲url
                url = ret_dict["req_0"]["data"]["sip"]
                song_url = url[1] + purl
                if len(song_url) <= 217:
                    #判断真假音乐播放地址
                    self.song_Url.append(song_url)
                else:
                    self.Cp.print_green_text(print_text="该音乐无法下载！")
        except:
                pass

    def song_datas_dic(self):
        """ song_datas_dic : 储存歌曲信息的字典 """
        try:
            self.datas = []
            #print(self.song_Name, self.song_Singer, self.song_AlbumName, self.song_StrMediaMid, self.song_url_list)
            for number in range(len(self.song_StrMediaMid)):
                self.song_datas = {
                    "song_Names" : self.song_Name[number],
                    "song_Singers" : self.song_Singer[number],
                    "song_AlbumName" : self.song_AlbumName[number],
                    "song_Url" : self.song_Url[number],
                    "song_Img" : "http://imgcache.qq.com/music/photo/album_300/%i/300_albumpic_%i_0.jpg" % (self.AlbumId[number]%100, self.AlbumId[number])
                }
                self.datas.append(self.song_datas)
            #print(self.datas)
            #return self.datas
        except:
            pass

def run():
    mc = Music("稻香")
run()
"""
https://u.y.qq.com/cgi-bin/musicu.fcg?data={"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"7208009084","songmid":"0040rS0Y2eItVE","songtype":[0],"uin":"2883","loginflag":1,"platform":"20"}}}
http://dl.stream.qqmusic.qq.com/C400001U2GJO2hSzQW.m4a?guid=5080691353&vkey=F27182982F4EB58E809420D33AE345A9D0C5037797A25D62BD8B26732B8BF81C2E511ECA62DAF5489AB7348CA28FDBF95DFD7C5A1F6275A1&uin=2843937603&fromtag=66
"""
