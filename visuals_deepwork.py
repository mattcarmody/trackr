import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import os

from date_related import get_date

def set_dates(week_date):
    for i in range(7, 0, -1):
        week_date.append(get_date(i))
    return week_date
    
def pull_data(cur, week_date, week_prog, week_web, week_excel, week_apps):
    for date in week_date:
        cur.execute("SELECT Programming, WebDevelopment, Excel, Applications FROM deepWork WHERE Date = ?", (date,))
        raw_data = cur.fetchone()
        week_prog.append(raw_data[0])
        week_web.append(raw_data[1])
        week_excel.append(raw_data[2])
        week_apps.append(raw_data[3])
    return week_prog, week_web, week_excel, week_apps
    
def sum_weeks_data(week_prog, week_web, week_excel, week_apps):
    sum_prog = [week_prog.pop(0)]
    sum_web = [week_web.pop(0)]
    sum_excel = [week_excel.pop(0)]
    sum_apps = [week_apps.pop(0)]
    for i in range(len(week_prog)):
        sum_prog.append(sum_prog[i] + week_prog[i])
        sum_web.append(sum_web[i] + week_web[i])
        sum_excel.append(sum_excel[i] + week_excel[i])
        sum_apps.append(sum_apps[i] + week_apps[i])
    return sum_prog, sum_web, sum_excel, sum_apps
    
def create_stackplot(target, week_date, sum_prog, sum_web, sum_excel, sum_apps):
    plt.figure(3, figsize=(20,10))
    plt.subplot()
    labels = ["Programming", "Web Development", "Excel", "Job Applications"]
    colors = ['m', 'b', 'g', 'k']
    plt.stackplot(week_date, sum_prog, sum_web, sum_excel, sum_apps, labels=labels, colors=colors)
    plt.legend(loc=2)
    plt.xlabel("Date")
    plt.ylabel("Total Hours")
    plt.title("Deep Work this Week")
    plt.plot([0, 6], [target/7, target], 'k-', lw=1)
    plt.show(block=True)
    plt.close()
    
    # OR set plot to background image
    #plt.savefig("/home/matt/Pictures/trackr/deep_work_visual.jpg")
    #os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-uri file:///home/matt/Pictures/trackr/deep_work_visual.jpg")
    #print("Changed background image.")

def deepwork_week_visuals(cur):
    DEEP_WORK_TARGET = 15
    week_Date = []
    week_Prog = []
    week_Web = []
    week_Excel = []
    week_Apps = []
    
    week_Date = set_dates(week_Date)
    week_Prog, week_Web, week_Excel, week_Apps = pull_data(cur, week_Date, week_Prog, week_Web, week_Excel, week_Apps) 
    sum_Prog, sum_Web, sum_Excel, sum_Apps = sum_weeks_data(week_Prog, week_Web, week_Excel, week_Apps)
    create_stackplot(DEEP_WORK_TARGET, week_Date, sum_Prog, sum_Web, sum_Excel, sum_Apps)
    
