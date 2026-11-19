# Registro problemi flotta CGSLIM

Aggiornato dall'agente il 19/11/2026 10:04. Una voce per causa; MHD senza zeri. Generato: non modificare a mano.

## Aperti

<a id="cg-003"></a>

### CG-003 · POS DISCONNECTED dopo timeout get_advanced_config: 24350 (6o giorno senza carte), 37008, nuova 36804, banco; 24338 rientrata da sola

- **Area:** pi · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-19
- **Macchine:** 24350, 37008, 33326, 23718, 36804, 36805, 24338, 24866, 25254, 28416, 33957, 11223344, 11155520, 11223355, 1470000, 54124120, 58547455, 58555555, 58888999, 99900055, 99990008, 36842, 24254, 32996, 28418, 21784, 25158, 29598, 32995, 26087, 29597
- **Prove:** Oggi DISCONNECTED con 'Timeout locale get_advanced_config':
- campo/lab: 24350 (boot alle 09:12, last_ok carta null), 37008;
- 36804 (nuova): carta approvata alle 09:24 dopo un codice 90, avviso alle 09:47;
- banco: 1470000, 11155520, 11223344, 11223355, 54124120, 58547455, 58555555, 58888999;
- 99900055 e 99990008, ieri IDLE: oggi Broken pipe alle 09:17 e alle 09:32, poi timeout.
36805: p95_error ma POS IDLE.
23718 e 33326 DISCONNECTED, ma sono offline.
24338: errore dalle 11:32 di ieri alle 04:47 di oggi, rientrato senza riavvio (uptime 80842 s).
Altri errori POS rientrati ieri:
- 26087: Broken pipe dalle 11:02;
- 29597: 'Operazione activate gia' in corso' dalle 18:17 alle 18:47.
- **Ipotesi:** Dopo un timeout di cashless_info il pos-engine resta DISCONNECTED. La 36804 mostra che il blocco puo' arrivare dopo un pagamento riuscito.
La ripresa spontanea della 24338 dopo circa 17 h fa pensare alla rilettura ogni 24 h o a un retry lento. Non confermato.
- **Proposta:** Maurizio:
- ritentare con backoff breve dopo l'errore;
- non avviare get_advanced_config durante o subito dopo una transazione;
- nascondere la carta a POS DISCONNECTED;
- verificare nel log della 24338 cosa l'ha sbloccata alle 04:47.
Campo Parma: spegnere e riaccendere il POS della 24350.
Dashboard: escludere il banco dall'avviso.
- **Gia' noto:** POS: get_advanced_config

<a id="cg-009"></a>

### CG-009 · 24254 (Aprilia): quinto giorno senza vendite, accesa solo 12:59-20:02, oggi alle 10:00 spenta

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-02 → 2026-11-19
- **Macchine:** 24254
- **Prove:** 18/11:
- reboot alle 12:59 (uptime 139), ultimo report alle 20:02;
- sottotensione ADESSO dalle 13:02 alle 20:17;
- 0 transazioni (anche il 14, 15, 16 e 17/11).
Oggi alle 10:00 offline (838 min). Le altre Aprilia accese tra le 05:41 (24866) e le 09:07 (29597).
POS IDLE, ultima carta approvata il 05/11.
- **Ipotesi:** Linea o timer diversi (fascia fissa 12:30-20:00 da 4 giorni) e alimentazione del Pi insufficiente. Non confermato.
- **Proposta:** Campo Aprilia, oggi:
- linea e timer;
- alimentatore del Pi;
- schermo e touch;
- vendita di prova cash e carta.
Maurizio: journal e dmesg del 18/11.

<a id="cg-004"></a>

