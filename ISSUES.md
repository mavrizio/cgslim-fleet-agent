# Registro problemi flotta CGSLIM

Aggiornato dall'agente il 15/11/2026 10:03. Una voce per causa; MHD senza zeri. Generato: non modificare a mano.

## Aperti

<a id="cg-003"></a>

### CG-003 · POS DISCONNECTED dopo timeout get_advanced_config: ora 5 macchine con la 24866 (Aprilia); la carta resta offerta e fallisce

- **Area:** pi · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-15
- **Macchine:** 24350, 37008, 33326, 23718, 24866, 11223344, 11155520, 11223355, 1470000, 54124120, 58547455, 58555555, 58888999, 33957, 36842, 24254, 32996, 24338, 28418, 25254, 21784, 25158
- **Prove:** Avviso 'POS in errore su 5 macchine' (era 4).
Online e DISCONNECTED con 'Timeout locale get_advanced_config':
- 24350 (199): ieri 23 transazioni, 7 con carta e 0 riuscite (4 'nessuna carta entro il tempo', 3 annullate); nessun dato P95 letto.
- 37008 (199): 20 vendite, tutte cash.
- 33326 (205): nessuna transazione.
- 23718 (205): nessuna transazione.
- 24866 (200, Aprilia), nuova: DISCONNECTED dopo il boot delle 05:41. Ieri 4 carte approvate, l'ultima alle 12:18. Ultima lettura P95 il 13/11 alle 20:31. Oggi 1 vendita alle 09:53.
'Connessione persa durante get_advanced_config' dopo l'avvio, rientrati: 25254 alle 07:47 (chiuso alle 08:02), 24254 alle 09:47 (ora IDLE).
Banco ancora offline dal 13/11.
- **Ipotesi:** Dopo un timeout della lettura cashless_info, il pos-engine resta DISCONNECTED senza ritentare; le release 199-205 non cambiano nulla.
La UI continua a offrire la carta, che finisce in timeout: le 'nessuna carta entro il tempo' della 24350 sono probabilmente POS muto, non clienti.
- **Proposta:** Maurizio:
- un errore di get_advanced_config non deve bloccare il P95: saltare la lettura e ritentarla con backoff;
- nascondere la carta a POS DISCONNECTED;
- log pos-engine della 24866 dalle 05:41.
Campo Parma: spegnere e riaccendere il POS della 24350 e provare una carta.
Campo Aprilia: idem sulla 24866.
Dashboard: escludere i Pi di banco dall'avviso.
- **Gia' noto:** POS: get_advanced_config

<a id="cg-009"></a>

### CG-009 · 24254 (Aprilia): accesa tardi ogni giorno (09:46 oggi), nessuna vendita ieri, sottotensione continua

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-02 → 2026-11-15
- **Macchine:** 24254
- **Prove:** 14/11:
- online dalle 09:50 alle 20:54 (ultimo report);
- 15 episodi di sottotensione ADESSO;
- nessuna transazione nelle 24 h (non compare nell'elenco vendite).
15/11:
- 09:46: reboot (uptime 139), mentre le altre Aprilia si sono accese tra le 05:41 (24866) e le 07:30 (26087);
- 09:47: 0x50005 e 'Connessione persa get_advanced_config', poi POS IDLE.
Ultima carta approvata il 05/11.
- **Ipotesi:** Due cose insieme, non confermate:
1. Linea o timer diverso dalle altre Aprilia: accensione verso le 09:50, spegnimento serale variabile (19:47-20:54).
2. Alimentatore del Pi debole.
Con zero vendite potrebbe anche essere poco visibile o fuori uso per il cliente.
- **Proposta:** Campo Aprilia:
- verificare presa, linea e timer (confronto con 24866/26087);
- sostituire l'alimentatore del Pi;
- controllare che lo schermo sia funzionante e fare una vendita di prova con carta.
Maurizio: journal e dmesg del 14/11.

<a id="cg-004"></a>

### CG-004 · Seriale GMI assente all'accensione (FTDI non enumerato), cavi lotto BG03E: 25158 e 32996 anche oggi

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-15
- **Macchine:** 25158, 32996
- **Prove:** 15/11:
- 32996 (BG03ER1N): alle 09:04 reboot (uptime 113), 'could not open port /dev/ttyUSB0', serial_missing not_enumerated (sul bus solo hub, ethernet e ILITEK); alle 09:08 reboot di recovery (uptime 50); alle 09:09 serial_recovery.
- 25158 (BG03ES5F): alle 09:22 reboot (uptime 110), stessa eccezione e serial_missing; alle 09:26 reboot di recovery (uptime 50); alle 09:27 serial_recovery.
La 25158 e' a 9 mattine su 10 (06 e dall'08 al 15/11).
Vendite 24 h: 25158 38 (30 approvate), 32996 26 (22 approvate).
Cavo della 25158 non ancora scambiato.
- **Ipotesi:** Lotto FT232R BG03E e/o alimentazione a ritroso dalla GMI. Il recovery funziona e costa circa 5 minuti al mattino.
- **Proposta:** Campo Parma: scambiare il cavo della 25158 con uno AL05 e lasciare la 32996 come controllo.
Pi: nel prossimo rilascio riavvio anticipato (~30-40 s), uhubctl e TX della GMI in high-Z.
- **Gia' noto:** Seriale assente al mattino (serial_missing, not_enumerated)

