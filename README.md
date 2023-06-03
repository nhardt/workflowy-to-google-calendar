# Workflowy Calendar

Workflowy calendar is a simple tool to synchronize dates in workflowy to google
calendar.

## Plan

### Prototype

* [ ] authenticate to workflowy
* [ ] create a sample date entry for testing
* [ ] read a single entry, document metadata
* [ ] authenticate to gcal
* [ ] publish sample date entry  

### Roadmap

* [ ] Get all dates or get all entries with a tag
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

### ID

A top of mind idea is that I'll need an ID of some sort. this will either exist in the 
workflowy metadata or i'll have to assign one. worst case i think a calendar
named workflowy on the gcal side could be cleared entirely an re-published to
would work for expensive 1 way sync.

## Reference

### Workflowy

* API Zendesk Ticket: https://workflowy.zendesk.com/hc/en-us/community/posts/201100295-API
* PHP: https://github.com/johansatge/workflowy-php
* JS: https://github.com/malcolmocean/opusfluxus
* Python: https://github.com/haaavk/wfapi

### Google Calendar

* Python GCal API: https://developers.google.com/calendar/api/guides/overview

