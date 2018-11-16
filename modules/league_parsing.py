from app import db
import urllib3
from bs4 import BeautifulSoup
from sqlalchemy import inspect

http = urllib3.PoolManager()


class League(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    numTeams = db.Column(db.Integer, nullable=False)
    firstYear = db.Column(db.Integer, nullable=False)
    teams = db.relationship("Team", backref="league", lazy=True, cascade="all, delete, delete-orphan")


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    ownerName = db.Column(db.String(128), nullable=False)
    leagueID = db.Column(db.Integer, db.ForeignKey("league.id"), nullable=False)
    year = db.Column(db.Integer, nullable=False)


def loadLeague(leagueID):
    return League.query.filter_by(id=leagueID).first()


def parseLeague(leagueID):
    url = "http://games.espn.com/ffl/leagueoffice?leagueId="
    url += leagueID
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, "html.parser")


    leagueName = soup.find_all("h1", title=True)[0].string
    numTeams = soup.find(text="Teams:").next

    #firstYear
    tag = soup.find(id="seasonHistoryMenu")
    if tag is None:
        firstYear = "2017"
    else:
        tag = tag.find_all("option")
        temp = BeautifulSoup(str(tag[-1]), "html.parser")
        firstYear = temp.find("option").contents[0]

    newLeague = League(id=int(leagueID), name=str(leagueName), numTeams=int(numTeams), firstYear=int(firstYear))
    return newLeague


def parseTeams(leagueID, numTeams):
    urlBase = "http://games.espn.com/ffl/clubhouse?leagueId="
    urlBase += leagueID
    urlBase += "&teamId="

    teams = []
    for i in range(1, numTeams + 1):
        url = urlBase
        url += str(i)
        response = http.request('GET', url)
        soup = BeautifulSoup(response.data, "html.parser")

        teamName = soup.find(class_="team-name").contents[0]
        ownerName = soup.find(class_="per-info").contents[0]
        team = Team(number=int(i), name=str(teamName), ownerName=str(ownerName), leagueID=str(leagueID), year=2017)
        teams.append(team)
    return teams


def updateLeagueInfo(leagueID):
    checkLeague = loadLeague(leagueID)
    if checkLeague is not None:
        #delete league before updating
        db.session.delete(checkLeague)
        db.session.commit()


    league = parseLeague(leagueID)
    teams = parseTeams(leagueID, league.numTeams)
    db.session.add(league)
    for team in teams:
        db.session.add(team)
    db.session.commit()


def upToDate(tableObject):
    defaults = {"INTEGER" : 0, "VARCHAR(128)" : ""}
    mapper = inspect(tableObject.__class__)
    for col in mapper.columns:
        name = col.name
        type = str(col.type)
        currentValue = tableObject.__getattribute__(name)
        if defaults[type] == currentValue:
            return False
    return True


# checks to see if league and teams are already in database with all attirbutes
# if not, any data is deleted and re-parsed from ESPN
def checkLeagueInfo(leagueID):
    league = loadLeague(leagueID)
    if league is not None:
        if upToDate(league):
            update = False
            for team in league.teams:
                if not upToDate(team):
                    update = True
            if not update:
                #league and team info is up to date
                return

    #re-parse all data
    updateLeagueInfo(leagueID)

