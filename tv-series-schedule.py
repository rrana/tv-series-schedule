#!/usr/bin/python

import argparse
import requests
from BeautifulSoup import BeautifulSoup
from datetime import datetime
import calendar


def date_in_imdb_format():
    now = datetime.now()
    current_date = now.day
    current_month = calendar.month_abbr[now.month] + "."
    current_year = now.year
    imdb_formatted_date = str(current_date) + " " + str(current_month) + " " + str(current_year)
    return imdb_formatted_date


def get_episode_information(args):
    #todo: suggest tv series name if no match found. Considering possibilites of spelling mistake
    tv_series_name = args.series_name.lower()

    #todo: get this mapping using api
    tv_series_mapping = {
                            "the big bang theory":"tt0898266", 
                            "the middle":"tt144246", 
                            "modern family":"tt1442437", 
                            "fresh off the boat":"tt3551096",
                            "shameless":"tt1586680",
                        }

    #todo: get this mapping using api
    current_season_mapping = {
                        "tt0898266":10, 
                        "tt144246":8, 
                        "tt1442437":8, 
                        "tt3551096":3,
                        "tt1586680":7,
                    }

    tv_series_id = tv_series_mapping[tv_series_name]
    current_season = str(current_season_mapping[tv_series_id])

    imdb_request_url = "http://www.imdb.com/title/" + tv_series_id + "/episodes?season=" + current_season

    imdb_response = requests.get(url=imdb_request_url)
    html_content = imdb_response.content
    soup = BeautifulSoup(html_content)

    air_date = []

    for episodes in soup.findAll('div', attrs={'class':'airdate'}):
         air_date.append(episodes.getText())

    today = str(date_in_imdb_format())
    
    if today in air_date:
        print "Found one episode of %s scheduled today: %s" % (args.series_name, today)
    else:
        #todo: print next episodes schedule
        print "Could not find any episode scheduled for: %s" % today
        print "Schedule for this season: \n"
        for dates in air_date:
            print dates


if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument('--series-name', '-n', dest='series_name', required=True, 
        help='--series-name \'The big bang theory\'')
    args = parser.parse_args()
    get_episode_information(args)
