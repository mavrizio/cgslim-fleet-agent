# Registro problemi flotta CGSLIM

Aggiornato dall'agente il 13/11/2026 10:02. Una voce per causa; MHD senza zeri. Generato: non modificare a mano.

## Aperti

<a id="cg-003"></a>

### CG-003 · POS DISCONNECTED dopo timeout get_advanced_config: 24350, 37008, 33326 e 23718 al nono giorno, anche con le release 200-202

- **Area:** pi · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-13
- **Macchine:** 24350, 37008, 33326, 23718, 11223344, 11155520, 11223355, 1470000, 54124120, 58547455, 58555555, 58888999, 24866, 33957, 36842, 24254, 32996, 24338, 28418, 25254, 21784
- **Prove:** Avviso 'POS in errore su 11 macchine' aperto dal 10/11.
Macchine in campo/beta alle 09:5x di oggi, tutte DISCONNECTED con 'Timeout locale get_advanced_config':
- 24350: riavviata alle 06:11 e alle 09:11, ancora DISCONNECTED; nessun dato P95 letto e nessuna transazione nelle 24 h.
- 37008: 10 vendite cash, nessuna carta.
- 33326: DISCONNECTED anche con la SLIM-4.20.202.
- 23718: 1 carta annullata alle 14:50.
Pi di banco DISCONNECTED: 1470000, 11155520, 11223344, 11223355, 58547455, 58555555, 58888999; 54124120 offline.
'Connessione persa durante get_advanced_config', tutte rientrate entro 15 min (orari locali):
- 12/11: 21784 alle 10:32, 36842 alle 11:47, 24866 e 25254 alle 13:47, 24338 alle 16:02 e alle 17:02, 28418 alle 17:32;
- 13/11: 32996 e 33957 alle 09:17.
- **Ipotesi:** Dopo un timeout della lettura cashless_info il pos-engine resta DISCONNECTED senza ritentare; le release 199-202 non cambiano il comportamento. I 'Connessione persa' sono transitori legati agli avvii.
- **Proposta:** Maurizio:
- un errore di get_advanced_config non deve bloccare il P95: saltare la lettura e ritentarla con backoff;
- nascondere la carta a POS DISCONNECTED;
- log pos-engine della 24350 dopo le 09:11 di oggi.
Campo Parma: spegnere e riaccendere il POS della 24350 e provare una carta.
Dashboard: escludere i Pi di banco dall'avviso.
- **Gia' noto:** POS: get_advanced_config; IP del Raspberry (bug 195 su POS dopo PI_IP)

<a id="cg-009"></a>

### CG-009 · 24254 (Aprilia): ieri spenta 09:47-12:58 e di nuovo dalle 19:47; stamattina non accesa

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-02 → 2026-11-13
- **Macchine:** 24254
- **Prove:** 12/11:
- 09:16: accesa;
- 09:47: sottotensione ADESSO, poi nessun report fino alle 12:58;
- 13:00: reboot (uptime 138);
- sottotensione a piu' riprese nel pomeriggio;
- 19:47: ultimo report.
13/11: alle 10:00 offline da 852 minuti, mentre le altre Aprilia si sono accese tra le 05:41 e le 07:30.
Nessuna transazione nelle 24 h; ultima carta approvata il 05/11.
- **Ipotesi:** Alimentazione interrotta o insufficiente: presa, timer o alimentatore. La sottotensione precede le perdite di corrente. Non confermato.
- **Proposta:** Campo Aprilia, oggi:
- verificare se la macchina e' alimentata, la presa e il timer;
- sostituire l'alimentatore del Pi;
- fare una vendita di prova.
Maurizio: journal e dmesg del 12/11 attorno alle 09:47 e alle 19:47, appena torna online.

<a id="cg-004"></a>

