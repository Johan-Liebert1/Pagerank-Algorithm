import sqlite3
import ssl
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse, urljoin
from termcolor import colored


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

connection = sqlite3.connect('spider_database.sqlite')
cur = connection.cursor()


#TODO
# checking if we're already in progress
# check if everything has been found 

def spider_website(all_allowed_websites):

    no_of_pages = 0

    while True:

        if no_of_pages < 1:
            number_pages = input("Enter the number of pages to retrieve: ")

            if len(number_pages) < 1: break 

            no_of_pages = int(number_pages)

        # setting up the condition to get out of while loop
        
        no_of_pages -= 1

        try:
            cur.execute("""
                SELECT id, url FROM Pages 
                WHERE html is NULL and error is NULL
                ORDER BY RANDOM() LIMIT 1
            """)
            row = cur.fetchone()
            fromId = row[0]
            website_url = row[1]

            print(colored(f'Currently Fetching : ', 'green'), website_url, end = " ")

        except:
            print("No unretrieved html pages found")
            break

        try:
            document = urlopen(website_url, context=ctx)
            
            website_html = document.read()

            if document.getcode() != 200:
                print(colored(f"\nCould not retrieve {website_url}", 'orange'))
                cur.execute("UPDATE Pages SET error = ? WHERE url = ?", (document.getcode(), website_url))
                connection.commit()

            if document.info().get_content_type() != 'text/html':
                print(colored(f"\nIgnoring non HTML page : {website_url}", 'yellow'))
                cur.execute("DELETE FROM Pages WHERE url = ?", (website_url,))
                connection.commit()
                continue
            
            # page was successfully retrieved 

            website_soup = BeautifulSoup(website_html, 'html.parser')

            all_anchor_tags = website_soup('a')

        except KeyboardInterrupt:
            print(colored("\nProgram Interrupted by User...", 'yellow'))
            break

        except:
            print(colored(f"Unable to get page on url {website_url}", 'red'))

            # now we don't want to ever check that url again

            cur.execute("UPDATE Pages SET error = -1 WHERE url = ? ", (website_url,))
            connection.commit()
            continue


        # at this point the page was successfully retrieved and all error checks are done

        cur.execute("""
            UPDATE Pages 
            SET html = ?
            WHERE url = ?
        """, (memoryview(website_html), website_url)
        )

        all_hrefs = []
        
        for tag in all_anchor_tags:
            href = tag.get('href')  

            if href is None or len(href) < 1:
                continue

            if href.endswith(".gif") or href.endswith('.jpeg') or href.endswith('.png') or href.endswith('.jpg') or href.endswith("#"):
                continue

            if href.endswith('/'):
                href = href[:-1]


            else:
                # as we do not want to wander out of the site
                
                # resolve relative refrernces

                #https://en.wikipedia.org/wiki/Internet

                parsed_href = urlparse(href)
                parsed_website_url = urlparse(website_url)

                if (parsed_href.netloc != '') and (parsed_href.netloc != parsed_website_url.netloc):
                    # link wanders out of current website
                    
                    continue

                if len(parsed_href.scheme) < 1:
                    # it's  a relative link
                    # make url out of relative link

                    href = f"{parsed_website_url.scheme}://{parsed_website_url.netloc}{parsed_href.path}"

                add = False
                all_hrefs.append(href)
                for website in all_allowed_websites:
                    if href.startswith(website):
                        add = True
                
                if not add: continue

                cur.execute("""
                    INSERT OR IGNORE INTO Pages 
                    (url, html, error, old_rank, new_rank)
                    VALUES (?, NULL, NULL, NULL, 1.0)
                """, (href, )
                )

                # now that href is inserted into pages, grab it's id which is toId,
                
                cur.execute("SELECT id FROM Pages WHERE url = ?", (href,))
                toId = cur.fetchone()[0]

                '''
                fromId is the id of the page that is linking to another pages which has 
                id equal to 'toId'. 
                one page links to another, thus fromId --> toId
                '''

                cur.execute("""
                    INSERT OR IGNORE INTO Links (from_page_id, to_page_id) 
                    VALUES (?, ?)
                """, (fromId, toId)
                )

        print(colored(f"< len(all_hrefs) = {len(all_hrefs)} >", 'green'))

        connection.commit()
    











