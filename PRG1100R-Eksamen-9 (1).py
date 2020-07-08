from tkinter import *
import pymysql
import time
from datetime import date

koblingDatabase = pymysql.connect(host='localhost',
                                  port=3306,
                                  user='Eksamenssjef',
                                  passwd='eksamen2018',
                                  db='Eksamen2018')

def r_sykkel():
    def registrerSykkel():
        def finnSykkelID(sykkelID):
            markor = koblingDatabase.cursor()
            markor.execute("SELECT * FROM Sykkel")

            sykkelID = int(sykkelID)

            # Gir sykkelID ein verdi for hver linje i tabellen Sykkel
            for row in markor:
                sykkelID += 1
            markor.close()

            markor = koblingDatabase.cursor()
            markor.execute("SELECT * FROM Sykkel")

            # Dersom sykkelID fremdeles finnes, kjør funksjonen på nytt heilt til ein ledig sykkelID blir funnet
            sykkelID_tabell = int(row[0])

            for row in markor:
                if sykkelID == sykkelID_tabell:
                    markor.close()
                    sykkelID += 1
                    finnSykkelID(sykkelID)
                    return

            markor.close()
            skrivInnITabell(sykkelID)

        def skrivInnITabell(sykkelID):
            # Henter dato
            sykkelID = sykkelID
            dato = str(date.today())

            dato = dato[0] + dato[1] + dato[2] + dato[3] + dato[5] + dato[6] + dato[8] + dato[9]

            # Legger til sykkel i databasen
            markor_skrivinn = koblingDatabase.cursor()
            variabel = ("INSERT INTO Sykkel"
                        "(SykkelID, Startdato, StativID, Låsnr)"
                        "VALUES(%s,%s,NULL,NULL)")
            markor_skrivinn.execute(variabel, (sykkelID, dato))
            koblingDatabase.commit()
            markor_skrivinn.close()

            # melding om at sykler er registrert
            feilmelding = 'Sykler registrert'
            utdata.set(str(feilmelding))

            #Oppdater liste
            oversiktavsykkel()

        try:
            antall_sykler = antallSykler_inn.get()

            # Sjekker feilmeldinger
            if len(str(antall_sykler)) == 0:
                feilmelding = 'Skriv inn antall sykler'
                utdata.set(str(feilmelding))
                return
            if len(str(antall_sykler)) > 4:
                feilmelding = 'For mange sykler'
                utdata.set(str(feilmelding))
                return
            if int(antall_sykler) == 0:
                feilmelding = 'Kan ikke registrere 0 sykler'
                utdata.set(str(feilmelding))
                return

            # start på registreing av sykler
            for i in range(int(antall_sykler)):
                sykkelID = 1000
                finnSykkelID(sykkelID)

        except ValueError:
            feilmelding = 'En feil oppstod'
            utdata.set(str(feilmelding))


    def oversiktavsykkel():
        markor = koblingDatabase.cursor()
        markor.execute("SELECT * FROM Sykkel")

        sykkel = []
        for row in markor:
            sykkel += [row[0] + ',     ' + str(row[1]) + ',     ' + str(row[2]) + ',     ' + str(row[3])]

        innhold_i_lst_sykkel.set(tuple(sykkel))
        markor.close()

    regOgOversiktAvSykkel = Toplevel()
    regOgOversiktAvSykkel.title('Registrer sykkel')

    # Labels
    lbl_innhold = Label(regOgOversiktAvSykkel, text='Innhold: sykkelID, startdato, stativID, låsID')
    lbl_innhold.grid(row=0, column=0)

    lbl_registrering = Label(regOgOversiktAvSykkel, text='Registrering av sykkel')
    lbl_registrering.grid(row=0, column=2, columnspan=2, padx=10, pady=10)

    lbl_antallLaaser = Label(regOgOversiktAvSykkel, text='Antall sykler:')
    lbl_antallLaaser.grid(row=1, column=2, padx=5, pady=10, sticky=E)

    # Scrollbar for listen
    y_scroll = Scrollbar(regOgOversiktAvSykkel, orient=VERTICAL)
    y_scroll.grid(row=1, column=1, rowspan=4, padx=(0, 50), pady=15, sticky=NS)

    # Lista
    innhold_i_lst_sykkel = StringVar()
    lst_sykkel = Listbox(regOgOversiktAvSykkel, height=21, width=50, listvariable=innhold_i_lst_sykkel,
                         yscrollcommand=y_scroll.set)
    lst_sykkel.grid(row=1, column=0, rowspan=4, padx=(50, 0), pady=15)
    y_scroll["command"] = lst_sykkel.yview

    # Input StativID og Antall låser
    antallSykler_inn = StringVar()
    ent_r_antallLaaser = Entry(regOgOversiktAvSykkel, width=4, textvariable=antallSykler_inn)
    ent_r_antallLaaser.grid(row=1, column=3, padx=5, pady=10)

    # Knapp
    btn_registrer = Button(regOgOversiktAvSykkel, text='Registrer ny sykkel', command=registrerSykkel)
    btn_registrer.grid(row=2, column=3, padx=5, pady=10, sticky=N)

    # Label
    lbl_melding = Label(regOgOversiktAvSykkel, text='Melding:')
    lbl_melding.grid(row=3, column=2, padx=10, pady=10, sticky=E)

    # Outputs
    utdata = StringVar()
    ent_utdata = Entry(regOgOversiktAvSykkel, width=40, state='readonly', textvariable=utdata)
    ent_utdata.grid(row=3, column=3, padx=15, pady=15)

    # tilbake til hovedmeny
    btn_avslutt = Button(regOgOversiktAvSykkel, text='Tilbake til meny', command=regOgOversiktAvSykkel.destroy)
    btn_avslutt.grid(row=4, column=3, pady=5, padx=5, sticky=SE)

    # vis oversikten
    oversiktavsykkel()

