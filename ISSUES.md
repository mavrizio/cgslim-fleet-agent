# Registro problemi flotta CGSLIM

Aggiornato dall'agente il 18/11/2026 10:04. Una voce per causa; MHD senza zeri. Generato: non modificare a mano.

## Aperti

<a id="cg-003"></a>

### CG-003 · POS DISCONNECTED dopo timeout get_advanced_config: 24350 (5o giorno senza carte), 37008, 23718, 33326 e 8 Pi di banco

- **Area:** pi · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-18
- **Macchine:** 24350, 37008, 33326, 23718, 24866, 25254, 28416, 33957, 11223344, 11155520, 11223355, 1470000, 54124120, 58547455, 58555555, 58888999, 36842, 24254, 32996, 24338, 28418, 21784, 25158, 29598, 32995
- **Prove:** Avviso 'POS in errore su 12 macchine' (Timeout locale get_advanced_config), tutte DISCONNECTED:
- campo/lab: 24350, 37008, 23718, 33326;
- banco: 1470000, 11155520, 11223344, 11223355, 54124120, 58547455, 58555555, 58888999. Tornati online il 17/11 verso le 12:11 e rimasti DISCONNECTED.
Per contro i banco nuovi 99900055 e 99990008 e il 99999901 sono IDLE.
24350:
- boot alle 09:12, ancora DISCONNECTED, cashless_info mai letta;
- 17/11: 6 vendite cash e 1 timeout carta alle 16:52; last_ok carta null.
Transitori rientrati:
- 29598: 'Connessione persa' alle 06:47;
- 32996: 'Connessione persa' alle 09:17.
Nuovo: 32995, 'Operazione get_advanced_config gia' in corso' nel report del boot (09:18).
24866: IDLE, 3 vendite cash ieri, nessuna carta.
- **Ipotesi:** Dopo un timeout della lettura cashless_info il pos-engine resta DISCONNECTED e non ritenta. Il 'gia' in corso' al boot della 32995 suggerisce due letture sovrapposte. Non confermato.
- **Proposta:** Maurizio:
- un errore di get_advanced_config non deve bloccare il P95: ritentare con backoff;
- evitare letture concorrenti;
- nascondere la carta a POS DISCONNECTED.
Campo Parma: spegnere e riaccendere il POS della 24350 e provare una carta.
Dashboard: escludere i Pi di banco dall'avviso.
- **Gia' noto:** POS: get_advanced_config

<a id="cg-009"></a>

### CG-009 · 24254 (Aprilia): quarto giorno senza vendite, accesa solo 12:49-19:56, oggi alle 10:00 spenta

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-02 → 2026-11-18
- **Macchine:** 24254
- **Prove:** 17/11:
- reboot alle 12:51 (uptime 138), quindi accesa verso le 12:49;
- sottotensione ADESSO dalle 13:02 alle 20:02;
- ultimo report alle 19:56;
- 0 transazioni (anche il 14, 15 e 16/11).
16/11: stesso schema, accesa verso le 12:35 e ultimo report alle 19:55.
18/11 alle 10:00: offline. Le altre Aprilia accese tra le 05:41 (24866) e le 07:30 (26087).
POS IDLE, carta mai provata in 24 h, ultima carta approvata il 05/11.
- **Ipotesi:** Non confermato:
- linea o timer diversi dalle vicine (fascia 12:30-20:00);
- alimentazione del Pi insufficiente, che rende la macchina inutilizzabile per il cliente.
- **Proposta:** Campo Aprilia, oggi:
- verificare linea e programmazione del timer;
- sostituire l'alimentatore del Pi;
- controllare schermo e touch;
- fare una vendita di prova cash e carta.
Maurizio: journal e dmesg del 17/11.

<a id="cg-026"></a>

### CG-026 · 25254 (Tiburtino): non riaccesa stamattina, 0 transazioni ieri

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-18 → 2026-11-18
- **Macchine:** 25254
- **Prove:** Ultimo report il 17/11 alle 21:04, con uptime 48012 s (boot verso le 07:43 del 17/11). Alle 10:00 di oggi offline (775 min).
Le altre 6 Tiburtino riaccese tra le 06:51 (25356) e le 08:54 (33090).
17/11: nessuna transazione.
Nell'ultimo report: POS IDLE, fe 13, throttled 0x0.
Ultima carta approvata il 16/11 verso le 18:24.
- **Ipotesi:** Interruttore, linea o timer della macchina; in alternativa il Pi non parte. La giornata a zero vendite di ieri potrebbe essere traffico oppure un problema gia' presente. Non confermato.
- **Proposta:** Campo Tiburtino:
- verificare che sia alimentata e accesa;
- controllare il display;
- fare una vendita di prova.
Maurizio: alla ripresa, controllare il journal del 17/11.

