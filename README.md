# Logs-SQL-Database
Udacity Assigment: Logs Analysis  
Nanodegree: Full Stack Web Developer

### PTYHON 3
Runs on git command line using vagrant virtual machine through virtual box  
Used Postgresql

## Files:  
newsdata.zip --> zip file of newsdata SQL database  
report.py --> Python file (python 3) to create views in database, most popular articles, most popular authors, and percentage of requests resulting in errors  
news_log_output.txt --> text file of prints in python file  

## SQL Tables
newsdata.sql includes 3 tables
- articles: author, title, slug, lead, body, time, id
- authors: name, bio, id
- log: path, ip, method, status, time, id

## Creating Views in newsdata.sql database
- article_path: splits log.path from the '/article/' so it can be connected to articles.slug  
"CREATE or REPLACE view article_path AS "  
              "SELECT path, split_part(path, '/', 3) AS "  
              "article_name FROM log;"  
              
- total_requests: total requests by day for use in calculating percentage of errors  
"CREATE or REPLACE view total_requests AS "  
              "SELECT DATE_TRUNC('day', time) AS day, COUNT(id) AS total "  
              "FROM log "  
              "GROUP BY day "  
              "ORDER BY total DESC;"  
              
- error_requests: total errors by day for use in calculating percentage of errors  
"CREATE or REPLACE view error_requests AS "  
              "SELECT DATE_TRUNC('day', time) AS date, COUNT(id) AS error, status "  
              "FROM log "  
              "WHERE log.status != '200 OK' "  
              "GROUP BY date, log.status "  
              "ORDER BY error DESC;"  
