import sqlmodel as sql

class HeroTeamLink(sql.SQLModel, table=True):
    team_id: int|None = sql.Field(
        default=None,
        foreign_key="team.id",
        primary_key=True
    )
    hero_id: int|None = sql.Field(
        default=None,
        foreign_key="hero.id",
        primary_key=True
    )

class Team(sql.SQLModel, table=True):
    id: int|None = sql.Field(default=None, primary_key=True)
    name: str = sql.Field(index=True)
    headquarter: str
    heroes: list["Hero"] = sql.Relationship(
        back_populates="teams",
        link_model=HeroTeamLink
    )

class Hero(sql.SQLModel, table=True):
    id: int|None = sql.Field(default=None, primary_key=True)
    name: str = sql.Field(index=True)
    secret_name: str
    age: int = sql.Field(index=True)
    team: Team|None = sql.Relationship(
        back_populates="heroes",
        link_model=HeroTeamLink
    )

# create engine
sqlite_file_name = "database3.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = sql.create_engine(sqlite_url, echo=True)

# create tables and db
def create_db_tables():
    sql.SQLModel.metadata.create_all(engine)

def main():
    create_db_tables()

if __name__ == "__main__":
    main()