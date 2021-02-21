from datetime import datetime
import sqlite3


def get_time() -> str:
    """Returned hour-minute-second string"""

    now = datetime.now()
    return now.strftime("%H:%M:%S")


def get_date() -> str:
    """Returned year-month-day string"""

    return datetime.now().strftime("%Y-%m-%d")


def get_day() -> int:
    """Returned weekday: integer (from 0: Monday to 6: Sunday)"""

    return datetime.today().weekday()


def no_date(date: str) -> bool:
    """Returned True if there is no date in database"""

    conn = sqlite3.connect('dbase.sqlite3')
    c = conn.cursor()
    c.execute("SELECT count(*) FROM my_log WHERE date = ?", (date,))
    data = c.fetchone()[0]
    conn.commit()
    conn.close()
    if data == 0:
        return True


def to_base(dict_: dict):
    """Commit data from dictionary to database"""

    date = dict_['date']
    day = dict_['day']
    get_out = dict_['out']
    bus = dict_['bus']
    subway = dict_['sub']
    school = dict_['school']

    conn = sqlite3.connect('dbase.sqlite3')
    c = conn.cursor()
    c.execute("INSERT INTO my_log VALUES (?, ?, ?, ?, ?, ?)",
              (date, day, get_out, bus, subway, school))
    conn.commit()
    conn.close()