### CG-004 · Seriale GMI assente all'accensione, cavi BG03E: 32996 (2 recovery oggi) e 25158 (ieri e oggi)

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-19
- **Macchine:** 25158, 32996
- **Prove:** 25158 (BG03ES5F):
- 18/11 10:05: serial_missing not_enumerated (reboot con uptime 114), recovery alle 10:09/10:10; avviso di 3 riavvii in 6 h. Correzione: ieri non e' stata una mattina pulita.
- 19/11 09:22: serial_missing, reboot alle 09:26, serial_recovery alle 09:27.
32996 (BG03ER1N), 19/11:
- 09:04 serial_missing, poi ancora alle 09:08 (reboot con uptime 32);
- serial_recovery alle 09:09 e alle 09:14: entrambi i tentativi consumati.
Sul bus solo hub, ethernet e ILITEK.
Ora entrambe IDLE.
Vendite: 25158 4 (1 carta); 32996 3, l'ultima carta approvata alle 09:52.
- **Ipotesi:** Lotto FT232R BG03E e/o alimentazione a ritroso dalla GMI. Il secondo recovery della 32996 mostra che un solo riavvio non sempre basta: col terzo caso la macchina resterebbe ferma.
- **Proposta:** Campo Parma: scambiare il cavo della 25158 con uno AL05, tenendo la 32996 come controllo.
Pi, prossimo rilascio: riavvio anticipato, uhubctl, TX della GMI in high-Z.
- **Gia' noto:** Seriale assente al mattino (serial_missing, not_enumerated)

<a id="cg-005"></a>

### CG-005 · Sottotensione del Raspberry: 24349 a intermittenza e ADESSO, 24254 tutto il pomeriggio, 23718 fissa, 24350/24338/36804 dal boot

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-19
- **Macchine:** 24349, 23718, 24254, 24350, 24338, 36804
- **Prove:** 18/11, orari locali:
- 24349: undervoltage_now alle 10:47, 13:17, 14:02, 15:02, 16:47, 18:02, 21:17 e 22:02; oggi 0x50005 alle 09:49.
- 24254: dalle 13:02 alle 20:17 senza pause.
- 23718: 0x50005 all'ultimo report (11:37 del 18/11).
Oggi 0x50000 su 24350, 24338 e 36804 (nuova).
- **Ipotesi:** Alimentatori o cavi del Pi deboli. Sulla 24254 probabile legame con lo stop vendite (CG-009). Non confermato.
- **Proposta:** Hardware/campo, alimentatore e cavo del Pi in quest'ordine:
1. 24254;
2. 24349;
3. 24350;
4. 23718;
5. 24338;
6. 36804.
- **Gia' noto:** host.throttled 0x50000 (scheda campi); sottotensione sospettata nei flash GMI falliti

<a id="cg-006"></a>

### CG-006 · TID di prova 97942484 su 11 terminali (23718, banco, tornello 99999901, nuove 99900055 e 99990008)

- **Area:** pos · **Gravita':** medium · **Visto:** 2026-10-30 → 2026-11-18
- **Macchine:** 23718, 24338, 28418, 11223344, 11223355, 1470000, 54124120, 58547455, 58555555, 58888999, 99999901, 99900055, 99990008
- **Prove:** TID 97942484 su:
- 23718;
- banco: 1470000, 11223344, 11223355, 54124120, 58547455, 58555555, 58888999;
- 99999901;
- da ieri anche 99900055 (terminale 58794933) e 99990008 (58794799).
99990008: 'POS non attivo (codice 90)' alle 08:59, poi carte approvate fino alle 09:09.
99900055: 2 carte approvate tra le 09:12 e le 09:18.
Altri TID di prova: 24338 97942485, 28418 97942488.
- **Ipotesi:** Con lo stesso TID su piu' terminali sono probabili errori 48 e rifiuti, soprattutto se le prove sono contemporanee.
- **Proposta:** Hardware/POS: TID distinti per tutti i terminali di banco e per il tornello prima delle prove carta.
Maurizio: nascondere la carta con TID 00000000 o senza acquirer.
- **Gia' noto:** POS: altri errori (errore 48, TID duplicato su 24338)

<a id="cg-014"></a>

### CG-014 · Tramogge a zero: 33180 ancora mod 2, 37008 ora 0,0,0 (schermata 73), 29597 tramoggia 1 a 0

- **Area:** firmware · **Gravita':** medium · **Visto:** 2026-11-05 → 2026-11-19
- **Macchine:** 23718, 33180, 28419, 25356, 36842, 37008, 29597
- **Prove:** - 33180: mod 2, schermata 40, tramogge 1,0,0, chl_mode 0; 18/11 6 vendite cash tra le 15:01 e le 18:20.
- 37008: schermata 73, tramogge 0,0,0 (ieri 1,0,0); 4 vendite cash tra le 16:03 e le 17:52.
- 29597 (nuova): schermata 72, tramogge 0,1,1, dopo i riavvii di ieri sera (CG-028).
- 23718: offline.
- 25356 e 36842: 1,1,0, schermata 70, regolari.
- Banco e nuove mod 5 (36804, 36805): tramogge a 0, probabilmente senza hopper collegati.
- **Ipotesi:** Tramogge vuote o non rispondenti. Le schermate 71, 72 e 73 sembrano indicare quali tramogge mancano. Non confermato.
- **Proposta:** Campo Tiburtino: tramogge 2 e 3 della 33180.
Campo Aprilia: tramoggia 1 della 29597.
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