<a id="cg-004"></a>

### CG-004 · Seriale GMI assente all'accensione (FTDI non enumerato), cavi lotto BG03E: oggi solo 32996

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-18
- **Macchine:** 25158, 32996
- **Prove:** 18/11:
- 32996 (BG03ER1N): 09:04 reboot (uptime 112), eccezione 'could not open port /dev/ttyUSB0' e serial_missing not_enumerated (sul bus solo hub, ethernet e touch ILITEK); 09:08 reboot di recovery (uptime 45); 09:09 serial_recovery. Ora POS IDLE, fe 5.
- 25158 (BG03ES5F): 09:22 reboot (uptime 112) senza serial_missing. E' la prima mattina pulita dopo una lunga serie.
Vendite 17/11: 32996 2 cash; 25158 nessuna transazione.
Cavo non ancora scambiato.
- **Ipotesi:** Lotto FT232R BG03E e/o alimentazione a ritroso dalla GMI. La mattina pulita della 25158 non cambia il quadro: il problema e' intermittente.
- **Proposta:** Campo Parma: scambiare il cavo della 25158 con uno AL05, tenendo la 32996 come controllo.
Pi, prossimo rilascio: riavvio anticipato, uhubctl, TX della GMI in high-Z.
- **Gia' noto:** Seriale assente al mattino (serial_missing, not_enumerated)

<a id="cg-005"></a>

### CG-005 · Sottotensione del Raspberry: 24254 tutto il pomeriggio, 24349 tutto il giorno a intermittenza, 23718 fissa, 24350 e 24338 dal boot

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-18
- **Macchine:** 24349, 23718, 24254, 24350, 24338
- **Prove:** 17/11, orari locali:
- 24254: undervoltage_now dalle 13:02 alle 20:02 quasi senza pause; ultimo stato 0x50005.
- 24349: undervoltage_now ripetuto dalle 10:02 alle 00:17 (circa 12 episodi); oggi di nuovo alle 09:32, ora 0x50000.
Oggi:
- 23718: 0x50005 fissa, avviso aperto dal 03/11;
- 24350 e 24338: 0x50000.
- **Ipotesi:** Alimentatori o cavi deboli. Sulla 24254 probabile legame col fermo vendite (CG-009). Non confermato.
- **Proposta:** Hardware/campo, sostituire alimentatore e cavo del Pi in quest'ordine:
1. 24254;
2. 24349;
3. 24350;
4. 23718;
5. 24338.
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

### CG-014 · Tramogge 2-3 a zero: 33180 ancora mod 2, 37008 ora 1,0,0; 25356 e 36842 rientrate; 23718 mod 4

- **Area:** firmware · **Gravita':** medium · **Visto:** 2026-11-05 → 2026-11-18
- **Macchine:** 23718, 33180, 28419, 25356, 36842, 37008
- **Prove:** Ancora anomale:
- 33180: mod 2, schermata 40, tramogge 1,0,0, chl_mode 0, pos-engine inactive. 17/11: 11 vendite cash tra le 11:24 e le 17:53.
- 37008 (nuova): mod 12, schermata 71, tramogge 1,0,0. 17/11: 9 vendite cash.
- 23718: mod 4, schermata 21, tramogge 0,1,1.
Rientrate:
- 25356: oggi mod 12, schermata 70, tramogge 1,1,0; 17/11 1 vendita cash alle 15:02.
- 36842: oggi 1,1,0, schermata 70; 17/11 3 approvate (2 carte).
- **Ipotesi:** La mod 2 compare quando la GMI trova solo la tramoggia 1. La schermata 71 compare con le tramogge 2 e 3 a 0, anche in mod 12. Le tramogge potrebbero essere vuote o non rispondere. Il ritorno di 25356 e 36842 fa pensare a un rifornimento. Non confermato.
- **Proposta:** Campo Tiburtino: tramogge 2 e 3 della 33180.
Chiedere dove si trova la 37008 e far controllare le tramogge 2 e 3.
Maurizio: documentare quando la GMI passa a mod 1, 2 o 4 e cosa significa la schermata 71.

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

