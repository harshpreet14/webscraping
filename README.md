# Github Topics Scraper
#### This is a Python script that scrapes the list of topics from the Github Topics page [(https://github.com/topics)] and the top repositories for each topic.
## Prerequisites
#### Before running the script, make sure that you have installed the following Python libraries:
#### >requests
#### > BeautifulSoup
#### > pandas
### Usage
#### To use this script, simply run it from the command line:
#### `python github_topic_scraper.py`
#### This will scrape the top repositories for each topic on GitHub and store the data in a separate CSV file for each topic in the data/ directory.
## How it works
#### The script first downloads the webpage for the GitHub topics page using the requests library. It then extracts the names, descriptions, and links for each topic using the BeautifulSoup library.

#### For each topic, the script then downloads the webpage for the topic and extracts the usernames, repository names, star counts, and repository URLs for the top repositories using BeautifulSoup.

#### Finally, the script stores the data for each topic in a separate CSV file in the data/ directory using the pandas library.

####  Note that if a CSV file for a particular topic already exists in the data/ directory, the script will skip that topic to avoid overwriting existing data.
## Contributing
####  If you find any issues or have any suggestions for improvement, please feel free to open an issue or submit a pull request on GitHub.