### CG-004 · Seriale GMI assente all'accensione (FTDI non enumerato), cavi lotto BG03E: oggi sia 25158 sia 32996

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-13
- **Macchine:** 25158, 32996
- **Prove:** 13/11:
- 32996 (BG03ER1N): 09:04 reboot (uptime 113), 'could not open port /dev/ttyUSB0', serial_missing not_enumerated (sul bus solo hub, ethernet e ILITEK); 09:08 reboot di recovery (uptime 45); 09:09 serial_recovery.
- 25158 (BG03ES5F): 09:22 stesso schema; 09:26 reboot; 09:27 serial_recovery.
La 25158 e' a 7 mattine su 8 (06, 08, 09, 10, 11, 12 e 13/11).
Vendite ieri: 32996 6 transazioni (5 approvate), 25158 3 (1 approvata).
Anche la 25254 (cavo AL05ZNNI) ha avuto serial_missing il 12/11 alle 11:49, rientrato dopo 5 s, durante l'installazione con l'ST-Link: non conta.
Cavo della 25158 non ancora scambiato.
- **Ipotesi:** Lotto FT232R BG03E e/o alimentazione a ritroso dalla GMI. Il recovery funziona e costa circa 5 minuti.
- **Proposta:** Campo Parma: scambiare il cavo della 25158 con uno AL05 e lasciare la 32996 come controllo.
Pi: nel prossimo rilascio riavvio anticipato (~30-40 s), uhubctl e TX della GMI in high-Z.
- **Gia' noto:** Seriale assente al mattino (serial_missing, not_enumerated)

<a id="cg-005"></a>

### CG-005 · Sottotensione del Raspberry: 24349 e 24254 a episodi tutto il giorno, 23718 fissa

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-13
- **Macchine:** 24349, 23718, 24254, 24350, 24338
- **Prove:** Avvisi undervoltage_now del 12/11, orari locali:
- 24349: circa 12 episodi (09:32, 10:17, 11:17-11:32, 12:32, 13:17, 14:02, 15:17-16:02, 17:02, 19:17-20:32, 21:47, 22:47). Oggi throttled 0x50005 alle 09:49, a circa 30 minuti dal boot delle 09:17.
- 24254: 09:47 e poi a piu' riprese dalle 13:32 fino all'arresto delle 19:47.
- 23718: 0x50005 fissa, avviso aperto dal 03/11.
- 24350 e 24338: 0x50000.
- 11223355 (banco): oggi 0x0.
- **Ipotesi:** Alimentatori o cavi deboli. Sulla 24254 probabilmente legata anche agli spegnimenti (CG-009).
- **Proposta:** Hardware/campo, in ordine:
1. 24254 (insieme a CG-009).
2. 24349.
3. 23718.
4. 24350 e 24338.
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

### CG-012 · POS non pronto dopo l'avvio o dopo un codice 90: 'activate gia' in corso', Broken pipe, rifiuti codice 31

- **Area:** pi · **Gravita':** medium · **Visto:** 2026-11-04 → 2026-11-12
- **Macchine:** 24254, 28418, 33957, 24866, 29597, 23718, 58888999, 33089, 25356
- **Prove:** 12/11:
- 33089 (nuova): 'Operazione activate gia' in corso' alle 17:02 e un pagamento in errore 'Broken pipe' alle 16:45; ultima approvata alle 17:59.
- 33957: 'POS riattivato dopo codice 90' alle 11:15, poi 4 rifiuti 'codice 31' tra le 11:15 e le 11:17; 8 approvate nella giornata.
- 25356: carta approvata dopo 'POS riattivato dopo codice 90' (~14:18).
- **Ipotesi:** Corsa all'avvio tra activate, lettura cashless_info e pagamento. Il codice 31 subito dopo il recupero da codice 90 potrebbe essere legato al terminale appena riattivato. Non confermato.
- **Proposta:** Maurizio:
- carta disabilitata finche' il POS non e' IDLE e cashless_info non ha finito;
- verificare il significato del codice 31 dopo il recupero da codice 90.
- **Gia' noto:** POS: get_advanced_config (operazione gia' in corso)

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

