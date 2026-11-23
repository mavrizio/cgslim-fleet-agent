# Registro problemi flotta CGSLIM

Aggiornato dall'agente il 23/11/2026 10:03. Una voce per causa; MHD senza zeri. Generato: non modificare a mano.

## Aperti

<a id="cg-003"></a>

### CG-003 · POS DISCONNECTED dopo timeout get_advanced_config: 24350 decimo giorno senza carte, 37008 da circa 66 h

- **Area:** pi · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-23
- **Macchine:** 24350, 37008, 33326, 23718, 36804, 36805, 24338, 24866, 25254, 28416, 33957, 11223344, 11155520, 11223355, 1470000, 54124120, 58547455, 58555555, 58888999, 99900055, 99990008, 36842, 24254, 32996, 28418, 21784, 25158, 29598, 32995, 26087, 29597, 99999901, 37108, 37109, 37110, 37111, 37112, 37114, 37115, 37116, 37117, 37118, 37119, 77700011
- **Prove:** 23/11:
- 24350: boot alle 09:12; avviso 'Timeout locale get_advanced_config' dalle 09:17; POS DISCONNECTED.
- 24350, ieri: avviso aperto tutto il giorno, chiuso solo allo spegnimento (00:47). 15 transazioni, 9 approvate tutte cash. 6 tentativi carta: 5 annullati e 1 'nessuna carta' (15:03). last_ok carta null.
- 37008: timeout dal 20/11 alle 16:17, ancora DISCONNECTED; uptime 1580555 s (circa 18 giorni). Ieri 25 vendite, tutte cash.
- 25158: 'Connessione persa durante get_advanced_config' alle 09:32, rientrato alle 09:47.
- 32995: ultimo stato con p95_error 'gia' in corso'; offline da ieri alle 09:21.
- Banco 371xx, 36804 e 54124120: DISCONNECTED (offline).
- **Ipotesi:** Dopo un timeout di cashless_info il pos-engine resta DISCONNECTED finche' non si riavvia il POS: il riavvio quotidiano del Pi della 24350 non basta. 'Connessione persa' rientra in circa 15 min. La carta resta proposta a POS fermo e i clienti annullano. Non confermato.
- **Proposta:** Maurizio:
- retry con backoff e reset della connessione TCP dopo il timeout;
- non lanciare get_advanced_config vicino a una transazione;
- nascondere la carta a POS DISCONNECTED.
Campo Parma: spegnere e riaccendere il POS della 24350; se resta in timeout, sostituirlo.
Dashboard: escludere il banco dall'avviso.
- **Gia' noto:** POS: get_advanced_config

<a id="cg-005"></a>

### CG-005 · Sottotensione del Raspberry: 24254 ADESSO per quasi tutto il 22/11, 24350 ADESSO due volte, nuova 29597 dal boot, 24349 ferma

- **Area:** hardware · **Gravita':** high · **Visto:** 2026-11-01 → 2026-11-23
- **Macchine:** 24349, 23718, 24254, 24350, 24338, 36804, 29597
- **Prove:** 22/11, ora locale:
- 24254: undervoltage_now (0x50005) continuo dalle 10:02 alle 14:47, poi a intermittenza fino alle 20:47 (15:17, 15:47-16:02, 16:47, 17:32, 18:17, 18:47, 19:32, 20:02-20:17, 20:47). Ultimo report alle 20:50; oggi alle 10:00 non ancora accesa.
- 24350: undervoltage_now alle 11:47 e alle 20:47; per il resto 0x50000. Oggi 0x50000 dopo il boot delle 09:12.
- 24338: 0x50000 tutto il giorno (uptime circa 118 h).
- 29597 (nuova): 0x50000 dal boot delle 06:53 di oggi.
- 24349: offline dal 19/11 alle 14:20 (CG-029).
- 23718 e 36804: offline.
- **Ipotesi:** Alimentatori o cavi del Pi deboli. Sulla 24254 la sottotensione c'e' a carico normale per tutta la giornata. Non confermato.
- **Proposta:** Hardware/campo, alimentatore e cavo del Pi in quest'ordine:
1. 24349;
2. 24254;
3. 24350;
4. 29597;
5. 24338;
6. 23718;
7. 36804.
- **Gia' noto:** host.throttled 0x50000 (scheda campi); sottotensione sospettata nei flash GMI falliti

<a id="cg-020"></a>

### CG-020 · Telemetria/rete: 32995 muta dalle 09:21 del 22/11 e non tornata, 21784 a singhiozzo tutto il 22/11 e offline dalle 20:22

