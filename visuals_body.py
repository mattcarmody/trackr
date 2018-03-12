import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import os

from getDate import get_date

def body_week_visuals(cur):
    #BODY_TARGET = 0
    week_Date = []
    week_stretch = []
    week_core = []
    week_pullup = []
    week_cardio = []
    
    # Set dates for the previous week
    for i in range(7, 0, -1):
        week_Date.append(get_date(i))
    
    # Pull db data for those dates
    for date in week_Date:
        cur.execute("SELECT Stretching, Core, PullUps, Cardio FROM body WHERE Date = ?", (date,))
        raw_data = cur.fetchone()
        week_stretch.append(raw_data[0])
        week_core.append(raw_data[1])
        week_pullup.append(raw_data[2])
        week_cardio.append(raw_data[3])
    
    # Create stacked bar chart
    week_core_pullup = []
    week_cps = []
    for i in range(len(week_stretch)):
        week_core_pullup.append(week_core[i] + week_pullup[i])
        week_cps.append(week_core[i] + week_pullup[i] + week_stretch[i])
    
    plt.figure(4, figsize=(20,10))
    p1 = plt.bar(week_Date, week_core, color='m')
    p2 = plt.bar(week_Date, week_pullup, bottom=week_core, color='b')
    p3 = plt.bar(week_Date, week_stretch, bottom=week_core_pullup, color='g')
    p4 = plt.bar(week_Date, week_cardio, bottom=week_cps, color='k')
    plt.subplot()
    
    plt.legend((p1[0], p2[0], p3[0], p4[0]), ("Core", "Pull ups", "Stretching", "Cardio"))
    plt.xlabel("Date")
    plt.ylabel("Minutes or Repetitions")
    plt.title("Body Work this Week")
    #plt.plot([0, 6], [BODY_TARGET/7, BODY_TARGET], 'k-', lw=1)
    plt.show()
    #plt.savefig("/home/matt/Pictures/trackr/body_visual.jpg")
    #os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-uri file:///home/matt/Pictures/trackr/body_visual.jpg")
