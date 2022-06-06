import matplotlib.pyplot as plt
from configparser import ConfigParser
import math
import json

config = ConfigParser()
config.read('settings.ini', encoding='utf-8')

data_dir = config['settings']['data_directory']
name = config['settings']['name']
email = f'{name}@miem.hse.ru'

month_eng = [
	'Jan', 'Feb', 'Mar', 
	'Apr', 'May', 'Jun', 
	'Jul', 'Aug', 'Sep', 
	'Oct', 'Nov', 'Dec'
]
month_full = [
	'January', 'February', 'March', 
	'April', 'May', 'June', 'July', 
	'August', 'September', 'October', 
	'November', 'December'
]
num_monthes = [
	'01', '02', '03', 
	'04', '05', '06', 
	'07', '08', '09', 
	'10', '11', '12'
]

numon = dict(zip(num_monthes, month_full))
dimon = dict(zip(month_eng, month_full))
git_account = git_commits = zulip_account = zulip_posts = False
messages = [0] * 4
commits = [0] * 4
seminars = [0] * 4
sessions = [0] * 4
monthes = ['str'] * 4
day = 'str'
was = False

with open(f'{data_dir}/GitStats.json', 'r', encoding = 'utf-8') as r:
    git_stats = json.load(r)

with open(f'{data_dir}/ZulipStats.json', 'r', encoding = 'utf-8') as r:
    zulip_stats = json.load(r)

with open(f'{data_dir}/JitsiClasses.json', 'r', encoding = 'utf-8') as r:
    jitsi_classes = json.load(r)

with open(f'{data_dir}/JitsiSession.json', 'r', encoding = 'utf-8') as r:
    jitsi_session = json.load(r)

for stats in git_stats:
    if stats['email'] == email:
        git_account = True
        for i in range(-1, -5, -1):
            monthes[i] = dimon[stats['commits_stats'][i]['beginDate'][4:7]]
            commits[i] = stats['commits_stats'][i]['commitCount']

for stats in zulip_stats:
    if stats['email'] == email:
        zulip_account = True
        for i in range(-1, -5, -1):
            messages[i] = stats['stats'][i]['messageCount']

for stats in jitsi_classes:
    was = False
    day = numon[stats['date'][5:7]]
    for aud in stats['auditoriums']:
        for cl in aud['classes']:
            for member in cl['members']:
                if member == email:
                    was = True
    if was == True:
        for i in range(4):
            if monthes[i] == day:
                seminars[i] += 1

all_messages = all_commits = all_seminars = all_sessions = 0

for i in range(4):
    all_messages += messages[i]
    all_commits += commits[i]
    all_seminars += seminars[i]
    all_sessions += sessions[i]

if all_messages > 0:
    zulip_posts = True

if all_commits > 0:
    git_commits = True

total = (
	int(git_account) + 
	int(zulip_account) + 
	int(git_commits) + 
	int(zulip_posts) + 
	all_seminars / 2 + 
	all_sessions / 2
)

total = math.ceil(total)

if total >= 10:
    total = 10

fig, graf = plt.subplots()
graf.set_xlabel('Monthes')
graf.set_ylabel('Quantity')
graf.set_title(email)
graf.plot(monthes, messages, marker = 'o', label = 'Zulip Messages')
graf.plot(monthes, commits, marker = 'o', label = 'Git Commits')
graf.plot(monthes, seminars, marker = 'o', label = 'Seminars')
graf.plot(monthes, sessions, marker = 'o', label = 'Sessions')
graf.legend(loc = 'best')
fig.savefig(f'/home/student/student_stats/{name}/{name}.png')

with open(f'/home/student/student_stats/{name}/{name}.html', 'w') as w:
    w.write(
		f'<html><head><meta charset="utf-8"><title>{name}'
		f'</title></head><body><img src="{name}.png" width="800" '
		f'height="600"><p>Git Account: {str(git_account)}</br>Git Commits: '
		f'{str(all_commits)}</br>Zulip Account: {str(zulip_account)}</br>'
		f'Zulip Messages: {str(all_messages)}</br>Visited Seminars: '
		f'{str(all_seminars)}</br>Visited Poster Sessions: {str(all_sessions)}'
		f'</p><h1>Total Mark: {str(total)}</h1></body></html>'
    )
