import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
# Use the requests library to download the webpage on the local server
'''github_url = "https://github.com/topics"
r = requests.get(github_url)
response = r.text
if r.status_code != 200:
    raise Exception("Failed to load page {}".format(github_url))
doc1 = BeautifulSoup(response, 'lxml')'''

# Extracting the names of the topics


def get_topic_titles(doc):
    topic_title_class = "f3 lh-condensed mb-0 mt-1 Link--primary"
    topic_title_tags = doc.find_all('p', {'class': topic_title_class})
    topic_titles = []
    for tag in topic_title_tags:
        topic_titles.append(tag.text)
    return topic_titles

# Extracting the description of the topic


def get_topic_description(doc):
    topic_description_class = "f5 color-fg-muted mb-0 mt-1"
    topic_description_tags = doc.find_all('p', {'class': topic_description_class})
    topic_descriptions = []
    for des in topic_description_tags:
        topic_descriptions.append(des.text.strip())
    return topic_descriptions


# Extracting the link to the topic
def get_topic_urls(doc):
    topic_link_class = "no-underline flex-1 d-flex flex-column"
    topic_link_tags = doc.find_all('a', {'class': topic_link_class})
    # topic_url = "https://github.com" + topic_link_tags[0]["href"]
    base_url = "https://github.com"
    topic_urls = []
    for url in topic_link_tags:
        topic_urls.append(base_url + url['href'])
    return topic_urls

# Creating a dataframe consisting of topics, descriptions and links


def scrape_topics():
    github_url = "https://github.com/topics"
    r = requests.get(github_url)
    response = r.text
    if r.status_code != 200:
        raise Exception("Failed to load page {}".format(github_url))
    doc1 = BeautifulSoup(response, 'lxml')
    table_dict = {
        'Topic Title': get_topic_titles(doc1),
        'Topic Link': get_topic_urls(doc1),
        'Topic Description': get_topic_description(doc1)
    }
    return pd.DataFrame(table_dict)


def get_topic_page(topic_url):
    r = requests.get(topic_url)
    response = r.text
    if r.status_code != 200:
        raise Exception("Failed to load page {}".format(topic_url))
    topic_doc = BeautifulSoup(response, 'lxml')
    return topic_doc


def get_repo_info(h3_tag, star_tag):
    a_tags = h3_tag.find_all('a')

    username = a_tags[0].text.strip()

    repo_name = a_tags[1].text.strip()
    base_url = "https://github.com"
    repo_url = base_url + a_tags[1]['href']

    star_count = star_tag.text.strip()
    return username, repo_name, repo_url, star_count


# FURTHER INFORMATION ABOUT TOPICS

def get_topic_repos(topic_doc):
    h3_selection_tag = 'f3 color-fg-muted text-normal lh-condensed'
    h3_tags = topic_doc.find_all('h3', {'class': h3_selection_tag})

    star_span_id = 'repo-stars-counter-star'
    star_tags = topic_doc.find_all('span', {'id': star_span_id})

    topic_repos_dict = {
        'username': [],
        'repo_name': [],
        'stars': [],
        'repo_url': []
    }

    for i in range(len(h3_tags)):
        repo_info = get_repo_info(h3_tags[i], star_tags[i])
        topic_repos_dict['username'].append(repo_info[0])
        topic_repos_dict['repo_name'].append(repo_info[1])
        topic_repos_dict['stars'].append(repo_info[2])
        topic_repos_dict['repo_url'].append(repo_info[3])

    return pd.DataFrame(topic_repos_dict)


def scrape_topic(topic_url, path):
    if os.path.exists(path):
        print("The file {} already exists. Skipping...".format(path))
        return
    topic_df = get_topic_repos(get_topic_page(topic_url))
    topic_df.to_csv(path, index=False)


def scrape_topics_repos():
    print('Scraping list of topics')
    topics_df = scrape_topics()

    os.makedirs('data', exist_ok=True)
    for index, row in topics_df.iterrows():
        print('Scraping top repositories for "{}"'.format(row['Topic Title']))
        scrape_topic(row['Topic Link'], 'data/{}.csv'.format(row['Topic Title']))


scrape_topics_repos()