<a id="cg-005"></a>

### CG-005 · Sottotensione del Raspberry: 24254 a episodi tutto il giorno (15 ieri), 23718 fissa, 24349/24350/24338 dal boot

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-15
- **Macchine:** 24349, 23718, 24254, 24350, 24338
- **Prove:** Avvisi undervoltage_now del 14/11, orari locali:
- 24254: 15 episodi tra le 10:02 e le 19:47. Oggi 0x50005 alle 09:47, subito dopo il boot delle 09:46; ora 0x50000.
- 24349: episodi alle 09:32 e dalle 10:17 alle 10:47, poi solo 0x50000. Oggi 0x50000 dopo il boot delle 09:17.
Stato attuale:
- 23718: 0x50005 fissa, avviso aperto dal 03/11 (uptime ~45 h);
- 24350: 0x50000, ieri sera 0xd0000 (anche limite termico soft);
- 24338: 0x50000.
- **Ipotesi:** Alimentatori o cavi deboli. La 24254 e' la piu' grave ed e' probabilmente legata anche agli orari anomali (CG-009).
- **Proposta:** Hardware/campo, in ordine:
1. 24254, insieme a CG-009;
2. 24349;
3. 23718;
4. 24350 e 24338.
Sostituire alimentatore e cavo del Pi.
- **Gia' noto:** host.throttled 0x50000 (scheda campi); sottotensione sospettata nei flash GMI falliti

<a id="cg-006"></a>

### CG-006 · TID di prova 97942484 su 8 terminali (23718 e banco); 36842 ora parametrizzata

- **Area:** pos · **Gravita':** medium · **Visto:** 2026-10-30 → 2026-11-13
- **Macchine:** 23718, 24338, 28418, 11223344, 11223355, 1470000, 54124120, 58547455, 58555555, 58888999
- **Prove:** 36842 risolta:
- ora TID 92868616, acquirer Mastercard, BANCOMAT e VISA, package 01.04.25.03;
- 12/11: 17 transazioni, 9 approvate; card_activity ok 4, ultima carta approvata alle 18:49.
TID 97942484 ancora su 23718, 1470000, 11223344, 11223355, 54124120, 58547455, 58555555 e 58888999. 1470000 e 58888999 sono senza acquirer letti.
Altri TID di prova: 24338 97942485, 28418 97942488.
Nessun errore codice 20 o 37 nelle 24 h (sul banco nessun pagamento carta).
- **Ipotesi:** Con lo stesso TID su piu' terminali sono probabili errori 48 e rifiuti (caso noto della 24338).
- **Proposta:** Hardware/POS: assegnare TID distinti ai terminali di banco prima della spedizione; 23718 da parametrizzare se va in servizio.
Maurizio: nascondere la carta con TID 00000000 o senza acquirer.
- **Gia' noto:** POS: altri errori (errore 48, TID duplicato su 24338)

<a id="cg-012"></a>

### CG-012 · Rifiuti codice 31 a coppie: 24349 (10) e 33957 (5); corsa POS all'avvio senza nuovi casi

