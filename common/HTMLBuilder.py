#-*-coding:utf-8-*-
from bs4 import BeautifulSoup

class HTMLBuilder():
    def __init__(self,report,path,templete_path,mailConfigData):
        self.report = report
        self.path = path
        self.mailConfigData = mailConfigData
        self.codeMessage = {
          200: '服务器成功返回请求的数据。',
          201: '新建或修改数据成功。',
          202: '一个请求已经进入后台排队（异步任务）。',
          204: '删除数据成功。',
          301: '请求地址被永久重定向。',
          302: '请求地址被临时重定向。',
          400: '发出的请求有错误，服务器没有进行新建或修改数据的操作。',
          401: '用户没有权限（令牌、用户名、密码错误）。',
          403: '用户得到授权，但是访问是被禁止的。',
          404: '发出的请求针对的是不存在的记录，服务器没有进行操作。',
          406: '请求的格式不可得。',
          410: '请求的资源被永久删除，且不会再得到的。',
          422: '当创建一个对象时，发生一个验证错误。',
          500: '服务器发生错误，请检查服务器。',
          502: '网关错误。',
          503: '服务不可用，服务器暂时过载或维护。',
          504: '网关超时。',
          0: '请求无响应，无法访问。',
        }
        with open(templete_path,'r') as foo_file :
            self.soup_foo = BeautifulSoup(foo_file, "html.parser")

    def set_header(self):
        title = self.soup_foo.find(attrs={"id": "title"})
        title.string = self.mailConfigData['mail_subject']

        #执行日期
        exc_date = self.soup_foo.find(attrs={"id":"exc_date"})
        new_strong_tag = self.soup_foo.new_tag("strong")
        new_strong_tag.string = '执行日期：'+ self.report['exc_date']
        exc_date.append(new_strong_tag)

        # 执行日期
        exc_dun_time = self.soup_foo.find(attrs={"id": "exc_dun_time"})
        new_strong_tag = self.soup_foo.new_tag("strong")
        new_strong_tag.string = '测试耗时：' + self.report['exc_dun_time']
        exc_dun_time.append(new_strong_tag)

        # 执行日期
        exc_status = self.soup_foo.find(attrs={"id": "exc_status"})
        new_strong_tag = self.soup_foo.new_tag("strong")
        new_strong_tag.string = '执行结果：' + self.report['exc_status']
        exc_status.append(new_strong_tag)

        # 饼图百分比由于邮件兼容问题，暂时屏蔽
        # pie = self.soup_foo.find(attrs={"id": "pie"})
        # pie['data'] = self.report['fail_percent']
        # if self.report['fail_percent'] == 0:
        #     pie['style'] = 'display:none'
        # else:
        #     pie['style'] = 'animation-delay:-%ss'%self.report['fail_percent']

        # report正文
        result_table = self.soup_foo.find(attrs={"id": "result_table"})
        if len(self.report['report_data']) > 0 :
            for item in self.report['report_data']:
                if item['status'] == 1:
                    new_tr_tag = self.soup_foo.new_tag("tr",attrs={'class':'passClass'})
                else:
                    new_tr_tag = self.soup_foo.new_tag("tr", attrs={'class': 'failClass'})

                td_id_tag = self.soup_foo.new_tag("td")
                td_id_tag.string = str(item['id'])

                td_page_tag = self.soup_foo.new_tag("td",attrs={'class':'url_text','style':'max-width:200px;width: 200px;overflow: hidden;text-overflow: ellipsis;white-space: nowrap;'})
                td_page_a_tag = self.soup_foo.new_tag("a",attrs={'title':item['page_url'],'href':item['page_url'],'target':'_blank'})
                td_page_a_tag.string = item['page_name']
                td_page_tag.append(td_page_a_tag)

                td_check_tag = self.soup_foo.new_tag("td", attrs={'class': 'url_text','style':'max-width:200px;width: 200px;overflow: hidden;text-overflow: ellipsis;white-space: nowrap;'})
                td_check_a_tag = self.soup_foo.new_tag("a",
                                                      attrs={'title': item['check_url'], 'href': item['check_url'],'target':'_blank'})
                td_check_a_tag.string = item['check_url']
                td_check_tag.append(td_check_a_tag)

                td_dep_tag = self.soup_foo.new_tag("td")
                td_dep_tag.string = item['dep_name']

                td_owner_tag = self.soup_foo.new_tag("td")
                td_owner_tag.string = item['owner']

                td_status_tag = self.soup_foo.new_tag("td")
                if item['status_code'] in self.codeMessage.keys():
                    td_status_tag.string = self.codeMessage[item['status_code']]
                else:
                    td_status_tag.string = str(item['status_code'])

                td_time_tag = self.soup_foo.new_tag("td")
                td_time_tag.string = str(item['request_time']) + ' s'

                new_tr_tag.append(td_id_tag)
                new_tr_tag.append(td_page_tag)
                new_tr_tag.append(td_check_tag)
                new_tr_tag.append(td_dep_tag)
                new_tr_tag.append(td_owner_tag)
                new_tr_tag.append(td_status_tag)
                new_tr_tag.append(td_time_tag)
                result_table.append(new_tr_tag)

    def write_to_Html(self):
        with open(self.path, "wb") as foo_file:
            foo_file.write(self.soup_foo.encode('utf-8'))

    def main(self):
        self.set_header()
        # self.write_to_Html()
        return self.soup_foo

if __name__ == "__main__":
    #调试代码
    report = {
        'exc_date' : '2019-05-06 00:06:00',
        'exc_dun_time' : '00:06:00',
        'exc_status' : 'Fail 2',
        'fail_percent' : 0.3,
        'report_data':[
            {
                "id":1,
                "page_name": '首页',
                "page_url": 'https://www.xxxxx.com/',
                "check_name": 'xxxx',
                "check_url": 'https://www.sgsgroup.com.cn/zh-cn/certified-clients-and-products/audited-supplier-verification',
                'dep_id':1,
                'dep_name':'客服部',
                'owner':'xxxxx@xxxxx.com',
                'status_code': 200,
                'status':1,
            },
            {
                "id": 2,
                "page_name": '首页',
                "page_url": 'https://www.xxxxxxx.com/',
                "check_name": 'xxxx',
                "check_url": 'https://www.sgsgroup.com.cn/zh-cn/certified-clients-and-products/audited-supplier-verification',
                'dep_id': 1,
                'dep_name': '客服部',
                'owner': 'xxxxx@xxxxxx.com',
                'status_code': 400,
                'status': 2,
            }
        ]
    }
    path = '../report/index.html'
    HTMLBuilder = HTMLBuilder(report,path)
    HTMLBuilder.main()
