import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

def deepWork_weekly_visuals(cur):
    DEEP_WORK_TARGET = 15
    week_Date = []
    week_Prog = []
    week_Web = []
    
    # Pull week's db data 
    # TODO: Pull the right data after the first week
    cur.execute("SELECT * FROM deepWork ORDER BY Date ASC LIMIT 7")
    raw_data = cur.fetchall()
    
    for i in range(len(raw_data)):
        week_Date.append(raw_data[i][0])
        week_Prog.append(raw_data[i][1])
        week_Web.append(raw_data[i][2])
        
    # Use first day as 0 point
    sum_Prog = [week_Prog.pop(0)]
    sum_Web = [week_Web.pop(0)]
    for i in range(len(week_Prog)):
        sum_Prog.append(sum_Prog[i] + week_Prog[i])
        sum_Web.append(sum_Web[i] + week_Web[i])
    
    plt.figure(3)
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
    