def r_stativ():
    def leggTilStativ():
        def r_stativ():
            stedID = gi_stedID()
            # Legger til stativet i databasen
            markor = koblingDatabase.cursor()
            variabel = ("INSERT INTO Sykkelstativ"
                        "(StativID, Sted)"
                        "VALUES(%s,%s)")
            markor.execute(variabel, (stedID, sted_inn.get()))
            koblingDatabase.commit()
            markor.close()

            # Oppdaterer oversikten
            vis_oversikt()

            # Registrerer lås
            leggTilLas(stedID)

        def gi_stedID():
            markor = koblingDatabase.cursor()
            markor.execute("SELECT * FROM Sykkelstativ")
            stedID = 1000

            for row in markor:
                stedID = stedID + 1

            # feilmelding
            if stedID >= 10000:
                feilmelding = 'Det er for mange stativer'
                utdata.set(str(feilmelding))
                return
            markor.close()
            return stedID

        def leggTilLas(stedID):
            antall_las = int(las_inn.get())

            while antall_las != 0:
                markor = koblingDatabase.cursor()
                variabel = ("INSERT INTO Lås"
                            "(StativID, Låsnr)"
                            "VALUES(%s,%s)")
                markor.execute(variabel, (stedID, antall_las))
                koblingDatabase.commit()
                markor.close()
                antall_las = antall_las - 1

            feilmelding = 'Stativ registrert i databasen med antall låser'
            utdata.set(str(feilmelding))
            vis_oversikt()
            return

        try:
            stedNavn_inndata = sted_inn.get()
            antallLas_inndata = las_inn.get()
            finnes = 1
            # Sjekk om stednavnet er skriven inn riktig
            if len(stedNavn_inndata) == 0:
                feilmelding = 'Skriv inn i stednavnsfeltet'
                utdata.set(str(feilmelding))
                return
            elif len(stedNavn_inndata) > 20:
                feilmelding = 'For langt stednavn'
                utdata.set(str(feilmelding))
                return

            # Sjekk om antall-lås er skriven inn riktig
            if len(antallLas_inndata) == 0:
                feilmelding = 'Skriv inn antall låser'
                utdata.set(str(feilmelding))
                return
            elif len(antallLas_inndata) >= 3:
                feilmelding = 'For mange låser'
                utdata.set(str(feilmelding))
                return
            elif int(antallLas_inndata) == 0:
                feilmelding = 'Kan ikke registrere 0 låser'
                utdata.set(str(feilmelding))
                return

            # Sjekk om stednavn ikke er tatt
            markor = koblingDatabase.cursor()
            markor.execute("SELECT * FROM Sykkelstativ")
            for row in markor:
                stedNavn_tabell = row[1]
                if stedNavn_tabell.upper() == stedNavn_inndata.upper():
                    finnes = 1
                    feilmelding = 'Stednavnet finnes allerede'
                    utdata.set(str(feilmelding))
                    return
                finnes = 0
            if finnes == 0:
                r_stativ()
                return
            markor.close()

        except ValueError:
            # Feilmelding for andre feil som vi ikke har funnet
            feilmelding = 'En feil oppstod'
            utdata.set(str(feilmelding))

    def vis_oversikt():
        markor = koblingDatabase.cursor()
        markor.execute(
            "SELECT Sykkelstativ. *, COUNT(Låsnr) AS låsNr FROM Sykkelstativ, Lås WHERE Sykkelstativ.StativID = Lås.StativID GROUP BY Sykkelstativ.StativID")

        stativ = []
        for row in markor:
            stativ += [row[0] + ',     ' + row[1] + ',     ' + str(row[2])]
        innhold_i_lst_stativ.set(tuple(stativ))
        markor.close()

    regOgOversiktAvStativ = Toplevel()
    regOgOversiktAvStativ.title('Registrer stativ')

    # Scrollbar for listen
    y_scroll = Scrollbar(regOgOversiktAvStativ, orient=VERTICAL)
    y_scroll.grid(row=1, column=1, rowspan=5, padx=(0, 50), pady=(0, 20), sticky=NS)

    # Lista
    innhold_i_lst_stativ = StringVar()
    lst_oversikt = Listbox(regOgOversiktAvStativ, height=20, width=60, listvariable=innhold_i_lst_stativ,
                           yscrollcommand=y_scroll.set)
    lst_oversikt.grid(row=1, column=0, rowspan=5, padx=(15, 0), pady=(0, 20), sticky=E)
    y_scroll["command"] = lst_oversikt.yview

    # Labels
    lbl_registrering = Label(regOgOversiktAvStativ, text='Registrering av sykkelstativ')
    lbl_registrering.grid(row=0, column=2, columnspan=2, padx=10, pady=10)

    lbl_innhold = Label(regOgOversiktAvStativ, text='Innhold: StativID, sted og antall låser')
    lbl_innhold.grid(row=0, column=0)

    lbl_sted = Label(regOgOversiktAvStativ, text='Stednavn:')
    lbl_sted.grid(row=1, column=2, padx=5, sticky=E)

    lbl_las = Label(regOgOversiktAvStativ, text='Antall låser på stativet:')
    lbl_las.grid(row=2, column=2, padx=5, sticky=E)

    # Input
    sted_inn = StringVar()
    ent_registrereSted = Entry(regOgOversiktAvStativ, width=20, textvariable=sted_inn)
    ent_registrereSted.grid(row=1, column=3, padx=15)

    las_inn = StringVar()
    ent_registrereLas = Entry(regOgOversiktAvStativ, width=2, textvariable=las_inn)
    ent_registrereLas.grid(row=2, column=3, padx=15)

    # Knapp
    btn_registrer = Button(regOgOversiktAvStativ, text='Registrer nytt stativ', command=leggTilStativ)
    btn_registrer.grid(row=3, column=3, padx=5, pady=10, sticky=N)

    # Label
    lbl_melding = Label(regOgOversiktAvStativ, text='Melding:')
    lbl_melding.grid(row=4, column=2, padx=5, pady=10, sticky=E)

    # Outputs
    utdata = StringVar()
    ent_utdata = Entry(regOgOversiktAvStativ, width=40, state='readonly', textvariable=utdata)
    ent_utdata.grid(row=4, column=3, padx=15, pady=15, sticky=W)

    # Avslutte og tilbake til hovedmeny
    btn_avslutt = Button(regOgOversiktAvStativ, text='Tilbake til meny', command=regOgOversiktAvStativ.destroy)
    btn_avslutt.grid(row=5, column=3, pady=5, padx=5, sticky=SE)

    # Kaller oversikten
    vis_oversikt()


