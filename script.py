import requests

def update_file(file, subreddit, title, selftext):
    file.close()
    write_file = open(file_name, 'w')
    write_file.write(subreddit.strip() + "\n")
    write_file.write(title.strip().replace('\r', '').replace('\n', '') + "\n")
    write_file.write(selftext.strip().replace('\r', '').replace('\n', ''))
    write_file.close()

username = '<username>'
url = "https://www.reddit.com/user/" + username + "/submitted.json"
slack_token = '<slack_token>'
slack_channel = '<slack_channel>'
headers = {
    'Accept': 'application/json',
    'User-agent': 'Track Script'
}
file_name = 'data.txt'

response = requests.get(url, headers = headers).json()
posts = response['data']['children']

for post in posts:
    if post['data']['pinned']:
        continue
    top_post = post
    break

subreddit = top_post['data']['subreddit']
title = top_post['data']['title'].strip().replace('\r', '').replace('\n', '')
selftext = top_post['data']['selftext'].strip().replace('\r', '').replace('\n', '')

with open(file_name, 'r') as file:
    contents = file.readlines()
    if not contents:
        update_file(file, subreddit, title, selftext)
    else:
        previous_subreddit = contents[0].strip()
        previous_title = contents[1].strip().replace('\r', '').replace('\n', '')
        previous_selftext = contents[2].strip().replace('\r', '').replace('\n', '')
        if previous_subreddit != subreddit or previous_title != title or previous_selftext != selftext:
            update_file(file, subreddit, title, selftext)
            slack_url = 'https://slack.com/api/chat.postMessage'
            message_body = {
                'channel': slack_channel,
                'text': 'A new post has been made *' + title + '* in the subreddit *' + subreddit + '* with the body \n>' + selftext + ''
            }
            headers = {
                'Authorization': 'Bearer ' + slack_token,
                'Content-type': 'application/json; charset=utf-8'
            }
            response = requests.post(slack_url, json = message_body, headers = headers)