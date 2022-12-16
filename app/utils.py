from fastapi import HTTPException, status
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashed(password: str):
    return password_context.hash(password)

def verified(password: str, db_password: str):
    return password_context.verify(password, db_password)

def isChoixSexe(choix) -> int:
    if choix == "M":
        temp = 1
    elif choix == "F":
        temp = 2	
    else:
        temp = 3	
    
    return temp	


def incorrect_pass():
    return "Mot de passe incorrect"

def no_account():
    return "Vous n'avez pas de compte"

def generateur_qualite_note_grade_mention(note: float):
    qualite_note_grade_mention = {"qualite_note": 0.0, "grade": "", "mention":""}

    if 0.00 <= note <= 28.99 :
        qualite_note_grade_mention["qualite_note"] = 0.00
        qualite_note_grade_mention["grade"] = "F"
        qualite_note_grade_mention["mention"] = "Echec"
    elif 29.00 <= note <= 34.99 :
        qualite_note_grade_mention["qualite_note"] = 0.00
        qualite_note_grade_mention["grade"] = "E"
        qualite_note_grade_mention["mention"] = "Echec"
    elif 35.00 <= note <= 39.99:
        qualite_note_grade_mention["qualite_note"] = 1.00
        qualite_note_grade_mention["grade"] = "D"
        qualite_note_grade_mention["mention"] = "Credits capitalisés non transférables"
    elif 40.00 <= note <= 44.99:
        qualite_note_grade_mention["qualite_note"] = 1.30
        qualite_note_grade_mention["grade"] = "D+"
        qualite_note_grade_mention["mention"] = "Credits capitalisés non transférables"
    elif 45.00 <= note <= 49.99:
        qualite_note_grade_mention["qualite_note"] = 1.70
        qualite_note_grade_mention["grade"] = "C-"
        qualite_note_grade_mention["mention"] = "Credits capitalisés non transférables"
    elif 50.00 <= note <= 54.99:
        qualite_note_grade_mention["qualite_note"] = 2.00
        qualite_note_grade_mention["grade"] = "C"
        qualite_note_grade_mention["mention"] = "Passable"
    elif 55.00 <= note <= 59.99:
        qualite_note_grade_mention["qualite_note"] = 2.30
        qualite_note_grade_mention["grade"] = "C+"
        qualite_note_grade_mention["mention"] = "Passable"
    elif 60.00 <= note <= 64.99:
        qualite_note_grade_mention["qualite_note"] = 2.70
        qualite_note_grade_mention["grade"] = "B-"
        qualite_note_grade_mention["mention"] = "Assez bien"
    elif 65.00 <= note <= 69.99:
        qualite_note_grade_mention["qualite_note"] = 3.00
        qualite_note_grade_mention["grade"] = "B"
        qualite_note_grade_mention["mention"] = "Assez bien"
    elif 70.00 <= note <= 74.99:
        qualite_note_grade_mention["qualite_note"] = 3.30
        qualite_note_grade_mention["grade"] = "B+"
        qualite_note_grade_mention["mention"] = "Bien"
    elif 75.00 <= note <= 79.99:
        qualite_note_grade_mention["qualite_note"] = 3.70
        qualite_note_grade_mention["grade"] = "A-"
        qualite_note_grade_mention["mention"] = "Bien"
    elif 80.00 <= note <= 100.00:
        qualite_note_grade_mention["qualite_note"] = 4.00
        qualite_note_grade_mention["grade"] = "A"
        qualite_note_grade_mention["mention"] = "Très bien"
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="La note doit etre comprise entre 0 et 100")
    
    return qualite_note_grade_mention	