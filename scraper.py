import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def scraper(url, resp):
    links = extract_next_links(url, resp)
    # create file with stats (here?)
    # remember to consider stop words
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    acquiredLinks = set()

    # check which status' are allowed (only 200?)
    if resp.status == 200:
        # add content checks to determine if it is worth crawling aka...
        # - check similarity to sites already visited & content amount

        print(resp.url + "\n")
        sp = BeautifulSoup(resp.raw_response.content, "lxml")
        urls = sp.find_all('a')
        for u in urls:
            # make sure to remove # part of the url as per instructions
            if u.has_attr("href"):
                validUrl = (u["href"].find(".ics.uci.edu/") != -1 or u["href"].find(".cs.uci.edu/") != -1
                            or u["href"].find(".informatics.uci.edu/") != -1 or u["href"].find(".stat.uci.edu/") != -1
                            or u["href"].find("today.uci.edu/department/information_computer_sciences/") != -1)

                if validUrl == True:
                    acquiredLinks.add(u["href"])

        print("RETRIEVED URLS:", acquiredLinks)
        print("\n\n")
    print("Finished")
    return list(acquiredLinks)

def is_valid(url):
    # Decide whether to crawl this url or not.
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False

        # add check to determine if url is a trap
        
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