def r_las():
    def registrerLaas():
        def sjekkOmMulig(stativID):
            stativID = stativID

            markor = koblingDatabase.cursor()
            variabel = ("SELECT * FROM Lås WHERE StativID = %s")
            markor.execute(variabel, stativID)

            las = 0
            antallLas = int(Las_inn.get())

            for row in markor:
                las += 1
            markor.close()

            sjekk = las + antallLas

            if sjekk > 99:
                feilmelding = 'Ikke nok plasser på stativet'
                utdata.set(str(feilmelding))
                mulig = False
            else:
                mulig = True

            return mulig


        def registrerAntallLaser(stativID):
            stativID = stativID
            antallLas = int(Las_inn.get())

            for i in range(antallLas):
                hentLas(stativID)

            melding = 'Lås(er) er registrert på stativet'
            utdata.set(str(melding))



        def hentLas(stativID):
            stativID = stativID

            markor = koblingDatabase.cursor()
            variabel = ("SELECT * FROM Lås WHERE StativID = %s")
            markor.execute(variabel, stativID)

            las = 1

            for row in markor:
                las += 1
            markor.close()

            registrerLaas(stativID, las)

        def registrerLaas(stativID, las):
            stativID = stativID
            las = las

            markor = koblingDatabase.cursor()
            variabel = ("INSERT INTO Lås"
                        "(StativID, Låsnr)"
                        "VALUES(%s,%s)")
            markor.execute(variabel, (stativID, las))
            koblingDatabase.commit()
            markor.close()

            # Oppdaterer oversikten
            vis_oversikt()

        try:
            markor = koblingDatabase.cursor()
            markor.execute("SELECT * FROM Sykkelstativ")

            sted = sted_inn.get()
            antallLas = int(Las_inn.get())

            for row in markor:

                if sted.upper() == row[1].upper():
                    stativID = row[0]
                    for i in range(antallLas):
                        mulig = sjekkOmMulig(stativID)
                        if mulig == True:
                            registrerAntallLaser(stativID)
                            return
                    markor.close()
                    return
            markor.close()

            # Sjekk feilmeldinger
            if len(sted) == 0:
                feilmelding = 'Skriv inn stednavn'
                utdata.set(str(feilmelding))

            elif len(sted) > 20:
                feilmelding = 'Stednavn for langt'
                utdata.set(str(feilmelding))
            else:
                feilmelding = 'Fant ikke stednavn'
                utdata.set(str(feilmelding))

        except:
            # Andre feilmeldinger
            feilmelding = ('En feil oppstod')
            utdata.set(str(feilmelding))


    def vis_oversikt():
        markor = koblingDatabase.cursor()
        markor.execute("SELECT Lås.StativID, Sykkelstativ.Sted, COUNT(Låsnr) FROM Lås, Sykkelstativ WHERE Lås.StativID = Sykkelstativ.StativID GROUP BY StativID")

        laas = []
        for row in markor:
            laas += [row[0] + ',     ' + row[1] + ',     ' + str(row[2])]
        innhold_i_lst_laas.set(tuple(laas))
        markor.close()

    # GUI
    regOgOversiktAvLas = Toplevel()
    regOgOversiktAvLas.title('Registrer Lås(er)')

    # Scrollbar for listen
    y_scroll = Scrollbar(regOgOversiktAvLas, orient=VERTICAL)
    y_scroll.grid(row=1, column=1, rowspan=4, padx=(0, 50), pady=(0, 20), sticky=NS)

    # Labels
    lbl_registrering = Label(regOgOversiktAvLas, text='Registrering')
    lbl_registrering.grid(row=0, column=2, columnspan=2, padx=10, pady=10)

    lbl_innhold = Label(regOgOversiktAvLas, text='Innhold: StativID, stednavn og antall låser på stativ')
    lbl_innhold.grid(row=0, column=0)

    lbl_sted = Label(regOgOversiktAvLas, text='Stednavn:')
    lbl_sted.grid(row=1, column=2, padx=5, pady=10, sticky=E)

    lbl_las = Label(regOgOversiktAvLas, text='Antall låser:')
    lbl_las.grid(row=2, column=2, padx=5, pady=10, sticky=E)

    # Lista
    innhold_i_lst_laas = StringVar()
    lst_oversikt = Listbox(regOgOversiktAvLas, width=50, height=20, listvariable=innhold_i_lst_laas, yscrollcommand=y_scroll.set)
    lst_oversikt.grid(row=1, column=0, rowspan=4, padx=(20, 0), pady=(0, 20), sticky=E)
    y_scroll["command"] = lst_oversikt.yview

    # Input
    sted_inn = StringVar()
    ent_registrereSted = Entry(regOgOversiktAvLas, width=20, textvariable=sted_inn)
    ent_registrereSted.grid(row=1, column=3, padx=5, pady=10)

    Las_inn = StringVar()
    ent_registrereLas = Entry(regOgOversiktAvLas, width=3, textvariable=Las_inn)
    ent_registrereLas.grid(row=2, column=3, padx=5, pady=10)

    # Knapp
    btn_registrer = Button(regOgOversiktAvLas, text='Registrer Lås(er)', command=registrerLaas)
    btn_registrer.grid(row=3, column=3, padx=5, pady=10, sticky=N)

    # Label
    lbl_melding = Label(regOgOversiktAvLas, text='Melding:')
    lbl_melding.grid(row=4, column=2, padx=5, pady=10)

    # Outputs
    utdata = StringVar()
    ent_utdata = Entry(regOgOversiktAvLas, width=30, state='readonly', textvariable=utdata)
    ent_utdata.grid(row=4, column=3, padx=5, pady=5)

    # Avslutte og tilbake til hovedmeny
    btn_avslutt = Button(regOgOversiktAvLas, text='Tilbake til meny', command=regOgOversiktAvLas.destroy)
    btn_avslutt.grid(row=5, column=3, pady=5, padx=5, sticky=SE)

    # Viser oversikten
    vis_oversikt()

