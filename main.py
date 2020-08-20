import sqlite3

from termcolor import colored
from spider import spider_website
from helpers import extract_domain

def create_tables():
    cur.executescript('''
        CREATE TABLE IF NOT EXISTS Websites (
            website_url TEXT UNIQUE 
        );

        CREATE TABLE IF NOT EXISTS Pages (
            id INTEGER NOT NULL PRIMARY KEY,
            url TEXT UNIQUE, 
            html TEXT, 
            error INTEGER DEFAULT NULL,
            old_rank REAL,
            new_rank REAL
        );

        CREATE TABLE IF NOT EXISTS Links (
            from_page_id INTEGER, 
            to_page_id INTEGER,

            UNIQUE (from_page_id, to_page_id)
        )
    ''')

def main():
    global connection, cur

    connection = sqlite3.connect('spider_database.sqlite')
    cur = connection.cursor()

    create_tables()

    while True:

        print("Please enter url of the form 'https://www.website-name.domain-name/'")
        website_url = input("Enter the website url to spider: ")

        if len(website_url) < 1:
            break

        website_domain = extract_domain(website_url)

        cur.execute("INSERT OR IGNORE INTO Websites (website_url) VALUES ( ? ) ", (website_domain,))
        cur.execute("""
            INSERT OR IGNORE INTO Pages
            (url, html, error, old_rank, new_rank)
            VALUES (?, NULL, NULL, NULL, 1.0)
        """, (website_url, )
        )
        connection.commit()

        cur.execute("SELECT website_url FROM Websites")

        print("Currently spidering " , colored(cur.fetchone()[0], 'green'))

        cur.close()

        spider_website(website_domain)

        break



if __name__ == "__main__":
    main()
