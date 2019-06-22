import argparse

from Utils.AlumniParser import AlumniParser
from Utils.Classroom import ClassDistribution, conditionBuilder


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', metavar='RUTA', type=str, nargs=1,
                        help='Ruta al fitxer csv')

    args = parser.parse_args()

    path_to_input_file = args.input_file[0]

    return path_to_input_file


def main():
    path_to_input_file = parseArguments()

    parser = AlumniParser(path_to_input_file)
    alumni = parser.getAlumni()

    #for alumnus in alumni:
        #print(alumnus)

    classDistribution = ClassDistribution(alumni, ['3r A', '3r B'], seed=1)
    c1 = conditionBuilder("SPLITTED", alumni[1], alumni[2])
    c2 = conditionBuilder("SPLITTED", alumni[3], alumni[4])
    c3 = conditionBuilder("SPLITTED", alumni[1], alumni[5])
    c4 = conditionBuilder("TOGETHER", alumni[1], alumni[6])
    classDistribution.addCondition(c1)
    classDistribution.addCondition(c2)
    classDistribution.addCondition(c3)
    classDistribution.addCondition(c4)
    print(c1)
    print(c2)
    print(c3)
    print(c4)

    classrooms = classDistribution.distributeAlumni()

    for classroom in classrooms:
        print(classroom)


if __name__ == '__main__':
    main()