- **Area:** pos · **Gravita':** medium · **Visto:** 2026-11-04 → 2026-11-14
- **Macchine:** 24254, 28418, 33957, 24866, 29597, 23718, 58888999, 33089, 25356, 24349
- **Prove:** 14/11, rifiuti 'codice 31':
- 24349: 10 rifiuti, 1 alle 10:00, 2 alle 13:28, 1 alle 14:24, 2 alle 15:41, 2 alle 16:31, 2 alle 16:34. Su 25 tentativi carta: 3 approvate, 9 annullate, 3 timeout.
- 33957: 5 rifiuti tra le 11:22 e le 11:25. 27 tentativi carta e 11 transazioni approvate in totale.
Alle 16:31 e alle 16:34 la vicina 24350 (POS DISCONNECTED) ha due 'nessuna carta entro il tempo' negli stessi minuti.
Altri esiti:
- 25158: 1 'codice 04' alle 17:03;
- 29597 alle 17:04: 'esito H scartato: STAN gia' registrato' (protezione dal doppio esito funzionante).
Nessun codice 90, 'activate gia' in corso' o Broken pipe nelle 24 h.
- **Ipotesi:** Il codice 31 arriva dalla banca o dall'acquirer per un tipo di carta non instradato (circuito o emittente non supportato), ritentata dallo stesso cliente, forse anche su piu' macchine. Non e' legato al recupero del POS. Non confermato.
- **Proposta:** Maurizio/Ingenico:
- chiedere all'acquirer il significato del codice 31 e il BIN o circuito delle carte rifiutate;
- valutare un messaggio al cliente 'carta non accettata, usa un'altra carta o contanti'.
Maurizio: carta disabilitata finche' il POS non e' IDLE e cashless_info non ha finito.
- **Gia' noto:** POS: altri errori; POS: get_advanced_config (operazione gia' in corso)

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

### CG-020 · Telemetria assente per ore con DNS KO mentre la macchina vende: 24349, 24350, 33957, 21784; 28416 non tornata stamattina

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-11 → 2026-11-15
- **Macchine:** 24350, 33957, 21784, 24349, 28416
- **Prove:** 14/11, buchi di telemetria con update_failed 'Could not resolve host' (orari locali):
- 24349: ultimo report alle 10:26, update_recovered alle 17:08. Intanto 44 transazioni (10:00-23:15). RSSI -48.
- 24350: ultimo report alle 09:27, update_recovered alle 18:43. 23 transazioni (10:01-23:09). RSSI -49.
- 33957: ultimo report alle 10:00, update_recovered alle 15:42. 33 transazioni (10:08-19:18).
- 21784: pause dopo le 15:07, 19:03 e 20:06; offline dalle 20:53.
Stamattina:
- 24350: avvio alle 06:11 (uptime 140), report alle 06:12, poi muta fino a un secondo avvio completo alle 09:12 (uptime 141).
- Ancora offline alle 10:00: 33957 (dalle 20:28), 21784 (dalle 20:53) e 28416 (Parma, dalle 21:49; ieri 19 transazioni fino alle 19:41), mentre le altre Parma sono tornate tra le 08:26 e le 09:27.
- **Ipotesi:** Il DNS dell'operatore o del router cade per ore. Il segnale e' buono (-48/-49 dBm a Parma), quindi non e' copertura. Il fleet-reporter non manda nulla finche' il DNS non torna; le transazioni arrivano in coda.
Per 28416, 33957 e 21784 di stamattina non si sa se sono spente o solo senza rete.
Il doppio avvio della 24350 fa pensare a un'interruzione di corrente. Non confermato.
- **Proposta:** Maurizio:
- DNS di riserva (es. 1.1.1.1/8.8.8.8) sul Pi o sul router;
- report del fleet-reporter anche quando il DNS fallisce, con il motivo;
- verificare i timestamp di inserimento delle transazioni.
Campo:
- Parma: router e SIM di 24349 e 24350; verificare se la 28416 e' accesa;
- Carpi: verificare se la 33957 e' accesa, router e SIM.
- **Gia' noto:** Aggiornamenti bloccati (update_failed, rete/SIM)

<a id="cg-011"></a>

### CG-011 · Dashboard: centro null su 6 macchine, Pi di banco nel conteggio (chiave 25355 rientrata)

- **Area:** dashboard · **Gravita':** low · **Visto:** 2026-11-04 → 2026-11-14
- **Macchine:** 21784, 23718, 24338, 28418, 33326, 37008
- **Prove:** Chiavi:
- 25355: device_key_enrolled ieri alle 11:15, avviso mismatch chiuso alle 11:17, oggi device_key_status 'ok';
- 23718: device_key_enrolled alle 11:24.
Centro null: 21784, 23718, 24338, 28418, 33326 e 37008.
Conteggio flotta 38: comprende 8 Pi di banco e il Pi senza MHD 4f2f67b8 (device_key 'missing').
- **Ipotesi:** Il mismatch nasceva dallo scambio o dalla clonazione delle SD durante l'installazione. Il re-enroll l'ha sistemato.
- **Proposta:** Dashboard/Maurizio:
- assegnare il centro (o 'banco');
- escludere i device di banco da conteggio e avvisi.
- **Gia' noto:** Profilo display auto / golden SD

