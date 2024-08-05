import sqlmodel as sql

class HeroTeamLink(sql.SQLModel, table=True):
    hero_id: int|None = sql.Field(default=None, foreign_key="hero.id", primary_key=True)
    team_id: int|None = sql.Field(default=None, foreign_key="team.id", primary_key=True)

class Team(sql.SQLModel, table=True):
    id: int|None = sql.Field(default=None, primary_key=True)
    name: str = sql.Field(index=True)
    headquarters: str
    heroes: list["Hero"] = sql.Relationship(back_populates="teams", link_model=HeroTeamLink)

class Hero(sql.SQLModel, table=True):
    id: int|None = sql.Field(default=None, primary_key=True)
    name: str = sql.Field(index=True)
    secret_name: str
    age: int|None = sql.Field(default=None, index=True)
    teams: list[Team] = sql.Relationship(back_populates="heroes", link_model=HeroTeamLink)

# setup engine
sqlite_file_name = "database4.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = sql.create_engine(sqlite_url, echo=True)

# create db and tables
def create_db_tables():
    sql.SQLModel.metadata.create_all(engine)

def create_heroes():
    with sql.Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

        hero_deadpond = Hero(name="Deadpond", secret_name="Dive Wilson", teams=[team_z_force, team_preventers])
        hero_rusty_man = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48, teams=[team_preventers])
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parquedor", teams=[team_preventers])

        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Deadpond:", hero_deadpond)
        print("Deadpond teams:", hero_deadpond.teams)
        print("Rusty-Man:", hero_rusty_man)
        print("Rusty-Man Teams:", hero_rusty_man.teams)
        print("Spider-Boy:", hero_spider_boy)
        print("Spider-Boy Teams:", hero_spider_boy.teams)

def main():
    create_db_tables()
    create_heroes()

if __name__ == "__main__":
    main()
