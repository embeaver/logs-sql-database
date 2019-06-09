import psycopg2
import bleach
import datetime

### USING PYTHON3 ###

DBNAME = "news"


# maybe not needed
def delete_spam():
    """Deletes spam from database"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # delete spam
    c.execute("delete from log "
              "where path like '/' "
              "or path like '%spam%' "
              "or path like '%20%'"
              "or path like '%+%';")
    # execute the changes in the database
    db.commit()
    # close the database
    db.close()


def create_views():
    """creates new table called article_path by splitting log.path from the /article/"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # count total of paths in descending order# #
    c.execute("CREATE or REPLACE view article_path AS "
              "SELECT path, split_part(path, '/', 3) AS "
              "article_name FROM log;")
    # Total requests by day
    c.execute("CREATE or REPLACE view total_requests AS "
              "SELECT DATE_TRUNC('day', time) AS day, COUNT(id) AS total "
              "FROM log "
              "GROUP BY day "
              "ORDER BY total DESC;")
    # Total error requests by day
    c.execute("CREATE or REPLACE view error_requests AS "
              "SELECT DATE_TRUNC('day', time) AS date, COUNT(id) AS error, status "
              "FROM log "
              "WHERE log.status != '200 OK' "
              "GROUP BY date, log.status "
              "ORDER BY error DESC;")
    # c.execute("select * from article_path limit 10;")
    # posts = c.fetchall()
    db.commit()
    db.close()
    # return posts


create_views()


# Most Popular Articles
def count_top_articles():
    """Return all posts from the database"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # delete spam posts from log table - not needed since they aren't in the slug
    # delete_spam()
    # count total of paths in descending order# #
    c.execute("SELECT title, count(*) AS num_views "
              "FROM articles, article_path "
              "WHERE articles.slug = article_path.article_name "
              "GROUP BY article_path.article_name, articles.title "
              "ORDER BY num_views DESC LIMIT 3;")
    posts = c.fetchall()
    db.close()
    print("\nMost Popular Articles:")
    for post in posts:
        print('\"{0}\" - {1} views'.format(post[0], post[1]))
    return posts


count_top_articles()


# Most Popular Authors
def count_popular_authors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # sum the views of all articles written by author
    c.execute("SELECT name, count(*) AS num "
              "FROM authors, articles, article_path "
              "WHERE authors.id = articles.author "
              "AND article_path.article_name = articles.slug "
              "GROUP BY authors.name "
              "ORDER BY num DESC")
    posts = c.fetchall()
    db.close()
    print("\nMost Popular Authors:")
    for post in posts:
        print("{0} - {1} views".format(post[0], post[1]))
    return posts


count_popular_authors()


# Days where more than 1% of request led to error
def errors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # use the two views created to divide errors by total requests, show if over 1%
    c.execute("SELECT (error/total::DECIMAL * 100) AS percentage, day "
              "FROM total_requests, error_requests "
              "WHERE total_requests.day = error_requests.date "
              "AND (error/total::DECIMAL * 100) > 1.0;")
    posts = c.fetchall()
    db.close()
    print('\nDays where more than 1% of requests led to errors')
    # print(posts)
    for post in posts:
        day = post[1].strftime('%B %d, %Y')
        print('{0} - {1}% errors'.format(day, "%.2f" % post[0]))
    return posts

errors()
