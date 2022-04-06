import psycopg2
import creds
from datetime import date

conn = psycopg2.connect(host=creds.host, dbname=creds.database,
                        user=creds.user, password=creds.password)

cur = conn.cursor()


# id
# user_id
# user_name
# first_name
# last_name
# sign
# day


def checker(user_id):
    cur.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
    data = cur.fetchone()
    if data is None:
        return None
    else:
        return True


def checker_f_sign(user_id, sign):
    cur.execute(f"SELECT sign, user_id FROM users WHERE sign = '{sign}' AND  user_id = '{user_id}';")
    data = cur.fetchone()
    if data is None:
        return None
    else:
        return True


def check_mailling(user_id):
    cur.execute(f"SELECT mailling FROM users WHERE user_id = '{user_id}';")
    return cur.fetchone()


def set_user(user_id, user_name, first_name, last_name):
    cur.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}';")
    data = cur.fetchone()
    if data is None:
        cur.execute(f"INSERT INTO users (user_id, user_name, first_name, last_name)"
                    f"VALUES ('{user_id}', '{user_name}','{first_name}', '{last_name}');")
        conn.commit()


def set_user_j_day(user_id):
    day = date.today()
    cur.execute(f"UPDATE users SET day = '{day}' WHERE user_id = '{user_id}'")
    conn.commit()


def set_user_sign(user_id, sign):
    cur.execute(f"SELECT sign, user_id FROM users WHERE sign = '{sign}' AND  user_id = '{user_id}';")
    data = cur.fetchone()
    if data is None:
        cur.execute(f"UPDATE users SET sign = '{sign}' WHERE user_id = '{user_id}';")
        conn.commit()


def power_set_sign(user_id, new_sign):
    cur.execute(f"UPDATE users SET sign = '{new_sign}' WHERE user_id = '{user_id}'; ")
    conn.commit()


def take_sign(user_id):
    cur.execute(f"SELECT sign FROM users WHERE user_id = '{user_id}';")
    return cur.fetchone()


def upmailling(user_id):
    cur.execute(f"UPDATE users SET mailling = TRUE WHERE user_id = '{user_id}';")
    conn.commit()


def downmailling(user_id):
    cur.execute(f"UPDATE users SET mailling = FALSE WHERE user_id = '{user_id}';")
    conn.commit()


def malling_list():
    cur.execute(f"SELECT user_id FROM users WHERE mailling = TRUE;")
    closed = cur.fetchall()
    open = [x for i in closed for x in i]
    return open
