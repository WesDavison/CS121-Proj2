from configparser import ConfigParser
from argparse import ArgumentParser

from utils.server_registration import get_cache_server
from utils.config import Config
from crawler import Crawler
import scraper


def main(config_file, restart):
    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)
    config.cache_server = get_cache_server(config, restart)
    crawler = Crawler(config, restart)
    crawler.start()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--restart", action="store_true", default=False)
    parser.add_argument("--config_file", type=str, default="config.ini")
    args = parser.parse_args()
    main(args.config_file, args.restart)

    #output reporting information to file
    with open('report_file.txt', 'w') as report_file:
        #writing unique pages found
        report_file.write(f'Unique pages found: {len(scraper.noFragmentURLs)}\n\n')

        #writing longest page and longest url
        report_file.write(f'Longest page length: {scraper.longestPageWordCount}\n')
        report_file.write(f'Longest page URL: {scraper.longestPageURL}\n\n')

        #writing 50 most seen words
        report_file.write(f'50 most seen words: \n')
        count = 0
        for token, occurance in sorted(scraper.totalWordsSeen.items(), reverse = True, key = lambda item: item[1]):
            if count >= 50:
                break
            report_file.write(f'{token} --> {occurance}\n')
            count += 1
        report_file.write('\n')

        #writing most seen subdomains
        report_file.write(f'Total list of seen subdomains\n')
        report_file.write(f'Number of subdomains: {len(scraper.subdomainsSeen)}\n')
        for subdomain, occurance in sorted(scraper.subdomainsSeen.items(), key = lambda item: item[0]):
            report_file.write(f'{subdomain}, {occurance}\n')