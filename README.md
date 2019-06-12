# 简介
大部分的网站都会有一些相关行业的外部链，这些一般是由相关模块的运营部门提供的，但是这些第三方链接可用性我们很难去保证。如果用户从我们这边点击了不可用的外链，也会对我们的服务产生质疑。因此开发了这个外链可用性监控系统。

# 框架
其实原理很简单，利用python requests库，加上一些超时、重试、切换代理的方式去多次检查链接的可用性，以保证报告的准确性。结合富文本邮件，并Email提供给相关人员报告展示。
数据我选择放在Excel里是为了降低系统的复杂度，主要是对接的运营人员都是Excel提供数据 ，你也可以改装下放数据库。
### 整体的架构
![url_check.jpg](https://upload-images.jianshu.io/upload_images/17067099-cf74e2394ad6a07c.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 工程结构
``` bash
├── common
│   ├── emailCommon.py     # 邮件发送模块
│   └── HTMLBuilder.py       # HTML报告生成模块
├── data
│   └── url_data.xls              # 测试&配置数据
├── templete
│   └── templete.html           # HTML模板
├── venv                              # 虚拟环境
├── .gitignore                       # 提交过滤模板
├── checkScript.py              # 检查核心脚本
├── requirements.txt            # 模块依赖说明
└── run.py                            # 启动脚本
```
# 功能点
- 定时执行检查任务
- 邮件及部门通知人可配置
- 支持2个以下的额外网络代理检查
- 是否只在失败时通知部门负责人可配置
- 测试报告邮件相关人员
# 报告
### 总览报告
![TM20190612143713.png](https://upload-images.jianshu.io/upload_images/17067099-47cdcb26cd2fd774.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
### 出错收到的报告
![TM20190612143822.png](https://upload-images.jianshu.io/upload_images/17067099-8b96fd0a013f8ceb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 配置
## 文件字段说明
系统中的配置信息都在url_data.xls的各个sheet中，其实就相当于数据库的各个表。
![TM20190612141442.png](https://upload-images.jianshu.io/upload_images/17067099-269add482c29d23d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
url_data.xls > mail_config    # 邮件及定时任务配置
- mail_server    # 邮件服务器
- user_name    # 发件人账号
- user_password    # 发件人密码
- mail_From_user    # 邮件中显示的发件人名
- mail_From    # 邮件中显示的发件人邮箱
- mail_subject   # 邮件标题
- admin_user   # 系统管理员邮箱（总览报告通知人）
- admin_cc_user   # 系统报告抄送人邮箱（总览报告通知人）
- run_time   # 定时任务启动时间

![TM20190612141713.png](https://upload-images.jianshu.io/upload_images/17067099-3136898f3e6c433c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
url_data.xls > proxy_config    # 可用代理配置
- id   # 序号
- name   # 代理名
- proxy    # 代理配置（可配置账号密码）

![TM20190612142002.png](https://upload-images.jianshu.io/upload_images/17067099-154b76e5c3b77237.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
url_data.xls > dep_config    # 部门配置
- id   # 部门ID（URL的所属用的）
- name   # 部门名称
- owner    # 部门负责人
- cc    # 抄送人
- report_type     # 是否只有出错时才通知（1.只有出错时通知，0.都会通知）
![TM20190612142559.png](https://upload-images.jianshu.io/upload_images/17067099-7a0945987c2187f7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

url_data.xls > data      # 部门配置
- id    # 序号
- page_name    # 检查的链接所属的页面名称
- page_url    # 检查的链接所属的页面链接
- check_name    # 检查的链接的名称（暂时没用，报告中直接显示了检查的URL）
- check_url    # 被检查的链接
- dep   # 所属的部门

## 安装依赖
系统是基于py3写的，使用的虚拟环境，具体用啥你随意。
``` bash
$ pip install -r requirements.txt
```

## 启动系统
``` bash
$ python run.py
```