<a id="cg-020"></a>

### CG-020 · Telemetria assente: 32995 vende ma tace pochi minuti dopo il boot (2o giorno), 21784 muta 2 h dopo l'accensione, DNS KO

- **Area:** pi · **Gravita':** medium · **Visto:** 2026-11-11 → 2026-11-19
- **Macchine:** 24350, 33957, 21784, 24349, 28416, 32995, 37008, 54124120, 11223344
- **Prove:** 32995:
- 18/11: ultimo report alle 09:19, ma 4 transazioni registrate tra le 16:39 e le 21:17 (1 approvata, 1 timeout carta, 2 annullate);
- oggi: reboot alle 09:17 (uptime 136), ultimo report alle 09:18, poi muta (41 min);
- stavolta network LTE, rssi -50.
21784: accesa verso le 07:39, primo report alle 09:39; update_failed DNS e port 443 alle 15:42, 17:14 e 09:39, rientrati.
DNS/port 443 KO rientrati:
- 37008 alle 04:03-04:04;
- 11223344 alle 08:58;
- 54124120 (CG-018).
- **Ipotesi:** Sulla 32995 la rete c'e' (rssi buono, transazioni arrivate) ma il fleet-reporter smette di mandare lo stato dopo il primo report: possibile blocco del servizio, non del modem. Non confermato.
- **Proposta:** Maurizio:
- journal di cgslim-tlm della 32995 (stato del servizio dopo le 09:18);
- report anche con DNS KO e DNS di riserva.
Campo Parma: verificare il router della 32995 solo se il journal non spiega.
- **Gia' noto:** Aggiornamenti bloccati (update_failed, rete/SIM)

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

### CG-028 · Aprilia: raffiche di riavvii in giornata su 26087 (5 in 23 min) e 29597 (4 in 16 min, poi spenta alle 18:22)

- **Area:** campo · **Gravita':** medium · **Visto:** 2026-11-18 → 2026-11-18
- **Macchine:** 26087, 29597
- **Prove:** 26087, 18/11:
- reboot alle 10:21, 10:24, 10:27, 10:39 e 10:44 (uptime 49-60);
- codice 90 alle 10:25, POS in Broken pipe dalle 11:02;
- 15 transazioni, 7 approvate (nessuna carta: 8 tentativi, 5 annullati, 2 timeout, 1 errore).
29597, 18/11:
- hostlink locked alle 17:47 e alle 17:53;
- reboot alle 18:01, 18:04, 18:08 e 18:17 (uptime 58-60);
- 'activate gia' in corso' dalle 18:17 alle 18:47, carta interrotta verso le 18:06;
- offline dalle 18:22, prima delle altre Aprilia (tra le 20:00 e le 23:38);
- oggi tramogge 0,1,1, schermata 72.
Entrambe oggi IDLE e online.
- **Ipotesi:** Interventi o spegnimenti manuali sul posto (forse in occasione della 24254), oppure alimentazione instabile della linea Aprilia. Non confermato.
- **Proposta:** Campo Aprilia: chiedere se ieri c'e' stato un intervento su 26087 e 29597; controllare la tramoggia 1 della 29597.
Maurizio: journal di entrambe, per vedere se i reboot sono comandati o watchdog/power.

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

### CG-016 · Errori seriali: 11223355 fe 990, 37008 ore 327 (+50), 29598 ne 103 al boot, 58555555 ferma a fe 1521 / ne 2020

