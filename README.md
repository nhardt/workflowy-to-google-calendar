# Workflowy Calendar

Workflowy calendar is a simple tool to synchronize dates in workflowy to google
calendar.

## Plan

### Prototype

* [X] authenticate to workflowy
* [X] create a sample date entry for testing at top level
~~read a single entry, document metadata~~
* [X] read initialization data to get root node
* [X] parse top level tree from initial data
* [X] find sample item in tree
* [X] authenticate to gcal
* [X] pull list of calendars from API
* [X] pull events from "workflowy" calendar
* [ ] publish any event to gcal
* [ ] publish sample workflowy event to gcal

### Roadmap

* [ ] Get all time tags or get all entries tagged for export (#cal)
* [ ] Publish all dates to calendar named "workflowy"
* [ ] Republish all: delete all dates, republish
* [ ] Smart republish: only publish changes
* [ ] 2 way sync: read/write data on both ends

## Notes

### Workflowy API

There is an unofficial PHP api which seems most supported. there is a python
API that looks half implemented. i'm doing this for fun and to experiment with
Copilot, so I'm going to use the PHP implementation as API docs and write a
Python implementation of the API.

#### Data Model

##### Projects

The entire tree is called a project. The id is projectid. Each project has a list
of child projects, listed under `ch` in the data structure.

##### ID

Each project has a server side assigned uuid named `id`.

### API Endpoints

#### Auth

Workflowy uses https to send a username and password as form data

Endpoint: https://workflowy.com/ajax\_login
Post data: username, password
Result Header: a session cookie
Result Body JSON: success: true|false

#### Init

Endpoint: https://workflowy.com/get\_initialization\_data
Post header: session cookie
Response: JSON encoded tree struccture

This gets your initial tree, not sure to what depth. It does not appear to have
descriptions. 4410c0683221 is what might be displayed in your browser when you
focus on a node, and it is the last part of the node id/uuid.

The result is a tree encoded as json.

```json
{
    "projectTreeData":
    {
        "mainProjectTreeInfo":
        {
            "rootProject": null,
            "rootProjectChildren":
            [
                {
                    "id": "ed8e78eb-dffc-4128-1a44-c60cda112ee6",
                    "nm": "Past",
                    "ct": 97551049,
                    "metadata": {},
                    "lm": 100652553,
                    "ch": []
                }
            ]
        } 
    }
}
```


```json
{
    "id": "d1fb00f8-a095-2483-decd-4410c0683221",
    "nm": "<time startYear=\"2023\" startMonth=\"6\" startDay=\"2\">Fri, Jun 2, 2023</time> post this test node to google calendar",
    "ct": 100726143,
    "metadata": {},
    "lm": 100780842
}
```

## Reference

### Workflowy

* API Zendesk Ticket: https://workflowy.zendesk.com/hc/en-us/community/posts/201100295-API
* PHP: https://github.com/johansatge/workflowy-php
* JS: https://github.com/malcolmocean/opusfluxus
* Python: https://github.com/haaavk/wfapi

### Google Calendar

#### Setup

This part is going to be a bit arduous. There might be an easier way for a
single human to manage their own calendar with scripting but what I've found are
instructions to write code against gcal as if you are an app developer.

In your google calendar, create a new calendar called "workflowy".

##### Create Project That Can Access The Calendar API

If you want to use this app to sync your workflowy to gcal, from what i've
found so far, you need to do these things.

https://developers.google.com/workspace/guides/create-project

##### Auth

Following the docs, to do this on your own you'll need to create an OAuth
client to programatically access your google calendar.

https://developers.google.com/calendar/api/quickstart/python#authorize\_credentials\_for\_a\_desktop\_application

The end result of these few steps are what you save to the
.gcal.credentials.json file. 

##### Enable calendar API

I thought I followed the docs on this before running the script, but on first
login if you haven't done this it will pop up a link to enable it.

#### Reference

* Python GCal API: https://developers.google.com/calendar/api/guides/overview
* https://developers.google.com/calendar/api/quickstart/python

### Python

* https://treelib.readthedocs.io/en/latest/
* https://pypi.org/project/argcomplete/

```
sudo activate-global-python-argcomplete
eval "$(register-python-argcomplete ./proto.py)"
./proto.py -
-h         --help     --wf-auth  --wf-init
```
