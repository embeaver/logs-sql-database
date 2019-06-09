import psycopg2
import bleach
import datetime
### USING PYTHON3 ###

DBNAME = "news"

# maybe not needed
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

def create_views_article_path():
    """creates new table called article_path by splitting log.path from the /article/"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # count total of paths in descending order# #
    c.execute("CREATE or REPLACE view article_path AS "
              "SELECT path, split_part(path, '/', 3) AS "
              "article_name FROM log;")
    c.execute("select * from article_path limit 10;")
    posts = c.fetchall()
    db.commit()
    db.close()
    #print(posts)
    return posts

create_views_article_path()

# Most Popular Articles
def count_top_articles():
    """Return all posts from the database"""
    db = psycopg2.connect(database = DBNAME)
    c = db.cursor()
    # delete spam posts from log table - not needed since they aren't in the slug
    #delete_spam()
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
        print('\"{0}\" - {1} views'.format(str(post[0]), str(post[1])))
    return posts

count_top_articles()

# Most Popular Authors
def count_popular_authors():
    db = psycopg2.connect(database = DBNAME)
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
        print("{0} - {1} views".format(str(post[0]), str(post[1])))
    return posts

count_popular_authors()
