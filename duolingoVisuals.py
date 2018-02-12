# Create visuals on regular intervals (week, bifortnight, quarter?, year)

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

# Every four weeks (12 units of 28 days & 29 days off, instead of 12 months)
def duolingo_bifortly_visuals(cur):
    DUO_BIFORT_TARGET = 1200
    bifort_Date = []
    bifort_Esperanto = []
    bifort_Portuguese = []
    bifort_Spanish = []
    
    # Pull 29 days of Duo data for hardcorded languages
    sql = 'SELECT Date, Esperanto, Portuguese, Spanish FROM duolingo ORDER BY Date DESC LIMIT 29'
    cur.execute(sql)
    raw_data = cur.fetchall()
    for i in range(len(raw_data)):
        bifort_Date.append(raw_data[i][0])
        bifort_Esperanto.append(raw_data[i][1])
        bifort_Portuguese.append(raw_data[i][2])
        bifort_Spanish.append(raw_data[i][3])
    
    # Use first day as 0 point
    bifort_Date.pop()
    start_Esperanto = bifort_Esperanto.pop()     
    start_Portuguese = bifort_Portuguese.pop()
    start_Spanish = bifort_Spanish.pop()
    for i in range(len(bifort_Date)):
        bifort_Esperanto[i] -= start_Esperanto
        bifort_Portuguese[i] -= start_Portuguese
        bifort_Spanish[i] -= start_Spanish
    
    # Stackplot w/ target line
    fig, ax = plt.subplots()
    labels = ["Esperanto", "Spanish", "Portuguese"]
    colors = ['g', 'r', 'y']
    ax.stackplot(bifort_Date, bifort_Esperanto, bifort_Spanish, bifort_Portuguese, labels=labels, colors=colors)
    ax.legend(loc=2)
    ax.set_xticks([0,7,14,21])
    ax.set_xticklabels(bifort_Date[-1::-7])
    plt.xlabel("Date")
    plt.ylabel("Total Points")
    plt.title("Duolingo this Bifort")
    plt.plot([0, 27], [DUO_BIFORT_TARGET/28, DUO_BIFORT_TARGET], 'k-', lw=1)
    plt.show()

def duolingo_weekly_visuals(cur):
    DUO_WEEKLY_TARGET = 300
    week_Date = []
    week_Esperanto = []
    week_Portuguese = []
    week_Spanish = []
    
    # Pull 8 days of Duo data for hardcoded languages
    sql = 'SELECT Date, Esperanto, Portuguese, Spanish FROM duolingo ORDER BY Date DESC LIMIT 8'
    cur.execute(sql)
    raw_data = cur.fetchall()
    for i in range(len(raw_data)):
        week_Date.append(raw_data[i][0])
        week_Esperanto.append(raw_data[i][1])
        week_Portuguese.append(raw_data[i][2])
        week_Spanish.append(raw_data[i][3])
    
    # Use first day as 0 point
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
    
