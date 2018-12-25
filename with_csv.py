import csv


def csv_writer(data, path):
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        init = 0
        for line in data:
            if line:

                init += 1
                writer.writerow([
                    init, line['name'], line['desc'], line['image']
                ])
