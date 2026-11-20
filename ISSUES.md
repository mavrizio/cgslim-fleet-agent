# Registro problemi flotta CGSLIM

Aggiornato dall'agente il 20/11/2026 10:04. Una voce per causa; MHD senza zeri. Generato: non modificare a mano.

## Aperti

<a id="cg-003"></a>

### CG-003 · POS DISCONNECTED dopo timeout get_advanced_config: 24350 (7o giorno senza carte), 37008, 36804 e 10 Pi di banco; 25158 rientrata in 15 min

- **Area:** pi · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-20
- **Macchine:** 24350, 37008, 33326, 23718, 36804, 36805, 24338, 24866, 25254, 28416, 33957, 11223344, 11155520, 11223355, 1470000, 54124120, 58547455, 58555555, 58888999, 99900055, 99990008, 36842, 24254, 32996, 28418, 21784, 25158, 29598, 32995, 26087, 29597, 99999901
- **Prove:** Oggi DISCONNECTED con 'Timeout locale get_advanced_config':
- campo/lab: 24350 (boot alle 09:12, last_ok carta null; ieri alle 16:59 un tentativo carta annullato), 37008 (uptime circa 15 giorni);
- 36804, offline dalle 10:06 di ieri;
- banco: 1470000, 11155520, 11223344, 11223355, 54124120, 58547455, 58555555, 58888999, 99900055 e 99990008.
Errori rientrati:
- 25158: 'Connessione persa get_advanced_config' alle 09:32, rientrato alle 09:47;
- 99999901: stesso errore il 19/11 alle 10:32, rientrato alle 10:47.
36805: POS IDLE.
77700011 (lab): DISCONNECTED senza p95_error.
- **Ipotesi:** Dopo un timeout di cashless_info il pos-engine resta DISCONNECTED. 'Connessione persa' invece rientra da sola, il timeout no. Non confermato.
- **Proposta:** Maurizio:
- retry con backoff breve dopo il timeout;
- non avviare get_advanced_config durante o subito dopo una transazione;
- nascondere la carta a POS DISCONNECTED.
Campo Parma: spegnere e riaccendere il POS della 24350.
Dashboard: escludere il banco dall'avviso.
- **Gia' noto:** POS: get_advanced_config

<a id="cg-005"></a>

### CG-005 · Sottotensione del Raspberry: 24349 ora ferma (CG-029), 24254 tutto il pomeriggio, 24350 ADESSO per la prima volta, 24338/36804 dal boot

- **Area:** hardware · **Gravita':** high · **Visto:** 2026-11-01 → 2026-11-20
- **Macchine:** 24349, 23718, 24254, 24350, 24338, 36804
- **Prove:** 19/11 (ora locale):
- 24349: undervoltage_now dalle 10:02 a intermittenza, poi offline dalle 14:20 (CG-029).
- 24254: ADESSO dalle 14:17 fino allo spegnimento (ultimo report alle 19:54).
- 24350: undervoltage_now alle 15:17, la prima volta che e' ADESSO; oggi 0x50000 dopo il boot delle 09:12.
- 24338: 0x50000, senza riavvii da circa 46 h.
- 36804: 0x50000 (offline).
- 23718: 0x50005 all'ultimo report del 18/11.
- **Ipotesi:** Alimentatori o cavi del Pi deboli. Sulla 24349 il problema ha portato al fermo. Sulla 24254 e' probabile il legame con lo stop vendite. Non confermato.
- **Proposta:** Hardware/campo, alimentatore e cavo del Pi in quest'ordine:
1. 24349 (oggi);
2. 24254;
3. 24350;
4. 23718;
5. 24338;
6. 36804.
- **Gia' noto:** host.throttled 0x50000 (scheda campi); sottotensione sospettata nei flash GMI falliti

<a id="cg-009"></a>

