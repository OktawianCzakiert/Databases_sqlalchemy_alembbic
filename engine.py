# First you have to run postgres by docker, then create table and insert data into table.
# docker run --name oktawian-postgres -p 5432:5432 -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=mydatabase -d postgres

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://postgres:admin@localhost:5432/mydatabase")
DBSession = sessionmaker(bind=engine)
session = DBSession()
