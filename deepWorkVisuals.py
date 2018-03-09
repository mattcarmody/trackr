import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

from getDate import get_date

def deepWork_weekly_visuals(cur):
    DEEP_WORK_TARGET = 15
    week_Date = []
    week_Prog = []
    week_Web = []
    
    # Set dates for the previous week
    for i in range(7, 0, -1):
        week_Date.append(get_date(i))
    
    # Pull db data for those dates
    for date in week_Date:
        cur.execute("SELECT Programming, WebDevelopment FROM deepWork WHERE Date = ?", (date,))
        raw_data = cur.fetchone()
        week_Prog.append(raw_data[0])
        week_Web.append(raw_data[1])
    
    # Sum over the week    
    sum_Prog = [week_Prog.pop(0)]
    sum_Web = [week_Web.pop(0)]
    for i in range(len(week_Prog)):
        sum_Prog.append(sum_Prog[i] + week_Prog[i])
        sum_Web.append(sum_Web[i] + week_Web[i])
    
    # Create stackplot
    plt.figure(3, figsize=(20,10))
    plt.subplot()
    labels = ["Programming", "Web Development"]
    colors = ['m', 'b']
    plt.stackplot(week_Date, sum_Prog, sum_Web, labels=labels, colors=colors)
    plt.legend(loc=2)
    plt.xlabel("Date")
    plt.ylabel("Total Hours")
    plt.title("Deep Work this Week")
    plt.plot([0, 6], [DEEP_WORK_TARGET/7, DEEP_WORK_TARGET], 'k-', lw=1)
    plt.show()
    