- **Area:** pi · **Gravita':** high · **Visto:** 2026-11-11 → 2026-11-23
- **Macchine:** 32995, 21784, 24350, 33957, 24349, 28416, 37008, 54124120
- **Prove:** 32995:
- ultimo report il 22/11 alle 09:21;
- stamattina non si e' riaccesa: alle 10:00 offline da 1479 min, mentre le altre Parma sono tornate tra le 08:26 e le 09:22;
- nessuna transazione nelle 24 h.
21784, 22/11:
- reboot alle 11:29 con uptime 3383 s, quindi acceso da circa le 10:33 ma senza report;
- update_failed per DNS alle 11:29, per port 443 alle 12:11, 14:17 e 15:03 (tutti recovered);
- offline dopo i report delle 13:13, 14:17, 15:22, 17:25 e 18:45, ultimo report alle 20:22;
- oggi alle 10:00 non tornata.
37008: update_failed DNS alle 04:03, recovered alle 04:04.
- **Ipotesi:** Rete mobile, SIM o router instabile, con DNS che non risolve all'avvio. Sulla 32995 non si esclude un'alimentazione intermittente o la macchina spenta. Non confermato.
- **Proposta:** Campo Parma: verificare subito la 32995 (accesa? router?).
Hardware: SIM e router della 21784 e della 32995.
Maurizio: escludere dall'avviso i fallimenti di massa simultanei.
- **Gia' noto:** Aggiornamenti bloccati (update_failed, rete/SIM)

<a id="cg-029"></a>

### CG-029 · 24349 (Parma) offline dalle 14:20 del 19/11, quarta mattina senza riaccensione

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-19 → 2026-11-23
- **Macchine:** 24349
- **Prove:** Ultimo report il 19/11 alle 14:20 (0x50005, dopo una mattina di undervoltage_now).
Oggi alle 10:00 offline da 5499 min.
Le altre Parma sono riaccese tra le 08:26 (25157) e le 09:22 (25158), tranne la 32995 (CG-020).
Nessuna transazione nelle 24 h; ultima carta approvata il 16/11.
- **Ipotesi:** Alimentatore del Pi ceduto, oppure macchina staccata. Non confermato.
- **Proposta:** Campo Parma, oggi:
1. verificare la macchina;
2. sostituire alimentatore e cavo del Pi;
3. riaccenderla;
4. fare una vendita di prova.
Se era spenta a mano, dirlo.
- **Gia' noto:** host.throttled 0x50000 (scheda campi); collegata a CG-005

<a id="cg-004"></a>

### CG-004 · Seriale GMI assente all'accensione, cavi BG03E: 25158 sesto giorno di fila, 32996 quinto (1 recovery ciascuna)

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-23
- **Macchine:** 25158, 32996, 77700011, 37116
- **Prove:** 23/11, 32996 (BG03ER1N):
- reboot alle 09:04 (uptime 113), eccezione 'could not open port /dev/ttyUSB0' e serial_missing not_enumerated;
- reboot alle 09:08 (uptime 47);
- serial_recovery alle 09:09.
23/11, 25158 (BG03ES5F):
- reboot alle 09:22 (uptime 112), eccezione e serial_missing;
- reboot alle 09:26;
- serial_recovery alle 09:27.
Sul bus USB solo hub, ethernet e ILITEK.
25158: giorni dal 18 al 23/11 consecutivi.
Ieri entrambe in vendita: 25158 12 approvate su 19, 32996 4 su 9.
77700011 (BG03ER1I): ancora senza contatori GMI.
37116 (BG03ER0O): offline dal 20/11.
- **Ipotesi:** Lotto FT232R BG03E e/o alimentazione a ritroso dalla GMI. Non confermato.
- **Proposta:** Campo Parma: scambiare il cavo della 25158 con uno AL05, tenendo la 32996 come controllo.
Lab:
- sostituire il BG03ER0O della 37116;
- verificare la 77700011.
Pi: riavvio anticipato (30-40 s), uhubctl, TX della GMI in high-Z.
- **Gia' noto:** Seriale assente al mattino (serial_missing, not_enumerated)

<a id="cg-006"></a>

### CG-006 · TID di prova 97942484 anche sulle nuove 37108-37119

- **Area:** pos · **Gravita':** medium · **Visto:** 2026-10-30 → 2026-11-21
- **Macchine:** 23718, 24338, 28418, 11223344, 11223355, 1470000, 54124120, 58547455, 58555555, 58888999, 99999901, 99900055, 99990008, 36805, 37108, 37110, 37111, 37112, 37114, 37115, 37117, 37118, 37119
- **Prove:** TID 97942484 su:
- 23718, 36805, 54124120, 99999901;
- nuove 37108, 37110, 37111, 37112, 37114, 37115, 37117, 37118 e 37119.
Su 37109 e 37116 il TID non e' leggibile (POS in timeout).
Altri TID di prova: 24338 97942485, 28418 97942488.
Storico sulle nuove: codice 90 (37109, 37111, 37112, 37116, 37118), codice 37 (37115), codice 20 (37114).
- **Ipotesi:** Con lo stesso TID su piu' terminali sono probabili rifiuti ed errori 48/90. Le 371xx sembrano destinate al campo.
- **Proposta:** Hardware/POS: TID distinti per tutte le 371xx prima dell'installazione.
Maurizio: nascondere la carta con TID di prova.
- **Gia' noto:** POS: altri errori (errore 48, TID duplicato su 24338)

