import argparse


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', metavar='RUTA', type=str, nargs=1,
                        help='Ruta al fitxer csv')

    args = parser.parse_args()

    path_to_input_file = args.input_file[0]

    return path_to_input_file


def main():
    path_to_input_file = parseArguments()

    inputFileParser = InputFileParser(path_to_input_file)
    settings = inputFileParser.createSettings()

    commandsBuilder = CommandsBuilder(settings)
    commands = commandsBuilder.createCommands()

    for command in commands:
        command.run()


if __name__ == '__main__':
    main()
