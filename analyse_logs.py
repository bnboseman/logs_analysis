#!/bin/env python2.7

import news_database_queries


print("What are the most popular three articles of all time?")
for result in news_database_queries.get_popular(3):
    print("\"" + result[1] + "\" - " + str(result[0]) + " views")

print

print("Who are the most popular article authors of all time?")
for result in news_database_queries.get_popular_authors(3):
    print("\"" + result[1] + "\" - " + str(result[0]) + " views")

print

print("On which days did more than 1% of requests lead to errors?")
for result in news_database_queries.get_percent_errors():
    print(result[0].strftime('%B %d, %Y') + " - " + str(round(result[1],1))+ "%")