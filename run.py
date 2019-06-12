#-*-coding:utf-8-*-
import schedule,subprocess,time
from checkScript import Check

def start_job():
    subprocess.call("python checkScript.py ",shell=True)


if __name__ == "__main__":
    Check = Check('data/url_data.xls', 'templete/templete.html')
    testData, depListData, proxy1, proxy2, mailConfigData = Check.read_data(Check.data_path)
    runTime = mailConfigData['run_time']
    if runTime:
        print("定时时任务开始：", runTime)
        schedule.every().day.at(str(runTime)).do(start_job)

        while True:
            schedule.run_pending()
            time.sleep(1)