<a id="cg-014"></a>

### CG-014 · MOD non documentate: 23718 mod 4, 33180 mod 2 ora con tramogge 0,0,0, 28419 riporta mod 2

- **Area:** firmware · **Gravita':** low · **Visto:** 2026-11-05 → 2026-11-15
- **Macchine:** 23718, 33180, 28419
- **Prove:** 23718 (beta, 205, fw 4.20.98): mod 4, schermata 21, tramogge 0,1,1, POS DISCONNECTED, nessuna vendita nelle 24 h.
33180:
- mod 2, schermata 41 (ieri 40), tramogge 0,0,0 (ieri 1,0,0);
- chl_mode 0, pos-engine inactive, MDB 10 e 60 con init false;
- 18 vendite cash ieri fino alle 17:55, boot oggi alle 08:47.
28419 (Parma): mod 2, schermata 70, tramogge 1,1,0, P95 IDLE, 16 transazioni ieri (13 approvate).
- **Ipotesi:** 23718 e' una macchina di prova. 33180 e' configurata per il solo contante; le tramogge a 0 potrebbero indicare un #HPS non ancora arrivato o una tramoggia vuota.
Sul valore mod 2 della 28419, con schermate MOD12, non si sa se e' un cambio reale o un campo letto male. Non confermato.
- **Proposta:** Maurizio:
- chiarire le MOD 1, 2 e 4 nella scheda;
- verificare da dove arriva mod=2 sulla 28419.
Campo Tiburtino: controllare le tramogge della 33180 e confermare che deve essere solo contante.

<a id="cg-015"></a>

### CG-015 · Nuova installazione 33957 (Carpi): GMI NCG4.09 senza bootloader programmata via ST-Link, linea seriale DISTURBATA

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-05 → 2026-11-06
- **Macchine:** 33957
- **Prove:** 05/11, installazione:
- 10:47: first_seen (hostname CG-25AA9765, golden).
- 10:48: exception 'GMI con firmware NCG4.09 senza bootloader' e gmi_mute no_bootloader.
- 10:50: stlink_program 4.20.90 ok, bootloader V2.
- 10:52: fw_change 4.09->4.20.90.
Linktest:
- 11:01 annullato;
- 11:02 DISTURBATA, GMI rossa, 12 errori uart verso la GMI su 24576, nessun errore dalla GMI.
gmi_hostlink locked/unlocked 3 volte tra le 11:26 e le 11:35, poi piu' nulla fino al reboot delle 09:00 di oggi.
STM32 'rev 0x101F (non in tabella ST)'.
Ora fe=3, POS IDLE. Ha sia il lettore MDB SELF/2000 sia il P95.
Vendite: 17 transazioni, 14 approvate (12 cash, 5 carta), 1 codice 90.
- **Ipotesi:** L'installazione e' riuscita. Gli errori uart verso la GMI su una GMI rossa non rientrano nel caso noto delle GMI verdi: possibile cavo o massa.
I lock hostlink erano probabilmente legati alle prove di installazione.
- **Proposta:** Campo Carpi: ripetere il test linea 8.4. Se resta DISTURBATA, provare un altro cavo FTDI.
Maurizio: verificare che la revisione STM32 0x101F sia gestita correttamente.
- **Gia' noto:** Aggiornamento firmware GMI / riavvii GMI (ST-Link menu 9.5)

<a id="cg-016"></a>

### CG-016 · Errori seriali: 29598 ne ~100 nelle prime 3 h; contatori in crescita su 28418, 23718, 33326 e 37008

- **Area:** hardware · **Gravita':** low · **Visto:** 2026-11-06 → 2026-11-15
- **Macchine:** 29598, 33326, 11223355, 58547455, 58555555, 37008, 23718, 28418
- **Prove:** - 29598: ne=98 con uptime 11022 s (boot alle 06:45), stesso schema dei giorni scorsi.
- 28418: fe 73, ne 14, ore 56 (era fe 30, ne 7, ore 18), uptime ~4,8 giorni, test linea del 20/10 KO.
- 23718: fe 46, ne 12, ore 65 (era fe 27, ore 44).
- 33326: fe 8, ne 15, ore 60 (era fe 2, ne 9, ore 28).
- 37008: ore 148 (era 56), uptime ~10 giorni.
- 29597: ne 19.
- Banco fermo dal 13/11: 11223355 fe 247; lato Pi 58547455 brk 132/frame 79 e 58555555 brk 162/frame 19.
- **Ipotesi:** 29598: rumore sistematico nelle prime ore (cavo A10KIK4A, massa o GMI verde).
Su 28418 e 23718 i frame error crescono senza riavvii: linea rumorosa. Gli ore crescono con l'uptime.
- **Proposta:** Campo Aprilia: test linea 8.4 sulla 29598.
Laboratorio: test linea su 28418 e 23718; sul banco su 58547455 e 58555555.
Maurizio: inviare i contatori come delta giornaliero.
- **Gia' noto:** Aggiornamento firmware GMI (linea disturbata GMI verdi)