<a id="cg-009"></a>

### CG-009 · 24254 (Aprilia): una sola vendita cash il 22/11, sottotensione quasi continua, alle 10:00 di oggi non ancora accesa

- **Area:** campo · **Gravita':** medium · **Visto:** 2026-11-02 → 2026-11-23
- **Macchine:** 24254
- **Prove:** 22/11:
- accesa circa alle 09:44 (uptime 39935 s all'ultimo report delle 20:50);
- 1 transazione, cash approvata alle 18:57;
- undervoltage_now quasi continuo dalle 10:02 alle 20:47 (CG-005).
Oggi alle 10:00: offline da 789 min. Ieri si era accesa alle 09:47, il 21/11 alle 10:04.
Le altre Aprilia sono riaccese tra le 05:41 (24866) e le 07:30 (26087).
Ultima carta approvata il 21/11 alle 15:56.
- **Ipotesi:** La macchina e' su una linea o un timer diverso (accensione dopo le 09:45) e il Pi ha l'alimentazione insufficiente. Le pochissime vendite possono dipendere dall'orario o dalla posizione. Non confermato.
- **Proposta:** Campo Aprilia:
- alimentatore e cavo del Pi;
- verificare il timer d'accensione;
- vendita di prova cash.
Se non compare entro mezzogiorno, controllare sul posto.

<a id="cg-014"></a>

### CG-014 · Tramogge: schermata 72 (tramoggia 1 a 0) su 32996, 25158 e ora 24350; schermata 71 su 37008 e 24866; 33180 ancora mod 2

- **Area:** firmware · **Gravita':** medium · **Visto:** 2026-11-05 → 2026-11-23
- **Macchine:** 33180, 37008, 32996, 23718, 28419, 25356, 36842, 29597, 25158, 33090, 24350, 24866
- **Prove:** Oggi:
- tramogge 0,1,0 con schermata 72: 32996 (quinto giorno; ieri 4 approvate su 9), 25158 (secondo giorno; ieri 12 su 19) e 24350 (nuova).
- 29597: tramogge 0,1,0 ma schermata 0, non idle (nuova).
- tramogge 1,0,0 con schermata 71: 37008 (ieri 25 vendite cash) e 24866 (nuova; ieri 24 approvate su 30).
- 33180: mod 2, schermata 40, tramogge 1,0,0, pos-engine inactive; ieri 16 vendite cash.
- 25356 e 33090: tornate a 1,1,0 con schermata 70, quindi probabilmente rifornite.
- 36842 e 28419: 1,1,0, regolari.
- **Ipotesi:** La 72 corrisponde alla tramoggia 1 assente o vuota, la 71 alla tramoggia 2. Le macchine continuano a vendere e 25356/33090 sono rientrate: e' livello basso da rifornire piu' che guasto. Non confermato.
- **Proposta:** Campo Parma: tramoggia 1 di 32996, 25158 e 24350.
Campo Aprilia: tramoggia 2 della 24866; schermo e tramoggia 1 della 29597.
Campo Tiburtino: tramogge della 33180.
Maurizio: documentare le schermate 71, 72, 73 e la mod 2; distinguere nel payload 'assente' da 'livello basso'.

<a id="cg-019"></a>

### CG-019 · ST-Link fallisce con 'unknown state when halt was requested' al primo tentativo: 5 GMI Tiburtino su 7, fino a 6 ore di installazione

- **Area:** firmware · **Gravita':** medium · **Visto:** 2026-11-10 → 2026-11-12
- **Macchine:** 58547455, 54124120, 1470000, 33089, 25254, 25355, 25356, 25357
- **Prove:** 12/11, GMI NCG 4.09 senza bootloader:
- 33089: falliti alle 10:30 (probe), 10:31 (erase_app), 10:48, 11:00 e 12:17 (probe); riuscito alle 16:35 ('legacy full', 3,19 V).
- 25355: falliti alle 14:28/14:29, 16:08/16:09 e 17:24 (probe ed erase_app); riuscito alle 17:35 (legacy full).
- 25254: falliti alle 11:51 (probe) e 11:52 (erase_app); RDY alle 11:53 e fw 4.20.93 via seriale alle 11:54.
- 25357: fallito alle 13:02, riuscito alle 13:06.
- 25356: fallito alle 14:05, riuscito alle 14:06.
- 33090: nessun ST-Link; fw da 4.09 a 4.20.92 alle 15:38.
Tutte ora a 4.20.93, bootloader V2.
- **Ipotesi:** L'halt fallisce su queste GMI col firmware NCG 4.09 in esecuzione; un nuovo tentativo, o il reset, lo fa riuscire. Non e' una GMI guasta. Non confermato.
- **Proposta:** Maurizio:
- connect-under-reset (reset_config srst) e un secondo tentativo automatico dopo 'unknown state';
- se dopo il fallimento la GMI risponde RDY, passare subito al flash seriale.
- **Gia' noto:** GMI 'muta' / NCG senza bootloader (menu 9.5 ST-Link)

<a id="cg-024"></a>

### CG-024 · 33326 (lab): dopo il cambio SD/GMI del 18/11 in loop RDY con NCG 4.09, offline dalle 10:50

- **Area:** firmware · **Gravita':** medium · **Visto:** 2026-11-16 → 2026-11-18
- **Macchine:** 33326
- **Prove:** 18/11:
- 10:44: reboot (uptime 38), version_change 205->192, gmi_mute NCG4.09 no_bootloader;
- 10:45: fw da 4.20.31 a 4.09, device_key_mismatch;
- 10:49: version_change 192->200, app_down e 'RILEVATO LOOP BOOTLOADER (RDY)' (YRDYRDY...);
- da allora nessun report (alle 10:50).
L'avviso gmi_blocked (errore 98) si e' chiuso alle 10:47.
Ora: branch mod5 (era beta), fw riportato 4.09, schermata 88.
La 24338 ha fatto lo stesso giro alle 11:13 (205->192, fw 4.09), ma alle 11:30 e' tornata a 205 / 4.20.98.
- **Ipotesi:** In laboratorio stanno usando la SD golden e/o un'altra GMI. Sulla 33326 il flash e' rimasto a meta' (RDY), come il 16/11 al blocco 13824. Non confermato.
- **Proposta:** Laboratorio: dire cosa e' stato montato sulla 33326.
ST-Link (9.5) con bootloader V2 e 4.20.93/98, poi riaccenderla.
Maurizio: loggare l'indirizzo del blocco fallito.
- **Gia' noto:** Aggiornamento firmware GMI che fallisce (gmi_flash_failed, gmi_blocked, loop RDY)

<a id="cg-030"></a>

### CG-030 · 21784: tutti i 19 pagamenti carta del 22/11 falliti con 'POS non configurato (codice 20)'

- **Area:** pos · **Gravita':** medium · **Visto:** 2026-11-20 → 2026-11-22
- **Macchine:** 21784
- **Prove:** 22/11:
- 30 transazioni, 11 approvate tutte cash;
- 19 errori carta 'POS non configurato (codice 20)': 11:54 (3), 11:55, 12:15, 15:58 (2), 16:02, 16:03 (3), 16:04, 19:29 (5) e 19:30 (2);
- card_activity: ko 19, ok 0 (ultima carta ok il 20/11, 'esito recuperato con H').
POS IDLE e connesso nell'ultimo report. Terminale 58127169 (TID 75501208), registrato anche su MDB.
I tentativi a raffica (5 in un minuto alle 19:29) indicano clienti che riprovano.
- **Ipotesi:** Il terminale ha perso la configurazione: dopo i cali di rete, o per il doppio uso MDB/P95. La carta resta proposta. Non confermato.
- **Proposta:** Hardware/POS: verificare la configurazione e l'acquirer del terminale 58127169; se serve, riconfigurarlo.
Maurizio: nascondere la carta dopo un codice 20 finche' una lettura di cashless_info non va a buon fine.
- **Gia' noto:** POS: altri errori

<a id="cg-011"></a>

### CG-011 · Dashboard: centro null su 22 macchine (nuove 37108-37119), chiave 'missing' su 21784, 'mismatch' su 33326 e 77700011

- **Area:** dashboard · **Gravita':** low · **Visto:** 2026-11-04 → 2026-11-21
- **Macchine:** 21784, 23718, 24338, 28418, 33326, 37008, 99999901, 36804, 36805, 77700011, 37108, 37109, 37110, 37111, 37112, 37114, 37115, 37116, 37117, 37118, 37119
- **Prove:** Centro null su:
- 21784, 23718, 24338, 28418, 33326, 37008, 99999901, 36804, 36805, 77700011, 54124120;
- le 11 nuove 37108-37119.
device_key_status 'missing' su 21784 e sul Pi senza MHD; 'mismatch' su 33326 e 77700011 (avviso aperto dal 19/11).
Conteggio flotta 47; gli ID di banco precedenti non compaiono piu'.
- **Ipotesi:** Macchine in preparazione senza registro. Probabilmente il banco e' stato rinumerato con gli MHD definitivi.
- **Proposta:** Dashboard/Maurizio:
- assegnare il centro o marcare 'banco' le 371xx, 36804 e 36805;
- escludere banco e lab da conteggio e avvisi;
- ri-registrare la chiave della 21784;
- ripulire i vecchi ID di banco.
- **Gia' noto:** Profilo display auto / golden SD

<a id="cg-016"></a>

### CG-016 · Errori seriali: 37008 ore 498 (+39), 24338 ore 218 (+39), 29598 ne 128

- **Area:** hardware · **Gravita':** low · **Visto:** 2026-11-06 → 2026-11-23
- **Macchine:** 29598, 37008, 24338, 28418, 54124120, 23718, 33326, 11223355, 58555555, 24866
- **Prove:** Oggi:
- 37008: ore 498 (ieri 459), uptime circa 18 giorni, Pi brk 2.
- 24338: ore 218 (ieri 179), uptime circa 118 h.
- 29598: ne 128 con uptime 11048 s (ieri 78, il giorno prima 127 a uptime simile).
- 24866: fe 9, ne 2.
- 24254: fe 12, ne 4.
- Offline: 54124120 ore 108; 28418 fe 137, ne 36, ore 115.
- **Ipotesi:** Linee rumorose (GMI verdi). Sulle macchine sempre accese il contatore ore cresce di circa 40 al giorno. Non confermato.
- **Proposta:** Campo Aprilia: test linea 8.4 sulla 29598.
Laboratorio: test 8.4 su 37008 e 24338.
Maurizio: mostrare i contatori come delta giornaliero.
- **Gia' noto:** Aggiornamento firmware GMI (linea disturbata GMI verdi)

<a id="cg-018"></a>

### CG-018 · Banco/lab: nuove 37108-37119 preparate il 20/11 con riavvii a raffica, 77700011 ancora muta, ID di banco spariti

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-09 → 2026-11-21
- **Macchine:** 37108, 37109, 37110, 37111, 37112, 37114, 37115, 37116, 37117, 37118, 37119, 77700011, 23718, 28418, 33326, 54124120, CG-4F2F67B8, 21784
- **Prove:** 20/11, 37108-37119 (11 macchine):
- reboot simultanei (uptime 134-142) alle 10:55 e alle 11:08;
- 37108, 37109, 37110, 37117 e 37118 anche alle 14:38 e alle 14:56;
- avvisi reboot_storm;
- 37118: repo_healed stale_lock alle 11:09;
- poi offline dalle 11:10-15:29.
Versioni: 37111 e 37112 beta 205 / fw 4.20.98; le altre mod5 200 / 4.20.93.
Line test 11/11 alle 13:04 su 37109, 37111 e 37112.
I vecchi ID di banco (11223344, 58555555...) non sono piu' nei dati.
77700011: mod 0, schermata 29, nessun contatore GMI, uptime circa 25 h.
Offline: 54124120 (dal 20/11 10:39), 23718, 33326, 28418, Pi senza MHD (dall'11/11).
- **Ipotesi:** Le 371xx sono le GMI di banco con l'MHD definitivo, accese e spente insieme per la preparazione. Non confermato.
- **Proposta:** Laboratorio:
- confermare la rinumerazione;
- dire la destinazione delle 371xx;
- stato di 23718, 28418, 33326 e 77700011.
- **Gia' noto:** GMI 'muta' / NCG senza bootloader; golden SD (CG-<seriale>)

<a id="cg-022"></a>

### CG-022 · gmi_hostlink: tornano i lock a macchina accesa (36842, 29598, 29597)

- **Area:** pi · **Gravita':** low · **Visto:** 2026-11-12 → 2026-11-23
- **Macchine:** 29597, 77700011, 37118, 24349, 25158, 36842, 24338, 28418, 23718, 32996, 25157, 28419, 32995, 29598, 25356, 58555555, 99999901, 26087, 25357, 36804
- **Prove:** Lock senza reboot ne' app_restart:
- 36842: locked=true e false il 22/11 alle 11:02 (riaccensione alle 09:10);
- 29598: locked=true alle 19:46, false alle 19:47 del 22/11 (riaccensione alle 06:46 di oggi);
- 29597: locked false e true entrambi alle 09:57 di oggi (boot alle 06:53). Ultimo report alle 09:57 con schermata 0, idle false, tramogge 0,1,0, throttled 0x50000.
Tutti gli altri lock delle 24 h coincidono con reboot e app_restart (accensioni mattutine, 21784 alle 11:29, recovery seriale di 32996 e 25158).
- **Ipotesi:** Blocchi brevi della seriale o del main loop del Pi. Sulla 29597 l'ordine degli eventi alle 09:57 non e' chiaro: potrebbe essere ancora bloccata. La sottotensione dal boot e' un sospetto. Non confermato.
- **Proposta:** Controllare il prossimo report della 29597: se resta su schermata 0 o locked, fare un controllo sul posto.
Maurizio:
- durata del blocco nell'evento;
- loggare l'ultima riga ricevuta prima del lock.
- **Gia' noto:** Pagamenti bloccati perche' la GMI non sente il Pi (evento gmi_hostlink)

<a id="cg-025"></a>

### CG-025 · Tornello di banco 99999901 (MOD10): 15 vendite su 19, STAN duplicato, schermata 161 a hopper vuoto

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-16 → 2026-11-19
- **Macchine:** 99999901
- **Prove:** 18/11:
- 19 transazioni tra le 10:02 e le 13:26, 15 approvate (14 cash, 5 tentativi carta);
- 10:04: codice 37 con 'POS riattivato dopo codice 90';
- 10:12: timeout con 'esito H scartato: STAN 000002 gia' registrato';
- nessun gate_short_change nelle 24 h.
Oggi: schermata 161 (non da' resto, importo esatto), tramogge 0,0,0, POS IDLE, TID 97942484.
- **Ipotesi:** La schermata 161 e' comportamento voluto con l'hopper vuoto. Il STAN duplicato e' coerente col TID condiviso (CG-006). Non confermato.
- **Proposta:** Laboratorio:
- rifornire l'hopper;
- TID distinto.
Maurizio: non emettere gate_short_change con missing=0; controllare la gestione del STAN duplicato.
- **Gia' noto:** MOD10 Tornello; POS: altri errori

<a id="cg-027"></a>

### CG-027 · Nuove macchine: 16234 (C.C. AURA) vende regolarmente, 36804 e 36805 offline dalle 10:06 del 19/11

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-18 → 2026-11-20
- **Macchine:** 16234, 36804, 36805
- **Prove:** 16234:
- 19/11: 10 transazioni, 9 approvate (2 carte); codice 90 alle 18:14;
- oggi boot alle 07:05, POS IDLE, TID 75709726.
36804 e 36805:
- ultimo report insieme alle 10:06 e alle 10:07 del 19/11 (uptime circa 71100 s);
- non tornate;
- 36804 POS in timeout; 36805 TID di prova (CG-006).
- **Ipotesi:** 16234 installata bene. 36804 e 36805 probabilmente spente per lo spostamento o la fine della preparazione. Non confermato.
- **Proposta:** Lab/campo:
- dire dove vanno 36804 e 36805;
- assegnare centro e TID;
- test linea 8.4 sulle tre.
- **Gia' noto:** GMI 'muta' / NCG senza bootloader (menu 9.5 ST-Link); IP del Raspberry (PI_IP)

## In osservazione

<a id="cg-031"></a>

### CG-031 · 33957 (Carpi): carte di nuovo regolari, nessun codice 90 nelle 24 h

- **Area:** pos · **Gravita':** low · **Visto:** 2026-11-21 → 2026-11-22
- **Macchine:** 33957
- **Prove:** 22/11-23/11:
- 29 transazioni, 25 approvate;
- 12 tentativi carta; card_activity ok 9, ko 3;
- errori solo 'nessuna carta entro il tempo' alle 18:21 e alle 19:18, piu' 2 annullate;
- nessun 'codice 90' e nessun riavvio in giornata.
Oggi riaccensione normale alle 09:00, vendita approvata alle 09:54, POS IDLE.
Ultimo test linea (05/11): DISTURBATA.
- **Ipotesi:** Il codice 90 e i 'nessuna carta' a grappolo del 21/11 sono rientrati. Forse il POS si era disattivato, forse c'erano clienti. Non confermato.
- **Proposta:** Chiudere se resta pulito anche domani.
Maurizio: riattivo automatico al POS dopo il codice 90.
- **Gia' noto:** POS: altri errori

## Risolti

<a id="cg-002"></a>

### CG-002 · 36842 offline dal 31/10 20:21: tornata online il 03/11 alle 12:21

- **Area:** campo · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-03
- **Macchine:** 36842
- **Prove:** 03/11:
- Reboot alle 12:21 (uptime 67) e alle 12:32.
- Aggiornata a SLIM-4.20.176 (12:32) e fw 4.20.84 (12:36).
- 1 vendita cash alle 16:53.
Notte e mattina:
- Spenta normalmente la notte (ultimo report 04/11 00:09).
- Riaccesa alle 09:10 di oggi.
Ora: POS IDLE connesso, GMI fe=3 (era 138). Resta throttled 0x50005, con sottotensione ADESSO dalle 09:32.
- **Ipotesi:** Probabilmente un intervento sul posto il 03/11 verso mezzogiorno: il reboot con uptime 67 e' fuori dall'orario del timer. La causa dello stop del 31/10 non e' nota.
- **Proposta:** Nessuna azione su questa voce. Alimentatore in CG-005, TID in CG-006. Se possibile, recuperare dal tecnico cosa ha trovato.

<a id="cg-001"></a>

### CG-001 · Aggiornamento firmware GMI: rollout beta 4.20.94-4.20.98 pulito, voce chiusa

- **Area:** firmware · **Gravita':** low · **Visto:** 2026-10-30 → 2026-11-10
- **Macchine:** 26087, 33326, 24338, 28418, 23718
- **Prove:** 13/11, rollout beta in tre passi, nessun gmi_flash_failed:
- 203 + fw 4.20.96 tra le 11:19 e le 12:04;
- 204 + 4.20.97 tra le 13:15 e le 14:10;
- 205 + 4.20.98 tra le 15:29 e le 16:16.
Macchine: 33326, 28418, 23718 e 24338 (11223344 fino a 204/4.20.97).
RDY loggato durante i flash, ogni volta seguito dal fw_change entro 2-5 minuti:
- 33326 alle 11:25 e alle 15:32;
- 28418 alle 11:31 e alle 15:41;
- 23718 alle 11:46 e alle 13:29.
33326: app_down alle 15:32, fw 4.20.98 alle 15:46, avviso chiuso alle 16:17.
- **Ipotesi:** La corruzione del 10/11 sulla 26087 era un disturbo occasionale. I RDY sono la fase normale del flash.
- **Proposta:** Chiusa. Non segnalare il RDY durante un flash pianificato. Riaprire se compare un gmi_flash_failed.
- **Gia' noto:** Aggiornamento firmware GMI che fallisce (gmi_flash_failed, gmi_blocked, loop RDY)

<a id="cg-007"></a>

### CG-007 · 36842 e 32996 di nuovo in vendita

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-01 → 2026-11-12
- **Macchine:** 36842, 32996
- **Prove:** 36842:
- ora tramogge 1,1,0, schermata 70;
- 12/11: 17 transazioni, 9 approvate (5 cash, carte approvate);
- riavvii fuori orario alle 11:41 (uptime 135) e alle 12:35 (uptime 66), probabile intervento.
32996: 6 transazioni, 5 approvate (12/11 16:40-19:08).
La 23718 passa in CG-014.
- **Ipotesi:** Intervento sul posto il 12/11 verso mezzogiorno (tramoggia e parametri POS).
- **Proposta:** Chiusa. Se possibile, farsi dire dal tecnico cosa ha sistemato sulla 36842.

<a id="cg-008"></a>

### CG-008 · Branch riportato 'parma' ma servizio gitpuller@beta su 3 macchine Aprilia

- **Area:** dashboard · **Gravita':** low · **Visto:** 2026-11-01 → 2026-11-01
- **Macchine:** 26087, 29597, 29598
- **Prove:** Il 02/11 dalle 16:35 e' stato applicato il provisioning GIT_BRANCH. Oggi 26087, 29597 e 29598 riportano branch 'beta', servizio gitpuller@beta, git_commit ea89cae e SLIM-4.20.179. Il branch riportato e il servizio coincidono.
- **Ipotesi:** Disallineamento sistemato dal provisioning del branch.
- **Proposta:** Nessuna azione.

<a id="cg-010"></a>

### CG-010 · 37008: stabile dal 05/11, resta accesa la notte; throttled 0x80000

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-03 → 2026-11-05
- **Macchine:** 37008
- **Prove:** Uptime 371178 s (~103 h): nessun reboot dal 05/11 circa alle 02:50.
27 vendite cash tra l'08/11 11:10 e le 20:43.
Throttled ancora 0x80000 (limite termico soft dal boot, nessuna sottotensione), CPU a 50,5 °C.
Centro ancora null.
- **Ipotesi:** Riavvio isolato, non ripetuto. La macchina e' alimentata 24 h. Il bit termico e' probabilmente dovuto al funzionamento continuo.
- **Proposta:** Chiusa.
Resta da chiedere dove si trova (CG-011) e da controllare la ventilazione se la temperatura sale.
POS in CG-003, contatori seriali in CG-016.

<a id="cg-012"></a>

### CG-012 · Codice 31: quattro giorni senza rifiuti, voce chiusa

- **Area:** pos · **Gravita':** low · **Visto:** 2026-11-04 → 2026-11-15
- **Macchine:** 24254, 28418, 33957, 24866, 29597, 23718, 58888999, 33089, 25356, 24349
- **Prove:** 16, 17, 18 e 19/11: nessun 'codice 31' in flotta.
33957: 16 approvate su 17 (7 carte).
Unici errori carta nelle 24 h: codice 90 (16234 alle 18:14, 29597 alle 13:56) e 'nessuna carta entro il tempo'.
- **Ipotesi:** I rifiuti del 15/11 sono rientrati dopo l'intervento POS sulla 33957.
- **Proposta:** Chiusa. Riaprire se ricompare il codice 31.
- **Gia' noto:** POS: altri errori

<a id="cg-013"></a>

### CG-013 · Beta Aprilia e 37008 passate a mod12: ora allineate a 187

- **Area:** pi · **Gravita':** low · **Visto:** 2026-11-05 → 2026-11-05
- **Macchine:** 26087, 29597, 29598, 37008
- **Prove:** Il 05/11 version_change 185->187:
- 37008 alle 16:01;
- 26087 alle 17:30;
- 29598 alle 17:45;
- 29597 alle 17:53.
Ora tutte le 15 mod12 hanno commit 23eb98c, SLIM-4.20.187 e fw 4.20.90.
- **Ipotesi:** Il merge di 187 su mod12 ha riallineato repo e release.
- **Proposta:** Nessuna azione. Resta utile un avviso dashboard per app_version incoerente col commit.

<a id="cg-015"></a>

### CG-015 · 33957 (Carpi): stabile, 27 vendite su 31, voce chiusa

- **Area:** hardware · **Gravita':** low · **Visto:** 2026-11-05 → 2026-11-16
- **Macchine:** 33957
- **Prove:** 20/11: 31 transazioni tra le 10:01 e le 19:55, 27 approvate (8 carte), 4 annullate.
Nessun evento seriale; fe 3, ore 1.
Oggi riaccensione normale alle 09:00 (uptime 125), POS IDLE.
- **Ipotesi:** Lo spegnimento del 19/11 era esterno.
- **Proposta:** Chiusa. Resta consigliato il test linea 8.4: l'ultimo, del 05/11, era DISTURBATA.
- **Gia' noto:** Seriale assente al mattino; aggiornamento firmware GMI (linea disturbata)

<a id="cg-017"></a>

### CG-017 · 33957 (Carpi): vendite e carte riprese

- **Area:** hardware · **Gravita':** low · **Visto:** 2026-11-07 → 2026-11-09
- **Macchine:** 33957
- **Prove:** 11/11: 10 transazioni tra le 11:19 e le 20:17, 8 approvate (4 carte). Unici errori: 2 codice 90 alle 12:42 (in CG-012).
Aggiornata a 199 e fw 4.20.93 senza problemi. Oggi reboot alle 09:00, POS IDLE.
- **Ipotesi:** Il calo di vendite era legato al traffico del sito o ai problemi POS gia' rientrati.
- **Proposta:** Chiusa. Linea DISTURBATA in CG-015.

<a id="cg-021"></a>

### CG-021 · Installazione Tiburtino Guidonia: tutte e 7 in vendita, voce chiusa

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-12 → 2026-11-14
- **Macchine:** 33089, 25254, 25355, 25356, 25357, 33090, 33180
- **Prove:** Oggi tutte online (SLIM-4.20.200, fw 4.20.93), riaccese tra le 06:51 (25356) e le 08:54 (33090).
Vendite 24 h, tutte approvate:
- 33090: 22;
- 33180: 18;
- 25254: 9;
- 33089: 9;
- 25356: 9 (6 con carta);
- 25355: 6;
- 25357: 5.
25254: 'Connessione persa get_advanced_config' alle 07:47, rientrato alle 08:02.
- **Ipotesi:** Installazione assestata. Le poche vendite dei giorni scorsi su 25356 e 25357 erano dovute al traffico.
- **Proposta:** Chiusa. Resta consigliato il test linea 8.4. Tramogge della 33180 in CG-014.
- **Gia' noto:** Profilo display auto / golden SD; GMI 'muta' / NCG senza bootloader

<a id="cg-023"></a>

### CG-023 · 36842 (Parma): niente piu' riavvii a meta' giornata, voce chiusa

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-12 → 2026-11-13
- **Macchine:** 36842
- **Prove:** 14 e 15/11 senza riavvii in giornata. Oggi solo la riaccensione normale alle 09:09 (uptime 135).
15/11: 36 transazioni, 32 approvate (8 con carta), 4 annullate. Throttled 0x0.
Ora tramogge 0,1,0 e schermata 72 (ieri 1,1,0): da tenere d'occhio.
- **Ipotesi:** I riavvii del 12 e del 13/11 erano interventi o interruzioni di corrente.
- **Proposta:** Chiusa. Se la tramoggia 1 resta a 0 nei prossimi giorni, far controllare dal campo.

<a id="cg-026"></a>

### CG-026 · 25254 (Tiburtino): spenta tutto il 18/11, di nuovo in vendita, voce chiusa

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-18 → 2026-11-18
- **Macchine:** 25254
- **Prove:** 19/11: 1 vendita cash approvata alle 20:43, ultimo report alle 21:04.
Oggi: riaccensione normale alle 07:46 (uptime 146), POS IDLE, throttled 0x0, schermata 70, tramogge 1,1,0.
- **Ipotesi:** Spegnimento a monte per un giorno intero il 18/11. Causa non nota.
- **Proposta:** Chiusa. Se il tecnico lo sa, annotare cosa e' successo il 18/11.

<a id="cg-028"></a>

### CG-028 · Aprilia: riavvii simultanei del 20/11 non ripetuti, voce chiusa

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-18 → 2026-11-20
- **Macchine:** 26087, 29597, 29598, 24866
- **Prove:** 21 e 22/11: nessun riavvio in giornata sulle quattro.
Vendite del 22/11:
- 26087: 24 su 26;
- 29597: 23 su 27;
- 29598: 17 su 17;
- 24866: 24 su 30.
Oggi accensioni singole: 24866 alle 05:41, 29598 alle 06:46, 29597 alle 06:53, 26087 alle 07:30.
- **Ipotesi:** Stacchi di alimentazione a monte del 19-20/11, non guasti delle macchine.
- **Proposta:** Chiusa. Riaprire se si ripetono riavvii simultanei in giornata.
