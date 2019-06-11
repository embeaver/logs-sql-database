#!/usr/bin/env python3
# USING PYTHON3
import psycopg2


DBNAME = "news"


def create_views():
    """creates new table called article_path by splitting log.path
    from the /article/
    creates new table called total_requests,
    to count total requests by day
    creates new table called error_requests,
    to count error requests by date"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # splits lot.path from the /article/
    c.execute("""
            CREATE or REPLACE view article_path AS
              SELECT path, split_part(path, '/', 3) AS
              article_name FROM log;
              """)
    # Total requests by day
    c.execute("""
            CREATE or REPLACE view total_requests AS
              SELECT DATE_TRUNC('day', time) AS day, COUNT(id) AS total
              FROM log
              GROUP BY day
              ORDER BY total DESC;
              """)
    # Total error requests by day
    c.execute("""
              CREATE or REPLACE view error_requests AS
              SELECT DATE_TRUNC('day', time) AS date, COUNT(id) AS error, status
              FROM log
              WHERE log.status != '200 OK'
              GROUP BY date, log.status
              ORDER BY error DESC;
              """)
    db.commit()
    db.close()


# Most Popular Articles
def count_top_articles():
    """Prints top 3 most popular articles in descending order"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # count total of paths in descending order# #
    c.execute("""
              SELECT title, count(*) AS num_views
              FROM articles, article_path
              WHERE articles.slug = article_path.article_name
              GROUP BY article_path.article_name, articles.title
              ORDER BY num_views DESC LIMIT 3;
              """)
    posts = c.fetchall()
    db.close()
    print("\nMost Popular Articles:")
    for post in posts:
        print('\"{0}\" - {1} views'.format(post[0], post[1]))
    return posts


# Most Popular Authors
def count_popular_authors():
    """Prints authors in descending order of most popular of articles viewed"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # sum the views of all articles written by author
    c.execute("""
              SELECT name, count(*) AS num
              FROM authors, articles, article_path
              WHERE authors.id = articles.author
              AND article_path.article_name = articles.slug
              GROUP BY authors.name
              ORDER BY num DESC;
              """)
    posts = c.fetchall()
    db.close()
    print("\nMost Popular Authors:")
    for post in posts:
        print("{0} - {1} views".format(post[0], post[1]))
    return posts


# Days where more than 1% of request led to error
def errors():
    """Prints the days when percentage of total requests resulting in errors is
    greater than 1%"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # use the two views created to divide errors by total requests,
    # show if over 1%
    c.execute("""
              SELECT (error/total::DECIMAL * 100) AS percentage, day
              FROM total_requests, error_requests
              WHERE total_requests.day = error_requests.date
              AND (error/total::DECIMAL * 100) > 1.0;
              """)
    posts = c.fetchall()
    db.close()
    print('\nDay(s) where more than 1% of requests led to errors')
    # print(posts)
    for post in posts:
        day = post[1].strftime('%B %d, %Y')
        print('{0} - {1}% errors'.format(day, "%.2f" % post[0]))
    return posts


# Main Program
def main():
    # Create views in database for easier manipulation
    create_views()

    # Most popular articles
    count_top_articles()

    # Most popular authors
    count_popular_authors()

    # Percent of total requests resulting in errors
    errors()


if __name__ == '__main__':
    main()
