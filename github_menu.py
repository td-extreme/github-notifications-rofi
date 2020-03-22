#!/usr/bin/python
import os
import json
import requests
from os.path import expanduser
import argparse

delimiter = "\t"
browser = 'qutebrowser --target window'

def main():
  args = parse()
  if args.selection:
    notification = find_notification(args.selection)
    url = notification_web_url(notification)
    open_url(url)
  else:
    for notification in get_notifications():
      print(notification_label(notification))

def parse():
  parser = argparse.ArgumentParser(description='Notification choosen by the user')
  parser.add_argument('selection', type=str, nargs='?', help='')
  return parser.parse_args()

def open_url(url):
  os.system(browser + " " + url)

def find_notification(selection):
  for notification in get_notifications():
    if notification_label(notification) == selection:
        return notification
  return ""

def _github_token():
  home = expanduser("~")
  github_token_file = open(home + "/.tokens/github/access.token", 'r')
  github_token = github_token_file.readline().rstrip()
  github_token_file.close()
  return github_token

def get_notifications():
  response = requests.get('https://api.github.com/notifications', auth=('token', _github_token()))
  return json.loads(response.text)

def notification_label(notification):
  repo = notification["repository"]["name"]
  title = notification["subject"]["title"]
  kind = notification["subject"]["type"]
  id = notification["id"]
  return id + delimiter + repo + delimiter + kind + delimiter + title 

def notification_web_url(notification):
  return notification["subject"]["url"].replace("api.github.com/repos", "github.com").replace("/pulls/", "/pull/")

def mark_as_read(notification):
  requests.patch('https://api.github.com/notifications/threads/' + notification["id"], auth=('token', _github_token()))

if __name__ == "__main__":
  main()
