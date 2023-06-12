from sqlmodel import Session, SQLModel, select
import json
import models


def load_from_json():
    models.create_db_and_tables()

    with open('seed_data.json') as f:
        data = json.load(f)
        
        with Session(models.engine) as session:
            for entry in data:
                if entry['model'] == 'relecloud.destination':
                    destination = models.Destination(
                        name=entry['fields']['name'],
                        id=entry['pk'],
                        description=entry['fields']['description'],
                    )
                    session.add(destination)
                    session.commit()
                    session.refresh(destination)
                if entry['model'] == 'relecloud.cruise':
                    destinations = []

                    for destination in entry['fields']['destinations']:
                        destination = session.exec(select(models.Destination).where(models.Destination.id == destination))
                        destinations.append(destination.first())
                    
                    cruise = models.Cruise(
                        name=entry['fields']['name'],
                        id=entry['pk'],
                        description=entry['fields']['description'],
                        destinations=destinations,
                    )
                    session.add(cruise)
                    session.commit()
                    session.refresh(cruise)

if __name__ == "__main__":
    load_from_json()