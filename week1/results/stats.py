import csv
import numpy as np


def main():
    avg_results = [0]
    with open('avg_results.csv', 'r') as csv_file:
        read_lines = csv.reader(csv_file)
        for row in read_lines:
            avg_results.append(row)

    repetitions = 5000
    randomization_test(np.array(avg_results[1], dtype=np.float), np.array(avg_results[3], dtype=np.float), repetitions)


def randomization_test(a, b, repetitions, alpha=0.05):
    a_bk = np.copy(a)
    b_bk = np.copy(b)
    mean_a = np.mean(a_bk)
    mean_b = np.mean(b_bk)
    differences = []
    for _ in np.arange(repetitions):
        a = np.copy(a_bk)
        b = np.copy(b_bk)
        swaps = np.random.randint(1, len(a) + 1)
        swaps_choices = np.random.choice(np.arange(len(a)), size=swaps, replace=False)
        for i in swaps_choices:
            tmp = a[i]
            a[i] = b[i]
            b[i] = tmp
        avg_a = np.mean(a)
        avg_b = np.mean(b)
        differences.append(avg_a - avg_b)
        del a, b
    differences = sorted(differences)
    diff_mean = mean_a - mean_b
    count = 0
    for diff in differences:
        if diff_mean > diff:
            count += 1
    if (count / repetitions) > (1 - alpha):
        print('Two systems are significantly different.')
    else:
        print('Two systems are not significantly different.')


if __name__ == '__main__':
    main()