def o_sykkler():  # Oversikt over sykklene
    def vis_o_BestemtDato():
        dato = dato_inn.get()
        oversiktSykler_markor = koblingDatabase.cursor()
        variabel = ("SELECT * FROM sykkel WHERE Startdato>%s")
        oversiktSykler_markor.execute(variabel, dato_inn.get())

        sykler = []
        for row in oversiktSykler_markor:
            sykler += [str(row[0]) + ',     ' + str(row[1]) + ',     ' + str(row[2]) + ',     ' + str(row[3])]

        i_lst_o_sykkel.set(tuple(sykler))
        oversiktSykler_markor.close()
        innhold = 'Innhold: SykkelID, startdato, stativID, låsnr'
        utdata.set(str(innhold))

    def SyklerLeidMerEnn100():
        oversiktSykler_markor = koblingDatabase.cursor()
        oversiktSykler_markor.execute(
            "SELECT SykkelID, Utlevert, Mobilnr, Innlevert, COUNT(SykkelID) AS AntallGangerUtleid FROM Utleie GROUP BY SykkelID HAVING AntallGangerUtleid >= 100 ORDER BY AntallGangerUtleid DESC")

        sykler = []
        for row in oversiktSykler_markor:
            sykler += [
                str(row[0]) + ',     ' + str(row[1]) + ',     ' + str(row[2]) + ',     ' + str(row[3]) + ',     ' + str(
                    row[4])]

        i_lst_o_sykkel.set(tuple(sykler))
        oversiktSykler_markor.close()
        innhold = 'Innhold: SykkelID, Utlevert(dato), Mobilnr, Innlevert(dato), antall ganger utleid'
        utdata.set(str(innhold))

    def syklerPaaLager():
        markor = koblingDatabase.cursor()
        markor.execute("SELECT * FROM Sykkel WHERE SykkelID NOT IN(SELECT SykkelID FROM Utleie) AND StativID IS NULL")

        lager = []
        for row in markor:
            lager += [str(row[0]) + ',     ' + str(row[1]) + ',     ' + str(row[2]) + ',     ' + str(row[3])]

        i_lst_o_sykkel.set(tuple(lager))
        markor.close()
        innhold = 'Innhold: SykkelID, StartDato, StativID, Låsnr'
        utdata.set(str(innhold))

    def IkkeLevertEtterEtDogn():
        oversiktSykler_markor = koblingDatabase.cursor()
        oversiktSykler_markor.execute(
            "SELECT Utleie.SykkelID, Kunde.Mobilnr, Kunde.Fornavn, Kunde.Etternavn FROM Utleie, Kunde WHERE Kunde.Mobilnr = Utleie.Mobilnr AND Utleie.Innlevert IS NULL AND Utleie.Utlevert < DATE_SUB(NOW(), INTERVAL 1 DAY) GROUP BY Utleie.SykkelID")

        sykler = []
        for row in oversiktSykler_markor:
            sykler += [str(row[0]) + ',     ' + str(row[1]) + ',     ' + str(row[2]) + ',     ' + str(row[3])]

        i_lst_o_sykkel.set(tuple(sykler))
        oversiktSykler_markor.close()
        innhold = 'Innhold: SykkelID, Mobilnr, fornavn, etternavn'
        utdata.set(str(innhold))

    oversiktSykler = Toplevel()
    oversiktSykler.title("Oversikter")

    # Scrollbar
    y_scroll = Scrollbar(oversiktSykler, orient=VERTICAL)
    y_scroll.grid(row=1, column=2, rowspan=5, padx=(0, 30), pady=15, sticky=NS)

    # Liste
    i_lst_o_sykkel = StringVar()
    lst_liste = Listbox(oversiktSykler, width=80, height=20, listvariable=i_lst_o_sykkel, yscrollcommand=y_scroll.set)
    lst_liste.grid(row=1, column=0, columnspan=2, rowspan=5, padx=(20, 0), pady=15, sticky=E)

    # Label
    lbl_overskrift = Label(oversiktSykler, text='Oversikter om sykler')
    lbl_overskrift.grid(row=0, column=3, padx=5, pady=5)

    lbl_startdato = Label(oversiktSykler,text='*Skriv inn dato (ååååmmdd):                                                           ')
    lbl_startdato.grid(row=1, column=3, sticky=SW)

    # Utdata
    utdata = StringVar()
    ent_utdata = Entry(oversiktSykler, width=80, state='readonly', textvariable=utdata)
    ent_utdata.grid(row=0, column=1, padx=(20, 0), pady=15)

    # Input
    dato_inn = StringVar()
    ent_dato = Entry(oversiktSykler, width=8, textvariable=dato_inn)
    ent_dato.grid(row=1, column=3, padx=(5, 80), sticky=SE)

    # knapper
    btn_bestemtdato = Button(oversiktSykler, width=45, text='Sykler tatt i bruk etter datoen*', command=vis_o_BestemtDato)
    btn_bestemtdato.grid(row=2, column=3, padx=5, pady=(5, 0))

    btn_100 = Button(oversiktSykler, width=45, text='Sykler som er leid ut meir enn 100 ganger', command=SyklerLeidMerEnn100)
    btn_100.grid(row=3, column=3, padx=15, pady=5)

    btn_ikkelevertettdogn = Button(oversiktSykler, width=45, text='Sykler og kunde som ikke er levert tilbake etter ett døgn', command=IkkeLevertEtterEtDogn)
    btn_ikkelevertettdogn.grid(row=4, column=3, padx=15, pady=5)

    btn_lager = Button(oversiktSykler, width=45, text='Ubrukte sykler', command=syklerPaaLager)
    btn_lager.grid(row=5, column=3, padx=15, pady=5)

    btn_avslutt = Button(oversiktSykler, text='Tilbake til meny', command=oversiktSykler.destroy)
    btn_avslutt.grid(row=6, column=3, pady=5, padx=5, sticky=SE)


def o_kunder():  # Oversikt over kundene
    def kundene():
        oversiktKunder_markor = koblingDatabase.cursor()
        oversiktKunder_markor.execute("SELECT Etternavn, Fornavn, Mobilnr FROM Kunde ORDER BY Etternavn ASC")

        kunder = []
        for row in oversiktKunder_markor:
            kunder += [row[0] + ',     ' + row[1] + ',     ' + row[2]]

        i_lst_o_kunder.set(tuple(kunder))
        oversiktKunder_markor.close()
        innhold = 'Innhold: Etternavn, Fornavn, Mobilnr'
        utdata.set(str(innhold))

    def antallkunder():
        antallKunder_markor = koblingDatabase.cursor()
        antallKunder_markor.execute("SELECT COUNT(*) AS AntallKunder FROM Kunde")

        antall = []
        for row in antallKunder_markor:
            antall += [row[0]]

        i_lst_o_kunder.set(tuple(antall))
        antallKunder_markor.close()
        innhold = 'Innhold: Antall kunder i bysykkel ordningen'
        utdata.set(str(innhold))

    def aldrileid():
        aldriLeid_markor = koblingDatabase.cursor()
        aldriLeid_markor.execute(
            "SELECT Kunde.Etternavn, Kunde.Fornavn, Kunde.Mobilnr FROM Kunde LEFT OUTER JOIN Utleie ON Kunde.Mobilnr = Utleie.Mobilnr WHERE Utleie.Mobilnr IS NULL ORDER BY Etternavn ASC")

        ikkeleid = []
        for row in aldriLeid_markor:
            ikkeleid += [row[0] + ',     ' + row[1] + ',     ' + row[2]]

        i_lst_o_kunder.set(tuple(ikkeleid))
        aldriLeid_markor.close()
        innhold = 'Innhold: Etternavn, Fornavn, Mobilnr'
        utdata.set(str(innhold))

    def aktivekunder():
        aktiveKunder_markor = koblingDatabase.cursor()
        aktiveKunder_markor.execute(
            "SELECT Kunde.Etternavn, Kunde.Fornavn, Kunde.Mobilnr, COUNT(Utleie.Mobilnr) AS AntallUtleie FROM Kunde LEFT JOIN Utleie ON Kunde.Mobilnr = Utleie.Mobilnr GROUP BY Kunde.Mobilnr ORDER BY AntallUtleie DESC")

        aktive = []
        for row in aktiveKunder_markor:
            aktive += [row[0] + ',     ' + row[1] + ',     ' + row[2] + ',     ' + str(row[3])]

        i_lst_o_kunder.set(tuple(aktive))
        aktiveKunder_markor.close()
        innhold = 'Innhold: Etternavn, Fornavn, Mobilnr, Antall utleie'
        utdata.set(str(innhold))

    def leier_nA():
        aktiveKunder_markor = koblingDatabase.cursor()
        aktiveKunder_markor.execute(
            "SELECT Kunde.Etternavn, Kunde.Mobilnr, Utleie.SykkelID, Sykkel.StartDato, Utleie.Utlevert FROM Kunde, Sykkel, Utleie WHERE Kunde.Mobilnr=Utleie.Mobilnr AND Utleie.SykkelID=Sykkel.SykkelID AND Sykkel.StativID IS NULL AND Utleie.Innlevert IS NULL")

        aktive = []
        for row in aktiveKunder_markor:
            aktive += [
                row[0] + ',     ' + str(row[1]) + ',     ' + str(row[2]) + ',     ' + str(row[3]) + ',     ' + str(
                    row[4])]

        i_lst_o_kunder.set(tuple(aktive))
        aktiveKunder_markor.close()
        innhold = 'Innhold: Etternavn, MobilNr, SykkelID, StartDato, Starttidspunkt'
        utdata.set(str(innhold))

    oversiktKunder = Toplevel()
    oversiktKunder.title("Oversikt alle kunder")

    # Scrollbar
    y_scroll = Scrollbar(oversiktKunder, orient=VERTICAL)
    y_scroll.grid(row=1, column=2, rowspan=5, padx=(0, 30), pady=15, sticky=NS)

    # Liste
    i_lst_o_kunder = StringVar()
    lst_liste = Listbox(oversiktKunder, width=80, height=20, listvariable=i_lst_o_kunder, yscrollcommand=y_scroll.set)
    lst_liste.grid(row=1, column=0, columnspan=2, rowspan=5, padx=(50, 0), pady=15, sticky=E)

    # Label
    lbl_overskrift = Label(oversiktKunder, text='Oversikt over alle kunder')
    lbl_overskrift.grid(row=0, column=3, padx=5, pady=5)

    # Utdata
    utdata = StringVar()
    ent_utdata = Entry(oversiktKunder, width=80, state='readonly', textvariable=utdata)
    ent_utdata.grid(row=0, column=1, padx=(50, 0), pady=15)

    # knapper
    btn_allekunder = Button(oversiktKunder, width=30, text='Alle kunder', command=kundene)
    btn_allekunder.grid(row=1, column=3, padx=25, pady=5)

    btn_antallkunder = Button(oversiktKunder, width=30, text='Antall kunder', command=antallkunder)
    btn_antallkunder.grid(row=2, column=3, padx=25, pady=5)

    btn_aldrileid = Button(oversiktKunder, width=30, text='Kunder som aldri har leid sykkel', command=aldrileid)
    btn_aldrileid.grid(row=3, column=3, padx=25, pady=5)

    btn_antallleid = Button(oversiktKunder, width=30, text='Alle kunder med utleieforhold', command=aktivekunder)
    btn_antallleid.grid(row=4, column=3, padx=25, pady=5)

    btn_leier_nA = Button(oversiktKunder, width=30, text='Kunder som leier en bysykkel akkurat nå', command=leier_nA)
    btn_leier_nA.grid(row=5, column=3, padx=25, pady=5)

    btn_avslutt = Button(oversiktKunder, text='Tilbake til meny', command=oversiktKunder.destroy)
    btn_avslutt.grid(row=6, column=3, pady=5, padx=5, sticky=SE)


