#!/usr/bin/env python3

from lib.Workflowy import Workflowy
from lib.GCal import GCal
from lib.Event import Event


def main():
    wf = Workflowy()
    if wf.has_init():
        wf.parse_init()
    elif wf.has_session():
        wf.init()
        wf.parse_init()
    else:
        wf.login()

    gcal = GCal()

    events = wf.get_events()
    for event in events:
        gcalEvent = gcal.get_event(event.uuid)
        if gcalEvent:
            print("Updating event: " + event.name)
            gcal.update_event(
                gcalEvent["id"],
                event.name,
                event.start.isoformat(),
                event.end.isoformat(),
            )
        else:
            print("Inserting event: " + event.name)
            gcal.insert_event(
                event.uuid,
                event.name,
                event.start.isoformat(),
                event.end.isoformat(),
            )


if __name__ == "__main__":
    main()