### CG-020 · Telemetria assente per ore con DNS non risolto mentre la macchina vende: 24350 e 33957

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-11 → 2026-11-13
- **Macchine:** 24350, 33957
- **Prove:** 24350, 12/11:
- 'Could not resolve host gitlab-dev' a ripetizione (11:18, 12:35, 13:07, 13:30, 14:10, 15:06, 15:55, 16:28, 17:02, 17:45, 20:28, 22:02);
- offline a tratti (ultimi report 10:20, 11:18, 14:25, 15:06, 20:37).
24350, 13/11:
- reboot alle 06:11, ultimo report alle 06:12;
- nuovo reboot alle 09:11 (uptime 140);
- nessuna transazione nelle 24 h.
33957 (Carpi):
- nessun report dalle 10:17 del 12/11 alle 09:06 di oggi, ma 14 transazioni ieri tra le 10:08 e le 18:53;
- alle 09:06 update_failed 'Could not resolve host', subito recuperato.
Separato: 502 di gitlab-dev alle 07:37 su 4 macchine, lato server, rientrato in 1 minuto.
- **Ipotesi:** Router o SIM che perdono DNS o dati per ore; le transazioni arrivano in coda. Sulla 24350 il doppio avvio di stamattina fa pensare anche a corrente instabile. Non confermato.
- **Proposta:** Campo Parma: controllare router e SIM della 24350 (log 12/11).
Campo Carpi: idem per la 33957.
Maurizio: verificare timestamp di inserimento delle transazioni e il retry del fleet-reporter senza rete.
- **Gia' noto:** Aggiornamenti bloccati (update_failed, rete/SIM)

<a id="cg-021"></a>

### CG-021 · Installazione Tiburtino Guidonia (12/11): 7 macchine nuove online e in vendita; chiave 25355 in mismatch, versioni ballerine sulla 33089

- **Area:** campo · **Gravita':** medium · **Visto:** 2026-11-12 → 2026-11-13
- **Macchine:** 33089, 25254, 25355, 25356, 25357, 33090, 33180
- **Prove:** 12/11, first_seen: 33089 alle 10:27, 25254 alle 11:14, 25357 alle 12:56, 25356 alle 13:59, 25355 alle 14:27, 33090 alle 15:35, 33180 alle 16:10.
Oggi tutte su SLIM-4.20.200, fw 4.20.93, ramo mod5, riaccese tra le 06:51 e le 08:54.
Vendite 24 h: 25254 11 (9 approvate), 33180 10/10, 33089 8 (3), 25357 7 (3), 25356 5 (4), 33090 4 (3).
33089:
- reboot_storm (5 in 6 h), version_change 199->192->199->200->199->200 tra le 10:57 e le 13:44;
- mismatch della chiave dalle 10:58.
25355: device_key_status mismatch, avviso aperto dalle 07:17.
25254: orologio sfasato di -38365 s alle 07:47, dopo il boot delle 07:45, rientrato entro 15 min.
- **Ipotesi:** Durante l'installazione sono state scambiate o riscritte delle SD (golden): da qui il rientro alla 192 e le chiavi in mismatch. L'orologio sfasato e' il Pi senza RTC prima della sincronizzazione NTP. Non confermato.
- **Proposta:** Maurizio/dashboard: re-enroll della chiave della 25355.
Campo Tiburtino: confermare quale SD e' montata su 33089 e 25355.
Verificare la carta sulla 33180 (CG-014).
Test linea 8.4 su tutte.
- **Gia' noto:** Profilo display auto / golden SD; GMI 'muta' / NCG senza bootloader

<a id="cg-011"></a>

### CG-011 · Dashboard: chiave 25355 in mismatch, centro null su 6 macchine, Pi di banco nel conteggio