def o_stativ():  # Oversikt over stativ
    oversiktStativ = Toplevel()
    oversiktStativ.title("Oversikter")

    # Oversikt over hvor mange ledige sykler som er tilgjengelig ved hvert sykkelstativ. Lista skal inneholde StativID, Sted og antall ledige sykler.
    def sykkelTilgjengelig():
        oversikt_marker = koblingDatabase.cursor()
        oversikt_marker.execute(
            'SELECT SykkelStativ.StativID, SykkelStativ.Sted, COUNT(Sykkel.StativID) AS AntallLedigeSykler FROM SykkelStativ LEFT JOIN Sykkel ON SykkelStativ.StativID=Sykkel.StativID GROUP BY SykkelStativ.StativID;')

        ledig = []
        for row in oversikt_marker:
            ledig += [row[0] + ',      ' + row[1] + ',      ' + str(row[2])]
        i_lst_o_stativ.set(tuple(ledig))
        oversikt_marker.close()
        innhold = 'Innhold: StativID, Sted, AntallLedigSykler '
        utdata.set(str(innhold))

    # Oversikt over sykkelstativer som er fullparkert av sykler og stativer uten parkerte sykler
    def fulleOgTommeStativer():
        fullTom_marker = koblingDatabase.cursor()
        fullTom_marker.execute(
            'SELECT lås.Sted, lås.Antall AS Låser, sykkel.Antall AS Sykler FROM (SELECT Sted, COUNT(Låsnr) AS Antall FROM Sykkelstativ LEFT JOIN Lås ON Lås.StativID = Sykkelstativ.StativID GROUP BY Sted) lås JOIN (SELECT sted, COUNT(SykkelID) AS Antall FROM Sykkelstativ LEFT JOIN Sykkel ON Sykkel.StativID = Sykkelstativ.StativID GROUP BY sted) sykkel ON sykkel.Sted = lås.Sted WHERE lås.Antall = sykkel.Antall OR sykkel.Antall = 0;')

        fullTom = []
        for row in fullTom_marker:
            fullTom += [row[0] + ',       ' + str(row[1]) + ',      ' + str(row[2])]
        i_lst_o_stativ.set(tuple(fullTom))
        fullTom_marker.close()
        innhold = 'Innhold: Sted, Antall plasser, Antall sykler '
        utdata.set(str(innhold))

    # Scrollbar
    y_scroll = Scrollbar(oversiktStativ, orient=VERTICAL)
    y_scroll.grid(row=1, column=2, rowspan=5, padx=(0, 100), pady=15, sticky=NS)

    # Liste
    i_lst_o_stativ = StringVar()
    lst_liste = Listbox(oversiktStativ, width=80, height=20, listvariable=i_lst_o_stativ, yscrollcommand=y_scroll.set)
    lst_liste.grid(row=1, column=0, columnspan=2, rowspan=5, padx=(50, 0), pady=15, sticky=E)

    # Label
    lbl_overskrift = Label(oversiktStativ, text='Oversikter om lån om Sykkelstativ')
    lbl_overskrift.grid(row=0, column=3, padx=5, pady=5)

    # Utdata
    utdata = StringVar()
    ent_utdata = Entry(oversiktStativ, width=80, state='readonly', textvariable=utdata)
    ent_utdata.grid(row=0, column=1, padx=(50, 0), pady=15)

    # knapper
    btn_ledigesykler = Button(oversiktStativ, width=55, text='Sykler som er tilgjengelig på hvert sykkelstativ',
                              command=sykkelTilgjengelig)
    btn_ledigesykler.grid(row=1, column=3, padx=5, pady=5)

    btn_fullogtom = Button(oversiktStativ, width=55,
                           text='Sykkelstativer som er fullparkert og stativer uten parkerte sykler',
                           command=fulleOgTommeStativer)
    btn_fullogtom.grid(row=2, column=3, padx=5, pady=5)

    btn_avslutt = Button(oversiktStativ, text='Tilbake til meny', command=oversiktStativ.destroy)
    btn_avslutt.grid(row=5, column=3, pady=5, padx=5, sticky=SE)


