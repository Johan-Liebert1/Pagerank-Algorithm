import sqlite3
from urllib.parse import urlparse

from termcolor import colored
from spider import spider_website

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

        
        if website_url.endswith("/"): website_url = website_url[:-1]

        website_domain = website_url

        print(colored(f'website_domain : {website_domain}', 'yellow'))

        cur.execute("INSERT OR IGNORE INTO Websites (website_url) VALUES ( ? ) ", (website_domain,))

        cur.execute("""
            INSERT OR IGNORE INTO Pages
            (url, html, error, old_rank, new_rank)
            VALUES (?, NULL, NULL, NULL, 1.0)
        """, (website_domain, )
        )

        connection.commit()

        cur.execute("SELECT website_url FROM Websites")

        rows = cur.fetchall()

        all_allowed_websites = []

        for row in rows:
            all_allowed_websites.append(row[0])


        print("Currently spidering " , colored(website_url, 'green'))

        cur.close()

        spider_website(all_allowed_websites)

        break


if __name__ == "__main__":
    main()
