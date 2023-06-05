#!/usr/bin/env python3

from lib.Workflowy import Workflowy
from lib.GCal import GCal
from lib.Event import Event


def main():
    wf = Workflowy()
    if wf.has_init():
        wf.parse_init()
    elif wf.has_session():
        wf.login()
    else:
        wf.init()

    events = wf.get_events()
    for event in events:
        print(f"uuid: {event.uuid}, name: {event.name}, start: {event.start}")

    gcal = GCal()
    # gcal.get_events()
    gcal.insert_event(
        events[0].uuid,
        events[0].name,
        events[0].start.isoformat(),
        events[0].end.isoformat(),
    )

    # for each wf event, gather uuid, name, start, end
    # for each gcal event, check uuid for wf
    #   if not exists, delete event from gcal, remove from wf event list
    #   if exists, update event in gcal, remove from wf event list
    # for each event in wf event list, create event in gcal


if __name__ == "__main__":
    main()
