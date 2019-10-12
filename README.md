# ScrapePlayStoreReviews

APIs to extract reviews from Google Play Store don't work beyond Page 111. This scraper is intended to scrape ALL reviews from an app. It works by automating the human action of scrolling play store reviews (via Selenium) and saving each review visible on the page.

## A product of &#10084; from 3B for the love of people and of course the internet and digital era
## A &#11088; would make my day if you find the script useful

## Installations Required (more to be added)
- `pip3 install selenium`
- `pip3 install matplotlib`
- `pip3 install requests-testadapter`
- `pip3 install lxml`



## Prerequisites
- Default to Python >3.5 and pip3
- Install the chromedriver from http://chromedriver.chromium.org/ and in the scraper.py code point the variable chromedriver to the same
<!-- - The base directory (from where you are running this code) has chromedriver (if it isn't already installed): http://chromedriver.chromium.org/ -->
- The json files with individual elements (only reviews, only dates) are saved in a directory called data_folder. If you want these files, create a directory in the base directory called 'debug' and run the code as is. If not, comment out all the lines where data is being saved to the 'debug' folder.

## Running 
- scraper.py is the primary scraper. If you have a stable Internet connection with minimal interruptions, this would be the only code you would have to run. 
- Enter the APP_ID and appname in scraper.py and execute script. The url and session_id will be printed on the console. Copy these values in scraper_open_browser.py 
- The scraper should run and save data in the base folder.
- In case the code is interrupted due to an error (usually because of connectivity loss), change the counter (k) in scraper_open_browser.py to the last review that was saved by the scraper. Ensure that the driver_id and url is that of the window created by scraper.py. Run scraper_open_browser.py
- Every time the code is interrupted because of an error, repeat previous step (change 'k' to the last review saved by scraper.py or scarper_open_browser.py)

<!-- ## Some Observations from My Experience running it:
  - Depending on the number of reviews, scrolling to the earliest review can take over two days. 
  - 10K reviews took ~5 hours to be scraped. 
  - The Google Play Store window controlled by the code must always be active for the page to load on scrolling. I had a spare monitor that I connected to my laptop to keep the window active, while I continued to use my laptop as usual.
  - The speed of loading a page on scrolling will depend on the speed of your Internet connection. You can adjust the sleep time based on your Internet speed.
  - If you lose Internet connection for too long, webdriver will lose the chrome window. In this case, use the scroll_open_browser code to reconnect to the window and begin scrolling from where it left off. Remember to change the driver_id and counter value to that provided by scroll.py
- There are a lot of values that are printed to the console that I used to debug the program. It might be preferrable to comment some of them out. To be able to keep a tab of the scrapers progress, I recommend not commenting out counter k.
 -->

# TO-DO
- [x] scraper
- [ ] add restart from last stop
- [ ] add multi threading if possible