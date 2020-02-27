# Component of trackr.py - saves data from Duolingo.com
# Requires a username in personal.data

import duolingo
import json
import requests

import date_related
import personal

order = ['Greek', 'Esperanto', 'Vietnamese', 'Italian', 'Welsh', 'Irish', 'Czech',
		 'Indonesian', 'Spanish', 'Chinese', 'Russian', 'Portuguese', 'Norwegian', 'Turkish',
		 'Romanian', 'Polish', 'Dutch', 'French', 'German', 'HighValyrian', 'Korean',
		 'Danish', 'Hungarian', 'Japanese', 'Hebrew', 'Swahili', 'Swedish', 'Ukrainian']
points = {'Greek': 0, 'Esperanto': 0, 'Vietnamese': 0, 'Italian': 0, 'Welsh': 0, 'Irish': 0, 'Czech': 0,
		  'Indonesian': 0, 'Spanish': 0, 'Chinese': 0, 'Russian': 0, 'Portuguese': 0, 'Norwegian': 0, 'Turkish': 0,
		  'Romanian': 0, 'Polish': 0, 'Dutch': 0, 'French': 0, 'German': 0, 'HighValyrian': 0, 'Korean': 0,
		  'Danish': 0, 'Hungarian': 0, 'Japanese': 0, 'Hebrew': 0, 'Swahili': 0, 'Swedish': 0, 'Ukrainian': 0}

def track_duolingo(cur):    
	last_entry_date = date_related.get_date_of_last_entry(cur, "duolingo")
	today = date_related.get_date()
	
	if today != last_entry_date[0]:
		scrape_duolingo()
		sql = ''' INSERT INTO duolingo(Date, Greek, Esperanto, Vietnamese, Italian, Welsh, Irish, Czech, Indonesian,
		 	Spanish, Chinese, Russian, Portuguese, Norwegian, Turkish, Romanian, Polish, Dutch, French, German, 
		 	HighValyrian, Korean, Danish, Hungarian, Japanese, Hebrew, Swahili, Swedish, Ukrainian
		 	) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
		new_entry = [today]
		for each in order:
			new_entry.append(points[each])

		cur.execute(sql, new_entry[0:29])
		print("New data added to Duolingo.")
	else:
		print("Duolingo was already updated today.")

def scrape_duolingo():
	lingo = duolingo.Duolingo(personal.data["duoUsername"], personal.data["duoPassword"])

	for lang in order:
		lang_data = lingo.get_language_details(lang)
		try:
			points[lang] = lang_data['points']
		except KeyError:
			pass