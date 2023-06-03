#!/usr/bin/env python3

import argparse
import urllib.request
import urllib.parse
import getpass


def main():
    # create argparse for wf-auth, wf-read
    parser = argparse.ArgumentParser(description="get commands")
    parser.add_argument("--wf-auth", action="store_true", help="test auth to workflowy")
    args = parser.parse_args()

    if args.wf_auth:
        (username, password) = login()
        wf_auth(username, password)
    else:
        print(parser.print_help())


# https://stackoverflow.com/a/1761754
def login():
    username = input("Username [%s]: " % getpass.getuser())
    password = getpass.getpass("Password: ")
    return username, password


def wf_auth(username, password):
    # it looks like to use the workflowy login API, you post urlencoded
    # username and password to the auth url

    # auth: https://workflowy.com/ajax_login
    # http post fields: username, password, next=/, redirect=false
    # post data is application/x-www-form-urlencoded

    # create http request to auth url
    request = urllib.request.Request("https://workflowy.com/ajax_login")
    # add headers
    request.add_header("Content-Type", "application/x-www-form-urlencoded")
    # add data
    data = urllib.parse.urlencode(
        {
            "username": username,
            "password": password,
            "next": "/",
            "redirect": "false",
        }
    )
    # encode data
    data = data.encode("ascii")
    # send request
    response = urllib.request.urlopen(request, data)
    # read response
    response = response.read().decode("utf-8")
    # print response
    print(response)


if __name__ == "__main__":
    main()
