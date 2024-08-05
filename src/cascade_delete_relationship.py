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
    team_id: int|None = sql.Field(default=None, foreign_key="team.id")
    team: Team|None = sql.Relationship(back_populates="heroes")

