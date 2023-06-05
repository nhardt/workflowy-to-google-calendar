#!/usr/bin/env python3

import Workflowy from lib.Worfklowy
import GCal from lib.GCal
import Event from lib.Event

class Event:
    def __init__(self, uuid, name, start, end):
        self.uuid = uuid
        self.name = name
        self.start = start
        self.end = end


def main():
    wf = Workflowy()
    if wf.has_session():
        wf.login()
    else:
        wf.init()

    gcal = GCal()
    gcal.get_events()

    events = wf.get_events()

    # for each wf event, gather uuid, name, start, end
    # for each gcal event, check uuid for wf
    #   if not exists, delete event from gcal, remove from wf event list
    #   if exists, update event in gcal, remove from wf event list
    # for each event in wf event list, create event in gcal


if __name__ == "__main__":
    main()