<a id="cg-018"></a>

### CG-018 · Preparazione macchine al banco: banco spento dal 13/11, 21784 offline dalle 20:53 di ieri

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-09 → 2026-11-15
- **Macchine:** 11223344, 11223355, 11155520, 1470000, 54124120, 58547455, 58555555, 58888999, 21784, CG-4F2F67B8
- **Prove:** Banco offline dal 13/11:
- 11223344, 11155520, 11223355, 1470000, 58547455, 58555555 e 58888999 dalle 15:18-15:26;
- 54124120 dalle 13:20, con updater 'Couldn't connect'.
21784 (centro null, mod5):
- 14/11: boot verso le 09:19, update_failed DNS e poi recovered alle 10:06; report a singhiozzo (pause dopo le 15:07, 19:03 e 20:06);
- 13 transazioni tra le 12:18 e le 18:51, 10 approvate (1 carta 'esito recuperato con H');
- offline dalle 20:53, non tornata alle 10:00.
Pi senza MHD 4f2f67b8 offline dall'11/11 08:54.
- **Ipotesi:** Banco spento per il fine settimana. 21784: rete instabile (vedi CG-020); non e' noto dove si trovi.
- **Proposta:** Maurizio/campo:
- MHD definitivi, centro e TID distinti prima della spedizione;
- test linea 8.4 su tutte;
- dire dove si trova la 21784.
Dashboard: marcare 'banco'.
- **Gia' noto:** GMI 'muta' / NCG senza bootloader (menu 9.5 ST-Link); golden SD (CG-<seriale>)

## In osservazione

<a id="cg-023"></a>

### CG-023 · 36842 (Parma): riavvii a meta' giornata il 12 e il 13/11, ieri nessuno

- **Area:** campo · **Gravita':** medium · **Visto:** 2026-11-12 → 2026-11-13
- **Macchine:** 36842
- **Prove:** Nelle 24 h solo la riaccensione normale alle 09:09 di oggi (uptime 135); nessun riavvio durante il 14/11.
14/11: 42 transazioni, 32 approvate (19 con carta), le 8 non riuscite sono timeout del cliente.
Throttled 0x0, nessun FAULT_REPORT.
Casi precedenti: 13/11 alle 13:33; 12/11 alle 11:41 e alle 12:35.
- **Ipotesi:** I riavvii del 12 e del 13/11 erano probabilmente interventi sul posto o interruzioni di corrente. Non confermato.
- **Proposta:** Campo Parma: chiedere se il 12 e il 13/11 ci sono stati interventi.
Chiudere se non si ripresenta nei prossimi giorni.

<a id="cg-022"></a>

### CG-022 · gmi_hostlink locked a macchina accesa senza riavvio: nessun caso nelle ultime 24 h

- **Area:** pi · **Gravita':** low · **Visto:** 2026-11-12 → 2026-11-13
- **Macchine:** 24349, 25158, 36842, 24338, 28418, 23718, 32996, 25157, 28419, 32995
- **Prove:** Nelle 24 h ci sono solo coppie locked/unlocked al boot o al recovery, cioe' insieme a reboot o app_restart:
- 21784 alle 10:06 (boot verso le 09:19, evento arrivato in ritardo);
- le riaccensioni del mattino tra le 05:41 e le 09:46;
- 32996 tra le 09:08 e le 09:09; 25158 tra le 09:26 e le 09:27.
Ultimo caso isolato: 32995 il 13/11 alle 12:42.
- **Ipotesi:** Il main loop del Pi resta fermo oltre 20 s (forse una chiamata bloccante POS o rete). Gli episodi sono in calo; causa ignota.
- **Proposta:** Maurizio: aggiungere all'evento la durata del blocco e l'ultima riga inviata. Chiudere se non si ripresenta entro qualche giorno.
- **Gia' noto:** Pagamenti bloccati perche' la GMI non sente il Pi (evento gmi_hostlink)

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
