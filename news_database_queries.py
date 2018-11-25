#!/bin/env python2.7

import psycopg2

DBNAME = "news"


def run_query(query, limit=None):
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor();

    if limit is not None:
        query = query + " limit " + str(limit);

    cursor.execute(query)
    results = cursor.fetchall();
    db.close()
    return results


def get_popular(limit=None):
    return run_query(
        """select count(*), title 
        from log 
        join articles 
        on path = concat('/article/',slug) 
        group by title 
        order by count desc""",
        limit)


def get_popular_authors(limit=None):
    return run_query(
        """
        select count(*), name 
        from log 
        join articles on path = concat('/article/',slug) 
        join authors on articles.author = authors.id 
        group by name 
        order by count desc
        """,
        limit)

def get_percent_errors(threshold=1, ):
    return run_query(
        """
        select * from (
            select
                total.date,
                (100*errors.count::float/total.count::float)
                as error_percentage
            from
                (
                    select DATE(time), count(*)
                    from log
                    group by date
                ) as total,
                (
                    select DATE(time), count(*)
                    from log
                    where status <> '200 OK'
                    group by date
                ) as errors
            where total.date = errors.date
        ) as sub
        where error_percentage > """ + str(threshold) + " order by error_percentage desc"
    )
