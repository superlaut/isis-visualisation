import json
import requests
import pandas as pd
from os import makedirs
from os.path import join, exists
from datetime import date, timedelta

ARTICLES_DIR = join('guardian', 'articles')
makedirs(ARTICLES_DIR, exist_ok=True)

API_ENDPOINT = 'http://content.guardianapis.com/search'
my_params = {
    'tag' : "world/isis",
    'from-date': "",
    'to-date': "",
    'order-by': "newest",
    'show-fields': 'all',
    'page-size': 200,
#    'api-key': ''
}

start_date = date(2013, 1, 1)
end_date = date(2017,12, 31)
dayrange = range((end_date - start_date).days + 1)

for daycount in dayrange:
    dt = start_date + timedelta(days=daycount)
    datestr = dt.strftime('%Y-%m-%d')
    filename = join(ARTICLES_DIR, datestr + '.json')
    if not exists(filename):
        all_results = []
        my_params['from-date'] = datestr
        my_params['to-date'] = datestr
        current_page = 1
        total_pages = 1
        while current_page <= total_pages:
            my_params['page'] = current_page
            resp = requests.get(API_ENDPOINT, my_params)
            data = resp.json()
            all_results.extend(data['response']['results'])
            current_page += 1
            total_pages = data['response']['pages']

        with open(filename, 'w') as f:
            #print("Writing to", filename)

            # re-serialize it for pretty indentation
            f.write(json.dumps(all_results, indent=2))
        

dates = pd.date_range(start = '2013-01-01', end = '2017-12-31')

allArticles = pd.DataFrame()
for date in dates:
    datestring = str(date).split(' ')[0]
    articleInDay = pd.read_json('../2019mt-st445-project-superlaut/guardian/articles/' + datestring + '.json')
    allArticles = pd.concat([allArticles, articleInDay], ignore_index = True)
    
allArticles.to_json('../2019mt-st445-project-superlaut/isisArticlesGuardian.json')