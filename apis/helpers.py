# These need to be while loops so we wont delete the same row twice and thus get an error
def deleteAllParents(person):
    """ Deletes all of the parents from the passed person Object """
    while True:
        if len(person.parents.all()) > 0:
            person.parents.remove(person.parents.first())
        else:
            break


def deleteAllClasses(person):
    """ Deletes all classes from passed object """
    while True:
        if len(person.classes.all()) > 0:
            person.classes.remove(person.classes.first())
        else:
            break


def deleteAllPupils(pClass):
    """ Deletes all pupils from passed class """
    while True:
        if len(pClass.pupils.all()) > 0:
            pClass.pupils.remove(pClass.pupils.first())
        else:
            break


def deleteAllProfessors(pClass):
    """ Deletes all professors from passed class """
    while True:
        if len(pClass.profs.all()) > 0:
            pClass.profs.remove(pClass.profs.first())
        else:
            break
