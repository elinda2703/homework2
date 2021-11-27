import csv
try:
    with open("vstup.csv", encoding="utf-8") as csvinfile, open("vystup_7denni.csv", "w", encoding="utf-8", newline="") as csvoutfile_week, open("vystup_rok.csv", "w", encoding="utf-8", newline="") as csvoutfile_year:
        reader = csv.reader(csvinfile, delimiter=",")
        writer_week = csv.writer(csvoutfile_week)
        writer_year = csv.writer(csvoutfile_year)
        first_date_week = None  # datum 1. dne v tydne
        first_date_year = None  # datum 1. dne v roce
        days_in_week = 0  # pocitatdlo dnu v tydnu, po 7 se vynuluje
        days_in_year = 0  # pocitadlo dnu v roce, po zmene roku se vynuluje
        prefix = None  # nejaky kod ze vstupniho souboru, celou dobu stejny
        prutok_sum_week = 0  # soucet prutoku z celeho tydne, ze ktereho se spocita prumer
        prutok_sum_year = 0  # soucet prutoku z roku tydne, ze ktereho se spocita prumer
        max_prutok = None  # vrati datum a velikost nejvetsiho prutoku ze vstupu
        min_prutok = None  # vrati datum a velikost nejmensiho prutoku ze vstupu
        chyby_v_prutoku = []  # vrati seznam dat zapornych a nulovych prutoku

        # cyklus probehne tolikrat, kolik je ve vstupu radku
        for row in reader:
            if max_prutok is None:
                max_prutok = row[2:6]

            if min_prutok is None:
                min_prutok = row[2:6]

            if float(row[5]) <= 0:
                chyby_v_prutoku.append(row[2:5])

            if float(max_prutok[3]) < float(row[5]):
                max_prutok = row[2:6]

            if float(min_prutok[3]) > float(row[5]):
                min_prutok = row[2:6]

            if prefix is None:
                prefix = row[0:2]

            if first_date_week is None:
                first_date_week = row[2:5]

            if first_date_year is None:
                first_date_year = row[2:5]

            # vypise prislusna data do vystupu, nastavi spravny 1. den v tydnu, vynuluje soucet prutoku a pocitatdlo dni
            if days_in_week == 7:

                writer_week.writerow(prefix + first_date_week +
                                     [round(prutok_sum_week/days_in_week, 4)])
                prutok_sum_week = 0
                first_date_week = row[2:5]
                days_in_week = 0

            # vypise prislusna data do vystupu, nastavi spravny 1. den v roce, vynuluje soucet prutoku a pocitatdlo dni
            if first_date_year[0] != row[2]:
                writer_year.writerow(prefix + first_date_year +
                                     [round(prutok_sum_year/days_in_year, 4)])
                prutok_sum_year = 0
                first_date_year = row[2:6]
                days_in_year = 0

            # prida den na konci cyklu
            days_in_week += 1
            days_in_year += 1

            # kumulativne scita prutoky
            prutok_sum_week += float(row[5])
            prutok_sum_year += float(row[5])
            
        # cyklus skonci pred vypsanim posledniho dne do vystupu, potreba pridat za cyklus
        writer_week.writerow(prefix + first_date_week +
                             [round(prutok_sum_year/days_in_week, 4)])
        writer_year.writerow(prefix + first_date_year +
                             [round(prutok_sum_year/days_in_year, 4)])
        print(
            f"Maximální průtok nastal {max_prutok[2]}.{max_prutok[1]}.{max_prutok[0]}, tento průtok byl {float(max_prutok[3])}.")
        print(
            f"Minimální průtok nastal {min_prutok[2]}.{min_prutok[1]}.{min_prutok[0]}, tento průtok byl {float(min_prutok[3])}.")

        if len(chyby_v_prutoku)!=0:
            print(f"Nekladný průtok nastal ve dnech {chyby_v_prutoku}.")


except FileNotFoundError:
    print("Neplatný vstup, soubor nenalezen")
except IndexError:
    print ("chyba ve vstupních datech")
