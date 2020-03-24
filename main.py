import time
import pymysql
from twython import Twython
userStart = 'laurebretton'


def loginTwitter():
    try:
        twitter = Twython('###','###','###','###')
    except:
        return False
    return twitter

def getFollowers(db, twitter, user, i):
    next_cursor = -1
    while(next_cursor):
        print("Iterations : ",i)
        print("Utilisateur :",user)
        get_friends = twitter.get_friends_list(screen_name=user,count=200,cursor=next_cursor)
        for friend in get_friends["users"]:
            if logToDb(db,user,friend["screen_name"]) == False:
                exit()
            next_cursor = get_friends["next_cursor"]
        time.sleep(60)
        if next_cursor == -1:
            next_cursor = 0
        i += 1
    userId = getUserIdWithDb(db,user)
    addInDbFollowingCheck(db, userId)
    nextUser = getNextUser(db)
    getFollowers(db,twitter,nextUser,i)

def connectToDb():
    connection = pymysql.connect('localhost','###','###',db='###')
    return connection

def closeDb(db):
    db.close()

def getNextUser(db):
    with db.cursor() as cursor:
        sql = "SELECT screenName FROM work.users WHERE idUsers NOT IN (SELECT fkIdUsers FROM followingcheck) LIMIT 1;"
        cursor.execute(sql)
        db.commit()
        result = cursor.fetchone()
        return result[0]

def addInDbFollowingCheck(db, userId):
    with db.cursor() as cursor:
        sql = "INSERT INTO followingcheck (fkIdUsers) VALUES (%s)"
        cursor.execute(sql,(userId))
        db.commit()

def logToDb(db,user,following):
    try:
        with db.cursor() as cursor:
            idUser = getUserIdWithCursor(cursor,user)
            if not idUser:
                sql = "INSERT INTO users (screenName) VALUES (%s)"
                cursor.execute(sql,(user))
                db.commit()
                idUser = getUserIdWithCursor(cursor,user)
            
            idFollow = getUserIdWithCursor(cursor,following)
            if not idFollow:
                sql = "INSERT INTO users (screenName) VALUES (%s)"
                cursor.execute(sql,(following))
                db.commit()
                idFollow = getUserIdWithCursor(cursor,following)
            sql = "INSERT INTO following (fkIdUsers,fkFollowingThisUsers) VALUES (%s,%s)"
            cursor.execute(sql,(idUser,idFollow))
            db.commit()
    except:
        return False

def getUserIdWithDb(db,screenName):
    with db.cursor() as cursor:
        sql = "SELECT idUsers FROM users WHERE screenName = %s"
        cursor.execute(sql,(screenName))
        result = cursor.fetchone()
        if not result:
            return []
        return result[0]


def getUserIdWithCursor(cursor,screenName):
    sql = "SELECT idUsers FROM users WHERE screenName = %s"
    cursor.execute(sql,(screenName))
    result = cursor.fetchone()
    if not result:
        return []
    return result[0]

def main():
    twitter = loginTwitter()
    if twitter == False:
        exit()
    else:
        print("Connexion valide !")
    try:
        db = connectToDb()
        with db.cursor() as cursor:
            id = getUserIdWithCursor(cursor,userStart)
            if not id:
                sql = "INSERT INTO users (screenName) VALUES (%s)"
                cursor.execute(sql,(userStart))
                db.commit()
            getFollowers(db,twitter, userStart, 1492)
    except:
        print("MARCHE PAS BORDEL DE FION")
    print("Fini")

main()
#1241443850524254213-zmc3ZMYQNiQIeSiNP9LOibN3teRKEw
#secret
#OQfLfkIplMWF2dJOxgDGxayqJKgwKPYGNYa0FmTNs2Tgx