- **Area:** hardware · **Gravita':** low · **Visto:** 2026-11-06 → 2026-11-19
- **Macchine:** 29598, 33326, 11223355, 58547455, 58555555, 37008, 23718, 28418, 99900055
- **Prove:** Oggi:
- 11223355: fe 990, ne 2, ore 45, con uptime del Pi di 1916 s (CG-018, 9 riavvii in 24 h).
- 37008: ore 327 (ieri 277), brk 2.
- 29598: ne 103 con uptime 11020 s (boot alle 06:46), stesso schema dei giorni scorsi.
- 58555555: fe 1521 e ne 2020 invariati, Pi brk 49.
- 99900055: Pi brk 240 / frame 243 invariati.
- 36804 e 36805: Pi brk 5.
- 23718 e 28418: offline.
- **Ipotesi:** Linee rumorose sulle GMI verdi.
Sulla 11223355 il valore alto si accompagna ai riavvii continui: possibile cavo o connessione del banco. Non confermato.
- **Proposta:** Laboratorio:
- test linea 8.4 e cavo su 11223355 e 58555555.
Campo Aprilia: test linea 8.4 sulla 29598.
Maurizio: contatori come delta giornaliero.
- **Gia' noto:** Aggiornamento firmware GMI (linea disturbata GMI verdi)

<a id="cg-018"></a>

### CG-018 · Banco/lab: 11223355 con 9 riavvii in 24 h, offline 23718, 33326, 28418 e 54124120; 21784 di nuovo online

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-09 → 2026-11-19
- **Macchine:** 11223344, 11223355, 11155520, 1470000, 54124120, 58547455, 58555555, 58888999, 21784, CG-4F2F67B8, 28418, 23718, 33326, 99900055, 99990008
- **Prove:** 11223355, reboot con uptime 47-61 s:
- 18/11: 10:27, 12:05, 12:06, 14:53, 15:22 e 16:10;
- 19/11: 08:53, 09:14 e 09:23;
- repo_healed stale_lock alle 12:07.
Offline:
- 23718: reboot alle 11:36 (uptime 68), poi muta dalle 11:37, mod 0 e schermata 55;
- 33326: dalle 10:50 (CG-024);
- 28418: dal 17/11 alle 03:51;
- 54124120: dalle 06:35, a tratti nella notte, con update_failed (port 443) alle 15:03, 20:17 e 04:45, tutti rientrati; test linea OK alle 11:29.
21784:
- online alle 09:39 (uptime 7191, quindi accesa verso le 07:39 ma muta fino ad allora);
- 1 vendita cash alle 12:46 di ieri.
Pi 4f2f67b8 offline dall'11/11.
- **Ipotesi:** Lavori di laboratorio. I riavvii regolari della 11223355 potrebbero essere spegnimenti manuali o un problema di alimentazione/app. Non confermato.
- **Proposta:** Laboratorio:
- dire cosa si sta facendo sulla 11223355 e, se nessuno la tocca, raccogliere il journal;
- stato di 23718, 28418 e 54124120;
- TID distinti.
Campo: dove si trova la 21784.
- **Gia' noto:** GMI 'muta' / NCG senza bootloader (menu 9.5 ST-Link); golden SD (CG-<seriale>)

<a id="cg-022"></a>

### CG-022 · gmi_hostlink locked a macchina accesa: 29597 (sera del 18/11, con riavvii), 26087, 25357, 36804

- **Area:** pi · **Gravita':** low · **Visto:** 2026-11-12 → 2026-11-19
- **Macchine:** 24349, 25158, 36842, 24338, 28418, 23718, 32996, 25157, 28419, 32995, 29598, 25356, 29597, 58555555, 99999901, 26087, 25357, 36804
- **Prove:** 18/11, blocchi senza reboot:
- 26087 dalle 13:08 alle 13:09;
- 25357 alle 14:49 (stesso minuto);
- 36804 alle 15:02;
- 29597 dalle 17:47 alle 17:48 e dalle 17:53 alle 17:54, poi locked/unlocked continui fino alle 18:22 mischiati a 4 reboot (CG-028).
Tutti gli altri sono coppie al boot.
- **Ipotesi:** Blocchi brevi: la protezione funziona. Sulla 29597 i lock prima dei riavvii fanno pensare a un Pi in difficolta' (main loop o alimentazione) prima di spegnersi.
- **Proposta:** Maurizio: durata del blocco e ultima riga inviata nell'evento; journal della 29597 del 18/11 dalle 17:40 alle 18:25.
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

