import json
import logging
import pathlib

from sqlmodel import Session, SQLModel, select

from fastapi_app import models


def load_from_json():
    models.create_db_and_tables()

    path = pathlib.Path(__file__).parent.parent.absolute()
    with open(path / "seed_data.json") as f:
        data = json.load(f)

        with Session(models.engine) as session:
            # check if data is already loaded
            if session.exec(select(models.Destination)).first():
                logging.info("Data already loaded, skipping seed data load")
                return
            for entry in data:
                if entry["model"] == "relecloud.destination":
                    destination = models.Destination(
                        name=entry["fields"]["name"],
                        id=entry["pk"],
                        description=entry["fields"]["description"],
                    )
                    session.add(destination)
                    session.commit()
                    session.refresh(destination)
                if entry["model"] == "relecloud.cruise":
                    destinations = []

                    for destination in entry["fields"]["destinations"]:
                        destination = session.exec(
                            select(models.Destination).where(models.Destination.id == destination)
                        )
                        destinations.append(destination.first())

                    cruise = models.Cruise(
                        name=entry["fields"]["name"],
                        id=entry["pk"],
                        description=entry["fields"]["description"],
                        destinations=destinations,
                    )
                    session.add(cruise)
                    session.commit()
                    session.refresh(cruise)


def drop_all():
    # Explicitly remove these tables first to avoid cascade errors
    SQLModel.metadata.remove(models.Cruise.__table__)
    SQLModel.metadata.remove(models.Destination.__table__)
    SQLModel.metadata.drop_all(models.engine)


if __name__ == "__main__":
    load_from_json()
