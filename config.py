import mySQLdb

hostname='sql3.freemysqlhosting.net'
username='sql3166077'
password='1K9R5ikdFX'
dbname='sql3166077'
port= 3306
charset='utf8'

try:
   conn = MySQLdb.connect(
       host=hostname,
       user=username,
       passwd=password,
       db=dbname,
       port=port,
       charset=charset,
       )

