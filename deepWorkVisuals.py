import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import os

from getDate import get_date

def deepWork_week_visuals(cur):
    DEEP_WORK_TARGET = 15
    week_Date = []
    week_Prog = []
    week_Web = []
    week_Excel = []
    week_Apps = []
    
    # Set dates for the previous week
    for i in range(7, 0, -1):
        week_Date.append(get_date(i))
    
    # Pull db data for those dates
    for date in week_Date:
        cur.execute("SELECT Programming, WebDevelopment, Excel, Applications FROM deepWork WHERE Date = ?", (date,))
        raw_data = cur.fetchone()
        week_Prog.append(raw_data[0])
        week_Web.append(raw_data[1])
        week_Excel.append(raw_data[2])
        week_Apps.append(raw_data[3])
    
    # Sum over the week    
    sum_Prog = [week_Prog.pop(0)]
    sum_Web = [week_Web.pop(0)]
    sum_Excel = [week_Excel.pop(0)]
    sum_Apps = [week_Apps.pop(0)]
    for i in range(len(week_Prog)):
        sum_Prog.append(sum_Prog[i] + week_Prog[i])
        sum_Web.append(sum_Web[i] + week_Web[i])
        sum_Excel.append(sum_Excel[i] + week_Excel[i])
        sum_Apps.append(sum_Apps[i] + week_Apps[i])
    
    # Create stackplot
    plt.figure(3, figsize=(20,10))
    plt.subplot()
    labels = ["Programming", "Web Development", "Excel", "Job Applications"]
    colors = ['m', 'b', 'g', 'k']
    plt.stackplot(week_Date, sum_Prog, sum_Web, sum_Excel, sum_Apps, labels=labels, colors=colors)
    plt.legend(loc=2)
    plt.xlabel("Date")
    plt.ylabel("Total Hours")
    plt.title("Deep Work this Week")
    plt.plot([0, 6], [DEEP_WORK_TARGET/7, DEEP_WORK_TARGET], 'k-', lw=1)
    #plt.show()
    plt.savefig("/home/matt/Pictures/trackr/deep_work_visual.jpg")
    os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-uri file:///home/matt/Pictures/trackr/deep_work_visual.jpg")
    print("Changed background image.")
