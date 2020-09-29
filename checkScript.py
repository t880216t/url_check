#-*-coding:utf-8-*-
import requests,xlrd,time
from requests.adapters import HTTPAdapter
from common import emailCommon
from common.HTMLBuilder import HTMLBuilder

some_urls = [
    'https://www.eda.admin.ch/countries/china/en/home.html',
    'https://www.eda.admin.ch/eda/en/home/reps/asia/vchn/embbei.html',
    'https://www.shangri-la.com/cn/',
    'https://www.jal.co.jp/en/',
    'https://www.united.com/en/us',
]

class Check():
    def __init__(self,data_path,templete_path):
        self.report = []
        self.data_path = data_path
        self.templete_path = templete_path
        requests.packages.urllib3.disable_warnings()
        self.s = requests.Session()

        self.s.mount('http://', HTTPAdapter(max_retries=2))
        self.s.mount('https://', HTTPAdapter(max_retries=2))

    def check_url(self, data, proxy1=None,proxy2=None):
        proxies1 = {'http': proxy1, 'https': proxy1}
        proxies2 = {'http': proxy2, 'https': proxy2}
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
        }
        statusCode = 0
        if data['check_url'] in some_urls:
            headers = {
                'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'upgrade-insecure-requests': '1',
            }
        try:
            try:
                try:
                    print('正在校验：', data['id'])
                    # res = self.s.get(data['check_url'], proxies=proxies, verify=False,timeout=30)
                    res = self.s.get(data['check_url'].replace(' ',''),headers=headers, verify=False,timeout=15,allow_redirects=False)
                    if res.status_code >= 400:
                        print('换代理')
                        raise NameError('oops!')
                except:
                    print('这个链接走的了代理1',data)
                    res = self.s.get(data['check_url'].replace(' ',''),headers=headers,proxies=proxies1, verify=False, timeout=15,allow_redirects=False)
                    if res.status_code >= 400:
                        print('换代理')
                        raise NameError('oops!')
            except:
                print('这个链接走的了代理2',data)
                print('链接:',data['check_url'])
                res = self.s.get(data['check_url'].replace(' ',''),headers=headers, proxies=proxies2, verify=False, timeout=15,allow_redirects=False)
                if res.status_code >= 400:
                    print('换代理')
                    raise NameError('oops!')
            report_data = data
            report_data['status_code'] = res.status_code
            report_data['request_time'] = round(res.elapsed.total_seconds(), 2)
            if res.status_code < 400:
                report_data['status'] = 1
            else:
                report_data['status'] = 2
            self.report.append(report_data)
        except Exception as e:
            print(e)
            print('这个链接哪都不行', data)
            report_data = data
            report_data['status'] = 3
            report_data['status_code'] = 0
            report_data['request_time'] = 0
            self.report.append(report_data)

    def read_data(self,path):
        data = xlrd.open_workbook(path)
        testData = data.sheet_by_name(u'data')
        n_of_rows = testData.nrows
        listData = []
        for i in range(1, n_of_rows):
            listData.append({
                "id": int(testData.row_values(i)[0]),
                "page_name": testData.row_values(i)[1],
                "page_url": testData.row_values(i)[2],
                "check_name": testData.row_values(i)[3],
                "check_url": testData.row_values(i)[4],
                "dep": int(testData.row_values(i)[5]),
            })

        depData = data.sheet_by_name(u'dep_config')
        dep_n_of_rows = depData.nrows
        depListData = []
        for i in range(1, dep_n_of_rows):
            depListData.append({
                "id": int(depData.row_values(i)[0]),
                "name": depData.row_values(i)[1],
                "owner": depData.row_values(i)[2],
                "cc_user": depData.row_values(i)[3],
                "report_type": depData.row_values(i)[4],
            })

        proxyData = data.sheet_by_name(u'proxy_config')
        # 目前只取前2个代理
        proxy1 = proxyData.row_values(1)[2]
        proxy2 = proxyData.row_values(2)[2]

        mailConfig = data.sheet_by_name(u'mail_config')
        mailConfigData = {
            'mail_server':mailConfig.row_values(1)[0],
            'user_name':mailConfig.row_values(1)[1],
            'user_password':mailConfig.row_values(1)[2],
            'mail_From_user':mailConfig.row_values(1)[3],
            'mail_From':mailConfig.row_values(1)[4],
            'mail_subject':mailConfig.row_values(1)[5],
            'admin_user':mailConfig.row_values(1)[6],
            'admin_cc_user':mailConfig.row_values(1)[7],
            'run_time':mailConfig.row_values(1)[8],
        }

        return listData,depListData,proxy1,proxy2,mailConfigData

    def main(self):
        exc_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        start_time = time.time()
        testData, depListData,proxy1,proxy2,mailConfigData = self.read_data(self.data_path)
        for item in testData:
            self.check_url(item,proxy1,proxy2)
        end_time = time.time()
        dur_time = end_time - start_time
        dur_time_str = '{:.0f}分 {:.0f}秒'.format(dur_time // 60, dur_time % 60)
        total_count = len(self.report)
        fail_count = 0
        for item in self.report:
            if item['status'] != 1:
                fail_count += 1
            for dep_item in depListData:
                if item['dep'] == dep_item['id']:
                    item['dep_name'] = dep_item['name']
                    item['owner'] = dep_item['owner']
        # 总测试报告
        totalMailConfigData = {
            'mail_server': mailConfigData['mail_server'],
            'user_name': mailConfigData['user_name'],
            'user_password': mailConfigData['user_password'],
            'mail_From_user': mailConfigData['mail_From_user'],
            'mail_From': mailConfigData['mail_From'],
            'mail_subject': str('{mail_subject}--总览').format(mail_subject=mailConfigData['mail_subject']),
            'mail_to_user': mailConfigData['admin_user'].split(','),
            'mail_cc_user': mailConfigData['admin_cc_user'].split(','),
        }
        report_data = {
            'exc_date':exc_date,
            'exc_dun_time':dur_time_str,
            'exc_status':'总计'+ str(total_count)+' 失败 '+ str(fail_count),
            'fail_percent':round(fail_count/total_count, 2),
            'report_data':self.report,
        }
        report_name = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime())
        out_path = 'report/'+report_name+'index.html'
        Builder = HTMLBuilder(report_data, out_path,self.templete_path,totalMailConfigData)
        Html_content = Builder.main()
        emailCommon.Send_Mail(Html_content,out_path,totalMailConfigData)
        # 分部门发送给负责人
        for dep in depListData:
            report_name = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())
            out_path = 'report/' + report_name + 'index.html'
            dep_report_data = [item for item in self.report if item['dep'] == dep['id']]
            if len(dep_report_data) == 0:
                print('该部门没有外链任务:',dep['name'])
                continue
            dep_fail_count = [item for item in dep_report_data if item['status'] != 1]
            if dep['report_type'] == 1 and len(dep_fail_count) == 0:
                print('该部门只有链接报错时才发邮件')
                continue
            dep_report = {
                'exc_date': exc_date,
                'exc_dun_time': dur_time_str,
                'exc_status': '总计' + str(len(dep_report_data)) + ' 失败 ' + str(len(dep_fail_count)),
                'fail_percent': round(len(dep_fail_count) / len(dep_report_data), 2),
                'report_data': dep_fail_count,
            }
            depTotalMailConfigData = {
                'mail_server': mailConfigData['mail_server'],
                'user_name': mailConfigData['user_name'],
                'user_password': mailConfigData['user_password'],
                'mail_From_user': mailConfigData['mail_From_user'],
                'mail_From': mailConfigData['mail_From'],
                'mail_subject': mailConfigData['mail_subject'] + '--'+dep['name'],
                'mail_to_user': dep['owner'].split(','),
                'mail_cc_user': dep['cc_user'].split(','),
            }
            Builder = HTMLBuilder(dep_report, out_path, self.templete_path,depTotalMailConfigData)
            Html_content = Builder.main()
            emailCommon.Send_Mail(Html_content, out_path,depTotalMailConfigData)
            time.sleep(1)


if __name__ == '__main__':
    Check = Check('data/url_data.xls','templete/templete.html')
    Check.main()