# Connect to the MySQL database
import mysql.connector
def db():
    conn = mysql.connector.connect(host='localhost',auth_plugin = 'mysql_native_password',user="root", password="admin", database="interappdata")
    return conn


