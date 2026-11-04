# Registro problemi flotta CGSLIM

Aggiornato dall'agente il 04/11/2026 10:04. Una voce per causa; MHD senza zeri. Generato: non modificare a mano.

## Aperti

### CG-001 · Aggiornamento firmware GMI fallito: 33326 bloccata (errore 98), ora fallisce anche con 4.20.88 e 4.20.90

- **Area:** firmware · **Gravita':** high · **Visto:** 2026-10-30 → 2026-11-04
- **Macchine:** 33326, 26087, 29597, 29598, 28418
- **Prove:** Cronologia di 33326 il 03/11:
- 15:40 UTC: comando REBOOT dalla dashboard, finito 'expired'.
- 15:42: reboot con uptime 44. version_change 176->SLIM-4.20.117, app_down ed eccezione 'RILEVATO LOOP BOOTLOADER (RDY)' con buffer di \x00.
- 15:47: passa alla 184. 15:48: device_key_mismatch.
- 15:50: fw_change 4.20.82->4.20.54.
- 16:08: gmi_flash_failed con CGT-4.20.88.bin, 15 tentativi, 'Timeout ACK al blocco 42624'.
- 23:48: passa alla 185, poi app_down e loop RDY.
- 04/11 00:08: gmi_flash_failed con CGT-4.20.90.bin, 15 tentativi, 'Errore CKS finale!'.
Stato attuale (09:45):
- gmi_blocked; fw 4.20.54, mod 0, screen 29, hopper null; POS DISCONNECTED.
- throttled 0x50005, con sottotensione ADESSO a intermittenza tutta la notte.
- Pi 3 Model B Rev 1.2, uptime 64988 s (avvio alle 15:42 del 03/11).
- Il GIT_BRANCH del 03/11 12:49 e' ancora pending.
Sulle altre beta il loop RDY e' rientrato da solo:
- 29597: 15:07, fw ok alle 15:09.
- 28418: 00:07, fw ok alle 00:14.
- 29598: 07:47, fw ok alle 07:49.
- 26087: 08:31, fw ok alle 08:38.
Tutte sono ora a fw 4.20.90.
- **Ipotesi:** Problema noto del bootloader V2. Su 33326 il flash fallisce a blocchi diversi (44544, 7808, 42624, poi CKS finale) e la sottotensione e' continua: la causa piu' probabile resta l'alimentazione del Pi, non cambiata. La versione 117 e la chiave diversa fanno pensare che ieri sia stata messa una SD con un'immagine vecchia. Questo non agisce sulla causa. Il fw 4.20.54 riportato potrebbe essere letto dal bootloader o da una scrittura parziale: e' da verificare. Il loop RDY breve durante il flash sulle altre beta e' normale e rientra.
- **Proposta:** Campo/hardware:
- Sostituire l'alimentatore del Pi di 33326 prima di qualunque altro tentativo.
- Poi spegnere e riaccendere GMI e Pi.
- Annotare il colore della GMI.
- Se fallisce ancora: flash manuale con ST-Link.
Maurizio:
- Non avviare il flash se throttled ha il bit 0x1, e sospendere i retry automatici dopo un ciclo fallito (sono gia' 45 tentativi, usura flash).
- Registrare throttled e il blocco al momento dell'errore.
- Spiegare il fw 4.20.54.
- Capire perche' il GIT_BRANCH resta pending.
- **Gia' noto:** Aggiornamento firmware GMI che fallisce (gmi_flash_failed, gmi_blocked, loop RDY)

### CG-003 · POS DISCONNECTED dopo timeout get_advanced_config: restano 24350, 24866, 37008 (anche con la 185)

- **Area:** pi · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-04
- **Macchine:** 24350, 24866, 37008, 24254, 26087, 29597, 29598, 36842
- **Prove:** Ancora DISCONNECTED il 04/11 con 'Timeout locale in attesa di get_advanced_config (15.0s)':
- 24350 (176): avvio alle 09:12, 0 tentativi carta.
- 24866 (176, mod5): reboot alle 05:41; 13 vendite cash nelle 24 h, nessuna carta.
- 37008: con SLIM-4.20.185 e fw 4.20.90 dalle 00:10; 6 vendite cash, l'ultima alle 09:37.
'Connessione persa durante get_advanced_config: chiusa dal dispositivo', sempre rientrata entro 15 min:
- 29597 e 29598 (03/11 11:02 UTC);
- 23718 (12:17 UTC);
- 29598 (14:17 UTC);
- 29597 e 24338 (15:17-15:32 UTC);
- 26087 e 29597 (23:02 UTC);
- 32996 e 25158 (04/11 09:17-09:32 UTC).
36842 ora e' IDLE e connessa.
- **Ipotesi:** Problema noto della lettura cashless_info. Su alcuni terminali la lettura va in timeout e il pos-engine resta DISCONNECTED. I rilasci 179-185 non lo risolvono: 37008 resta DISCONNECTED con la 185. Le chiusure della connessione sono frequenti ma innocue.
- **Proposta:** Maurizio:
- Un errore di get_advanced_config non deve lasciare il P95 DISCONNECTED: saltare la lettura e ritentarla con backoff a POS libero.
- Rilasciare su mod12, mod5 e beta.
- Analizzare il log di pos-engine di 37008, che e' su beta e raggiungibile.
Campo: prova con carta reale su 24350 e 24866.
- **Gia' noto:** POS: get_advanced_config

### CG-009 · 24254 (Aprilia) si ferma alle ~19:47 e non si riaccende al mattino (3 volte)

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-02 → 2026-11-04
- **Macchine:** 24254
- **Prove:** Episodi:
- Offline dal 01/11 20:43, rientrata il 02/11 alle 10:45.
- Offline dal 02/11 19:48, rientrata il 03/11 alle 13:00 (reboot con uptime 136, fuori dall'orario del timer).
- Offline dal 03/11 19:47: ora 852 min, non si e' riaccesa stamattina.
Le altre Aprilia hanno trasmesso fino alle 20:30 (24866) e alle 23:15-23:46.
Ultimo payload: uptime 24582 s, throttled 0x50000, POS IDLE connesso, fe=4.
Nelle 24 h:
- 5 transazioni (1 cash approvata alle 17:40);
- 4 tentativi carta: 2 timeout cliente, 2 annullati.
- **Ipotesi:** Si ferma due sere di fila alle 19:47-19:48 e torna solo a mezzogiorno con un riavvio fuori dal timer. Questo fa pensare a un'alimentazione tolta a orario fisso (presa o timer del centro configurati diversamente) e a una riaccensione manuale. In alternativa, l'alimentatore debole (sottotensione osservata). Rete/router meno probabile, perche' sparisce del tutto.
- **Proposta:** Campo Aprilia:
- Verificare a quale presa o timer e' collegata e se va in comune con le altre.
- Chiedere chi la riaccende a mezzogiorno.
- Sostituire l'alimentatore.
- Recuperare journal e dmesg dal 03/11 19:40.

### CG-004 · Seriale GMI assente all'accensione (FTDI non enumerato), cavi lotto BG03E

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-04
- **Macchine:** 25158, 32996
- **Prove:** 04/11, 32996 (cavo BG03ER1N):
- avvio 09:03 (uptime 113), serial_missing not_enumerated ed eccezione 'could not open port /dev/ttyUSB0';
- sul bus solo gli hub 0424:2514, 0424:7800 e ILITEK;
- reboot alle 09:07, serial_recovery alle 09:08.
04/11, 25158 (cavo BG03ES5F):
- avvio 09:22 (uptime 112), stesso quadro;
- reboot alle 09:26, serial_recovery alle 09:27.
Entrambe ora a posto con 1 recovery.
Giorni di fila: 25158 quattro (01-04/11), 32996 tre (02-04/11).
Il cavo di 25158 e' ancora BG03ES5F: lo scambio non e' stato fatto. Nessun'altra macchina ha il problema.
- **Ipotesi:** Problema noto: lotto di cavi FT232R BG03E e/o chip FTDI alimentato a ritroso dalla GMI. Il lotto e' colpito al 100% ogni mattina.
- **Proposta:** Campo Parma: scambiare il cavo della 25158 con uno AL05 e lasciare 32996 come controllo.
Pi: nel prossimo rilascio importante riavvio anticipato (~30-40 s), uhubctl e TX della GMI in high-Z.
- **Gia' noto:** Seriale assente al mattino (serial_missing, not_enumerated)

### CG-005 · Sottotensione del Raspberry (alimentatori/cavi): 33326 continua, 24349 ogni ora, 36842 e 23718 in corso

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-04
- **Macchine:** 33326, 24349, 36842, 23718, 24254, 24350, 24338
- **Prove:** Orari degli avvisi in UTC.
In corso:
- 33326: undervoltage_now a intermittenza dalle 08:32 del 03/11 a stamattina (ultimo aperto alle 08:47); 0x50005.
- 24349: undervoltage_now aperto e chiuso 12 volte il 03/11 (09:17-22:47); oggi 0x50000 a 33 min dall'avvio.
- 36842: 0x50005 aperto alle 08:32 di oggi.
- 23718 (nuova): 0x50005 aperto dal 03/11 10:47, ancora attivo alle 08:47 di oggi.
Sottotensione avvenuta dal boot (0x50000): 24254 (ultimo report), 24350, 24338.
Tutte le altre sono a 0x0.
- **Ipotesi:** Alimentatori o cavi deboli. 33326 (flash fallito) e 24254 (si ferma la sera) ne sono colpite.
- **Proposta:** Hardware/campo, in ordine:
1. Sostituire l'alimentatore di 33326.
2. Poi 24254, 24349 e 36842.
3. Poi 23718 (nuova installazione: verificare l'alimentatore fornito).
4. Infine 24350 e 24338.
- **Gia' noto:** host.throttled 0x50000 (scheda campi); sottotensione sospettata nei flash GMI falliti

### CG-006 · TID POS anomali: 36842 con TID 00000000 (ora online), 24338 e 33326 con TID duplicato

- **Area:** pos · **Gravita':** medium · **Visto:** 2026-10-30 → 2026-11-04
- **Macchine:** 36842, 24338, 33326
- **Prove:** 36842 e' online dal 03/11 e il POS e' IDLE e connesso. La lettura delle 09:00 circa del 04/11 mostra:
- TID 00000000;
- package PYP-SELF2000 01.04.25.03 (RSW006549), SN 58551425;
- nessun acquirer.
Nessuna transazione carta nelle 24 h.
24338: TID 97942485 (SN 58795528) letto oggi, stesso package 01.04.25.03; nessuna carta nelle 24 h.
33326: POS non leggibile (GMI bloccata).
- **Ipotesi:** Il terminale della 36842 non e' parametrizzato: senza TID e senza acquirer la carta non puo' funzionare. Il TID duplicato e' una causa nota di errore 48.
- **Proposta:** Hardware/POS:
- Far parametrizzare oggi il terminale della 36842 con il TID di produzione.
- Assegnare TID distinti a 24338 e 33326.
- **Gia' noto:** POS: altri errori (errore 48, TID duplicato su 24338)

### CG-007 · Tramogge 0,0,0 e schermata 73 dopo l'avvio su macchine Parma MOD12 (varia da giorno a giorno)

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-01 → 2026-11-04
- **Macchine:** 24350, 28417, 32996, 25158, 37008
- **Prove:** 04/11 alle 09:49-09:58:
- hopper ['0','0','0'] e screen 73 su 24350 (uptime 2908), 28417 (uptime 4706) e 32996 (uptime 2827);
- 25158 e 37008 sono ora a ['1','0','0'] con screen 71, come le altre MOD12.
Vendite cash nelle 24 h: 28417 2, 32996 3, 25158 2. 24350 nessuna.
- **Ipotesi:** Lo stato cambia macchina ogni giorno e non impedisce le vendite. Probabilmente e' uno stato legittimo legato al livello della tramoggia 1 o a una schermata specifica. Il significato di screen 73 non e' nella scheda.
- **Proposta:** Maurizio: chiarire cosa indica screen 73 e quando la GMI manda #HPS 0,0,0.
Campo Parma: controllare il livello della tramoggia 1 di 24350.

### CG-011 · machine_registry incompleto (centro null) e chiave macchina non corrispondente su 33326

- **Area:** dashboard · **Gravita':** low · **Visto:** 2026-11-04 → 2026-11-04
- **Macchine:** 23718, 24338, 28418, 33326, 37008
- **Prove:** Centro null in machine_registry per:
- 23718: nuova, first_seen 03/11 11:44, hostname CG-NFC-BETA, branch mod5 ma mod 4;
- 24338, 28418, 33326 e 37008.
33326:
- device_key_mismatch dalle 15:48 del 03/11, comparso dopo il reboot con SLIM-4.20.117;
- avviso aperto dalle 15:02 UTC, ma i report arrivano.
GIT_BRANCH pending:
- sul device 000000006118315b, quello del 03/11 20:46 (applicato quello delle 12:49): MHD non presente nei dati;
- su 33326 dalle 12:49.
- **Ipotesi:** Registro non aggiornato per le macchine beta e per la nuova installazione. La chiave diversa su 33326 e' probabilmente dovuta alla SD sostituita o reimmaginata ieri.
- **Proposta:** Dashboard/Maurizio:
- Completare il centro delle 5 macchine.
- Ri-registrare la chiave di 33326 dopo aver verificato che la SD e' legittima.
- Identificare il device 000000006118315b.
- Chiarire mod 4 su 23718.

## In osservazione

### CG-010 · 37008 offline dal 02/11 19:30 al 03/11 15:01: tornata online

- **Area:** campo · **Gravita':** medium · **Visto:** 2026-11-03 → 2026-11-03
- **Macchine:** 37008
- **Prove:** Rientro il 03/11:
- Reboot alle 15:01 con uptime 59: riaccensione, non ripresa della rete.
- Poi 183 (15:09), fw 4.20.88 (15:12), 184 (22:04), 185 e fw 4.20.90 (04/11 00:10-00:13).
Stato attuale:
- Online, uptime 68337 s: non si e' spenta stanotte.
- throttled 0x0, hopper 1,0,0, screen 71.
- 6 vendite cash, l'ultima alle 09:37.
- POS ancora DISCONNECTED (CG-003).
Centro ancora null.
- **Ipotesi:** Il ritorno con uptime 59 indica che la macchina era senza corrente o bloccata ed e' stata riaccesa, probabilmente a mano. Causa non nota.
- **Proposta:** Monitorare. Chiudere se resta online fino a venerdi'.
Registro del centro in CG-011.

## Risolti

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

### CG-008 · Branch riportato 'parma' ma servizio gitpuller@beta su 3 macchine Aprilia

- **Area:** dashboard · **Gravita':** low · **Visto:** 2026-11-01 → 2026-11-01
- **Macchine:** 26087, 29597, 29598
- **Prove:** Il 02/11 dalle 16:35 e' stato applicato il provisioning GIT_BRANCH. Oggi 26087, 29597 e 29598 riportano branch 'beta', servizio gitpuller@beta, git_commit ea89cae e SLIM-4.20.179. Il branch riportato e il servizio coincidono.
- **Ipotesi:** Disallineamento sistemato dal provisioning del branch.
- **Proposta:** Nessuna azione.