### CG-009 · 24254 (Aprilia): sesto giorno senza vendite, accesa solo dalle 13:03 alle 19:54, oggi alle 10:00 spenta

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-02 → 2026-11-20
- **Macchine:** 24254
- **Prove:** 19/11:
- reboot alle 13:05 (uptime 138), cioe' accesa verso le 13:03;
- ultimo report alle 19:54;
- sottotensione ADESSO (0x50005) dalle 14:17 fino allo spegnimento;
- 0 transazioni, come dal 14/11.
Oggi alle 10:00 offline (845 min). Le altre Aprilia riaccese tra le 05:41 (24866) e le 07:30 (26087).
POS IDLE. Ultima carta approvata il 05/11.
- **Ipotesi:** Linea o timer diversi (fascia fissa circa 13:00-20:00 da 5 giorni) e alimentazione del Pi insufficiente. Non confermato.
- **Proposta:** Campo Aprilia, oggi:
- linea e timer;
- alimentatore del Pi;
- schermo e touch;
- vendita di prova cash e carta.
Maurizio: journal e dmesg del 19/11.

<a id="cg-020"></a>

### CG-020 · Telemetria assente: 32995 muta da 25 h e senza transazioni, 21784 a singhiozzo tutto il 19/11, port 443 KO su banco

- **Area:** pi · **Gravita':** high · **Visto:** 2026-11-11 → 2026-11-20
- **Macchine:** 24350, 33957, 21784, 24349, 28416, 32995, 37008, 54124120, 11223344, 58888999, 1470000
- **Prove:** 32995:
- ultimo report il 19/11 alle 09:18 (uptime 198);
- non tornata stamattina, mentre le altre Parma si sono riaccese entro le 09:22;
- nessuna transazione registrata nelle 24 h (il 18/11 invece ne arrivavano).
21784, 19/11:
- report interrotti dalle 09:39 alle 10:47, dalle 10:41 alle 12:47, dalle 12:53 alle 16:32 e dalle 17:28 alle 18:32;
- update_failed port 443 alle 10:41, 12:38, 16:30 (x2), 17:28 e 18:31, tutti rientrati;
- avviso updater_failing '29 di fila' alle 16:32;
- oggi riaccesa verso le 09:47, report subito.
24350: DNS KO alle 14:12, rientrato.
Banco, port 443 rientrati:
- 58888999 alle 01:59;
- 1470000 alle 05:38;
- 54124120 alle 05:38 e alle 07:03.
- **Ipotesi:** Sulla 32995 l'assenza anche delle transazioni fa pensare a una macchina spenta o senza rete, non piu' solo a un fleet-reporter bloccato.
Sulla 21784 la connettivita' LTE e' intermittente (rssi -52 buono: forse la SIM o il router). Non confermato.
- **Proposta:** Campo Parma: verificare oggi se la 32995 e' accesa, e il suo router.
Maurizio: journal di cgslim-tlm della 32995 quando torna; report anche con DNS KO.
Hardware: SIM e router della 21784.
- **Gia' noto:** Aggiornamenti bloccati (update_failed, rete/SIM)

<a id="cg-029"></a>