- **Area:** dashboard · **Gravita':** low · **Visto:** 2026-11-04 → 2026-11-13
- **Macchine:** 21784, 23718, 24338, 28418, 33326, 37008, 25355
- **Prove:** - 25355: device_key_enrolled alle 14:28 di ieri e device_key_mismatch alle 16:08; avviso riaperto oggi alle 07:17, device_key_status 'mismatch'.
- 33089: mismatch dalle 10:58 alle 14:47 di ieri, poi rientrato.
- Centro null: 21784, 23718, 24338, 28418, 33326 e 37008.
- Conteggio flotta 38: comprende 8 Pi di banco e il Pi senza MHD 4f2f67b8.
- **Ipotesi:** Il mismatch nasce probabilmente dallo scambio o dalla clonazione delle SD durante l'installazione (golden). Non confermato.
- **Proposta:** Dashboard/Maurizio:
- riallineare la chiave della 25355;
- assegnare il centro (o 'banco');
- escludere i device di banco da conteggio e avvisi.
- **Gia' noto:** Profilo display auto / golden SD; IP del Raspberry (PI_IP)

<a id="cg-014"></a>

### CG-014 · MOD non documentate: 23718 mod 4 (prima mod 1), 33180 mod 2 con MDB non inizializzato

- **Area:** firmware · **Gravita':** low · **Visto:** 2026-11-05 → 2026-11-13
- **Macchine:** 23718, 33180
- **Prove:** MOD 12 sul ramo mod5 e' una configurazione normale: e' cosi' su tutte le Tiburtino e su 21784. La 24866 e' esclusa.
23718 (branch mod5):
- ieri mod 1, oggi mod 4, schermata 21, tramogge 0,1,1;
- 1 carta annullata, nessuna vendita;
- POS DISCONNECTED, uptime 242176 s.
33180 (Tiburtino, nuova):
- mod 2, schermata 40, tramogge 1,0,0, chl_mode 2;
- MDB indirizzi 10 e 60 con init false, pos-engine inactive;
- 10 vendite cash ieri (17:09-18:41).
- **Ipotesi:** 23718 e' una macchina di prova riconfigurata. 33180 potrebbe essere configurata per il solo contante, o avere il lettore MDB non collegato. Non confermato.
- **Proposta:** Maurizio: chiarire le MOD 1, 2 e 4 nella scheda.
Campo Tiburtino: dire se la 33180 deve avere la carta (lettore MDB presente?).
Dire se la 23718 e' in servizio.

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

### CG-016 · Errori seriali: 29598 ne ~100 nelle prime 3 h; fe alti su 11223355; brk/frame lato Pi su 58547455 e 58555555

- **Area:** hardware · **Gravita':** low · **Visto:** 2026-11-06 → 2026-11-13
- **Macchine:** 29598, 33326, 11223355, 58547455, 58555555, 37008, 23718, 28418
- **Prove:** - 29598: ne=105 con uptime 11026 s (boot alle 06:45), stesso schema dei giorni scorsi.
- 11223355: fe 247, ore 50.
- 33326 dopo il reflash a 4.20.95: fe 2, ne 9, ore 28.
- Lato Pi (pi_uart), valori fermi rispetto a ieri:
  - 58547455: brk 132, frame 79;
  - 58555555: brk 162, frame 19.
- ore 65-70 sui Pi di banco con uptime lunga: 1470000, 11155520, 54124120, 58547455, 58888999.
- 37008: ore 56.
- 23718: fe 27, ore 44.
- 28418: fe 30, ne 7, ore 18 (test linea del 20/10 KO).
- **Ipotesi:** 29598: rumore sistematico nelle prime ore (cavo A10KIK4A, massa o GMI verde). Gli ore crescono con l'uptime.
- **Proposta:** Campo Aprilia: test linea 8.4 sulla 29598.
Banco: test linea su 58547455 e 58555555.
Maurizio: inviare i contatori come delta giornaliero.
- **Gia' noto:** Aggiornamento firmware GMI (linea disturbata GMI verdi)

<a id="cg-018"></a>

