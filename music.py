import os
import sys
import json
import time
import requests
import pyperclip    #用于复制内容
from ttkbootstrap import Style  #用于美化界面
import tkinter.messagebox
import tkinter.filedialog   #用于选择保存路径
from tkinter import *
from tkinter import ttk
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+"\\packages\\")
import easy_pack
from functions import Music_ui as Mc
from color_print import Color as Cp

class Music_ui():
    def __init__(self, init_window):
        """ 初始化函数 """
        #初始化窗口
        self.init_window = init_window
        #添加保存路径SrtingVar()相当于一个寄存器， 详见：https://www.cnblogs.com/wangjiyuan/p/PythonEntry.html
        self.get_save_path = StringVar()
        self.get_value = StringVar()
        #初始化自定义包
        self.Mc = Mc
        #引用虚拟请求头
        self.Fc = Fc
        #输出着色
        self.Cp = Cp()

    def set_init_window(self):
        """ 设置窗口的函数 """
        #设置窗口标题
        self.init_window.title("Music下载器")
        #设置窗口图标
        self.init_window.iconbitmap(os.path.dirname(os.path.abspath(__file__))+'\packages\icon.ico')
        #设置窗口大小和最初的显示位置(+10+10)
        self.init_window.geometry("+10+10")

        #进行范围分割
        self.labelframe1 = LabelFrame(width=700, height=100, text="搜索配置")
        self.labelframe1.grid(row=0, column=0, padx=10, pady=10)

        #添加提示标签
        self.init_point_out_label1 = Label(self.labelframe1, text="请输入歌名(歌手,歌词)：")
        #将标签挂载在ui界面上, row为行 column为列 columnspan为所占的列数(都从0开始)
        self.init_point_out_label1.grid(row=0, column=0)

        #添加输入框
        self.init_text_label1 = Entry(self.labelframe1)
        #将其挂载到ui上，否则不会显示
        #colmunspan：设置单元格横向跨越的列数,即控件占据的列数(宽度) 
        #rowspan：设置单元格纵向跨越的行数,即控件占据的行数(高度)。
        #fg=bule此参数是设置按钮文字颜色的参数
        self.init_text_label1.grid(row=0, column=1, columnspan=3)

        #添加搜索按钮
        self.init_sure_button1 = Button(self.labelframe1, text="搜索", command=self.sure_button1_click)
        self.init_sure_button1.grid(row=0, column=4)

        #添加保存路径
        self.init_save_path = Entry(self.labelframe1, text="保存路径：", textvariable=self.get_save_path)
        self.init_save_path.grid(row=0, column=7)
        self.file = Button(self.labelframe1, text="选择音乐保存目录", command=self.add_choice_file).grid(row=0, column=8)

        #添加高级设置按钮
        self.advanced_setting = Button(self.labelframe1, text="高级设置", command=self.advanced_setting_click)
        self.advanced_setting.grid(row=1, column=2, rowspan=1)

        #添加使用方法按钮
        self.how_to_use_button = Button(self.labelframe1, text="使用方法", command=self.how_to_use_button_click)
        self.how_to_use_button.grid(row=1, column=7, rowspan=1)

        '''#进行范围分割
        labelframe2 = LabelFrame(width=700, height=100, text="音乐信息")
        #sticky=N/S/E//W:顶端对齐/底端对齐/右对齐/左对齐
        #详见：https://blog.csdn.net/hyf64/article/details/121220643
        labelframe2.grid(row=3, column=0, padx=10, pady=10)'''

        #进行范围分割
        self.labelframe2 = LabelFrame(text="音乐信息")
        self.labelframe2.grid(row=3, column=0, columnspan=4, sticky=NSEW)

        #定义树形结构与滚动条
        self.music_tree = ttk.Treeview(self.labelframe2, show="headings", columns=("a", "b", "c", "d", "e"))		
        self.vbar = ttk.Scrollbar(self.labelframe2, orient=VERTICAL, command=self.music_tree.yview)       
        self.music_tree.configure(yscrollcommand=self.vbar.set)

        # 表格的标题
        self.music_tree.column("a", width=75, anchor="center")
        self.music_tree.column("b", width=125, anchor="center")
        self.music_tree.column("c", width=125, anchor="center")
        self.music_tree.column("d", width=125, anchor="center")
        self.music_tree.column("e", width=175, anchor="center")
        
        self.music_tree.heading("a", text="歌曲列表")
        self.music_tree.heading("b", text="音乐名称")
        self.music_tree.heading("c", text="歌曲原唱")
        self.music_tree.heading("d", text="歌曲专辑")
        self.music_tree.heading("e", text="歌曲链接")

        self.music_tree.grid(row=4, column=0, sticky=NSEW)
        self.music_tree.bind("<Double-1>",self.onDBClick)
        self.vbar.grid(row=4, column=1, sticky=NS)

        #添加状态栏
        self.status_label = Label(self.init_window, text="状态栏：")
        self.status_label.grid(row=5, column=0)
        self.status_labe2 = Label(self.init_window, text="正在获取...")
        self.status_labe2.grid(row=5, column=1)

    def sure_button1_click(self):
        """ 按钮点击程序(获取输入框内容，并进行搜索) """
        try:
            datas = self.music_tree.get_children()
            for item in datas:
                self.music_tree.delete(item)
            self.keyword = str(self.init_text_label1.get())
            if self.keyword != "":
                self.data = self.Mc(keyword=self.keyword)
                self.show_music_lists(self.data)
            else:
                self.Cp.print_red_text(print_text="您还未输入内容！")
        except:
            self.Cp.print_red_text(print_text="搜索程序错误！")

    def add_choice_file(self):
        """ 选择保存目录程序 """
        try:
            #askdirectory()为选择文件夹，详见：https://blog.csdn.net/nilvya/article/details/106221666
            self.filename = tkinter.filedialog.askdirectory()
            self.entry_text = self.get_save_path.set(self.filename)
        except:
            self.Cp.print_red_text(print_text="选择保存目录程序错误！")

    def get_file_path(self):
        """get_file_path : 获取当前文件所在的绝对路径 """
        try:
            self.get_path = sys.path[0] + "\\"
            return self.get_path
        except:
            self.Cp.print_red_text(print_tex="获取当前目录路径错误！")

    def advanced_setting_click(self):
        """ advanced_setting_click : 检查高级设置文件是否存在(高级设置) """
        try:
            json_data = {
                "AI_download" : "Flase",            #自动下载
                "@AI_download" : "自动下载：Flase=关闭; True=开启",    
                "Lyric_download" : "Flase",         #下载歌词
                "@Lyric_download" : "下载歌词：Flase=关闭; True=开启",  
                "Try_listen" : "Flase",         #试听歌曲
                "@Try_listen" : "音乐试听：Flase=关闭; True=开启",  
                "Song_sound_quality" : "mp3",           #歌曲音质
                "@Song_sound_quaility" : "音乐品质：低音质：mp3; 无损音质：flac; 波形音频：wav",  
                "Use_music_list" : "Flase",         #使用字典
                "@Use_music_list" : "读取字典下载：Flase=关闭; True=开启",  
                "API_url" : "http://dl.stream.qqmusic.qq.com/",#音乐AIP接口
                "@API_url" : "音乐链接接口：可用于官方接口更换，以继续保持软件可用性。",  
                "Show_QRCode" : "Flase",
                "@Show_QRCode" : "显示音乐链接二维码：Flase=关闭; True=开启",  
                "Version" : "1.0.0",           #版本号
                "@Version" : "版本号"
            }
            file_name = "setting.json"
            files = os.path.exists(self.get_file_path()+file_name)
            if files != True:
                with open(self.get_file_path()+file_name, 'a') as f:
                    pass
                with open(self.get_file_path()+file_name, 'w') as code:
                    json.dump(json_data, code, indent=4, ensure_ascii=False)
                    #indent=4, ensure_ascii=False       让json字符格式化添加
                os.system(self.get_file_path()+file_name)
            else:
                os.system(self.get_file_path()+file_name)
        except:
            self.Cp.print_red_text(print_text="高级设置程序错误！")

    def how_to_use_button_click(self):
        """ how_to_use_buton_click : 显示本产品使用方法 """
        try:
            how_to_use_txt = """
                                                    本产品可以下载并搜索歌曲

                搜索示例：
                    稻香                    (只输入歌手)
                    稻香 周杰伦             (输入歌手 歌曲名称————这样搜索可以使结果更加精准)
                    周杰伦                  (只输入歌手————这样搜索可以自动获取该歌手最新音乐)
                    还记得你说家是...        (只输入歌词)

                按键解释：
                    选择路径：可以选择歌曲保存的位置
                    高级设置：可以设置其它选项(如：下载歌词, 使用音乐字典, 选择音质等...)

                注意：
                    1. 本产品由于技术限制，目前只能够下载大部分可以完整听完的歌曲，若播放时为试听，则无法下载。
                    2. 修改setting.json文件时记得保存后再关闭,当想要恢复原来的设置时只需删除即可。
                    3. 下载音乐时需要先选择文件保存路径
                    """
            #init_window_message = Tk()
            style2 = Style(theme="lumen")
            init_window_message = style2.master
            init_window_message.title("使用方法：")
            Message(init_window_message, text=how_to_use_txt).grid()
        except:
            self.Cp.print_red_text(print_text="显示产品使用方法程序错误！")

    def onDBClick(self, event):
        """ onDBClick : Treeview绑定事件 """
        try:
            self.sels = event.widget.selection()
            Button(self.labelframe1, text="下载音乐", command=self.download_music).grid(row=2, column=2, rowspan=1)
            Button(self.labelframe1, text="复制链接", command=self.url_copy_button_click).grid(row=2, column=7, rowspan=1)
        except:
            self.Cp.print_red_text(print_text="TreeView程序出错！")

    def show_music_lists(self, data):
        """ show_music_lists : 显示歌曲数据 """
        try:
            song_data_list = self.data.song_datas_dic()
            for index, music_info in enumerate(song_data_list):
                infos = json.dumps(music_info, ensure_ascii=False)
                #ensure_ascii=False 将乱码显示成中文， 详见：https://blog.csdn.net/qq284489030/article/details/90260699
                self.info = json.loads(infos)
                #print(self.info)
                #print("%-*s| %s | %*s |%*s\n"%(20,index,self.info["song_Names"],self.info["song_Singers"],self.info["song_AlbumName"],self.info["song_Img"]))
                if self.info["song_Url"] == "http://isure.stream.qqmusic.qq.com/":
                    self.music_tree.insert("",'end',values=(index + 1,self.info["song_Names"],self.info["song_Singers"],self.info["song_AlbumName"],"此歌曲为VIP音乐，歌曲链接暂时无法获取！"))
                else:
                    self.music_tree.insert("",'end',values=(index + 1,self.info["song_Names"],self.info["song_Singers"],self.info["song_AlbumName"],self.info["song_Url"]))
        except:
            self.Cp.print_red_text(print_text="显示歌曲程序错误！")

    def url_copy_button_click(self):
        """ url_copy_button_click : 点击复制音乐链接 """
        try:
            music_tree_value = self.music_tree.item(self.sels,"values")[4]
            if music_tree_value != "此歌曲为VIP音乐，歌曲链接暂时无法获取！":
                pyperclip.copy(music_tree_value)
                tkinter.messagebox.showinfo("消息提示", "音乐链接复制成功！")
            else:
                tkinter.messagebox.showinfo("消息提示", "此歌曲为VIP音乐，歌曲链接暂时无法获取！")
                #点击后摧毁此窗口
        except:
            self.Cp.print_red_text(print_text="复制音乐链接程序错误！")

    def download_music(self):
            """ download_music : 下载音乐 """
            get_path = sys.path[0] + "\\" + "setting.json"
            try:
                with open(get_path, 'r') as f:
                    json_datas = f.read()
                    json_data1 = json.loads(json_datas)
            except FileNotFoundError:
                self.advanced_setting_click()
                with open(get_path, 'r') as f:
                    json_datas = f.read()
                    json_data1 = json.loads(json_datas)
            AI_download = json_data1['AI_download']
            Lyric_download = json_data1['Lyric_download']
            Try_listen = json_data1['Try_listen']
            Song_sound_quaility = json_data1['Song_sound_quality']
            Use_music_list = json_data1['Use_music_list']
            Show_QRCode = json_data1['Show_QRCode']
            #print(AI_download, Lyric_download, Try_listen, Song_sound_quaility, Use_music_list, Show_QRCode)
            if Song_sound_quaility not in ["mp3", "flac", "wav"]:
                Song_sound_quaility = "mp3"
                self.Cp.print_red_text(print_text="您输入的音乐格式有误！\n已自动为您下载mp3类型的音乐")
            else:
                Song_sound_quaility = Song_sound_quaility
            if self.get_save_path.get() == "":
                tkinter.messagebox.showinfo("提示：", "请选择音乐保存路径！")
            else:
                music_tree_name = self.music_tree.item(self.sels,"values")[1]
                music_tree_singer = self.music_tree.item(self.sels,"values")[2]
                music_tree_url = self.music_tree.item(self.sels,"values")[4]
                music_file_name = self.get_save_path.get() + "\\" + music_tree_name + "-" + music_tree_singer + "." + Song_sound_quaility
                if music_tree_url != "此歌曲为VIP音乐，歌曲链接暂时无法获取！":
                    try:
                        music_url_response = requests.get(music_tree_url, headers=self.Fc.Agents(self))
                        with open(music_file_name, 'wb') as f:
                            f.write(music_url_response.content)
                        tkinter.messagebox.showinfo("消息提示", "歌曲：{}     歌手：{}.....下载成功！".format(music_tree_name, music_tree_singer))
                    except:
                        tkinter.messagebox.showinfo("消息提示", "歌曲：{}     歌手：{}.....下载失败！".format(music_tree_name, music_tree_singer))
                else:
                    tkinter.messagebox.showinfo("消息提示", "此歌曲为VIP音乐，歌曲链接暂时无法获取！")

def start():
    style1 = Style(theme="sandstone") # 使用的主题名称, 主题还有：
    #light
        #cosmo - flatly - journal - literal - lumen - minty - pulse - sandstone - united - yeti
    #dark:
        #cyborg - darkly - solar - superhero
    init_window = style1.master
    run = Music_ui(init_window)
    run.set_init_window()
    init_window.mainloop()

start()