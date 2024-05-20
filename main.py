import stubhub
import influx

EVENT_PATHS = [
    "/taylor-swift-madrid-tickets-5-29-2024/event/153154649/",
    "/taylor-swift-lisboa-tickets-5-25-2024/event/152013610/",
    "/taylor-swift-london-tickets-6-21-2024/event/151949677/",
    "/taylor-swift-hamburg-tickets-7-23-2024/event/151950363/",
    "/taylor-swift-hamburg-tickets-7-24-2024/event/151973556/",
    "/taylor-swift-london-tickets-8-15-2024/event/151973572/",
    "/taylor-swift-new-orleans-tickets-10-25-2024/event/152129103/",
    "/taylor-swift-new-orleans-tickets-10-26-2024/event/152129104/",
    "/taylor-swift-new-orleans-tickets-10-27-2024/event/152129105/",
    "/taylor-swift-toronto-tickets-11-14-2024/event/152129115/",
    "/taylor-swift-toronto-tickets-11-15-2024/event/152129114/",
    "/taylor-swift-toronto-tickets-11-16-2024/event/152129116/",
    "/taylor-swift-toronto-tickets-11-21-2024/event/152129140/",
    "/taylor-swift-toronto-tickets-11-22-2024/event/152129141/",
    "/taylor-swift-toronto-tickets-11-23-2024/event/152129139/",
    "/taylor-swift-vancouver-tickets-12-6-2024/event/152543798/"
]

events = [stubhub.Event(path) for path in EVENT_PATHS]

for event in events:
    event_tickets = event.get_tickets()
    points = [ticket.to_point("eras-tour-tickets") for ticket in event_tickets]

    for point in points:
        influx.write(point)