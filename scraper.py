import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from collections import defaultdict
from simhash import Simhash


visitedURLs = set()
noFragmentURLs = set()
simHashes = set()
simObjects = list()

#report info
longestPageWordCount = 0
longestPageURL = ''
totalWordsSeen = dict()
subdomainsSeen = dict()

stop_words = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]


#https://github.com/1e0ng/simhash
def get_features(s):
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]


def scraper(url, resp, masterDict):
    links = extract_next_links(url, resp, masterDict)
    # create file with stats (here?)
    # remember to consider stop words
    return [link for link in links if is_valid(link)]



def extract_webpage_text(url, resp, masterDict):
    #parsing and reading webpage
    bs = BeautifulSoup(resp.raw_response.content, "lxml")
    text.encode("utf-8", errors="ignore")
    text = text.strip().split("\n")

    #finding tokens and most used workds
    tokens = []
    for line in text:
        tokens.extend([x.lower() for x in re.findall('[a-zA-Z0-9]+', line)])
    page_word_length = len(tokens)  #number of words in the page
    tokens_nostop = [token for token in tokens if token not in stop_words]
    word_freqs = defaultdict(int) 
    for token in tokens_nostop:
        word_freqs[token] += 1
    
    
# def isSimilarPageContent(url, resp, tokens):
#     tokensDict = {}
#     for prevURL, prevTokens in tokensDict:
#         # gets length of intersection
#         numIntersections = len(set(tokens).intersection(set(prevTokens)))
#         if numIntersections / len(tokens) >= 0.70:
#             return True
#     return False

def isSimilarPage(simhashObj):
    for obj in simObjects:
        if obj.distance(simhashObj) < 5:
            return True
    return False

def isDuplicatePage(simhashObj):
    return simhashObj.value in simHashes

def notEnoughInfo(tokens):
    if len(tokens) < 100:
        return True
    return False

    

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
    if resp.status == 200 and resp.raw_response != None:
        # add content checks to determine if it is worth crawling aka...
        # - check similarity to sites already visited & content amount

        if url in visitedURLs:
            #already visited
            return list()

        #print(resp.url + "\n")
        sp = BeautifulSoup(resp.raw_response.content, "lxml")

        simhashObj = Simhash(value = get_features(sp.get_text()), f = 128)

        if isDuplicatePage(simhashObj) or isSimilarPage(simhashObj):
            print('found similar or duplicate page')
            visitedURLs.add(url)
            return list()
        
        #add hash value to set
        simHashes.add(simhashObj.value)
        #add object to set
        simObjects.append(simhashObj)

        for aTag in sp.find_all('a'):
            if aTag.has_attr("href"):
                url = aTag["href"]
                link = url
                # remove # segment of the url
                link = link if '#' not in link else link[:link.index('#')]

                # checks if formerly visited and if it is valid
                # added valid check (keep?)
                if is_valid(url):
                    acquiredLinks.add(url)
                    visitedURLs.add(url)
                    noFragmentURLs.add(link)

                    #print("token checking\n")

                    # get_text gets all the words of a web page, and split them by newlines to be
                    # processed properly into tokens using code from the first part.
                    test = sp.get_text().strip().split("\n")

                    # TODO: Figure out a way to scrape tokens from the page.
                    masterDict[resp.url] = 0



       # print("RETRIEVED URLS:", acquiredLinks)
        #print("\n\n")
        #print(masterDict)
    else:
        #bad link
        visitedURLs.add(url)
        return list()
    #("Finished")
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
        
        # additional file types to ignore
        if re.match(r".*\.(odc|html|ppsx)", parsed.path.lower()):
            return False

        if isBlacklisted(url):
            return False

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


def isBlacklisted(url):
    unsafeURLs = ["/photo", "/events", "/?share=", "/pdf", "/calendar", "sli.ics.uci.edu", "?ical"]
    for component in  unsafeURLs:
        if component in url:
            return True
    return False


# def hasher(string):
#     s = string.encode('utf-8')
#     hash = hashlib.new('md5')
#     hash.update(s)
#     return hash.hexdigest()