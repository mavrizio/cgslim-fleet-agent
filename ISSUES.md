# Registro problemi flotta CGSLIM

Aggiornato dall'agente il 14/11/2026 10:03. Una voce per causa; MHD senza zeri. Generato: non modificare a mano.

## Aperti

<a id="cg-003"></a>

### CG-003 · POS DISCONNECTED dopo timeout get_advanced_config: 24350, 37008, 33326 e 23718 al decimo giorno, anche con la 205

- **Area:** pi · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-14
- **Macchine:** 24350, 37008, 33326, 23718, 11223344, 11155520, 11223355, 1470000, 54124120, 58547455, 58555555, 58888999, 24866, 33957, 36842, 24254, 32996, 24338, 28418, 25254, 21784, 25158
- **Prove:** Avviso 'POS in errore su 4 macchine' aperto dal 10/11 (il banco offline non e' piu' contato).
Online e DISCONNECTED con 'Timeout locale get_advanced_config':
- 24350 (199): nessun dato P95 letto; 6 transazioni ieri, 5 cash approvate e 1 carta annullata.
- 37008 (199): 14 vendite cash, nessuna carta.
- 33326 (205): ferma anche dopo 203, 204 e 205.
- 23718 (205): 1 vendita cash.
Il banco (8 Pi) era DISCONNECTED all'ultimo report, ieri alle 15:2x.
'Connessione persa durante get_advanced_config', tutte rientrate entro 15 minuti (orari locali):
- 13/11: 28418 alle 11:47 e alle 13:47, 36842 alle 13:47;
- 14/11: 32996 alle 09:17 e 25158 alle 09:32, subito dopo il serial_recovery.
- **Ipotesi:** Dopo un timeout della lettura cashless_info il pos-engine resta DISCONNECTED senza ritentare. Le release 199-205 non cambiano il comportamento. I 'Connessione persa' sono transitori legati agli avvii.
- **Proposta:** Maurizio:
- un errore di get_advanced_config non deve bloccare il P95: saltare la lettura e ritentarla con backoff;
- nascondere la carta a POS DISCONNECTED;
- log pos-engine della 24350 dopo il boot delle 09:11 di oggi.
Campo Parma: spegnere e riaccendere il POS della 24350 e provare una carta.
Dashboard: escludere i Pi di banco dall'avviso.
- **Gia' noto:** POS: get_advanced_config; IP del Raspberry (bug 195 su POS dopo PI_IP)

<a id="cg-009"></a>

### CG-009 · 24254 (Aprilia): accesa solo dalle 11:04 alle 19:53 ieri, oggi alle 09:50, con sottotensione

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-02 → 2026-11-14
- **Macchine:** 24254
- **Prove:** 13/11:
- 11:04: reboot (uptime 139);
- sottotensione ADESSO in 10 episodi tra le 11:17 e le 19:47;
- 19:53: ultimo report;
- 1 sola vendita cash, alle 17:16.
14/11:
- 09:50: reboot (uptime 138), mentre le altre Aprilia si sono accese tra le 05:41 (24866) e le 07:30 (26087);
- throttled 0x50005 alle 09:51.
Ultima carta approvata il 05/11.
Gli spegnimenti serali sono sempre intorno alle 19:47-19:58 (anche il 12/11 alle 19:47).
- **Ipotesi:** Due cose insieme. 1) La macchina sembra su una linea o un timer diverso dalle altre Aprilia: accensione tarda e spegnimento verso le 19:50 tutti i giorni. 2) L'alimentatore del Pi e' debole. Non confermato.
- **Proposta:** Campo Aprilia:
- verificare presa, linea e timer (confronto con 24866/26087);
- sostituire l'alimentatore del Pi;
- fare una vendita di prova con carta.
Maurizio: journal e dmesg attorno alle 19:47-19:53 del 12 e del 13/11.

<a id="cg-004"></a>