### CG-027 · Nuove macchine: 16234 (C.C. AURA) in vendita, 36804 e 36805 preparate senza centro

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-18 → 2026-11-19
- **Macchine:** 16234, 36804, 36805
- **Prove:** 16234 (CG-97DCE378):
- first_seen alle 13:44, gmi_mute NCG4.09;
- ST-Link legacy full riuscito al primo tentativo alle 13:49 (3,23 V, 88 KiB/s), fw 4.20.93;
- PI_IP da .97 a .99 alle 14:06 (applicato);
- 8 vendite approvate tra le 14:12 e le 18:11 (3 carte);
- oggi boot alle 07:05, POS IDLE, TID 75709726.
36804:
- first_seen alle 14:22, fw da 4.09 a 4.20.92 alle 14:29 senza ST-Link, poi 4.20.93;
- 7 transazioni, 6 approvate.
36805:
- ST-Link alle 15:06 (lettura 2,6 KiB/s);
- 6 transazioni, 2 approvate.
36804 e 36805: mod 5, uptime ~70200 s (accese tutta la notte), centro null, POS in CG-003.
- **Ipotesi:** Installazione o preparazione regolare. Il primo tentativo ST-Link riuscito su 16234 e 36805 va contro CG-019.
- **Proposta:** Campo/lab:
- centro e TID di 36804 e 36805;
- test linea 8.4 sulle tre;
- dire se 36804 e 36805 sono gia' in un centro (accese di notte).
- **Gia' noto:** GMI 'muta' / NCG senza bootloader (menu 9.5 ST-Link); IP del Raspberry (PI_IP)

## In osservazione

<a id="cg-012"></a>

### CG-012 · Codice 31: terzo giorno senza rifiuti

- **Area:** pos · **Gravita':** medium · **Visto:** 2026-11-04 → 2026-11-15
- **Macchine:** 24254, 28418, 33957, 24866, 29597, 23718, 58888999, 33089, 25356, 24349
- **Prove:** 16, 17 e 18/11: nessun 'codice 31' in flotta.
33957: 14 transazioni su 14 approvate (2 carte).
Unico rifiuto bancario: codice 37 sul tornello di banco 99999901 alle 10:04.
- **Ipotesi:** I rifiuti del 15/11 sono rientrati dopo l'intervento POS sulla 33957.
- **Proposta:** Chiudere domani (20/11) se non ricompare.
- **Gia' noto:** POS: altri errori

<a id="cg-015"></a>

### CG-015 · 33957 (Carpi): secondo giorno senza perdite seriali, 14 vendite su 14; linea ancora DISTURBATA

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-05 → 2026-11-16
- **Macchine:** 33957
- **Prove:** 18/11:
- nessun evento seriale;
- 14 transazioni tra le 16:47 e le 18:34, tutte approvate (2 carte).
Oggi: boot alle 09:00, fe 3, ore 0, POS IDLE.
Ultimo test linea il 05/11: DISTURBATA. Cavo A10LF8Y6.
- **Ipotesi:** Le disconnessioni del 16/11 erano probabilmente dovute a un intervento o a un contatto smosso.
- **Proposta:** Chiudere se resta pulita fino al 21/11.
Campo Carpi: ripetere il test linea 8.4.
- **Gia' noto:** Seriale assente al mattino (eccezione 'Disconnessione hardware seriale'); aggiornamento firmware GMI (linea disturbata)

<a id="cg-026"></a>

### CG-026 · 25254 (Tiburtino): spenta tutto il 18/11, riaccesa oggi alle 07:46

- **Area:** campo · **Gravita':** medium · **Visto:** 2026-11-18 → 2026-11-18
- **Macchine:** 25254
- **Prove:** Ultimo report il 17/11 alle 21:04. Nessun report il 18/11, avviso offline chiuso il 19/11 alle 07:47.
Oggi:
- reboot alle 07:46 (uptime 144);
- mod 12, schermata 70, tramogge 1,1,0, POS IDLE, throttled 0x0, fe 9.
0 transazioni il 17 e il 18/11. Ultima carta approvata il 16/11.
- **Ipotesi:** Spenta a monte (interruttore, linea o timer) per un giorno intero, poi riaccesa. Causa non nota.
- **Proposta:** Campo Tiburtino: chiedere cosa e' successo il 18/11 e fare una vendita di prova.
Chiudere se oggi vende.

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