def e_endrestativ():
    def endre():
        def sjekkOmFinnes():
            markor = koblingDatabase.cursor()
            markor.execute('SELECT * FROM Sykkelstativ')

            stativID = stativID_inn.get()

            for row in markor:
                if stativID == row[0]:
                    skrivInnIdatabase()
            markor.close()

        def skrivInnIdatabase():
            stativID = stativID_inn.get()
            stednavn = navn_inn.get()

            markor = koblingDatabase.cursor()
            variabel = ("UPDATE Sykkelstativ SET Sted = %s WHERE StativID = %s")
            inndata = (stednavn, stativID)
            markor.execute(variabel, inndata)
            koblingDatabase.commit()
            utdata.set('Endring registrert')
            markor.close()
            vis_oversikt()

            return

        try:
            stativID = stativID_inn.get()
            stednavn = navn_inn.get()

            if len(stativID) != 4:
                feilmelding = 'Skriv inn i stativID, 4 siffer'
                utdata.set(str(feilmelding))
                return

            # Sjekk om stativsted er skriven inn riktig
            elif len(stednavn) == 0:
                feilmelding = 'Skriv inn stednavn'
                utdata.set(str(feilmelding))
                return
            elif len(stednavn) > 20:
                feilmelding = 'For lang stedsnavn'
                utdata.set(str(feilmelding))
                return

            sjekkOmFinnes()
        except:
            feilmelding = 'En feil oppstod'
            utdata.set(str(feilmelding))

    def vis_oversikt():
        markor = koblingDatabase.cursor()
        markor.execute(
            "SELECT Sykkelstativ. * FROM Sykkelstativ, Lås WHERE Sykkelstativ.StativID = Lås.StativID GROUP BY Sykkelstativ.StativID")

        stativ = []
        for row in markor:
            stativ += [row[0] + ',     ' + row[1]]
        innhold_i_lst_stativ.set(tuple(stativ))
        markor.close()

    # GUI
    endre_stativ = Toplevel()
    endre_stativ.title('Flytt/endre navn på sykkelstativ')

    # Scrollbar for listen
    y_scroll = Scrollbar(endre_stativ, orient=VERTICAL)
    y_scroll.grid(row=1, column=1, rowspan=5, padx=(0, 50), pady=(0, 20), sticky=NS)

    # Lista
    innhold_i_lst_stativ = StringVar()
    lst_oversikt = Listbox(endre_stativ, height=20, width=60, listvariable=innhold_i_lst_stativ,
                           yscrollcommand=y_scroll.set)
    lst_oversikt.grid(row=1, column=0, rowspan=5, padx=(15, 0), pady=(0, 20), sticky=E)
    y_scroll["command"] = lst_oversikt.yview

    # Labels
    lbl_registrering = Label(endre_stativ, text='Endre stativnavn')
    lbl_registrering.grid(row=0, columnspan=2, padx=10, pady=10)

    lbl_sykkelID = Label(endre_stativ, text='StativID:')
    lbl_sykkelID.grid(row=1, padx=5, column=2, pady=10, sticky=W)

    lbl_stativ = Label(endre_stativ, text='Nytt stativsted:')
    lbl_stativ.grid(row=2, padx=5, column=2, pady=10, sticky=W)

    # Input
    stativID_inn = StringVar()
    ent_ID = Entry(endre_stativ, width=8, textvariable=stativID_inn)
    ent_ID.grid(row=1, column=2, padx=20, pady=10, sticky=E)

    navn_inn = StringVar()
    ent_stedinn = Entry(endre_stativ, width=20, textvariable=navn_inn)
    ent_stedinn.grid(row=2, column=2, padx=20, pady=10, sticky=E)

    # Knapp
    btn_registrer = Button(endre_stativ, width=20, text='Endre stativnavn', command=endre)
    btn_registrer.grid(row=4, columnspan=2, column=2, padx=5, pady=10, sticky=N)

    # Label
    lbl_melding = Label(endre_stativ, text='Melding:')
    lbl_melding.grid(row=5, column=2, padx=25, pady=10)

    # Outputs
    utdata = StringVar()
    ent_utdata = Entry(endre_stativ, width=40, state='readonly', textvariable=utdata)
    ent_utdata.grid(row=5, column=2, padx=15, pady=25, sticky=W)

    # tilbake til hovedmeny
    btn_avslutt = Button(endre_stativ, text='Tilbake til meny', command=endre_stativ.destroy)
    btn_avslutt.grid(row=6, column=2, pady=5, padx=5, sticky=SE)

    vis_oversikt()


def o_belop():  # Oversikt over sykklene
    def vis_o_belopdag():
        markor = koblingDatabase.cursor()
        markor.execute(
            'SELECT DATE (Innlevert), SUM(Beløp) FROM Utleie WHERE Innlevert IS NOT NULL GROUP BY DATE(Innlevert)')

        mnd_liste = []
        for row in markor:
            mnd_liste += [str(row[0]) + ',     ' + str(row[1])]

        i_lst_o_belop.set(tuple(mnd_liste))
        markor.close()
        innhold = 'Innhold: Dato, Beløp'
        utdata.set(str(innhold))

    def vis_o_belopmnd():
        markor = koblingDatabase.cursor()
        markor.execute(
            'SELECT YEAR(Innlevert), MONTH(Innlevert), SUM(Beløp) FROM Utleie WHERE Innlevert IS NOT NULL GROUP BY YEAR(Innlevert), MONTH(Innlevert)')

        mnd_liste = []
        for row in markor:
            mnd_liste += [str(row[0]) + ',     ' + str(row[1]) + ',     ' + str(row[2])]

        i_lst_o_belop.set(tuple(mnd_liste))
        markor.close()
        innhold = 'Innhold: År, Måned, Beløp'
        utdata.set(str(innhold))

    def vis_o_belopAr():
        markor = koblingDatabase.cursor()
        markor.execute(
            'SELECT YEAR (Innlevert), SUM(Beløp) FROM Utleie WHERE Innlevert IS NOT NULL GROUP BY YEAR(Innlevert)')

        mnd_liste = []
        for row in markor:
            mnd_liste += [str(row[0]) + ',     ' + str(row[1])]

        i_lst_o_belop.set(tuple(mnd_liste))
        markor.close()
        innhold = 'Innhold: År, Beløp'
        utdata.set(str(innhold))

    def vis_o_totalkunde():
        markor = koblingDatabase.cursor()
        markor.execute(
            'SELECT Kunde.Mobilnr, Kunde.Fornavn, Kunde.Etternavn, SUM(Beløp) AS TotalBeløp FROM Kunde LEFT JOIN Utleie ON Kunde.Mobilnr=Utleie.Mobilnr GROUP BY Kunde.Mobilnr ORDER BY TotalBeløp DESC ')

        mnd_liste = []
        for row in markor:
            mnd_liste += [str(row[0]) + ',     ' + str(row[1]) + ',     ' + str(row[2]) + ',     ' + str(row[3])]

        i_lst_o_belop.set(tuple(mnd_liste))
        markor.close()
        innhold = 'Innhold: Mobilnr, Fornavn, Etternavn, Beløp'
        utdata.set(str(innhold))

    oversiktBelop = Toplevel()
    oversiktBelop.title("Oversikter")

    # Scrollbar
    y_scroll = Scrollbar(oversiktBelop, orient=VERTICAL)
    y_scroll.grid(row=1, column=2, rowspan=5, padx=(0, 30), pady=15, sticky=NS)

    # Liste
    i_lst_o_belop = StringVar()
    lst_liste = Listbox(oversiktBelop, width=80, height=20, listvariable=i_lst_o_belop, yscrollcommand=y_scroll.set)
    lst_liste.grid(row=1, column=0, columnspan=2, rowspan=5, padx=(20, 0), pady=15, sticky=E)

    # Label
    lbl_overskrift = Label(oversiktBelop, text='Oversikter over Økonomi')
    lbl_overskrift.grid(row=0, column=3, padx=5, pady=5)

    # Utdata
    utdata = StringVar()
    ent_utdata = Entry(oversiktBelop, width=80, state='readonly', textvariable=utdata)
    ent_utdata.grid(row=0, column=1, padx=(20, 0), pady=15)

    # knapper
    btn_dag = Button(oversiktBelop, width=45, text='Totalt beløp tjent hver dag', command=vis_o_belopdag)
    btn_dag.grid(row=1, column=3, padx=15, pady=5)

    btn_MND = Button(oversiktBelop, width=45, text='Totalt beløp tjent hver mnd*', command=vis_o_belopmnd)
    btn_MND.grid(row=2, column=3, padx=5, pady=(5, 0))

    btn_Ar = Button(oversiktBelop, width=45, text='Totalt beløp tjent hvert år', command=vis_o_belopAr)
    btn_Ar.grid(row=3, column=3, padx=15, pady=5)

    btn_totalkunde = Button(oversiktBelop, width=45, text='Totalt beløp på hver enkel kunde', command=vis_o_totalkunde)
    btn_totalkunde.grid(row=4, column=3, padx=15, pady=5)

    btn_avslutt = Button(oversiktBelop, text='Tilbake til meny', command=oversiktBelop.destroy)
    btn_avslutt.grid(row=5, column=3, pady=5, padx=5, sticky=SE)


