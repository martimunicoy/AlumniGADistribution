import argparse

from Utils.Classroom import ClassDistribution, addConditionsFromFile
from Utils.AlumniParser import AlumniParser
from Utils.Optimizer import BruteForceOptimizer


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', metavar='RUTA', type=str, nargs=1,
                        help='Ruta al fitxer csv')
    parser.add_argument('-c', '--conditions', metavar='RUTA', type=str,
                        nargs=1, required=False, default=[None, ],
                        help='Ruta al fitxer amb les condicions inicials')
    parser.add_argument('-o', '--output', metavar='RUTA', type=str,
                        nargs=1, required=False, default=['resultats.txt', ],
                        help='Ruta cap al fitxer de sortida')
    parser.add_argument('-i', '--iterations', metavar='RUTA', type=int,
                        nargs=1, required=False, default=[1000, ],
                        help='Número d\'iteracions de l\'optimitzador')
    parser.add_argument('-s', '--seed', metavar='RUTA', type=int,
                        nargs=1, required=False, default=[None, ],
                        help='Llavor pel generador de nombres pseudoaleatoris')
    parser.add_argument('-n', '--classnames', metavar='NAME', type=str,
                        nargs='*', required=False,
                        default=["Classe A", "Classe B"],
                        help='Nom de cada classe')

    args = parser.parse_args()

    path_to_input_file = args.input_file[0]
    path_to_conditions_file = args.conditions[0]
    output_path = args.output[0]
    iterations = args.iterations[0]
    seed = args.seed[0]
    class_names = args.classnames

    return path_to_input_file, path_to_conditions_file, output_path, \
        iterations, seed, class_names


def main():
    print("----------------------------------")
    print("|     Distribuidor d\'alumnes     |")
    print("----------------------------------")
    print(" Versió: 1.0")
    print(" Autor: Martí Municoy Terol")
    print(" Contacte: mail@martimunicoy.com")
    print("----------------------------------")
    path_to_input_file, path_to_conditions_file, output_path, iterations, \
        seed, class_names = parseArguments()

    try:
        parser = AlumniParser(path_to_input_file)
    except FileNotFoundError:
        raise NameError("No s\'ha trobat el fitxer csv a " +
                        "\'{}\'".format(path_to_input_file))

    alumni = parser.getAlumni()

    class_distribution = ClassDistribution(alumni, class_names, seed=seed)

    if (path_to_conditions_file is not None):
        try:
            addConditionsFromFile(path_to_conditions_file, class_distribution)
        except FileNotFoundError:
            raise NameError("No s\'ha trobat el fitxer de condicions " +
                            "inicials a " +
                            "\'{}\'".format(path_to_conditions_file))

    optimizer = BruteForceOptimizer(class_distribution, iterations=iterations)
    optimizer.optimize()
    optimizer.writeBestClassDistribution(output_path)


if __name__ == '__main__':
    main()
