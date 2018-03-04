import sqlite3

from getDate import get_date

def update_warmup(trackr_cur):
    SRC = "/home/matt/Warm-Up-Quiz/warmUp.db"
    today = get_date()
    new_data = []
    py_count = 0
    ex_count = 0
    
    # Pull activity data from db
    warmup_conn = sqlite3.connect(SRC)
    warmup_cur = warmup_conn.cursor()
    warmup_cur.execute("SELECT tool, date FROM calls WHERE calls_id > 64")
    raw_data = warmup_cur.fetchall()
    
    # Trim time for datetime
    for i in range(len(raw_data)):
        new_data.append((raw_data[i][0], raw_data[i][1][0:10]))
    
    # Count datapoints for each category
    for i in range(len(new_data)):
        if new_data[i][1] == today:
            if new_data[i][0] == "python":
                py_count += 1
            elif new_data[i][0] == "excel":
                ex_count += 1
            else:
                print("Rogue datapoint! Doesn't belong to an established category.")
    '''
    # Pull previous data point
    trackr_cur.execute("SELECT Python, Excel FROM warmup WHERE Date = ?", (today,))
    prev_py_count, prev_ex_count = trackr_cur.fetchone()
    '''
    # Update db with counts
    trackr_cur.execute("UPDATE warmup SET Python = ?, Excel = ? WHERE Date = ?", (py_count, ex_count, today))
    warmup_conn.commit()
    print("Completed update to warmup.")
    return cur