### CG-004 · Seriale GMI assente all'accensione (FTDI non enumerato), cavi lotto BG03E: 25158 e 32996 anche oggi

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-14
- **Macchine:** 25158, 32996
- **Prove:** 14/11:
- 32996 (BG03ER1N): alle 09:04 reboot (uptime 113), 'could not open port /dev/ttyUSB0', serial_missing not_enumerated (sul bus solo hub, ethernet e ILITEK); alle 09:08 reboot di recovery (uptime 45); alle 09:09 serial_recovery.
- 25158 (BG03ES5F): alle 09:26 reboot (uptime 50); alle 09:27 serial_recovery not_enumerated.
Su entrambe un 'Connessione persa get_advanced_config' subito dopo, rientrato.
La 25158 e' a 8 mattine su 9 (06 e dall'08 al 14/11).
Vendite 24 h: 25158 7 (5 approvate), 32996 7 (6 approvate, l'ultima alle 09:54 di oggi).
Cavo della 25158 non ancora scambiato.
- **Ipotesi:** Lotto FT232R BG03E e/o alimentazione a ritroso dalla GMI. Il recovery funziona e costa circa 5 minuti al mattino.
- **Proposta:** Campo Parma: scambiare il cavo della 25158 con uno AL05 e lasciare la 32996 come controllo.
Pi: nel prossimo rilascio riavvio anticipato (~30-40 s), uhubctl e TX della GMI in high-Z.
- **Gia' noto:** Seriale assente al mattino (serial_missing, not_enumerated)

<a id="cg-005"></a>

### CG-005 · Sottotensione del Raspberry: 24349 e 24254 a episodi tutto il giorno (24349 ora silente), 23718 fissa

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-14
- **Macchine:** 24349, 23718, 24254, 24350, 24338
- **Prove:** Avvisi undervoltage_now del 13/11, orari locali:
- 24349: circa 11 episodi (10:02, 10:47, 12:02, 13:17, 15:32, 17:47, 19:02, 19:47, 20:32, 22:02, 23:02). Oggi reboot alle 09:17, 0x50005 nel report delle 09:19, poi nessun report (offline da 41 minuti alle 10:00).
- 24254: 10 episodi tra le 11:17 e le 19:47 (11:17, 11:47, 12:47, 13:47, 14:47, 15:32, 17:02, 17:47, 19:02, 19:47). Oggi 0x50005 gia' a 201 s dal boot delle 09:50.
- 23718: 0x50005 fissa, avviso aperto dal 03/11.
- 24350 (dal boot delle 09:11) e 24338: 0x50000.
- **Ipotesi:** Alimentatori o cavi deboli. Sulla 24349 il silenzio dopo le 09:19 potrebbe essere un blocco o un riavvio da brown-out (non confermato). Sulla 24254 probabilmente legata anche agli spegnimenti (CG-009).
- **Proposta:** Hardware/campo, in ordine:
1. 24254, insieme a CG-009;
2. 24349, oggi: verificare se e' accesa e cambiare alimentatore/cavo;
3. 23718;
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

### CG-012 · POS non pronto dopo l'avvio o dopo un codice 90; rifiuti codice 31 a raffica sulla 33957

- **Area:** pi · **Gravita':** medium · **Visto:** 2026-11-04 → 2026-11-13
- **Macchine:** 24254, 28418, 33957, 24866, 29597, 23718, 58888999, 33089, 25356
- **Prove:** 13/11, 33957: 3 rifiuti 'codice 31' (2 alle 16:26, 1 alle 16:27). Nelle 24 h 22 transazioni, 19 approvate (18 cash, 4 carta), ultima alle 09:41 di oggi. Nei dati non c'e' un codice 90 prima dei rifiuti (card_activity ok 1, ko 3).
Nessun 'activate gia' in corso' o Broken pipe nelle 24 h.
12/11, gia' registrato:
- 33089: Broken pipe alle 16:45 e activate gia' in corso alle 17:02;
- 33957: codice 31 dopo il codice 90 delle 11:15.
- **Ipotesi:** La corsa all'avvio (activate/cashless_info/pagamento) resta possibile. Il codice 31 si ripete senza codice 90: potrebbe essere un rifiuto lato banca/emittente della stessa carta ritentata, non legato al recupero del POS. Non confermato.
- **Proposta:** Maurizio:
- carta disabilitata finche' il POS non e' IDLE e cashless_info non ha finito;
- verificare con Ingenico/acquirer il significato del codice 31 e se arriva sempre dalla stessa carta.
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

### CG-020 · Telemetria assente per ore con DNS/rete KO mentre la macchina vende: 24350 e 33957 (anche ieri), forse 21784

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-11 → 2026-11-14
- **Macchine:** 24350, 33957, 21784
- **Prove:** 24350:
- 13/11: ultimo report alle 11:21, dopo update_failed 'Could not resolve host';
- nessun report fino al boot delle 09:11 di oggi, ma 6 transazioni ieri tra le 17:16 e le 23:47.
33957 (Carpi):
- 13/11: ultimo report alle 12:57;
- update_failed 'Could not resolve host' da ieri sera circa alle 20:35;
- update_recovered e reboot alle 09:29 di oggi;
- intanto 22 transazioni, dalle 11:14 di ieri alle 09:41 di oggi.
21784: report a singhiozzo ieri (10:28, 19:01, 19:49), updater 'Couldn't connect'.
- **Ipotesi:** Router o SIM che perdono DNS o dati per ore; le transazioni arrivano in coda. Si ripete ogni giorno su 24350 e 33957. Non confermato.
- **Proposta:** Campo Parma: controllare router e SIM della 24350.
Campo Carpi: idem per la 33957.
Maurizio:
- verificare i timestamp di inserimento delle transazioni;
- retry del fleet-reporter senza rete;
- report anche quando il DNS fallisce.
- **Gia' noto:** Aggiornamenti bloccati (update_failed, rete/SIM)

<a id="cg-023"></a>

### CG-023 · 36842 (Parma): riavvii completi a meta' giornata (13/11 alle 13:33; 12/11 alle 11:41 e alle 12:35)

- **Area:** campo · **Gravita':** medium · **Visto:** 2026-11-12 → 2026-11-13
- **Macchine:** 36842
- **Prove:** 13/11 alle 13:33: reboot con uptime 136, app_restart e coppia gmi_hostlink. La macchina vendeva gia' dalle 10:53: 12 transazioni tra le 10:53 e le 23:55, 11 approvate.
12/11: riavvii fuori orario alle 11:41 (uptime 135) e alle 12:35 (uptime 66), allora attribuiti a un intervento.
Nessun FAULT_REPORT o eccezione nelle 24 h. Throttled oggi 0x0. Riaccensione normale alle 09:09 di oggi.
- **Ipotesi:** Un uptime di ~135 s indica un avvio completo (Pi riacceso), quindi probabilmente un'interruzione di corrente della macchina o un intervento sul posto. Lo storico (stop del 31/10, sottotensione passata) fa pensare all'alimentazione. Non confermato.
- **Proposta:** Campo Parma: chiedere se il 13/11 alle 13:33 c'e' stato un intervento; altrimenti controllare presa, alimentatore e timer.
Maurizio: journal e dmesg prima delle 13:33 del 13/11 (last reboot, sottotensione).

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

### CG-014 · MOD non documentate: 23718 mod 4 (ora su beta), 33180 mod 2 senza cashless

- **Area:** firmware · **Gravita':** low · **Visto:** 2026-11-05 → 2026-11-14
- **Macchine:** 23718, 33180
- **Prove:** 23718:
- 13/11: provisioning GIT_BRANCH applicato alle 11:40, passata da mod5 a beta, poi 203, 204 e 205 con fw fino a 4.20.98;
- oggi mod 4, schermata 21, tramogge 0,1,1, POS DISCONNECTED;
- 1 vendita cash alle 12:34;
- reboot alle 12:24 (uptime 136) e app_restart_storm (5 in 6 h, dovuta al rollout).
33180:
- mod 2, schermata 40, tramogge 1,0,0, chl_mode ora 0 (era 2), pos null, pos-engine inactive;
- MDB 10 e 60 con init false;
- 6 vendite cash ieri.
- **Ipotesi:** 23718 e' una macchina di prova riconfigurata, ora usata per la beta. 33180 sembra configurata per il solo contante (chl_mode 0). Non confermato.
- **Proposta:** Maurizio: chiarire le MOD 1, 2 e 4 nella scheda e dire se la 23718 e' di laboratorio.
Campo Tiburtino: confermare che la 33180 deve essere solo contante.

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

### CG-018 · Preparazione macchine al banco: banco spento da ieri pomeriggio, 21784 offline dalle 19:49

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-09 → 2026-11-14
- **Macchine:** 11223344, 11223355, 11155520, 1470000, 54124120, 58547455, 58555555, 58888999, 21784, CG-4F2F67B8
- **Prove:** Banco offline:
- 11223344, 11155520, 11223355, 1470000, 58547455, 58555555 e 58888999 offline dalle 15:18-15:26 di ieri, tutti insieme;
- 54124120 dalle 13:20, con updater 'Couldn't connect';
- 11223344 ferma a SLIM-4.20.204 e fw 4.20.97.
21784:
- 12 transazioni ieri tra le 11:42 e le 19:15, 11 approvate;
- offline alle 10:28 e alle 19:01 (rientrata), poi definitivamente dalle 19:49 con updater 'Failed to connect' (2 fallimenti);
- alle 10:00 non ancora tornata.
Pi senza MHD 4f2f67b8 offline dall'11/11 08:54.
- **Ipotesi:** Banco spento per il fine settimana. 21784: rete instabile o accensione tardiva; non e' noto dove si trovi.
- **Proposta:** Maurizio/campo: MHD definitivi, centro e TID distinti prima della spedizione; test linea 8.4 su tutte.
Dire dove si trova la 21784.
Dashboard: marcare 'banco'.
- **Gia' noto:** GMI 'muta' / NCG senza bootloader (menu 9.5 ST-Link); golden SD (CG-<seriale>)

<a id="cg-022"></a>

### CG-022 · gmi_hostlink locked per 1-2 minuti a macchina accesa, senza riavvio: ieri solo 32995

- **Area:** pi · **Gravita':** low · **Visto:** 2026-11-12 → 2026-11-13
- **Macchine:** 24349, 25158, 36842, 24338, 28418, 23718, 32996, 25157, 28419, 32995
- **Prove:** 13/11: 32995 locked alle 12:42 e unlocked alle 12:43, senza reboot ne' app_restart. E' l'unico caso nelle 24 h.
12/11: 9 macchine (24349, 25158, 36842, 24338/28418, 23718, 32996, 25157, 28419).
Le coppie agli avvii e ai rollout sono normali e non sono incluse.
- **Ipotesi:** Il main loop del Pi resta fermo oltre 20 s (forse una chiamata bloccante POS o rete). La frequenza e' scesa, ma la causa resta ignota.
- **Proposta:** Maurizio:
- nei log di 32995 (12:42 di ieri) e di 24349/25158 cercare cosa fa il main loop;
- aggiungere all'evento la durata del blocco e l'ultima riga inviata.
- **Gia' noto:** Pagamenti bloccati perche' la GMI non sente il Pi (evento gmi_hostlink)

## In osservazione

<a id="cg-021"></a>

### CG-021 · Installazione Tiburtino Guidonia: 7 macchine in vendita, chiave 25355 sistemata; 25356 e 25357 senza vendite approvate ieri

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-12 → 2026-11-14
- **Macchine:** 33089, 25254, 25355, 25356, 25357, 33090, 33180
- **Prove:** Oggi tutte online: SLIM-4.20.200, fw 4.20.93, ramo mod5. Riaccese tra le 06:51 (25356) e le 08:54 (33090); 33089 stabile (reboot alle 07:58).
25355: chiave re-enrolled alle 11:15 di ieri, status ok.
Vendite 24 h:
- 33090: 9 (7 approvate);
- 25355: 6 (5);
- 33180: 6 (6);
- 33089: 4 (3);
- 25254: 3 (2);
- 25356: 1 carta annullata;
- 25357: 1 carta annullata.
25356 e 25357 sono IDLE con il POS connesso.
- **Ipotesi:** Installazione assestata. Le poche vendite su 25356 e 25357 sono probabilmente dovute al traffico. Non confermato.
- **Proposta:** Campo Tiburtino:
- vendita di prova su 25356 e 25357;
- test linea 8.4 su tutte.
- **Gia' noto:** Profilo display auto / golden SD; GMI 'muta' / NCG senza bootloader

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
