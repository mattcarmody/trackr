# Create visuals on regular intervals (week, month, quarter, year)

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

def duolingo_weekly_visuals(cur):
    # Pull all Duo data for hardcoded languages
    DUO_WEEKLY_TARGET = 300
    week_Date = []
    week_Esperanto = []
    week_Spanish = []
    week_Portuguese = []
    sql = 'SELECT Date, Esperanto, Portuguese, Spanish FROM duolingo ORDER BY Date DESC LIMIT 8'
    cur.execute(sql)
    raw_data = cur.fetchall()
    for i in range(len(raw_data)):
        week_Date.append(raw_data[i][0])
        week_Esperanto.append(raw_data[i][1])
        week_Portuguese.append(raw_data[i][2])
        week_Spanish.append(raw_data[i][3])
    
    week_Date.pop()  
    start_Esperanto = week_Esperanto.pop()     
    start_Portuguese = week_Portuguese.pop()
    start_Spanish = week_Spanish.pop()
    for i in range(len(week_Date)):
        week_Esperanto[i] -= start_Esperanto
        week_Portuguese[i] -= start_Portuguese
        week_Spanish[i] -= start_Spanish
    
    # Stackplot w/ target line
    fig, ax = plt.subplots()
    labels = ["Esperanto", "Spanish", "Portuguese"]
    colors = ['g', 'r', 'y']
    ax.stackplot(week_Date, week_Esperanto, week_Spanish, week_Portuguese, labels=labels, colors=colors)
    ax.legend(loc=2)
    plt.xlabel("Date")
    plt.ylabel("Total Points")
    plt.title("Duolingo this Week")
    plt.plot([0, 6], [DUO_WEEKLY_TARGET/7, DUO_WEEKLY_TARGET], 'k-', lw=1)
    plt.show()
    