### CG-020 · Telemetria assente con rete/DNS KO: 32995 muta dalle 12:19 di ieri e rete null oggi, 21784 a singhiozzo

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-11 → 2026-11-18
- **Macchine:** 24350, 33957, 21784, 24349, 28416, 32995, 37008, 54124120
- **Prove:** 32995:
- nessun report dal 17/11 alle 12:19 alle 09:18 di oggi;
- reboot alle 09:18 (uptime 151), poi un solo report alle 09:19 con network e rssi null;
- muta da 40 minuti;
- nessuna transazione registrata il 17/11.
21784:
- offline alle 14:40 e alle 17:17;
- update_failed 'Could not resolve host' alle 14:39, rientrato alle 14:40;
- ultimo report alle 19:55, oggi non tornata.
DNS KO rientrati: 37008 alle 04:03, 54124120 dalle 08:14 alle 09:34.
24349: ieri telemetria regolare.
- **Ipotesi:** Sulla 32995 il modem o il router non si connettono (network null). Negli altri casi DNS dell'operatore che cade. Non confermato.
- **Proposta:** Campo Parma: router e SIM della 32995, verificare che venda.
Maurizio:
- DNS di riserva;
- report anche con DNS KO;
- loggare lo stato del modem.
- **Gia' noto:** Aggiornamenti bloccati (update_failed, rete/SIM)

<a id="cg-024"></a>

### CG-024 · 33326 (lab): GMI bloccata (errore 98), reflash 4.20.98 fallito 15 volte sempre al blocco 13824

- **Area:** firmware · **Gravita':** medium · **Visto:** 2026-11-16 → 2026-11-17
- **Macchine:** 33326
- **Prove:** 16/11, mattina:
- 09:45 reboot e gmi_mute NCG4.09;
- 09:53 fw 4.20.31 con loop RDY.
16/11 10:01: gmi_flash_failed con CGT-4.20.98.bin, 15 tentativi, 'Timeout o errore ACK al blocco 13824. Ricevuto: T\x00RDY'. Avviso gmi_blocked crit aperto da allora.
Ora:
- fw riportato 4.20.31, mod 5, schermata 29, idle false;
- contatori GMI null, POS DISCONNECTED;
- uptime ~24 h: nessun riavvio dopo il blocco;
- throttled 0x0 (niente sottotensione);
- test linea del 06/11 OK, cavo A10LFLHS.
- **Ipotesi:** Il Pi riflasha la GMI quando il fw non coincide con la release (domanda di ieri chiarita).
Il fallimento sempre allo stesso blocco con risposta RDY indica che la GMI si resetta nel bootloader a quel punto. Non sembra rumore di linea. Possibili cause: bootloader o flash della scheda montata a mano incompatibili con la dimensione della 4.20.98, oppure un settore protetto o guasto. Non confermato.
Piu' probabile un problema della scheda sostituita che una regressione dell'aggiornamento: CG-001 resta chiusa.
- **Proposta:** Laboratorio/Maurizio:
- leggere bootloader (versione, dimensione) e flash della GMI;
- riprogrammare via ST-Link bootloader V2 e 4.20.98;
- se ricapita al blocco 13824 su un'altra GMI, riaprire CG-001.
Pi: loggare l'indirizzo flash del blocco fallito.
- **Gia' noto:** Aggiornamento firmware GMI che fallisce (gmi_flash_failed, gmi_blocked, loop RDY)

<a id="cg-011"></a>

### CG-011 · Dashboard: centro null su 9 macchine, device_key 'missing' sul Pi 4f2f67b8, banco nel conteggio (41)

- **Area:** dashboard · **Gravita':** low · **Visto:** 2026-11-04 → 2026-11-18
- **Macchine:** 21784, 23718, 24338, 28418, 33326, 37008, 99999901, 99900055, 99990008
- **Prove:** Centro null su:
- 21784, 23718, 24338, 28418, 33326, 37008, 99999901;
- da ieri le nuove 99900055 (CG-263E51CC, first_seen alle 16:28) e 99990008 (CG-04DDE436, alle 16:23).
Conteggio flotta 41: comprende 10 Pi di banco, il tornello e il Pi senza MHD 4f2f67b8 (device_key missing).
- **Ipotesi:** Configurazione mancante sulle macchine di banco e di laboratorio.
- **Proposta:** Dashboard/Maurizio:
- assegnare il centro (o 'banco');
- escludere banco e laboratorio da conteggio e avvisi.
- **Gia' noto:** Profilo display auto / golden SD

