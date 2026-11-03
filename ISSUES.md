# Registro problemi flotta CGSLIM

Aggiornato dall'agente il 03/11/2026 10:04. Una voce per causa; MHD senza zeri. Generato: non modificare a mano.

## Aperti

### CG-001 · Aggiornamento firmware GMI fallito: 33326 bloccata (errore 98) da 01/11

- **Area:** firmware · **Gravita':** high · **Visto:** 2026-10-30 → 2026-11-03
- **Macchine:** 33326, 26087, 29597
- **Prove:** 33326, report delle 09:48 del 03/11:
- gmi_blocked ancora attivo dal 01/11 09:36: 15 tentativi con CGT-4.20.84.bin, 'Timeout ACK al blocco 7808'.
- Fw 4.20.82, mod 0, screen 29, hopper e contatori GMI null.
- Uptime 337340 s (~94 h): nessun riavvio e nessun intervento.
Sottotensione:
- undervoltage_now aperto e chiuso piu' volte nella notte (02/11 18:32-21:02, 21:17-00:02, 00:47-04:32, 05:02-08:17; aperto alle 09:32 ora locale).
- Throttled 0x50000 nell'ultimo payload.
Il provisioning GIT_BRANCH del 02/11 16:35 su 33326 e' rimasto 'delivered' e non e' stato applicato (le altre macchine lo hanno applicato in 4-13 min).
Il 30/10 era gia' fallito il flash di CGT-4.20.83.bin (blocco 44544).
26087 e 29597: dopo il loop RDY del 01/11 restano a fw 4.20.84 e funzionano.
- **Ipotesi:** Problema noto del bootloader V2. Il flash fallisce a blocchi diversi e c'e' una sottotensione intermittente continua, quindi la causa piu' probabile e' l'alimentazione del Pi (Pi 3 Model B Rev 1.2) o un disturbo di linea. Il colore della GMI non e' noto. Il cambio branch non applicato puo' dipendere dallo stato bloccato, ma e' solo un'ipotesi.
- **Proposta:** Campo/hardware:
- Sostituire l'alimentatore del Pi di 33326.
- Spegnere e riaccendere GMI e Pi.
- Annotare il colore della GMI.
- Se fallisce di nuovo: flash manuale con ST-Link.
Pi:
- Rimandare il flash della GMI quando il bit 0x1 di throttled e' attivo.
- Registrare throttled e il blocco al momento del Timeout ACK.
- Verificare perche' il GIT_BRANCH resta 'delivered'.
Dashboard: il centro di 33326 e' null, va completato.
- **Gia' noto:** Aggiornamento firmware GMI che fallisce (gmi_flash_failed, gmi_blocked, loop RDY)

### CG-002 · 36842 offline dal 31/10 20:21 e non riaccesa (terzo mattino)

- **Area:** campo · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-03
- **Macchine:** 36842
- **Prove:** Stato attuale:
- Ultimo report 31/10 20:21, offline da 3698 min alle 10:00 del 03/11.
- Le altre 9 Parma si sono riaccese oggi tra le 08:26 (25157) e le 09:27 (25158).
Ultimo payload:
- uptime 140 s;
- throttled 0x50005;
- GMI fe=138 (le altre Parma 3-6);
- SLIM-4.20.172, fw 4.20.83;
- TID 00000000;
- p95_error: timeout get_advanced_config.
Nessun intervento risulta fatto.
- **Ipotesi:** Alimentazione insufficiente (sottotensione in corso ed errori di frame lato GMI), oppure un guasto di rete o del router. I dati non permettono di distinguere.
- **Proposta:** Campo Parma oggi, senza rimandare ancora:
- Verificare se la macchina e' accesa e cosa mostra lo schermo.
- Controllare alimentatore, cavo del Pi e router.
- Recuperare journal e dmesg dal 31/10 20:20.
Al ritorno: verificare l'aggiornamento a SLIM-4.20.176 e fw 4.20.84, e la parametrizzazione del TID (CG-006).

### CG-003 · POS DISCONNECTED dopo timeout get_advanced_config: rientrato su 3 Aprilia, resta su 24350, 24866, 37008

