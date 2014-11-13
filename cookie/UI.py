# -*- coding: utf-8 -*- 
import Tkinter
import thread
import copy
import os
from Tracking import Tracking
from Device import Deviceid
class UI:
    def __init__(self):
        self.root = Tkinter.Tk()
        self.root.title("cookie")
        self.root.geometry('540x700')
        self.root.resizable(0, 0)
        self.device = Deviceid()
        self.device.getDevices()
        #选中的device_id
        self.device_chose = ''
        self.mac_list = []
        self.requestHost = []
        self.cookie = []
        self.thread = ''
        self.tracking_info = []
        #Tracking 类
        self.tracking = ''
        #选中的mac
        self.mac_chose = ''
        #选中的request
        self.domain_chose = ''
        #tracking 定义
        self.tracking = Tracking(self.device_chose)
        
        #device 列表
        self.device_list = Tkinter.Listbox(self.root,width = 50,height = 10,
                                           selectmode = 'SINGLE',selectbackground = 'red')
        #device 滑块
        self.device_bar = Tkinter.Scrollbar(self.root,activebackground='grey');
        
        #tracking 列表
        self.track_list = Tkinter.Listbox(self.root,width = 15,height = 10,
                                          selectmode = 'SINGLE',selectbackground = 'red')
        #tracking 滑块
        self.track_bar = Tkinter.Scrollbar(self.root,activebackground='grey')
        
        #domain 列表
        self.domain_list = Tkinter.Listbox(self.root,width = 15, height = 20,
                                           selectmode = 'SINGLE',selectbackground = 'red')
        #dimain 滑块
        self.domain_bar = Tkinter.Scrollbar(self.root,activebackground='grey')
        
        #detail 列表
        self.cookie_tr_list = Tkinter.Listbox(self.root,width = 50, height = 20,
                                           selectmode = 'SINGLE',selectbackground = 'red')
        #detail 滑块
        self.cookie_tr_bar = Tkinter.Scrollbar(self.root,activebackground='grey')
        
        #ouput
        self.outputLabel = Tkinter.Text(self.root,width = 75, height = 10)
        
        #shilter domain
        self.domain_shilter = Tkinter.Entry(self.root,width = 10)
        
        #是否输出
        self.printCookie_cookie = False
        self.printCookie_anget = False
    def sub_thread_tracker(self,num):
        if self.tracking:
            self.tracking.end = True
        self.tracking = Tracking(num)
        self.tracking.get_datas()
    def printList(self,event):
        '''获取 device列表中选中的device_id'''
        self.device_chose =  self.device_list.get(self.device_list.curselection())
        print 'Chosen device: %s'%self.device_chose[0]
        self.tracking.device_id=self.device_chose[0]
        if self.thread == '':
            thread.start_new(self.sub_thread_tracker, (self.device_chose[0],))
            self.tread = '1'
    def printMac(self,event):
        '''获取mac列表中选中的mac'''
        temp = self.track_list.get(self.track_list.curselection())
        if temp != self.mac_chose:
            self.mac_chose = temp
            print 'Chosen mac: %s'%self.mac_chose
            if len(self.requestHost)>0:
                self.domain_list.delete(0, len(self.requestHost))
                self.requestHost[:] = []
    def refreshLayout(self):
        if len(self.requestHost)>0:
            self.domain_list.delete(0, len(self.requestHost))
            self.requestHost[:] = []
        if len(self.cookie)>0:
            self.cookie_tr_list.delete(0, len(self.cookie))
            self.cookie[:] =[]
    def printDomain(self,event):
        self.domain_chose = self.domain_list.get(self.domain_list.curselection())
        print 'Chosen domain: %s'%self.domain_chose
        if len(self.cookie)>0:
            self.cookie_tr_list.delete(0, len(self.cookie))
            self.cookie[:] =[]
    def printCookie(self,event):
        temp = self.cookie_tr_list.get(self.cookie_tr_list.curselection())
        temp1 = temp.split('\n')
        strr = ''
        if self.printCookie_cookie:
            temp2 = temp1[4]
            strr += '\n******Cookie******\n'
            temp2 = temp2.replace('; ','\n')
            strr += temp2
        if self.printCookie_anget:
            strr += '\n******UserAgent*****\n'
            temp2 = temp1[3]
            strr += temp2
        if len(strr)>1:
            temp = strr
        file = open('temap_data.xml','w')
        file.write(temp)
        file.close()
        #os.startfile('temap_data.xml')
        self.outputLabel.insert( 1.0,temp+'\n\n\n')
    def Update_track_info(self):
        temp =  self.tracking.track_datas
        #mac列表更新
        if len(temp)>0 and len(temp)>len(self.tracking_info):
            index = len(self.tracking_info)
            self.tracking_info=copy.deepcopy(temp)
            for ele in self.tracking_info[index-1:]:
                mac = ele['mac']
                if not mac in self.mac_list:
                    self.mac_list.append(mac+'')
                    index2 = len(self.mac_list)
                    self.track_list.insert(index2,self.mac_list[-1])
        #domain列表更新
        domain_shilter = self.domain_shilter.get()
        if len(self.tracking_info)>0 and len(self.mac_chose) > 0:
            #print len(self.requestHost)
            for ele in self.tracking_info:
                if ele['mac'] == self.mac_chose and not ele['requestHost'] in self.requestHost:
                    requestHost = ele['requestHost']
                    if len(domain_shilter)==0 or domain_shilter in requestHost:
                        index = len(self.requestHost)
                        self.requestHost.append(requestHost+'')
                        self.domain_list.insert(index,self.requestHost[-1])
        elif len(self.tracking_info)>0:
            for ele in self.tracking_info:
                if not ele['requestHost'] in self.requestHost:
                    requestHost = ele['requestHost']
                    if len(domain_shilter)==0 or domain_shilter in requestHost:
                        index = len(self.requestHost)
                        self.requestHost.append(requestHost+'')
                        self.domain_list.insert(index,self.requestHost[-1])
                    
        #cookie列表更新
        if len(self.tracking_info)>0 and len(self.domain_chose) > 0:
            for ele in self.tracking_info:
                if ele['mac'] == self.mac_chose and ele['requestHost'] == self.domain_chose and not ele in self.cookie:
                    mac = ele['mac']+'\n'
                    domain = ele['requestHost']+'\n'
                    userAgent = ele['userAgent']+'\n'
                    cookie = ele['cookieData']+'\n'
                    refererUrl = ele['refererUrl']+'\n'
                    str = refererUrl + domain + mac + userAgent+cookie
                    index = len(self.cookie)
                    self.cookie.append(ele)
                    self.cookie_tr_list.insert(index,str)
                    
        self.root.update()        
        self.track_list.after(10, self.Update_track_info)
    def change_cookie_check_state(self):
        self.printCookie_cookie = not self.printCookie_cookie
    def change_agent_check_state(self):
        self.printCookie_anget = not self.printCookie_anget
    def run(self):
        '''界面主循环'''
        
        #在列表中添加device
        for i in range(len(self.device.device_id)):
            device_info = self.device.device_id[i],self.device.device_mac[i],self.device.device_name[i]
            self.device_list.insert(i,device_info)
        #设置列表相
        self.device_list.bind('<Double-Button-1>',self.printList)
        self.device_list.place(x=0,y=20,anchor='nw')
        #滚动条关联至device_list
        self.device_bar.config(command = self.device_list.yview)
        self.device_bar.place(x=355,y=20,anchor='nw',height = 160)
        
        #设置mac列表
        self.track_list.bind('<Double-Button-1>',self.printMac)
        self.track_list.place(x=400,y=20,anchor='nw')
        self.track_list.insert(0,'')
        self.track_list.after(10, self.Update_track_info)
        #设置mac滚动条
        self.track_bar.config(command = self.track_list.yview)
        self.track_bar.place(x=510,y=20,anchor='nw',height = 160)
        
        #设置domain列表
        self.domain_list.bind('<Double-Button-1>',self.printDomain)
        self.domain_list.place(x=0,y=220,anchor='nw')
        #设置domain滚动条
        self.domain_bar.config(command = self.domain_list.yview)
        self.domain_bar.place(x=110,y=220,anchor='nw',height = 160)
        #domain过滤
        self.domain_shilter.place( x = 0, y = 190)
        domain_refresh_button = Tkinter.Button(self.root,text = 'url -refresh',command=self.refreshLayout)
        domain_refresh_button.place(x = 80, y =190)
        #设置cookie列表
        self.cookie_tr_list.bind('<Double-Button-1>',self.printCookie)
        self.cookie_tr_list.place(x=150,y=220,anchor='nw')
        #self.cookie_tr_list.after(10, self.Update_track_info)
        #设置cookie滚动条
        self.cookie_tr_bar.config(command = self.domain_list.yview)
        self.cookie_tr_bar.place(x=510,y=220,anchor='nw',height = 160)
        c_cookie = Tkinter.Checkbutton(self.root,text = "Cookie", offvalue = 0, height = 1, width = 5,
                                       command = self.change_cookie_check_state)
        c_cookie.place(x = 170, y = 190)
        
        c_agent = Tkinter.Checkbutton(self.root,text = "Agent", offvalue = 0, height = 1, width = 5,
                                       command = self.change_agent_check_state)
        c_agent.place(x = 240, y = 190)
        #显示选中输出
        self.outputLabel.place( x = 0, y = 560)
       
        #root主循环
        self.root.mainloop()

if __name__ == '__main__':
    ui = UI()
    ui.run()
