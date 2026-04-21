import sqlite3

def get_admins():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, password, rights FROM myapp_register WHERE rights LIKE '%admin%'")
    rows = cursor.fetchall()
    if not rows:
        print("No admins found.")
    for row in rows:
        print(f"Name: {row[0]}, Email: {row[1]}, Password Hash: {row[2]}, Rights: {row[3]}")
    conn.close()

if __name__ == '__main__':
    get_admins()