def e_utavbruk():
    def sjekkutleie():
        def settSykkelUtAvBruk():
            markor = koblingDatabase.cursor()
            # Oppdaterer, og setter sykkel på lager
            variabel = ("UPDATE Sykkel SET StativID = %s, LåsNr = %s WHERE SykkelID = %s")
            inndata = (None, None, sykkelID)
            markor.execute(variabel, inndata)
            koblingDatabase.commit()
            # Oppdater oversikten
            vis_oversikt()

            utdata.set('Endring registrert')
            return


        try:
            # sjekk om sykkel finnes
            markor = koblingDatabase.cursor()
            markor.execute('SELECT Sykkel.SykkelID, Sykkel.LåsNr FROM Utleie, Sykkel WHERE NOT EXISTS (SELECT SykkelID FROM Utleie WHERE Innlevert IS NULL AND Sykkel.StativID IS NULL AND Sykkel.LåsNr IS NULL) GROUP BY Sykkel.SykkelID')

            sykkelID = sykkelid_inn.get()

            for row in markor:
                if sykkelID == row[0]:
                    settSykkelUtAvBruk()
                    markor.close()
                    return
            markor.close()

            if len(sykkelID) == 0:
                feilmelding = ('Skriv inn sykkelID!')
                utdata.set(str(feilmelding))
            elif len(sykkelID) > 4:
                feilmelding = ('Skriv inn gyldig sykkelID!')
                utdata.set(str(feilmelding))
            else:
                feilmelding = ('fant ikke sykkelID som ikke var utlånt')
                utdata.set(str(feilmelding))


        except:
            feilmelding = ('En feil oppstod')
            utdata.set(str(feilmelding))





    def vis_oversikt():
        markor = koblingDatabase.cursor()
        markor.execute('SELECT Sykkel.SykkelID, Sykkel.LåsNr FROM Utleie, Sykkel WHERE NOT EXISTS (SELECT SykkelID FROM Utleie WHERE Innlevert IS NULL AND Sykkel.StativID IS NULL AND Sykkel.LåsNr IS NULL) GROUP BY Sykkel.SykkelID')

        stativ = []
        for row in markor:
            stativ += [str(row[0])]
        i_lst_stativ.set(tuple(stativ))
        markor.close()
        innhold.set('Innhold: sykkelID som ikke er utlånt')

    # GUI
    utavbrukvindu = Toplevel()
    utavbrukvindu.title("Ta sykkel ut av bruk")

    # Scrollbar
    y_scroll = Scrollbar(utavbrukvindu, orient=VERTICAL)
    y_scroll.grid(row=1, column=2, rowspan=3, padx=(0, 30), pady=15, sticky=NS)

    # Input
    sykkelid_inn = StringVar()
    ent_ID = Entry(utavbrukvindu, width=8, textvariable=sykkelid_inn)
    ent_ID.grid(row=1, column=4, padx=20, pady=10)

    # Liste
    i_lst_stativ = StringVar()
    lst_liste = Listbox(utavbrukvindu, width=40, height=15, listvariable=i_lst_stativ, yscrollcommand=y_scroll.set)
    lst_liste.grid(row=1, column=0, columnspan=2, rowspan=3, padx=(20, 0), pady=15, sticky=E)

    # Label
    lbl_overskrift = Label(utavbrukvindu, text='Endring')
    lbl_overskrift.grid(row=0, column=3, columnspan=2, padx=5, pady=5)

    lbl_input = Label(utavbrukvindu, text='SykkelID:')
    lbl_input.grid(row=1, column=3, padx=5, pady=5, sticky=W)

    lbl_melding = Label(utavbrukvindu, text='Melding:')
    lbl_melding.grid(row=3, column=3, padx=5, pady=15, sticky=NW)

    # Utdata
    innhold = StringVar()
    ent_innhold = Entry(utavbrukvindu, width=40, state='readonly', textvariable=innhold)
    ent_innhold.grid(row=0, column=1, padx=(20, 0), pady=15)

    utdata = StringVar()
    ent_utdata = Entry(utavbrukvindu, width=35, state='readonly', textvariable=utdata)
    ent_utdata.grid(row=3, column=4, padx=20, pady=15, sticky=N)

    # knapper
    btn_utavbruk = Button(utavbrukvindu, width=20, text='Ta sykkel ut av bruk', command=sjekkutleie)
    btn_utavbruk.grid(row=2, column=3, columnspan=2, padx=15, pady=5)

    btn_avslutt = Button(utavbrukvindu, text='Tilbake til meny', command=utavbrukvindu.destroy)
    btn_avslutt.grid(row=4, column=4, pady=5, padx=5, sticky=SE)

    vis_oversikt()


