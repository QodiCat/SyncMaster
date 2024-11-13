# upload.py
import requests  


class UploadPic:  
    def __init__(self, cookie):  
        self.cookie = cookie  
  
        # 解析  
        self.file_path = ''  
        self.img_type = ''  
  
        # 两个请求体  
        self.upload_data = {}  
        self.csdn_data = {}  
        self.output_url = ''  
  
    def _get_file(self, file_path):  
        with open(file_path, mode='rb') as f:  
            binary_data = f.read()  
        return binary_data  
  
    def _upload_request(self):  
        headers = {  
            'accept': '*/*',  
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',  
            'content-type': 'application/json',  
            'cookie': self.cookie,  
            'origin': 'https://editor.csdn.net',  
            'priority': 'u=1, i',  
            'referer': 'https://editor.csdn.net/',  
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',  
            'sec-ch-ua-mobile': '?0',  
            'sec-ch-ua-platform': '"Windows"',  
            'sec-fetch-dest': 'empty',  
            'sec-fetch-mode': 'cors',  
            'sec-fetch-site': 'same-site',  
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',  
        }  
  
        params = {  
            'type': 'blog',  
            'rtype': 'markdown',  
            'x-image-template': '',  
            'x-image-app': 'direct_blog',  
            'x-image-dir': 'direct',  
            'x-image-suffix': self.img_type,  
        }  
  
        url = 'https://imgservice.csdn.net/direct/v1.0/image/upload'  
  
        response = requests.get(url, params=params, headers=headers)  
        try:  
            self.upload_data = response.json()  
        except Exception as e:  
            return e  
  
    def _csdn_request(self):  
        headers = {  
            'Accept': 'application/json, text/javascript, */*; q=0.01',  
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',  
            'Connection': 'keep-alive',  
            'Origin': 'https://editor.csdn.net',  
            'Referer': 'https://editor.csdn.net/',  
            'Sec-Fetch-Dest': 'empty',  
            'Sec-Fetch-Mode': 'cors',  
            'Sec-Fetch-Site': 'cross-site',  
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',  
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',  
            'sec-ch-ua-mobile': '?0',  
            'sec-ch-ua-platform': '"Windows"',  
        }  
  
        files = {  
            'key': (None, self.upload_data['data']['filePath']),  
            'policy': (None, self.upload_data['data']['policy']),  
            'OSSAccessKeyId': (None, self.upload_data['data']['accessId']),  
            'success_action_status': (None, '200'),  
            'signature': (None, self.upload_data['data']['signature']),  
            'callback': (None, self.upload_data['data']['callbackUrl']),  
            'file': (f'image.{self.img_type}', self._get_file(self.file_path), f'image/{self.img_type}'),  
        }  
  
        url = 'https://csdn-img-blog.oss-cn-beijing.aliyuncs.com/'  
  
        response = requests.post(url, headers=headers, files=files)  
        try:  
            self.csdn_data = response.json()  
            self.output_url = self.csdn_data['data']['imageUrl']  
        except Exception as e:  
            return e  
  
    def upload_image(self, file_path):  
        self.file_path = file_path  
        self.img_type = self.file_path.split('.')[-1]  
  
        exception_1 = self._upload_request()  
        assert exception_1 is None, exception_1  
        exception_2 = self._csdn_request()  
        assert exception_2 is None, exception_2  
  
        return self.output_url  
  
  