- **Area:** pi · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-03
- **Macchine:** 24350, 24866, 37008, 24254, 26087, 29597, 29598, 36842
- **Prove:** Stato del POS il 03/11 alle 09:46-09:57.
Ancora DISCONNECTED con 'Timeout locale in attesa di get_advanced_config (15.0s)', senza dati p95:
- 24350 (Parma, 176): avvio alle 09:11.
- 24866 (Aprilia, 176, mod5, mod 2): nessun tentativo carta nelle 24 h, 25 vendite contanti.
- 37008 (179 dalle 16:44 del 02/11): ultimo report 19:30, 6 tentativi carta con 0 approvati (4 annullati, 2 timeout).
Tornati IDLE, connessi e con p95 letto:
- 29597: 3 carte approvate, l'ultima alle 09:38 del 03/11.
- 29598: 3 approvate.
- 26087: 1 approvata, ~12:10 del 02/11.
- 24254: p95 letto ~10:55 del 02/11, ma 0 approvate su 5.
Il 02/11 'POS non attivo (codice 90)' e' comparso su 24254 (10:56), 29597 (11:03), 29598 (11:11) e 26087 (11:19); poco dopo sono arrivate le prime carte approvate.
Errori 'Connessione persa durante get_advanced_config: Connessione chiusa dal dispositivo', tutti rientrati entro 15 min:
- 29598, 24338 e 29597 alle 17:02 del 02/11, subito dopo il passaggio alla 179;
- 25158 alle 09:32 del 03/11.
24349 e le altre Parma sono connesse.
- **Ipotesi:** Problema noto della lettura cashless_info (v.171+). Su alcuni terminali la lettura non risponde e il pos-engine resta DISCONNECTED. La sequenza codice 90 seguita da carte ok suggerisce che i terminali di Aprilia siano stati attivati o riparametrizzati il 02/11 verso le 11:00 (forse un intervento, 24254 riavviata alle 10:45): la causa potrebbe quindi essere in parte lato terminale. Non e' verificato. La 4.20.179 da sola non risolve: 37008 e' rimasta DISCONNECTED.
- **Proposta:** Maurizio:
- In core/cashless_info.py, un errore di get_advanced_config non deve lasciare il P95 DISCONNECTED. Saltare la lettura e ritentarla con backoff a POS libero; poi rilasciare su mod12, mod5 e beta2.
- Analizzare i log di pos-engine di 24350 o 24866.
Campo:
- Chiedere ai tecnici di Aprilia cosa e' stato fatto il 02/11 verso le 10:45-11:20.
- Verificare se i POS di 24350 e 24866 sono attivi e parametrizzati (prova con carta reale).
- **Gia' noto:** POS: get_advanced_config

### CG-009 · 24254 (Aprilia) si ferma la sera e non si riaccende al mattino (2 volte)

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-02 → 2026-11-03
- **Macchine:** 24254
- **Prove:** Primo episodio:
- Offline dal 01/11 20:43.
- Rientrata il 02/11 alle 10:45 con un reboot (uptime 138 s), non con l'accensione a timer: le altre Aprilia si erano riaccese alle 05:42-07:30.
Secondo episodio:
- Il 02/11 alle 12:32 sottotensione in corso (0x50005).
- Ultimo report alle 19:48, ora offline da 851 min. Le altre Aprilia hanno trasmesso fino alle 20:24 (24866) e alle 23:16-23:47.
- Stamattina non si e' riaccesa.
Ultimo payload: uptime 32728 s, throttled 0x50000, GMI fe=5, POS IDLE connesso, LTE rssi -66.
02/11: 5 tentativi carta, 0 approvati (2 timeout, 1 codice 90, 2 annullati), ultimo alle 16:35.
- **Ipotesi:** Lo schema si ripete: si ferma in anticipo la sera e non riparte da sola. Con la sottotensione in corso osservata in giornata, la causa piu' probabile e' l'alimentatore (il Pi si blocca o non riparte). Restano possibili rete/router o un blocco del Pi.
- **Proposta:** Campo Aprilia:
- Sostituire l'alimentatore del Pi.
- Verificare cosa mostra lo schermo e lo stato del router.
- Recuperare journal e dmesg dal 02/11 19:45.
Chiedere se il riavvio delle 10:45 del 02/11 e' stato manuale.

