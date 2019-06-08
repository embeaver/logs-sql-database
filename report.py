import psycopg2
import bleach
import datetime


DBNAME = 'news'

def delete_spam():
    """Deletes spam from database"""
    db = psycopg2.connect(database = DBNAME)
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

#delete_spam()

#def combine_authors():
#    """Return all posts from the database"""
#    db = psycopg2.connect(database=DBNAME)
#    c = db.cursor()
#    # join article authors to authors id and select title and name
#    c.execute('select title, name from articles, authors'
#              'where articles.author = authors.id')
#    posts = c.fetchall()
 #   db.commit()
#    db.close()
#    print(posts)
#    return posts

#def combine_article_log():
 #   db = psycopg2.connect(datebase = DBNAME)
 #   c = db.cursor()
    # match article name in article table to path name in log table
#    c.execute('select path, title from log '
#              'where path like articles.title' )
             # 'where articles.title = log.path')

def create_views_article_path():
    """creates new table called article_path by splitting log.path from the /article/"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # count total of paths in descending order# #
    c.execute('CREATE or REPLACE view article_path AS '
              'SELECT path, SPLIT_PART(path, '/', 3) AS'
              'article_name FROM log;')
    posts = c.fetchall()

    db.close()
    print(posts)
    return posts



def count_best_articles():
    """Return all posts from the database"""
    db = psycopg2.connect(database = DBNAME)
    c = db.cursor()
    # delete spam posts from log table
    delete_spam()
    # count total of paths in descending order# #
    c.execute('SELECT title, count(*) AS views'
              'FROM articles, article_path'
              'WHERE articles.slug = article_path.article_name'
              'GROUP BY article_path.article_name, articles.title'
              'ORDER BY views DESC LIMIT 3;'
              #'SELECT path, count(*) AS num '
              #'FROM log GROUP BY path '
              #'ORDER BY num DESC LIMIT 10;')
    posts = c.fetchall()

    db.close()
    print(posts)
    return posts

count_best_articles()
