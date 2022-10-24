import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

visitedURLs = set()

stop_words = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]

def scraper(url, resp, masterDict):
    links = extract_next_links(url, resp, masterDict)
    # create file with stats (here?)
    # remember to consider stop words
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp, masterDict):
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
        for aTag in sp.find_all('a'):
            if aTag.has_attr("href"):
                link = aTag["href"]
                # remove # segment of the url
                link = link if '#' not in link else link[:link.index('#')]

                # checks if formerly visited and if it is valid
                # added valid check (keep?)
                if is_valid(link) and (link not in visitedURLs):
                    acquiredLinks.add(link)
                    visitedURLs.add(link)

                    # TODO: Figure out a way to scrape tokens from the page.
                    masterDict[resp.url] = 0


        print("RETRIEVED URLS:", acquiredLinks)
        print("\n\n")
        print(masterDict)
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

        # checks if valid URL (detailed in instructions)
        validURL = (url.find(".ics.uci.edu/") != -1 or url.find(".cs.uci.edu/") != -1
                    or url.find(".informatics.uci.edu/") != -1 or url.find(".stat.uci.edu/") != -1
                    or url.find("today.uci.edu/department/information_computer_sciences/") != -1)
        if not validURL:
            return False

        # add check to determine if url is a potential trap

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
