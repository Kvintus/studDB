from sqlalchemy import text
from sqlClasses import *
import generator

gen = generator.Generator()

def getSurnames():
    surnames = []
    students = db.engine.execute(
        text('select distinct studentSurname from Students'))
    for student in students:
        surnames.append(student[0])

    for i in range(len(surnames)):
        if surnames[i][-3:] == "ová":
            surnames[i] = surnames[i][:-3]

    return surnames


def main():
    hlav = list(set(getSurnames()))
    for surname in hlav:
        # Vytovrit zenu
        zena_meno = gen.generateZena()
        zena = Parent(
            parentName = zena_meno,
            parentSurname = surname + "ová",
            parentEmail = "{}.{}@gmail.com".format(surname.lower() + "ová", zena_meno.lower()),
            parentPhone = gen.generatePhoneNumber(),
            parentAdress = gen.generateStreet()
        )
        db.session.add(zena)
        # vyrvorit muza
        muz_meno = gen.generateMuz()
        muz = Parent(
            parentName = muz_meno,
            parentSurname = surname,
            parentEmail = "{}.{}@gmail.com".format(surname.lower(), muz_meno.lower()),
            parentPhone = gen.generatePhoneNumber(),
            parentAdress = gen.generateStreet()
        )
        db.session.add(muz)

        for student in Students.query.all():
            if surname in student.studentSurname:
                student.parents.append(zena)
                student.parents.append(muz)
    
    db.session.commit()


        


if __name__ == '__main__':
    main()
