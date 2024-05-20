import re
import json
import requests
from dataclasses import dataclass

LOCATION_REGEX = r"taylor-swift-(.*?)-tickets"
DATE_REGEX = r"(\d{1,2}-\d{1,2}-\d{4})"
STUBHUB_URL = "https://www.stubhub.ca/"

@dataclass
class Event:
    path: str

    @classmethod
    def search_params(cls, sort_by="CALCULATEDBESTVALUE", page_size=100, sort_direction=0):
        return {
            "ShowAllTickets": False,
            "HideDuplicateTicketsV2": True,
            "Quantity": 2,
            "PageSize": 100,
            "SortBy": sort_by,
            "SortDirection": sort_direction,
            "ExcludeSoldListings": True,
            "RemoveObstructedView": True,
            "Method": "IndexSh",
        }

    def location(self):
        return re.search(LOCATION_REGEX, self.path).group(1)

    def date(self):
        return re.search(DATE_REGEX, self.path).group(1)
    
    def search_tickets(self, sort_by="CALCULATEDBESTVALUE", page_size=100, sort_direction=0):
        search_params = self.search_params(sort_by, page_size, sort_direction)
        response = requests.post(
            self.event_page,
            headers={'content-type': 'application/json'},
            data=json.dumps(search_params)
        )

        return response.json()["items"]

    @property
    def event_page(self):
        return f"{STUBHUB_URL}{self.path}/"

    def get_tickets(self):
        best_value = self.search_tickets()
        cheapest = self.search_tickets(sort_by="NEWPRICE", page_size=200)
        most_expensive = self.search_tickets(sort_by="PRICE", page_size=100, sort_direction=1)

        items = best_value + cheapest + most_expensive

        tickets = [self.build_ticket(item) for item in items if self.build_ticket(item) is not None]

        return tickets

    def build_ticket(self, data):
        data["date"] = self.date()
        data["location"] = self.location()
        try:
            return Ticket.from_dict(data)
        except KeyError as e:
            print(f"Error parsing ticket: {data}")
            print(e)
            return None

@dataclass
class Ticket:
    id: int
    ticketClass: str
    date: str
    location: str
    rawPrice: int
    section: str
    row: str
    listing_notes: str
    vfs_url: str
    active_since: str
    created_at: str
    dealScore: float
    seatQualityScore: float
    discount: float

    @classmethod
    def from_dict(cls, data):

        listing_notes = data.get("listingNotes", [])
        formatted_notes = [note["formattedListingNoteContent"] for note in listing_notes]
        formatted_notes = " ".join(formatted_notes)

        score = data.get("inventoryListingScore", {})

        return cls(
            id=data["id"],
            ticketClass=data.get("ticketClassName", "Unknown"),
            date=data["date"],
            location=data["location"],
            rawPrice=data["rawPrice"],
            section=data["section"],
            row=data.get("row", ""),    
            listing_notes=formatted_notes,
            vfs_url=data.get("vfsUrl", ""),
            active_since=data["formattedActiveSince"],
            created_at=data["createdDateTime"],
            dealScore=score.get("dealScore", 0),
            seatQualityScore=score.get("seatQualityScore", 0),
            discount=score.get("discount", 0),
        )
    

    def to_point(self, measurement="ts-ticket"):
        return {
            "measurement": measurement,
            "tags": {
                "date": self.date,
                "location": self.location,
                "section": self.section,
                "row": self.row,
                "ticketClass": self.ticketClass,
                "vfs_url": self.vfs_url,
                "dealScore": self.dealScore,
                "seatQualityScore": self.seatQualityScore,
                "discount": self.discount,
            },
            "fields": {
                "price": self.rawPrice,
                "id": self.id,
                "dealScore": float(self.dealScore),
                "seatQualityScore": float(self.seatQualityScore),
                "discount": float(self.discount),
            },
            "time": self.created_at
        }