<a id="cg-016"></a>

### CG-016 · Errori seriali in crescita: 23718 (+53 fe), 37008 (+50 ore), 29598 ne ~95 al boot, banco 58555555 fe 1521 / ne 2020

- **Area:** hardware · **Gravita':** low · **Visto:** 2026-11-06 → 2026-11-18
- **Macchine:** 29598, 33326, 11223355, 58547455, 58555555, 37008, 23718, 28418, 99900055
- **Prove:** Contatori di oggi:
- 23718: fe 164, ne 36, ore 179 (ieri 111, 27, 145).
- 37008: ore 277 (ieri 227), brk 2.
- 29598: ne 94 a uptime 11029 s (boot alle 06:46), stesso schema dei giorni scorsi.
- 28418: offline, ultimi valori fe 137 e ne 36.
Banco:
- 58555555: fe 1521, ne 2020, Pi brk 49 e frame 3. gmi_mute alle 12:12 di ieri, gmi_back alle 16:00, hostlink locked dalle 18:23 alle 18:29.
- 99900055 (nuova): Pi brk 240 e frame 243.
- **Ipotesi:** Linee rumorose su 23718. Sulla 58555555 cavo o connessione del banco difettosi, coerente col gmi_mute e con 6 minuti di hostlink perso. Sulla 99900055 i brk/frame lato Pi sono probabilmente il periodo di GMI muta prima dell'ST-Link.
- **Proposta:** Laboratorio:
- cavo e test linea 8.4 della 58555555;
- test linea su 23718.
Campo Aprilia: test linea 8.4 sulla 29598.
Maurizio: inviare i contatori come delta giornaliero.
- **Gia' noto:** Aggiornamento firmware GMI (linea disturbata GMI verdi)

<a id="cg-018"></a>

### CG-018 · Banco tornato il 17/11 con 2 GMI nuove (99900055, 99990008); 28418 (lab) offline dal 17/11 03:51; 21784 non tornata

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-09 → 2026-11-18
- **Macchine:** 11223344, 11223355, 11155520, 1470000, 54124120, 58547455, 58555555, 58888999, 21784, CG-4F2F67B8, 28418, 99900055, 99990008
- **Prove:** Banco:
- riacceso il 17/11 verso le 12:11 (reboot con uptime 126-143);
- 11223344 aggiornata a 205 e fw 4.20.98 alle 12:14.
- 54124120: reboot alle 13:12 (uptime 3802), offline a tratti nella notte, update_failed DNS alle 08:14 rientrato alle 09:34.
Nuove GMI:
- 99990008: first_seen alle 16:23, gmi_mute, loop RDY alle 16:28, gmi_uninit (matricola mancante), mode 255->5 alle 08:39, init_ok alle 08:44;
- 99900055: first_seen alle 16:28, gmi_mute, ST-Link legacy 4.20.93 riuscito alle 08:42 (3,21 V), init_ok alle 08:54.
28418: offline dal 17/11 alle 03:51.
21784: ultimo report il 17/11 alle 19:55; 1 vendita cash alle 10:10.
Pi 4f2f67b8 offline dall'11/11.
- **Ipotesi:** Preparazione di macchine nuove in laboratorio. 28418 spenta, causa non nota.
- **Proposta:** Laboratorio:
- dire se 28418 e' stata spenta;
- assegnare MHD, centro e TID distinti prima della spedizione;
- test linea 8.4.
Campo: dire dove si trova la 21784 e controllarla.
- **Gia' noto:** GMI 'muta' / NCG senza bootloader (menu 9.5 ST-Link); golden SD (CG-<seriale>)

<a id="cg-022"></a>

### CG-022 · gmi_hostlink locked a macchina accesa senza reboot: 25356, 29597, 58555555 (6 min), 99999901