### CG-018 · Preparazione macchine al banco: 8 Pi con MHD provvisori, 21784 tornata online, 54124120 con rete instabile

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-09 → 2026-11-13
- **Macchine:** 11223344, 11223355, 11155520, 1470000, 54124120, 58547455, 58555555, 58888999, 21784, CG-4F2F67B8
- **Prove:** 21784:
- 12/11 10:20 tornata online, poi SLIM-4.20.199 e 200; 2 vendite approvate (ultima alle 17:32);
- offline dalle 20:01 alle 09:54 di oggi (reboot uptime 421);
- MDB SELF/2000 + P95 con TID 75501208, centro null.
54124120:
- report a singhiozzo tutta la notte;
- update_failed 'Couldn't connect' e 'Could not resolve host' (10:40, 11:59, 23:23, 02:28);
- offline dalle 08:41.
11223344 e' passata sulla beta: 202 e fw 4.20.95.
Il Pi senza MHD 4f2f67b8 e' offline dall'11/11 08:54.
- **Ipotesi:** Lotto in preparazione; la rete LTE del banco e' instabile (54124120).
- **Proposta:** Maurizio/campo: MHD definitivi, centro e TID distinti prima della spedizione; test linea 8.4 su tutte.
Dire se la 21784 e' gia' in campo e dove.
Dashboard: marcare 'banco'.
- **Gia' noto:** GMI 'muta' / NCG senza bootloader (menu 9.5 ST-Link); golden SD (CG-<seriale>)

<a id="cg-022"></a>

### CG-022 · gmi_hostlink locked per 1-2 minuti a macchina accesa, senza riavvio, su 8 macchine

- **Area:** pi · **Gravita':** low · **Visto:** 2026-11-12 → 2026-11-12
- **Macchine:** 24349, 25158, 36842, 24338, 28418, 23718, 32996, 25157, 28419
- **Prove:** 12/11, coppie locked/unlocked senza reboot ne' app_restart:
- 24349: 11:03-11:05;
- 25158: 11:34-11:35;
- 36842: 11:56-11:57;
- 24338 e 28418: 12:59-13:01, nello stesso minuto;
- 23718: 13:03-13:04;
- 32996: 15:13;
- 25157: 16:08-16:09;
- 28419: 16:41-16:42.
Le coppie agli avvii e ai rollout sono normali e non sono incluse.
- **Ipotesi:** Il main loop del Pi resta fermo oltre 20 s; per circa un minuto banconote, monete e carta sono chiusi. Causa ignota: forse una chiamata bloccante (lettura POS, rete). Non confermato.
- **Proposta:** Maurizio:
- nei log di 24349 e 25158 cercare cosa fa il main loop in quei minuti;
- aggiungere all'evento la durata del blocco e l'ultima riga inviata.
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

### CG-001 · Aggiornamento firmware GMI: rollout beta 4.20.94/4.20.95 pulito, voce chiusa

- **Area:** firmware · **Gravita':** low · **Visto:** 2026-10-30 → 2026-11-10
- **Macchine:** 26087, 33326, 24338
- **Prove:** 12/11, rollout beta, nessun gmi_flash_failed:
- 11223344: 4.20.94 alle 15:08, 4.20.95 alle 16:32;
- 33326: 4.20.94 alle 15:16, 4.20.95 alle 17:21; RDY atteso alle 15:13 durante il flash;
- 28418: alle 15:22 e alle 17:27;
- 24338: alle 15:54 e alle 17:00.
Sulle GMI Tiburtino il passaggio da RDY al flash seriale e' riuscito (es. 25254 alle 11:53-11:54).
26087: 8 vendite ieri, nessun problema dal 10/11.
- **Ipotesi:** La corruzione del 10/11 sulla 26087 era un disturbo occasionale.
- **Proposta:** Chiusa. Resta valido non segnalare come eccezione il RDY durante un flash pianificato. Riaprire se ricompare un gmi_flash_failed.
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
