"Утилита для обновления прочности по заданным параметрам в csv-файле"
import csv
import sys
import glob


def get_models_durability():
    """Загрузить прочность объектов из csv-файла"""
    models_durability = {}
    with open('durability.csv') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            models_durability[row[0]] = int(row[1])
    return models_durability


def update_durability(group_file):
    """Обновить прочность объектов в .Group файле"""
    models_durability = get_models_durability()
    lines = []
    next_durability = 0
    wait_durability = False
    with open(group_file) as file:
        for line in file.readlines():
            if line.strip().startswith('Model ='):
                lines.append(line)
                for model, durability in models_durability.items():
                    if model in line:
                        wait_durability = True
                        next_durability = durability
                        break
            elif wait_durability and line.strip().startswith('Durability ='):
                wait_durability = False
                line_parts = line.split(' = ')
                new_line = '{field} = {value};\n'.format(field=line_parts[0], value=next_durability)
                lines.append(new_line)
            else:
                lines.append(line)

    with open(group_file, 'w') as file:
        file.writelines(lines)


if __name__ == '__main__':
    try:
        files = glob.glob(str(sys.argv[1]) + '/**', recursive=True)
        for path in files:
            if path.endswith('.Group'):
                print(path)
                update_durability(path)
    except Exception as exception:
        print(exception)
        input('Press enter to close...')