- **Area:** pi · **Gravita':** low · **Visto:** 2026-11-12 → 2026-11-18
- **Macchine:** 24349, 25158, 36842, 24338, 28418, 23718, 32996, 25157, 28419, 32995, 29598, 25356, 29597, 58555555, 99999901
- **Prove:** Blocchi senza reboot ne' app_restart:
- 17/11: 25356 11:55-11:56; 29597 19:00-19:01; 58555555 18:23-18:29;
- 18/11: 99999901 09:31-09:32 e 09:49-09:50.
Gli altri eventi sono coppie locked/unlocked al boot o al recovery.
- **Ipotesi:** Blocchi brevi di 1 minuto, probabilmente seriale o main loop fermi per qualche secondo; la protezione funziona.
Sulla 58555555 il blocco e' compatibile con la linea pessima (fe 1521).
- **Proposta:** Maurizio: aggiungere all'evento la durata del blocco e l'ultima riga inviata.
Incrociare con i contatori fe/ne della stessa macchina.
- **Gia' noto:** Pagamenti bloccati perche' la GMI non sente il Pi (evento gmi_hostlink)

<a id="cg-025"></a>

### CG-025 · Tornello di banco 99999901 (MOD10): resto non erogato (4,00 €), evento gate_short_change a zero, riavvii

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-16 → 2026-11-18
- **Macchine:** 99999901
- **Prove:** 17/11:
- 18 transazioni tra le 10:56 e le 12:13, 13 approvate (12 cash, 1 carta), 5 annullate;
- gate_short_change alle 11:01: dovuti 400, erogati 0, mancanti 400;
- alle 12:10 un gate_short_change con due/paid/missing tutti a 0;
- reboot alle 11:53 e alle 12:02 (uptime 65); avvisi di 7 riavvii dell'app e 3 del Pi in 6 h.
Oggi:
- hostlink locked alle 09:31 e alle 09:49;
- POS IDLE, tramogge 1,0,0, schermata 160.
- **Ipotesi:** Banco in lavorazione: hopper vuoto o inceppato (resto 4 € non erogato). L'evento a zeri sembra un falso positivo del firmware o del Pi. Non confermato.
- **Proposta:** Laboratorio:
- rifornire e verificare l'hopper;
- marcarla 'banco';
- assegnarle un TID distinto.
Maurizio: non emettere gate_short_change con missing=0.
- **Gia' noto:** MOD10 Tornello; IP del Raspberry (PI_IP)

## In osservazione

<a id="cg-012"></a>

### CG-012 · Codice 31: secondo giorno senza rifiuti

- **Area:** pos · **Gravita':** medium · **Visto:** 2026-11-04 → 2026-11-15
- **Macchine:** 24254, 28418, 33957, 24866, 29597, 23718, 58888999, 33089, 25356, 24349
- **Prove:** 16/11 e 17/11: nessun 'codice 31' in flotta.
17/11:
- 33957: 7 transazioni, 4 approvate, 1 timeout carta alle 14:59, 2 annullate;
- unico rifiuto bancario: codice 04 sulla 29598 alle 14:49.
- **Ipotesi:** I rifiuti del 15/11 sembrano rientrati dopo l'intervento POS sulla 33957. Non confermato.
- **Proposta:** Chiudere se non ricompare entro il 20/11.
Maurizio: mostrare 'carta non disponibile' dopo N rifiuti consecutivi.
- **Gia' noto:** POS: altri errori

<a id="cg-015"></a>

### CG-015 · 33957 (Carpi): nessuna nuova perdita seriale ieri; linea ancora DISTURBATA

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-05 → 2026-11-16
- **Macchine:** 33957
- **Prove:** 17/11:
- nessun evento seriale (disconnessione, serial_missing, recovery);
- 7 transazioni tra le 13:04 e le 18:02, 4 approvate, 1 timeout carta e 2 annullate.
Oggi: boot alle 09:00 (uptime 125), fe 3, ore 3, POS IDLE.
Ultimo test linea il 05/11: DISTURBATA. Cavo A10LF8Y6.
- **Ipotesi:** Le disconnessioni del 16/11 tra le 11:27 e le 11:39 coincidono con la prova carta: probabile intervento del tecnico o contatto USB smosso. Non confermato.
- **Proposta:** Campo Carpi:
- chiedere se il 16/11 c'e' stato un intervento;
- ripetere il test linea 8.4;
- sostituire il cavo se ricapita.
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