if __name__ == '__main__':  
    cookie = 'UN=Q52099999; c_ins_um=-; c_ins_prid=1708649472616_269269; c_ins_rid=1710250689358_949706; c_ins_fref=https://blog.csdn.net/u010835747/article/details/121252314; c_ins_fpage=/index.html; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22Q52099999%22%2C%22scope%22%3A1%7D%7D; cf_clearance=YrlGXGh8qNoeTYI0OEy1BsILQN_8XT3bD.M03o5jVws-1715134849-1.0.1.1-0q8r0pPnHLXwi_eRhcdfGuWGCL4spMwnwbu.e8vH8S_dRumkhdZ6lSRxJauR6unZyC1OuhlVq_dAxeXd3uzMfA; cf_clearance=fk3tSqJxzQ15DusgYVnTzwtpT72EitN7OqIuZAvk4ww-1716780615-1.0.1.1-vn43XgP3YnfiosYp7ymUaeJBm.t4Nil8NPZ7QYHGbK_cVr45rBiE6BkK5ztVOp6RdLU4L.BGCQERrX9ugGHbNw; uuid_tt_dd=10_21307064330-1718440442086-271038; __gads=ID=8f0e423301ccd243:T=1719708239:RT=1720184132:S=ALNI_Mbn_NlvBA-rJQr0zn8ubpcqQ3gR0Q; __gpi=UID=00000e6c22e1c1f4:T=1719708239:RT=1720184132:S=ALNI_Ma5ti8PKRm0U1DIKzU7PiqPMulmQg; __eoi=ID=04ab73f6c18c09b5:T=1719151077:RT=1720184132:S=AA-AfjZhM7FP1u2WtbnTvsRvrCgc; fid=20_19291140282-1723286679960-561069; c_adb=1; csdn_newcert_Q52099999=1; p_uid=U010000; Q52099999comment_new=1729652707075; _gid=GA1.2.1239923813.1731322574; _ga_7W1N0GEY1P=GS1.1.1731382876.13.0.1731382876.60.0.0; is_advert=1; firstDie=1; creative_btn_mp=3; _clck=14d77ga%7C2%7Cfqu%7C0%7C1546; _ga_JJBD2VG1H7=GS1.1.1731463151.5.0.1731463151.60.0.0; _ga=GA1.2.470733722.1728052844; FCNEC=%5B%5B%22AKsRol_oPX4LaKx1wL26ZX7RcL21YEwd-cvayzaQsfOOvNRDVGCaog7ho0LsAkkC7F2K1e0qyVTvcv09PD6qLNZ40gOxAAx9J1tJLECu_AElrT8vKtEE4Mq9IMuWhmbckRGLSTdgqD6ZLHhO8rTpdA2wbZKWhwl0AQ%3D%3D%22%5D%5D; ssxmod_itna=eqRxRQDQe7qiqBKK0dy7tGGOKUvruDAKUoYqQD/KevDnqD=GFDK40EoO5DCbIQbQ32tYEepiuNrQbj4b++w7UbnhW=Z1x0aDbqGkh0G4ii9DCeDIDWeDiDG+=DFxYoDe=sQDF7dytz9DYPDWxDFj=Kiom0koDDz3fBYCDi3ja5HDY5Dpx07DivKc=0DjxG1DQ5Dsobfd4DCfR84MaHAwtO3Ix0kS40OD0IIj=vHC4GdXcy1w=gNtm+xtQhNKjue+j45MiGqYZ0NQD2KFD2DA7DiMD+qhmcn7Q=Di2DxVGhDD; ssxmod_itna2=eqRxRQDQe7qiqBKK0dy7tGGOKUvruDAKUoYqG9iO7ODBLG2D7P6g9yxwmgxDCSpT2j1ehBbewzqI1Wehpx1=8IAz5uWTf=zPCxmoqr0WRCitpD822aRubk=qQ90ptQ6=gfusW=6uYZIO5x2kVrBkjo5WEaBtU7T8VE2Wo9K=1Zb8Q2wK+g+munPphRwIV7AWL2BGGfqWgrDA8BDWKDcDw6F49ibkLExiemgjl9nhGt4WjieE+A7OoDfYVccrExWADUEA62qy8iLdsvHt1dyyVZbSzdAWsy3l6u6CCtNk/mGnjVuBE4YM4hVBINlhxKYTAmlRP4MhNKYRmywFBxgIc8YD1vx0byehYKDmbpizqURr9KGOzYa9WCzhKbvSi4=9caixDKq4VBGq2DrDFQovKeKQEviBvZisD7=DYF4eD===; tfstk=fMBojDv7J_RSunGDmSJ7TeTWsNVYV09BbwHpJpLUgE8bAppRetYhuZHJywE5npjCrBWJyy1hiZbipU-paZvhxGSRewE5oMSOJpIJy9n5GNIZeTFWpvvWdpzTWReTVg9BLSZEBj0Wghts4JLyahDNDBaTWRevyerUVPQJ8wYqoHT24HlrUov2vH9E8H7euI-wX4JF8prDg3tZT38yzEk2jE8eLp7F0X1sOeWF_tzJ2aiT-6_Fn3A4Mg84IgB2qL8N4TDELf-kZFSyuPNCKCAVABXIAvA541_BbauzWQsFiZxkK-hyQifFSUIuabjXEUANTIqzUivkrCBDMDcyE675KQ1oAls2UZ165QPblnXRBBY6iqzPDiYys6b8lv8Rsi7D6t3xBp_fTw-hu4jPkjlZwJkB0kBqOXOycnY9Dyl4RdKqfPr0m4v2ant6WoqmOXOycnYTmo0l_Q-XfFC..; toolbar_remind_num=3; dc_session_id=10_1731482684159.286978; c_segment=14; dc_sid=775960218748c31622a0c69db0ec3a69; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1731456141,1731463151,1731464234,1731482687; HMACCOUNT=6D489A8A92F6EC0D; SESSION=f4030c41-eee9-4e2b-8b53-a760cae87c2f; hide_login=1; UserName=Q52099999; UserInfo=09333075d29745c0b74eaf3f2952a8d1; UserToken=09333075d29745c0b74eaf3f2952a8d1; UserNick=Qodicat; AU=407; BT=1731482714140; c_pref=default; c_ref=default; c_first_ref=default; c_first_page=https%3A//blog.csdn.net/u010835747/article/details/121252314; c_dsid=11_1731484316932.150612; c_page_id=default; log_Id_pv=8; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1731484318; log_Id_click=6; _clsk=8reme0%7C1731484319384%7C3%7C0%7Cv.clarity.ms%2Fcollect; creativeSetApiNew=%7B%22toolbarImg%22%3A%22https%3A//img-home.csdnimg.cn/images/20230921102607.png%22%2C%22publishSuccessImg%22%3A%22https%3A//img-home.csdnimg.cn/images/20240229024608.png%22%2C%22articleNum%22%3A195%2C%22type%22%3A2%2C%22oldUser%22%3Atrue%2C%22useSeven%22%3Afalse%2C%22oldFullVersion%22%3Atrue%2C%22userName%22%3A%22Q52099999%22%7D; log_Id_view=235; dc_tos=smvpww' 
    # 输入你的cookie  
    upload = UploadPic(cookie)  
    output_url = upload.upload_image('1.jpg')  #输入你需要上传的文件位置
    print(output_url)