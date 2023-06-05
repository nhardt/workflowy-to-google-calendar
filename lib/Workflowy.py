#!/usr/bin/env python3
import urllib.request
import urllib.parse
import getpass
import json
import os
from treelib import Node, Tree


class Workflowy:
    def __init__(
        self, state_file=".wf.token.json", last_init_file=".wf.last_init.json"
    ):
        self.state_file = state_file
        self.last_init_file = last_init_file
        self.state = self.load_state()
        self.root_project_node = None

    def load_state(self):
        with open(self.state_file, "r") as f:
            return json.load(f)

    def has_session(self):
        return "sessionid" in self.state

    def has_init(self):
        # return true if init file exists
        return os.path.isfile(self.last_init_file)

    def login(self):
        username = input("Username [%s]: " % getpass.getuser())
        password = getpass.getpass("Password: ")
        self.auth(username, password)

    def auth(username, password):
        request = urllib.request.Request("https://workflowy.com/ajax_login")
        request.add_header("Content-Type", "application/x-www-form-urlencoded")
        data = urllib.parse.urlencode(
            {
                "username": username,
                "password": password,
                "next": "/",
                "redirect": "false",
            }
        )
        response = urllib.request.urlopen(request, data.encode("ascii"))
        response_body = response.read().decode("utf-8")
        response_body_json = json.loads(response_body)
        if response_body_json["success"]:
            for cookie in response.info().get_all("Set-Cookie"):
                # parse cookie. form is name=value; expires=...; path=...
                # we only want the name=value part
                cookie = cookie.split(";")[0]
                (name, value) = cookie.split("=")
                if name == "sessionid":
                    self.state["sessionid"] = value
                    with open(self.state_file, "w") as f:
                        json.dump(self.state, f)
                        return
        raise Exception("login failed")

    def init(self):
        # this call seems gets the initial data for the user
        request = urllib.request.Request(
            "https://workflowy.com/get_initialization_data"
        )
        request.add_header("Cookie", "sessionid=" + self.state["sessionid"])
        response = urllib.request.urlopen(request)
        response_body = response.read().decode("utf-8")
        with open(self.last_init_file, "w") as f:
            f.write(response_body)

    def parse_init(self):
        with open(self.last_init_file, "r") as f:
            data = json.load(f)
        self.root_project_node = data["projectTreeData"]["mainProjectTreeInfo"][
            "rootProjectChildren"
        ]
        # tree = Tree()
        # tree.create_node("root", "root")
        # for child in data["projectTreeData"]["mainProjectTreeInfo"][
        #     "rootProjectChildren"
        # ]:
        #     tree.create_node(child["nm"], child["id"], parent="root", data=child)
        # tree.show()

    def push_and_poll(self):
        # push_and_poll: https://workflowy.com/push_and_poll
        #   this seems to do most of the work. there are 4 actions you can peform:
        #   create, edit, move, delete
        #   each node has properties `projectid`, `name` and `description`
        raise NotImplementedError

    def get_events(self):
        events = []
        self._get_nodes_that_are_events(self.root_project_node, events)
        return events

    def _get_nodes_that_are_events(self, project):
        for node in project:
            if node["nm"].contains("<time"):
                events.append(node)
                print(node)
            else:
                self._get_nodes_that_are_events(node["ch"])


if __name__ == "__main__":
    main()
