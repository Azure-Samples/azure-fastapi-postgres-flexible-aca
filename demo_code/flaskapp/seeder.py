import json

from . import models


def seed_data(db, filename):
    with open(filename) as f:
        data = json.load(f)
        session = db.session
        for entry in data:
            if entry['model'] == 'relecloud.destination':
                destination = session.get(models.Destination, entry['pk'])
                if destination is None:
                    destination = models.Destination(
                        name=entry['fields']['name'],
                        id=entry['pk'],
                        description=entry['fields']['description'],
                    )
                    session.add(destination)
                    session.commit()
                    session.refresh(destination)
            if entry['model'] == 'relecloud.cruise':
                cruise = session.get(models.Cruise, entry['pk'])
                if cruise is None:
                    destinations = []

                    for destination_id in entry['fields']['destinations']:
                        destination = session.get(models.Destination, destination_id)
                        if destination is None:
                            raise Exception(f"Destination with id {destination_id} not found")
                        link = models.CruiseDestinationLink()
                        link.destination = destination
                        destinations.append(link)
                    
                    cruise = models.Cruise(
                        name=entry['fields']['name'],
                        id=entry['pk'],
                        description=entry['fields']['description'],
                        destinations=destinations,
                    )
                    session.add(cruise)
                    session.commit()
                    session.refresh(cruise)