def dbMinInfo(db):
    cursor = db.execute("SELECT id, naziv FROM ministarstvo order by id")
    rows = cursor.fetchall()
    ministarsvaList = []
    for row in rows:
        ministarsvaList.append({'id': row[0],
                            'naziv': row[1],
                            })
    return ministarsvaList

def dbGlasaj(db, obecanje, opcija):
    if opcija == 1:
        db.execute("UPDATE obecanje SET ostvareno = ostvareno + 1 WHERE id = ?", (obecanje,))
    elif opcija == 2:
        db.execute("UPDATE obecanje SET utijeku = utijeku + 1 WHERE id = ?", (obecanje,))
    elif opcija == 3:
        db.execute("UPDATE obecanje SET prekrseno = prekrseno + 1 WHERE id = ?", (obecanje,))
    #db.commit()
    return

def dbPonovnoGlasaj(db, obecanje, staraopcija, opcija):
    if opcija == 1:
        db.execute("UPDATE obecanje SET ostvareno = ostvareno + 1 WHERE id = ?", (obecanje,))
    elif opcija == 2:
        db.execute("UPDATE obecanje SET utijeku = utijeku + 1 WHERE id = ?", (obecanje,))
    elif opcija == 3:
        db.execute("UPDATE obecanje SET prekrseno = prekrseno + 1 WHERE id = ?", (obecanje,))

    if staraopcija == 1:
        db.execute("UPDATE obecanje SET ostvareno = ostvareno - 1 WHERE id = ?", (obecanje,))
    elif staraopcija == 2:
        db.execute("UPDATE obecanje SET utijeku = utijeku - 1 WHERE id = ?", (obecanje,))
    elif staraopcija == 3:
        db.execute("UPDATE obecanje SET prekrseno = prekrseno - 1 WHERE id = ?", (obecanje,))
    #db.commit()
    return

def dbObecanja(db):
    cursor = db.execute("SELECT id, tekst, id_min, ostvareno, prekrseno, utijeku, zapoceto FROM obecanje ORDER BY id_min")
    rows = cursor.fetchall()
    obecanjeList = []
    for row in rows:
        obecanjeList.append({'id': row[0],
                            'tekst': row[1],
                            'id_min':row[2],
                            'ostvareno':row[3],
                            'prekrseno':row[4],
                            'utijeku':row[5],
                            'zapoceto':row[6]
                            })
    return obecanjeList

def dbGlasovi(db, obecanje):
    cursor = db.execute("SELECT ostvareno, prekrseno, utijeku FROM obecanje WHERE id = ?", (obecanje,))
    row = cursor.fetchone();
    return {'ostvareno':row[0],
            'prekrseno':row[1],
            'utijeku':row[2],
            'obecanjeId':obecanje
            }