def e_endreBruker():
    # Sjekk om bruker finnes
    # Sjekk at bruker ikkje leier ein sykkel no
    # Endre brukers bankkonto til 'NULL'

    def Blokker():
        def brukerLeierIkke():
            markor = koblingDatabase.cursor()
            markor.execute("SELECT * FROM Utleie WHERE Innlevert IS NULL")

            tlfNr = Tlf_inn.get()

            for row in markor:
                if tlfNr == str(row[2]) and row[3] == None:
                    feilmelding = 'Bruker leier en sykkel, og kan ikke blokkeres enda'
                    melding.set(str(feilmelding))
                    return
            markor.close()

            # bruker leier ikke en sykkel akkurat nå
            endreBankKonto()

        def endreBankKonto():
            tlfNr = Tlf_inn.get()

            markor = koblingDatabase.cursor()
            variabel = "UPDATE Kunde SET Betalingskortnr = %s WHERE Mobilnr = %s"
            inndata = (None, tlfNr)
            markor.execute(variabel, inndata)
            koblingDatabase.commit()
            markor.close()

            melding = 'Brukers betalingskort er fjernet'
            utdata.set(str(melding))

            vis_oversikt()

        try:
            tlfNr = Tlf_inn.get()

            # Feilmeldinger
            if len(str(tlfNr)) == 0:
                feilmelding = 'skriv inn telefonnr'
                utdata.set(str(feilmelding))
                return
            elif len(str(tlfNr)) > 11:
                feilmelding = 'for lang telefonnr'
                utdata.set(str(feilmelding))
                return

            markor = koblingDatabase.cursor()
            markor.execute("SELECT * FROM Kunde")

            # Start på funksjonen, sjekker om bruker finnes
            for row in markor:
                if tlfNr == str(row[0]) and row[3] != None:
                    # bruker finnes, sjekk om bruker ikke leier en sykkel
                    brukerLeierIkke()
                    markor.close()
                    return
                elif tlfNr == str(row[0]) and row[3] == None:
                    feilmelding = 'Kunden sitt betalingskort er allerede låst'
                    utdata.set(str(feilmelding))
                    return
            markor.close()

            # Fant ikke telfonnr
            if tlfNr != str(row[0]):
                feilmelding = 'Finner ikke telefonnr i databasen'
                utdata.set(str(feilmelding))
                return


        except:
            # Andre feilmeldinger
            feilmelding = 'En feil oppstod'
            utdata.set(str(feilmelding))

    def vis_oversikt():
        markor = koblingDatabase.cursor()
        markor.execute("SELECT * FROM Kunde")

        kunde = []
        for row in markor:
            kunde += [row[0] + ',     ' + str(row[1]) + ',     ' + str(row[2]) + ',     ' + str(row[3])]

        innhold_i_lst_kunde.set(tuple(kunde))
        markor.close()

    # GUI
    endreBruker = Toplevel()
    endreBruker.title('Registrer sykkel')

    # Labels
    lbl_innhold = Label(endreBruker, text='Innhold: Telefonnummer, fornavn, etternavn, bankkontonr')
    lbl_innhold.grid(row=0, column=0)

    lbl_endring = Label(endreBruker, text='Utesteng bruker fra å leie sykkel')
    lbl_endring.grid(row=0, column=2, columnspan=2, padx=10, pady=10)

    lbl_telefon = Label(endreBruker, text='Brukers telefonnr:')
    lbl_telefon.grid(row=1, column=2, padx=5, pady=10, sticky=E)

    # Scrollbar for listen
    y_scroll = Scrollbar(endreBruker, orient=VERTICAL)
    y_scroll.grid(row=1, column=1, rowspan=4, padx=(0, 50), pady=15, sticky=NS)

    # Lista
    innhold_i_lst_kunde = StringVar()
    lst_kunde = Listbox(endreBruker, height=21, width=70, listvariable=innhold_i_lst_kunde, yscrollcommand=y_scroll.set)
    lst_kunde.grid(row=1, column=0, rowspan=4, padx=(50, 0), pady=15)
    y_scroll["command"] = lst_kunde.yview

    # Input StativID og Antall låser
    Tlf_inn = StringVar()
    ent_a_tlf = Entry(endreBruker, width=12, textvariable=Tlf_inn)
    ent_a_tlf.grid(row=1, column=3, padx=5, pady=10)

    # Knapp
    btn_blokker = Button(endreBruker, text='Blokker bruker', command=Blokker)
    btn_blokker.grid(row=2, column=3, padx=5, pady=10, sticky=N)

    # Label
    lbl_melding = Label(endreBruker, text='Melding:')
    lbl_melding.grid(row=3, column=2, padx=10, pady=10, sticky=E)

    # Outputs
    utdata = StringVar()
    ent_utdata = Entry(endreBruker, width=40, state='readonly', textvariable=utdata)
    ent_utdata.grid(row=3, column=3, padx=15, pady=15)

    # tilbake til hovedmeny
    btn_avslutt = Button(endreBruker, text='Tilbake til meny', command=endreBruker.destroy)
    btn_avslutt.grid(row=4, column=3, pady=5, padx=5, sticky=SE)

    # vis oversikten
    vis_oversikt()


def main():
    hovedvindu = Tk()
    hovedvindu.title('Administrerende program for sykkel-appen')

    # Labels
    lbl_r = Label(hovedvindu, text='Registrering')
    lbl_r.grid(row=0, column=0, padx=(15, 50), pady=10)

    lbl_e = Label(hovedvindu, text='Endringer/Ajourhold')
    lbl_e.grid(row=0, column=1, padx=50, pady=10)

    lbl_o = Label(hovedvindu, text='Oversikter')
    lbl_o.grid(row=0, column=2, padx=(50, 15), pady=10)

    # Registrering
    btn_r_sykkel = Button(hovedvindu, width=20, text='Sykkel', command=r_sykkel)
    btn_r_sykkel.grid(row=1, column=0, padx=(15, 50), pady=5)

    btn_r_stativ = Button(hovedvindu, width=20, text='Stativ', command=r_stativ)
    btn_r_stativ.grid(row=2, column=0, padx=(15, 50), pady=5)

    btn_r_las = Button(hovedvindu, width=20, text='Lås', command=r_las)
    btn_r_las.grid(row=3, column=0, padx=(15, 50), pady=5)

    # Endring/ajourhold
    btn_e_utavbruk = Button(hovedvindu, width=20, text='Ta sykkel ut av bruk', command=e_utavbruk)
    btn_e_utavbruk.grid(row=1, column=1, padx=50, pady=5)

    btn_e_endrestativ = Button(hovedvindu, width=20, text='Endre/flytt stativ', command=e_endrestativ)
    btn_e_endrestativ.grid(row=2, column=1, padx=50, pady=5)

    btn_e_endreBruker = Button(hovedvindu, width=20, text='Utesteng bruker', command=e_endreBruker)
    btn_e_endreBruker.grid(row=3, column=1, padx=50, pady=5)

    # Oversikter
    btn_o_sykler = Button(hovedvindu, width=20, text='Oversikt over sykler', command=o_sykkler)
    btn_o_sykler.grid(row=1, column=2, padx=(50, 15), pady=5)

    btn_o_kunder = Button(hovedvindu, width=20, text='Oversikt over kunder', command=o_kunder)
    btn_o_kunder.grid(row=2, column=2, padx=(50, 15), pady=5)

    btn_o_stativ = Button(hovedvindu, width=20, text='Oversikt over stativ', command=o_stativ)
    btn_o_stativ.grid(row=3, column=2, padx=(50, 15), pady=5)

    btn_o_belop = Button(hovedvindu, width=20, text='Oversikt over økonomi', command=o_belop)
    btn_o_belop.grid(row=4, column=2, padx=(50, 15), pady=5)

    # Avslutt
    btn_avslutt = Button(hovedvindu, text='Avslutt', command=hovedvindu.destroy)
    btn_avslutt.grid(row=6, column=2, padx=5, pady=5, sticky=E)

    hovedvindu.mainloop()
main()