### CG-029 · 24349 (Parma) offline dalle 14:20 del 19/11 dopo una mattina di sottotensione ADESSO, non riaccesa oggi

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-19 → 2026-11-20
- **Macchine:** 24349
- **Prove:** 19/11:
- boot verso le 09:16 (uptime 18263 all'ultimo report);
- avvisi undervoltage_now (0x50005) alle 10:02, 11:47, 12:47 e 13:47 (ora locale), fino all'ultimo report delle 14:20;
- offline dalle 14:20.
Oggi alle 10:00:
- ancora offline (1179 min);
- le altre Parma riaccese tra le 08:26 (25157) e le 09:22 (25158).
Nessuna transazione nelle 24 h. Ultima carta approvata il 16/11. POS IDLE all'ultimo report.
- **Ipotesi:** Alimentatore del Pi in cedimento: sottotensione sempre piu' frequente il 18 e il 19/11, poi lo spegnimento. Possibile anche un intervento o lo stacco della linea. Non confermato.
- **Proposta:** Campo Parma, oggi:
1. verificare se la macchina e' accesa;
2. sostituire alimentatore e cavo del Pi;
3. riaccenderla;
4. fare una vendita di prova.
Se era spenta a mano, dirlo.
- **Gia' noto:** host.throttled 0x50000 (scheda campi); collegata a CG-005

<a id="cg-004"></a>

### CG-004 · Seriale GMI assente all'accensione, cavi BG03E: 25158 terzo giorno di fila, 32996 di nuovo (1 recovery ciascuna)

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-20
- **Macchine:** 25158, 32996
- **Prove:** 20/11, 32996 (BG03ER1N):
- serial_missing not_enumerated alle 09:04 (reboot con uptime 111);
- reboot alle 09:08, serial_recovery alle 09:09.
20/11, 25158 (BG03ES5F):
- serial_missing alle 09:22;
- reboot alle 09:26, serial_recovery alle 09:27;
- terzo giorno di fila (18, 19 e 20/11).
In entrambi i casi sul bus solo hub, ethernet e ILITEK.
Ora entrambe IDLE.
Vendite 24 h: 25158 6 approvate su 11; 32996 1 cash.
Anche la lab 77700011 ha un cavo BG03ER1I ed e' gmi_mute oggi alle 08:29: va verificato se e' lo stesso fenomeno.
- **Ipotesi:** Lotto FT232R BG03E e/o alimentazione a ritroso dalla GMI. Il caso della 77700011 sarebbe un terzo cavo dello stesso lotto. Non confermato.
- **Proposta:** Campo Parma: scambiare il cavo della 25158 con uno AL05, tenendo la 32996 come controllo.
Lab: controllare se la 77700011 enumera l'FTDI.
Pi, prossimo rilascio: riavvio anticipato, uhubctl, TX della GMI in high-Z.
- **Gia' noto:** Seriale assente al mattino (serial_missing, not_enumerated)

<a id="cg-006"></a>

### CG-006 · TID di prova 97942484 su 12 terminali (si aggiunge la 36805)

- **Area:** pos · **Gravita':** medium · **Visto:** 2026-10-30 → 2026-11-20
- **Macchine:** 23718, 24338, 28418, 11223344, 11223355, 1470000, 54124120, 58547455, 58555555, 58888999, 99999901, 99900055, 99990008, 36805
- **Prove:** TID 97942484 su:
- 23718;
- banco: 1470000, 11223344, 11223355, 54124120, 58547455, 58555555, 58888999, 99900055, 99990008;
- 99999901;
- ora anche 36805 (terminale 58795441). Il 19/11 la 36805 ha avuto 3 KO (codice 90, l'ultimo verso le 10:04) e 2 carte approvate.
Altri TID di prova: 24338 97942485, 28418 97942488.
- **Ipotesi:** Con lo stesso TID su piu' terminali sono probabili errori 48 e rifiuti, soprattutto con prove contemporanee.
- **Proposta:** Hardware/POS: TID distinti per banco, tornello e 36805, prima di installarla in un centro.
Maurizio: nascondere la carta con TID di prova o senza acquirer.
- **Gia' noto:** POS: altri errori (errore 48, TID duplicato su 24338)

<a id="cg-014"></a>

### CG-014 · Tramogge a zero: 33180 ancora mod 2, 37008 0,0,0, nuova 32996 tramoggia 1 a 0; 29597 rientrata

- **Area:** firmware · **Gravita':** medium · **Visto:** 2026-11-05 → 2026-11-20
- **Macchine:** 23718, 33180, 28419, 25356, 36842, 37008, 29597, 32996
- **Prove:** - 33180: mod 2, schermata 40, tramogge 1,0,0, chl_mode 0, pos-engine inactive; 2 vendite cash il 19/11.
- 37008: schermata 73, tramogge 0,0,0 (secondo giorno).
- 32996 (nuova): schermata 72, tramogge 0,1,0; 1 sola vendita (cash, 16:20 del 19/11).
- 29597: tornata 1,1,0, schermata 70.
- 25356 e 36842: 1,1,0, regolari.
- Banco e mod 5 (36804, 36805, 11223355): tramogge a 0, probabilmente senza hopper.
- **Ipotesi:** Tramogge vuote o non rispondenti. La schermata 72 sembra corrispondere alla tramoggia 1 assente. Non confermato.
- **Proposta:** Campo Parma: tramoggia 1 della 32996.
Campo Tiburtino: tramogge 2 e 3 della 33180.
Chiedere dove si trova la 37008.
Maurizio: documentare le mod 1, 2, 4 e le schermate 71, 72, 73.

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

<a id="cg-028"></a>

### CG-028 · Aprilia: riavvii e spegnimenti in giornata su 29597 (16:28 e 16:31 del 19/11, 0 carte su 12) e 26087 (spenta dalle 08:32 alle 09:48 di oggi)

- **Area:** campo · **Gravita':** medium · **Visto:** 2026-11-18 → 2026-11-20
- **Macchine:** 26087, 29597
- **Prove:** 29597, 19/11:
- reboot alle 16:28 e alle 16:31 (uptime 50-51);
- hostlink locked/unlocked alle 16:33 e alle 16:49;
- 18 transazioni, 6 approvate (tutte cash);
- 12 tentativi carta: 10 annullati, 2 timeout (uno alle 13:56 con 'POS riattivato dopo codice 90');
- ultima carta approvata il 15/11.
Oggi 29597: boot normale alle 06:53, tramogge 1,1,0, schermata 70.
26087, 19/11: 8 approvate su 9.
26087, oggi:
- boot alle 07:30;
- ultimo report alle 08:32;
- di nuovo reboot alle 09:50 (uptime 124): spenta per circa 1 h 15.
Nel 18/11: raffiche di 5 e 4 riavvii.
- **Ipotesi:** Spegnimenti o riavvii manuali, oppure alimentazione instabile sulla linea Aprilia (anche la 24254 ha problemi di alimentazione).
Sulla 29597 i molti annullamenti carta con zero approvazioni fanno sospettare un problema del POS o del lettore, non solo dei clienti. Non confermato.
- **Proposta:** Campo Aprilia:
- chiedere degli interventi del 19/11 alle 16:30 sulla 29597 e di stamattina alle 08:30-09:48 sulla 26087;
- fare una carta di prova sulla 29597.
Maurizio: journal di entrambe (riavvio comandato o power loss).

<a id="cg-011"></a>

### CG-011 · Dashboard: centro null su 11 macchine (nuove 36804, 36805), device_key 'missing' su 21784 e Pi 4f2f67b8, banco nel conteggio (44)

- **Area:** dashboard · **Gravita':** low · **Visto:** 2026-11-04 → 2026-11-19
- **Macchine:** 21784, 23718, 24338, 28418, 33326, 37008, 99999901, 99900055, 99990008, 36804, 36805
- **Prove:** Centro null su:
- 21784, 23718, 24338, 28418, 33326, 37008, 99999901, 99900055, 99990008;
- nuove 36804 (CG-BD56C5A2, first_seen alle 14:22) e 36805 (CG-F87A507A, alle 14:23).
16234 ha invece il centro (C.C. AURA).
device_key_status 'missing' su 21784 e sul Pi senza MHD; 'mismatch' sulla 33326.
Conteggio flotta 44.
- **Ipotesi:** Configurazione mancante su banco, laboratorio e macchine appena preparate.
- **Proposta:** Dashboard/Maurizio:
- assegnare il centro a 36804 e 36805 (o marcarle 'banco');
- escludere banco e laboratorio da conteggio e avvisi;
- ri-registrare la chiave della 21784.
- **Gia' noto:** Profilo display auto / golden SD

<a id="cg-016"></a>

### CG-016 · Errori seriali: 37008 ore 370 (+43), 11223355 fe 990 ferma, 29598 ne 93 al boot, 58555555 invariata

- **Area:** hardware · **Gravita':** low · **Visto:** 2026-11-06 → 2026-11-20
- **Macchine:** 29598, 33326, 11223355, 58547455, 58555555, 37008, 23718, 28418, 99900055
- **Prove:** Oggi:
- 37008: ore 370 (ieri 327), brk 2.
- 11223355: fe 990 invariato, ore 78 (ieri 45), uptime 88495 s.
- 29598: ne 93 con uptime 11015 s (boot alle 06:45), stesso schema dei giorni scorsi.
- 58555555: fe 1521 / ne 2020 invariati, Pi brk 49.
- 99900055: Pi brk 240 / frame 243 invariati.
- 99990008: Pi brk 9.
- 24338: ore 101.
- 23718 e 28418: offline.
- **Ipotesi:** Linee rumorose sulle GMI verdi.
Sulla 37008 l'overrun cresce di circa 45 al giorno con il Pi sempre acceso. Non confermato.
- **Proposta:** Laboratorio: test linea 8.4 e cavo su 11223355 e 58555555.
Campo Aprilia: test linea 8.4 sulla 29598.
Maurizio: contatori come delta giornaliero.
- **Gia' noto:** Aggiornamento firmware GMI (linea disturbata GMI verdi)

<a id="cg-018"></a>

### CG-018 · Banco/lab: 11223355 senza riavvii, nuova 77700011 con 14 riavvii e gmi_mute, offline 23718/33326/28418

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-09 → 2026-11-20
- **Macchine:** 11223344, 11223355, 11155520, 1470000, 54124120, 58547455, 58555555, 58888999, 21784, CG-4F2F67B8, 28418, 23718, 33326, 99900055, 99990008, 77700011
- **Prove:** 11223355: nessun riavvio da ieri alle 09:23 (uptime 88495). L'avviso reboot_storm si e' chiuso alle 15:02.
77700011 (nuova, centro null, cavo BG03ER1I):
- 19/11 11:00: version_change 200->192, poi alle 11:02 di nuovo 200;
- 14 reboot tra le 11:00 e le 12:59 (uptime 45-70);
- device_key_mismatch;
- mode_change 10->5;
- oggi: reboot alle 08:23 e alle 08:27, gmi_mute alle 08:29 (fw null, 5 probe);
- ora mod 0, schermata 29.
11155520: app_restart alle 04:33.
1470000: offline dall'01:25 alle 05:38.
54124120: di nuovo online, update_failed rientrati.
Offline: 23718 (dal 18/11 11:37), 33326 (dal 18/11 10:50), 28418 (dal 17/11 03:51), Pi 4f2f67b8 (dall'11/11).
- **Ipotesi:** Lavori di laboratorio. La 77700011 sembra una macchina di prova preparata con la golden; la GMI muta potrebbe essere scollegata o il cavo BG03E (CG-004). Non confermato.
- **Proposta:** Laboratorio:
- dire cos'e' la 77700011 e se va esclusa dall'analisi;
- stato di 23718, 28418 e 33326;
- TID distinti.
- **Gia' noto:** GMI 'muta' / NCG senza bootloader (menu 9.5 ST-Link); golden SD (CG-<seriale>)

<a id="cg-022"></a>

### CG-022 · gmi_hostlink locked a macchina accesa: 29597 (16:33 e 16:49 del 19/11), 77700011 in lab

- **Area:** pi · **Gravita':** low · **Visto:** 2026-11-12 → 2026-11-20
- **Macchine:** 24349, 25158, 36842, 24338, 28418, 23718, 32996, 25157, 28419, 32995, 29598, 25356, 29597, 58555555, 99999901, 26087, 25357, 36804, 77700011
- **Prove:** 19/11, blocchi senza reboot:
- 29597: lock e unlock nello stesso minuto alle 16:33 e alle 16:49, dopo i reboot delle 16:28 e 16:31;
- 77700011 (lab): 11:28-11:29, 11:31-11:32, 11:34-11:35 e 11:35-11:36.
Tutti gli altri lock sono coppie al boot.
- **Ipotesi:** Blocchi brevi: la protezione funziona. Sulla 29597 si ripete il legame con i riavvii (CG-028).
- **Proposta:** Maurizio: durata del blocco e ultima riga inviata nell'evento; journal della 29597 del 19/11 dalle 16:20 alle 16:55.
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

<a id="cg-015"></a>

### CG-015 · 33957 (Carpi): 16 vendite su 17, nessuna perdita seriale; spenta dalle 09:46 alle 11:16 del 19/11

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-05 → 2026-11-16
- **Macchine:** 33957
- **Prove:** 19/11:
- ultimo report alle 09:46, poi reboot alle 11:18 (uptime 125): spenta per circa 1 h 30, senza eventi seriali;
- 17 transazioni dalle 13:08, 16 approvate (7 carte).
Oggi: boot alle 09:00, vendita approvata alle 09:54, fe 3, POS IDLE.
Ultimo test linea il 05/11: DISTURBATA.
- **Ipotesi:** Lo spegnimento di meta' mattina e' probabilmente esterno (intervento o corrente), non seriale. Non confermato.
- **Proposta:** Chiudere domani (21/11) se resta pulita.
Campo Carpi: ripetere il test linea 8.4 e chiedere dello spegnimento del 19/11.
- **Gia' noto:** Seriale assente al mattino (eccezione 'Disconnessione hardware seriale'); aggiornamento firmware GMI (linea disturbata)

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
