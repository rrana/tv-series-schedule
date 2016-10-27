#!/usr/bin/python

import argparse
import requests
from BeautifulSoup import BeautifulSoup
from datetime import datetime
import calendar


def get_omdb_result(tv_series_name):
    omdb_url = 'http://www.omdbapi.com/'

    params = {
        't': tv_series_name,
    }

    api_response = requests.get(url=omdb_url, params=params)
    return api_response

def validate_omdb_result(api_response):
    if api_response.json()['Response'] == 'False':
        print "Invalid name! Please check the name again!"
        return
    elif api_response.json()['Type'] != 'series':
        print "Not tv series. Found match for %s instead" % api_response.json()['Type']
        return
    else:
        return api_response

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
    omdb_result =  get_omdb_result(tv_series_name)

    if validate_omdb_result(omdb_result):
        tv_series_id = omdb_result.json()['imdbID']
        current_season = omdb_result.json()['totalSeasons']
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
