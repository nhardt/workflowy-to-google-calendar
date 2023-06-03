#!/usr/bin/env python3

import argparse
import urllib.request
import urllib.parse
import getpass
import json


def main():
    # create argparse for wf-auth, wf-read
    parser = argparse.ArgumentParser(description="get commands")
    parser.add_argument("--wf-auth", action="store_true", help="test auth to workflowy")
    parser.add_argument(
        "--wf-init", action="store_true", help="read init data from workflowy"
    )
    args = parser.parse_args()
    state = load_state()
    if args.wf_auth:
        (username, password) = login()
        wf_auth(state, username, password)
    elif args.wf_read:
        wf_init(state)
    else:
        print(parser.print_help())


def load_state():
    with open(".private_json", "r") as f:
        return json.load(f)


# https://stackoverflow.com/a/1761754
def login():
    username = input("Username [%s]: " % getpass.getuser())
    password = getpass.getpass("Password: ")
    return username, password


def wf_auth(state, username, password):
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
    response = urllib.request.urlopen(request, data.encode("ascii"))
    print(response.info())
    response_body = response.read().decode("utf-8")
    print(response_body)
    response_body_json = json.loads(response_body)
    if response_body_json["success"]:
        for cookie in response.info().get_all("Set-Cookie"):
            # parse cookie. form is name=value; expires=...; path=...
            # we only want the name=value part
            cookie = cookie.split(";")[0]
            (name, value) = cookie.split("=")
            if name == "sessionid":
                state["session_id"] = value
                with open(".private_json", "w") as f:
                    json.dump(state, f)
        print("login successful")


def wf_init(state):
    # i see two other api calls, get_initialization_data and push_and_poll
    # get_initialization_data: https://workflowy.com/get_initialization_data
    # push_and_poll: https://workflowy.com/push_and_poll
    #   this seems to do most of the work. there are 4 actions you can peform:
    #   create, edit, move, delete
    #   each node has properties `projectid`, `name` and `description`

    # looking that php api, it looks like filtering and everything is done
    # client side. from what i can tell, the php client just builds the full
    # tree on start up.
    wf_get_initialization_data(state)
    pass


def wf_get_initialization_data(state):
    ## this call seems to get you the full tree without descriptions
    request = urllib.request.Request("https://workflowy.com/get_initialization_data")
    request.add_header("Cookie", "sessionid=" + state["session_id"])
    response = urllib.request.urlopen(request)
    print(response.info())
    response_body = response.read().decode("utf-8")
    print(response_body)


if __name__ == "__main__":
    main()
