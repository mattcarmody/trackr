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
    bifort_Italian = []
    
    # Pull 29 days of Duo data for hardcorded languages
    sql = 'SELECT Date, Esperanto, Portuguese, Spanish, Italian FROM duolingo ORDER BY Date DESC LIMIT 29'
    cur.execute(sql)
    raw_data = cur.fetchall()
    for i in range(len(raw_data)):
        bifort_Date.append(raw_data[i][0])
        bifort_Esperanto.append(raw_data[i][1])
        bifort_Portuguese.append(raw_data[i][2])
        bifort_Spanish.append(raw_data[i][3])
        bifort_Italian.append(raw_data[i][4])
    
    # Use first day as 0 point
    bifort_Date.pop()
    start_Esperanto = bifort_Esperanto.pop()     
    start_Portuguese = bifort_Portuguese.pop()
    start_Spanish = bifort_Spanish.pop()
    start_Italian = bifort_Italian.pop()
    for i in range(len(bifort_Date)):
        bifort_Esperanto[i] -= start_Esperanto
        bifort_Portuguese[i] -= start_Portuguese
        bifort_Spanish[i] -= start_Spanish
        bifort_Italian[i] -= start_Italian
    
    # Stackplot w/ target line
    plt.figure(1, figsize=(20,10))
    plt.subplot()
    labels = ["Esperanto", "Spanish", "Portuguese", "Italian"]
    colors = ['g', 'r', 'y', 'b']
    plt.stackplot(bifort_Date, bifort_Esperanto, bifort_Spanish, bifort_Portuguese, bifort_Italian, labels=labels, colors=colors)
    plt.legend(loc=2)
    ax = plt.gca()
    ax.set_xticks([0,7,14,21])
    ax.set_xticklabels(bifort_Date[-1::-7])
    plt.xlabel("Date")
    plt.ylabel("Total Points")
    plt.title("Duolingo this Bifort")
    plt.plot([0, 27], [DUO_BIFORT_TARGET/28, DUO_BIFORT_TARGET], 'k-', lw=1)
    plt.show(block=True)
    plt.close()

def duolingo_weekly_visuals(cur):
    DUO_WEEKLY_TARGET = 300
    week_Date = []
    week_Esperanto = []
    week_Portuguese = []
    week_Spanish = []
    week_Italian = []
    
    # Pull 8 days of Duo data for hardcoded languages
    sql = 'SELECT Date, Esperanto, Portuguese, Spanish, Italian FROM duolingo ORDER BY Date DESC LIMIT 8'
    cur.execute(sql)
    raw_data = cur.fetchall()
    for i in range(len(raw_data)):
        week_Date.append(raw_data[i][0])
        week_Esperanto.append(raw_data[i][1])
        week_Portuguese.append(raw_data[i][2])
        week_Spanish.append(raw_data[i][3])
        week_Italian.append(raw_data[i][4])
    
    # Use first day as 0 point
    week_Date.pop()  
    start_Esperanto = week_Esperanto.pop()     
    start_Portuguese = week_Portuguese.pop()
    start_Spanish = week_Spanish.pop()
    start_Italian = week_Italian.pop()
    for i in range(len(week_Date)):
        week_Esperanto[i] -= start_Esperanto
        week_Portuguese[i] -= start_Portuguese
        week_Spanish[i] -= start_Spanish
        week_Italian[i] -= start_Italian
    
    # Stackplot w/ target line
    plt.figure(2, figsize=(20,10))
    plt.subplot()
    labels = ["Esperanto", "Spanish", "Portuguese", "Italian"]
    colors = ['g', 'r', 'y', 'b']
    plt.stackplot(week_Date, week_Esperanto, week_Spanish, week_Portuguese, week_Italian, labels=labels, colors=colors)
    plt.legend(loc=2)
    plt.xlabel("Date")
    plt.ylabel("Total Points")
    plt.title("Duolingo this Week")
    plt.plot([0, 6], [DUO_WEEKLY_TARGET/7, DUO_WEEKLY_TARGET], 'k-', lw=1)
    plt.show(block=True)
    plt.close()
    