### CG-010 · 37008 offline dal 02/11 19:30, non riapparsa (centro non registrato)

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-03 → 2026-11-03
- **Macchine:** 37008
- **Prove:** Ultimo report 02/11 19:30, offline da 869 min alle 10:00; ultima transazione registrata alle 19:39.
Ultimo payload:
- uptime 103848 s (accesa dal 01/11 ~14:40): non si spegne la notte;
- SLIM-4.20.179 (dalle 16:44 del 02/11), fw 4.20.84, branch beta;
- throttled 0x0, LTE rssi -71;
- GMI ore=10;
- POS DISCONNECTED (timeout get_advanced_config);
- screen 73, idle false, hopper 0,0,0.
Nelle 24 h: 35 transazioni, 29 cash approvate; carte 0 su 6.
Il centro in machine_registry e' null.
- **Ipotesi:** Non e' lo spegnimento notturno, perche' la macchina restava accesa anche di notte. Le cause possibili sono rete/LTE, spegnimento del centro, blocco del Pi dopo l'aggiornamento a 179 (avvenuto 3 ore prima) o mancanza di corrente. Non c'e' sottotensione. Dai dati non si distingue.
- **Proposta:** Maurizio/dashboard: identificare il centro di 37008 e completare machine_registry.
Campo: verificare se e' accesa, cosa mostra lo schermo e il router; recuperare journal dal 02/11 19:25.

### CG-004 · Seriale GMI assente all'accensione (FTDI non enumerato), cavi lotto BG03E

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-03
- **Macchine:** 25158, 32996
- **Prove:** 03/11, 32996 (cavo BG03ER1N):
- avvio 09:03 (uptime 111 s), serial_missing not_enumerated ed eccezione 'could not open port /dev/ttyUSB0';
- sul bus solo gli hub 0424:2514, la LAN 0424:7800 e il touch ILITEK;
- reboot alle 09:07 (uptime 59), serial_recovery alle 09:08.
03/11, 25158 (cavo BG03ES5F):
- stesso quadro all'avvio delle 09:22 (uptime 108);
- reboot alle 09:27 (uptime 60), serial_recovery alle 09:28.
Entrambe sono ora a posto, con 1 recovery su 2.
25158 ha il problema per il terzo giorno di fila (01, 02 e 03/11), 32996 per il secondo (02 e 03/11).
Il cavo di 25158 e' ancora BG03ES5F: lo scambio non e' stato fatto. Nessun'altra macchina ce l'ha.
- **Ipotesi:** Problema noto: lotto di cavi FT232R BG03E difettoso, e/o chip FTDI alimentato a ritroso dalla GMI. Il lotto e' colpito al 100% tutti i giorni.
- **Proposta:** Campo Parma: scambiare oggi il cavo della 25158 con uno AL05 e lasciare 32996 come controllo.
Pi: nel prossimo rilascio importante riavvio anticipato (~30-40 s), uhubctl e TX della GMI in high-Z.
- **Gia' noto:** Seriale assente al mattino (serial_missing, not_enumerated)

