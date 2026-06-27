import requests

headers = {
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

r = requests.get('https://api.fifa.com/api/v3/calendar/matches?idCompetition=17&idSeason=285023&count=104&language=en-GB', headers=headers)
matches = r.json().get('Results', [])
print('Total matches fetched:', len(matches))

for m in matches[:20]:
    home = m['Home']['Abbreviation']
    away = m['Away']['Abbreviation']
    status = m['MatchStatus']
    date = m['Date'][:10]
    print(home + ' vs ' + away + ' | Status: ' + str(status) + ' | Date: ' + date)
