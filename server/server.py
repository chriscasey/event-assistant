from mcp.server.fastmcp import FastMCP
from db import Session, init_db
from models import Event, Location, Speaker

init_db()
mcp = FastMCP("EventServer")

@mcp.tool()
def get_schedule() -> list:
    """Get the complete event schedule with all talks, times, locations, and speakers"""
    with Session() as session:
        events = session.query(Event).all()
        return [{
            'id': e.id,
            'name': e.name,
            'time': e.time,
            'location_name': e.location_name,
            'speaker_name': e.speaker_name
        } for e in events]

@mcp.tool()
def get_talk_by_time(time: str) -> dict:
    """Find a specific event/talk happening at a given time (e.g., '10:00', '14:30')"""
    with Session() as session:
        event = session.query(Event).filter_by(time=time).first()
        if event:
            return {
                'id': event.id,
                'name': event.name,
                'time': event.time,
                'location_name': event.location_name,
                'speaker_name': event.speaker_name
            }
        else:
            return {"error": "Not found"}

@mcp.tool()
def get_location(name: str) -> str:
    """Get information about a specific venue or location by name"""
    with Session() as session:
        loc = session.query(Location).filter_by(name=name).first()
        return loc.description if loc else "Unknown location"

@mcp.tool()
def get_speaker_info(name: str) -> str:
    """Get biographical information about a specific speaker by name"""
    with Session() as session:
        speaker = session.query(Speaker).filter_by(name=name).first()
        return speaker.bio if speaker else "Unknown speaker"