### CG-005 · Sottotensione del Raspberry (alimentatori/cavi): 33326 continua, 24349 e 24254 intermittenti

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-03
- **Macchine:** 33326, 36842, 24349, 24254, 24350, 24338
- **Prove:** Orari in ora locale.
- 33326: sottotensione in corso (0x50005) a intermittenza per tutta la notte; aperta di nuovo alle 09:32 del 03/11.
- 24349: 0xd0005 alle 16:17, 17:02 e 19:47 del 02/11; oggi 0x50000 a 38 min dall'avvio delle 09:18.
- 24254: 0x50005 alle 12:32 del 02/11, poi offline dalle 19:48.
- 24350: 0xd0000 il 02/11; oggi 0x50000 a 48 min dall'avvio.
- 24338: 0x50000 (uptime ~93 h).
- 36842: 0x50005 nell'ultimo report.
- 26087: 0x0 per il secondo giorno, quindi tolta dalla lista.
Le altre macchine sono a 0x0.
- **Ipotesi:** Alimentatori o cavi deboli. Tre delle quattro macchine ferme o bloccate (33326, 36842, 24254) hanno avuto sottotensione in corso.
- **Proposta:** Hardware/campo, in ordine:
1. Sostituire gli alimentatori di 33326, 36842 e 24254.
2. Poi 24349 (sottotensione attiva in giornata).
3. Infine 24350 e 24338.
- **Gia' noto:** host.throttled 0x50000 (scheda campi); sottotensione sospettata nei flash GMI falliti

### CG-006 · TID POS anomali: 36842 senza TID, 24338 e 33326 con TID duplicato

- **Area:** pos · **Gravita':** medium · **Visto:** 2026-10-30 → 2026-11-01
- **Macchine:** 36842, 24338, 33326
- **Prove:** 36842 (Parma, produzione): TID 00000000, package PYP-SELF2000 01.04.25.03 (le altre Parma hanno 01.04.02), SN 58551425; lettura del 31/10 00:21; nessuna transazione carta nelle 24 h. 24338 e 33326 riportano lo stesso TID 97942485 su terminali diversi (SN 58795528 e 53818418). 24338: ultimo errore 48 il 30/10 alle 13:21; il POS di 33326 era attivo e letto il 30/10 alle 14:06.
- **Ipotesi:** Il terminale della 36842 non e' parametrizzato (forse dopo un cambio POS o un aggiornamento del package): la carta non puo' funzionare. Il TID duplicato e' una causa nota di errore 48.
- **Proposta:** Hardware/POS: far parametrizzare la 36842 con il TID di produzione; assegnare TID distinti a 24338 e 33326.
- **Gia' noto:** POS: altri errori (errore 48, TID duplicato su 24338)

### CG-007 · Tramogge 0,0,0 e schermata 73 dopo l'avvio (25158, 24350, 37008): non blocca le vendite

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-01 → 2026-11-03
- **Macchine:** 25158, 24350, 37008
- **Prove:** 03/11, report delle 09:57-09:58:
- 25158 e 24350 hanno di nuovo hopper ['0','0','0'] e screen 73.
- Le altre Parma MOD12 hanno ['1','0','0'] e screen 71.
- 37008 era nello stesso stato nell'ultimo report (19:30 del 02/11, idle false).
Nelle 24 h le tre macchine hanno comunque venduto:
- 25158: 3 vendite (2 con carta approvata), dalle 12:07 alle 14:51;
- 24350: 1 vendita cash alle 18:48;
- 37008: 29 vendite cash.
- **Ipotesi:** Non e' legato al recupero seriale (24350 e 37008 non lo hanno avuto). Visto che le vendite avvengono, e' probabilmente uno stato legittimo: tramoggia 1 vuota o bassa, oppure una schermata diversa. Il significato di screen 73 non e' nella scheda.
- **Proposta:** Maurizio: chiarire cosa indica screen 73 e quando la GMI manda #HPS 0,0,0.
Campo Parma: controllare il livello della tramoggia 1 di 24350 e 25158 durante la visita.

## Risolti

### CG-008 · Branch riportato 'parma' ma servizio gitpuller@beta su 3 macchine Aprilia

- **Area:** dashboard · **Gravita':** low · **Visto:** 2026-11-01 → 2026-11-01
- **Macchine:** 26087, 29597, 29598
- **Prove:** Il 02/11 dalle 16:35 e' stato applicato il provisioning GIT_BRANCH. Oggi 26087, 29597 e 29598 riportano branch 'beta', servizio gitpuller@beta, git_commit ea89cae e SLIM-4.20.179. Il branch riportato e il servizio coincidono.
- **Ipotesi:** Disallineamento sistemato dal provisioning del branch.
- **Proposta:** Nessuna azione.
