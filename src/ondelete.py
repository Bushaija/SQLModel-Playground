import sqlmodel as sql

class Team(sql.SQLModel, table=True):
    id: int|None = sql.Field(default=None, primary_key=True)
    name: str = sql.Field(index=True)
    headquarters: str
    heroes: list["Hero"] = sql.Relationship(
        back_populates="team",
        cascade_delete=True
    )

class Hero(sql.SQLModel, table=True):
    id: int|None = sql.Field(default=None, primary_key=True)
    name: str = sql.Field(index=True)
    secret_name: str 
    age: int|None = sql.Field(default=None, index=True)
    team_id: int|None = sql.Field(
        default=None, 
        foreign_key="team.id", 
        ondelete="CASCADE" # SET NULL
    )
    team: Team|None = sql.Relationship(back_populates="heroes")

# create engine
sqlite_filename = "database3"
sqlite_url = f"sqlite:///{sqlite_filename}"
engine = sql.create_engine(sqlite_url, echo=True)

# Enable foreign key support in SQLite
def create_db_tables():
    sql.SQLModel.metadata.create_all(engine)
    with engine.connect() as connection:
        connection.execute(sql.text("PRAGMA foreign_keys=ON"))
