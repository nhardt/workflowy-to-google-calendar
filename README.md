# Workflowy Calendar

Workflowy calendar is a simple tool to synchronize dates in workflowy to google
calendar.

## Plan

### Prototype

* [X] authenticate to workflowy
* [X] create a sample date entry for testing at top level
~~read a single entry, document metadata~~
* [X] read initialization data to get root node
* [ ] read top level list to get sample item
* [ ] print sample item details
* [ ] authenticate to gcal
* [ ] publish sample date entry  

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

* Python GCal API: https://developers.google.com/calendar/api/guides/overview

### Treelib

* https://treelib.readthedocs.io/en/latest/
