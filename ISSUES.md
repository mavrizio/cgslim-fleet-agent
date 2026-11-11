# Registro problemi flotta CGSLIM

Aggiornato dall'agente il 11/11/2026 10:03. Una voce per causa; MHD senza zeri. Generato: non modificare a mano.

## Aperti

<a id="cg-003"></a>

### CG-003 · POS DISCONNECTED dopo timeout get_advanced_config: 24350, 37008 e 33326 al settimo giorno, resiste a reboot e aggiornamenti

- **Area:** pi · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-11
- **Macchine:** 24350, 37008, 33326, 11223344, 11155520, 11223355, 28416, 24338
- **Prove:** Avviso 'POS in errore su 6 macchine' (Timeout locale get_advanced_config 15 s) aperto dal 10/11 09:17 UTC.
Macchine in campo/beta, oggi alle 09:5x:
- 24350: DISCONNECTED dopo il reboot delle 09:13; 5 vendite cash ieri, nessun tentativo carta.
- 37008: DISCONNECTED anche dopo il restart della 192 (13:22) e il flash delle 13:25; 4 vendite cash.
- 33326: DISCONNECTED con SLIM-4.20.194.
Le altre 3 sono di banco: 11155520 e 11223344 DISCONNECTED, 11223355 IDLE ma con p95_error e senza acquirer letti.
'Connessione persa durante get_advanced_config', tutte rientrate entro 15 min:
- 24338 alle 12:17 UTC;
- 5 macchine alle 12:32 UTC (durante il rollout);
- 28416 alle 07:47 UTC di oggi.
- **Ipotesi:** Dopo un timeout della lettura cashless_info il pos-engine resta DISCONNECTED senza ritentare. Ne' il reboot del Pi ne' le release 192/194 lo correggono.
I casi 'Connessione persa' sono transitori legati ai riavvii dell'app.
- **Proposta:** Maurizio:
- Un errore di get_advanced_config non deve bloccare il P95: saltare la lettura e ritentarla con backoff.
- Nascondere la carta a POS DISCONNECTED.
- Escludere dall'avviso i device di banco.
- Log di pos-engine della 24350 dopo le 09:13.
Campo Parma: spegnere e riaccendere il POS della 24350 e provare una carta reale.
- **Gia' noto:** POS: get_advanced_config

<a id="cg-006"></a>

### CG-006 · 36842 senza parametri bancari (TID 00000000, codice 20 ancora ieri); TID di prova 97942484 su 3 terminali

- **Area:** pos · **Gravita':** high · **Visto:** 2026-10-30 → 2026-11-10
- **Macchine:** 36842, 24338, 23718, 28418, 33326, 11223344, 11223355
- **Prove:** 36842:
- 10/11 18:09: un pagamento carta 'POS non configurato (codice 20)', unica transazione nelle 24 h;
- TID 00000000, nessun acquirer, package 01.04.25.03;
- nessuna carta approvata nello storico.
TID di prova:
- 97942484 sulla 23718 e sui terminali di banco 11223344 (SN 58795085) e 11223355 (SN 58794857, nessun acquirer letto);
- 24338 97942485, 28418 97942488.
Codice 90 sulle macchine di banco: 11223355 alle 14:46 e alle 09:15, 11155520 alle 15:59, 11223344 alle 16:11.
- **Ipotesi:** Senza parametri ogni carta sulla 36842 fallisce.
Lo stesso TID su piu' terminali puo' dare errore 48 (caso noto della 24338) se sono attivi insieme.
- **Proposta:** Hardware/POS:
- Parametrizzare la 36842 con il TID di produzione.
- Assegnare TID distinti ai terminali di banco prima di spedirli.
Maurizio: nascondere la carta con TID 00000000 o senza acquirer.
- **Gia' noto:** POS: altri errori (errore 48, TID duplicato su 24338)

<a id="cg-007"></a>

### CG-007 · 32996 e 36842: vendite quasi nulle; oggi 32996 a tramogge 1,1,0, 36842 a 0,1,0 e schermata 72

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-01 → 2026-11-11
- **Macchine:** 32996, 36842, 23718
- **Prove:** 11/11 alle 09:5x:
- 32996: tramogge 1,1,0, schermata 70 (come le altre Parma);
- 36842: tramogge 0,1,0, schermata 72.
Vendite del 10/11:
- 32996 nessuna transazione;
- 36842 solo 1 carta fallita (codice 20);
- le altre Parma: 25158 9, 24350 5, 24349 5, 28417 3, 32995 3, 25157 2 (annullate), 28416 1, 28419 1.
23718: ancora 0,0,0, schermata 46, 0 transazioni.
37008: 1,0,0, schermata 71, 4 vendite.
- **Ipotesi:** Con il martedi' le altre Parma sono tornate a vendere, mentre 32996 e 36842 no: il traffico basso non spiega piu' la differenza.
Sulla 36842 la tramoggia 1 non risulta presente. Per la 32996 non e' chiaro cosa impedisca la vendita.
Non confermato.
- **Proposta:** Campo Parma, oggi:
- Display e menu tecnico su 32996 e 36842.
- Controllare le tramogge.
- Provare una vendita cash.
Maurizio: chiarire cosa indicano le schermate 72 e 73 e se la GMI ripete #HPS dopo l'avvio.

<a id="cg-009"></a>

### CG-009 · 24254 (Aprilia): accensione tardiva e arresto serale per la decima sera, zero vendite

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-02 → 2026-11-11
- **Macchine:** 24254
- **Prove:** 10/11:
- 12:58: reboot (uptime 138), dopo le altre Aprilia (05:41-07:30 di oggi).
- 13:02: POS 'activate gia' in corso' (12:02 UTC).
- 13:23 e 13:27: aggiornata a 192 e fw 4.20.92 senza problemi.
- Sottotensione ADESSO 7 volte tra le 13:02 e le 19:02.
- 19:58: ultimo report, decima sera di fila con arresto.
11/11 alle 10:00: offline da 841 min, non ripartita.
Nessuna transazione nelle 24 h; ultima carta approvata il 05/11.
- **Ipotesi:** Alimentazione debole o interrotta: sottotensione per tutto il pomeriggio, poi spegnimento serale. L'accensione tardiva fa pensare a una presa o un timer diversi dalle altre Aprilia, oppure a un'accensione manuale.
Non confermato.
- **Proposta:** Campo Aprilia, oggi:
- Riaccendere la macchina.
- Verificare presa e timer.
- Sostituire l'alimentatore del Pi.
- Fare una vendita di prova cash e carta.
- Recuperare journal e dmesg del 10/11 attorno alle 19:58.

<a id="cg-001"></a>

### CG-001 · Aggiornamento firmware GMI: rollout 4.20.92 ok, 26087 bloccata 1,5 h per corruzione al byte 26880

- **Area:** firmware · **Gravita':** medium · **Visto:** 2026-10-30 → 2026-11-10
- **Macchine:** 26087, 33326, 24338
- **Prove:** 10/11, fw_change 4.20.90->4.20.92:
- 13:23-13:28 riuscito su 24349, 24350, 24866, 25157, 25158, 28416, 28417, 28419, 29598, 32995, 32996, 33957, 36842, 37008, 23718, 24254;
- 29597 alle 14:26.
26087:
- 13:21: eccezione RDY;
- 13:33: gmi_flash_failed 'CORRUZIONE DATI PERSISTENTE al byte 26880 dopo 20 tentativi', 15 tentativi, gmi_blocked;
- 14:56: reboot (uptime 31), di nuovo RDY, app_down;
- 15:02: fw_change ok.
Oggi 26087 e' a 4.20.92, MOD 12, schermata 70, 5 vendite ieri (ultima alle 19:49).
Eccezioni RDY 'T\xffRDY...' anche su 29598, 24866 e 33957 (13:21-13:24), che hanno poi flashato regolarmente.
33326 (V1 debug): flash ok alle 13:03 (4.20.92) e alle 19:48 (4.20.93).
24338 (bootloader sconosciuto): flash ok alle 13:10 e alle 21:50.
- **Ipotesi:** Il caso noto di linea disturbata durante il bootloader: con 20 ritrasmissioni allo stesso offset sembra un disturbo sistematico (GMI verde?) piu' che un byte spurio isolato. Non si sa cosa abbia provocato il reboot delle 14:56.
Le eccezioni RDY durante un flash voluto sono rumore.
I bootloader non standard di 33326 e 24338 per ora funzionano.
- **Proposta:** Maurizio:
- Recuperare il log del gitpuller/flash della 26087 delle 13:20-15:02 e verificare se la GMI e' verde.
- Non segnalare come eccezione il RDY atteso durante un flash pianificato.
Campo Aprilia: test linea 8.4 sulla 26087.
Bootloader V2 su 33326 e 24338 resta consigliato, ma non e' urgente.
- **Gia' noto:** Aggiornamento firmware GMI che fallisce (gmi_flash_failed, gmi_blocked, loop RDY)

<a id="cg-004"></a>

### CG-004 · Seriale GMI assente all'accensione (FTDI non enumerato), cavi lotto BG03E: oggi solo la 25158

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-11
- **Macchine:** 25158, 32996
- **Prove:** 11/11, 25158 (BG03ES5F):
- 09:22: reboot (uptime 112), eccezione 'could not open port /dev/ttyUSB0' e serial_missing not_enumerated (USB: solo hub, ethernet e ILITEK);
- 09:26: reboot di recovery (uptime 40);
- 09:27: serial_recovery.
La 25158 e' a 5 mattine su 6 (06, 08, 09, 10 e 11/11).
32996 (BG03ER1N) oggi pulita: reboot alle 09:04, nessun serial_missing.
Cavo della 25158 non ancora scambiato.
- **Ipotesi:** Lotto FT232R BG03E e/o alimentazione a ritroso dalla GMI. Il recovery funziona e costa circa 5 minuti.
- **Proposta:** Campo Parma: scambiare il cavo della 25158 con uno AL05 e lasciare la 32996 come controllo.
Pi: nel prossimo rilascio riavvio anticipato (~30-40 s), uhubctl e TX della GMI in high-Z.
- **Gia' noto:** Seriale assente al mattino (serial_missing, not_enumerated)

<a id="cg-005"></a>

### CG-005 · Sottotensione del Raspberry: 24349 peggiorata (15 episodi ieri, anche adesso), 23718 fissa, 24254 a episodi

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-11
- **Macchine:** 24349, 23718, 24254, 24350, 24338, 11223355
- **Prove:** Avvisi undervoltage_now del 10/11, orari UTC:
- 24349: 15 episodi (10:47, 12:02, 12:32, 14:17, 14:47, 15:17, 15:47, 16:47, 17:32, 18:17, 19:32, 20:17, 21:32, 22:02, 22:47). Oggi alle 09:48 locali di nuovo 0x50005, a 33 min dal boot.
- 24254: 7 episodi (12:02, 13:32, 14:32, 15:17, 16:02, 17:17, 18:02).
- 23718: 0x50005 fissa, avviso aperto dal 03/11.
- 24338 e 24350: 0x50000.
- 11223355 (banco): una volta alle 13:47.
Le altre a 0x0; 37008 a 0x80000.
- **Ipotesi:** Alimentatori o cavi deboli. Sulla 24349 il problema e' peggiorato (da 5 a 15 episodi al giorno).
- **Proposta:** Hardware/campo, in ordine:
1. 24254 (insieme a CG-009).
2. 24349.
3. 23718.
4. 24350 e 24338.
- **Gia' noto:** host.throttled 0x50000 (scheda campi); sottotensione sospettata nei flash GMI falliti

<a id="cg-014"></a>

### CG-014 · MOD inattesa su branch mod5: 24866 mod 12 col Pi nuovo, 23718 ora mod 1 senza vendite

- **Area:** firmware · **Gravita':** medium · **Visto:** 2026-11-05 → 2026-11-07
- **Macchine:** 24866, 23718
- **Prove:** 24866 (branch mod5):
- device nuovo a mod 12, screen 70, hopper 1,1,0;
- il device vecchio riportava mod 2, screen 40;
- 06/11: reboot fuori orario alle 12:25 e alle 14:00 (uptime ~60), con gmi_hostlink locked/unlocked ripetuti (12:27-12:30, 13:52, 14:01-14:05): probabile intervento sul posto;
- 40 transazioni, 11 approvate.
23718 (branch mod5):
- ora mod 1, screen 46, hopper 0,0,0;
- ieri era mod 4, screen 23;
- nessuna transazione nelle 24 h;
- riavviata alle 21:49 del 06/11.
- **Ipotesi:** Su 24866 la modalita' e' stata probabilmente reimpostata dal tecnico durante l'intervento del 06/11.
Su 23718 la MOD cambia tra un report e l'altro: macchina di prova, oppure valore non affidabile. Mod 1 e mod 4 non sono nella scheda.
- **Proposta:** Maurizio: chiarire quali MOD sono attese per 24866 e 23718.
Campo:
- Aprilia: confermare la MOD di 24866 dal menu tecnico.
- 23718: verificare se e' una macchina di prova o in servizio.

<a id="cg-019"></a>

### CG-019 · GMI NCG4.09 al banco (device a9603f2d, cavo BG04MVBD): la flash non si cancella ne' via bootloader seriale ne' via ST-Link

- **Area:** firmware · **Gravita':** medium · **Visto:** 2026-11-10 → 2026-11-10
- **Macchine:** a9603f2d
- **Prove:** 10/11, device CG-A9603F2D senza MHD:
- 14:09: first_seen; 14:11 gmi_mute;
- 14:15: stlink_program fallito (step probe, 'target was in unknown state when halt was requested');
- 14:16-15:41: eccezioni RDY loop;
- 14:25, 14:48, 15:02 e 15:51: gmi_flash_failed 'Timeout o fallimento cancellazione flash', 15 tentativi ciascuno, gmi_blocked;
- 16:04 e 16:29: gmi_mute NCG4.09 no_bootloader;
- 16:07-16:36: 8 stlink_program falliti, su probe ed erase_app;
- 16:25: serial_missing con solo l'STLink sul bus, serial_back dopo 65 s.
Oggi il device con fw 4.09, uptime 62732 s e schermata 29 e' probabilmente lo stesso: l'uptime e' compatibile col reboot delle 16:29.
- **Ipotesi:** Flash protetta in scrittura (option bytes WRP/RDP) oppure GMI guasta o alimentata male, dato che falliscono le cancellazioni con entrambi i metodi.
Non e' chiaro perche' prima rispondesse con RDY e dopo si presentasse come NCG4.09 senza bootloader.
- **Proposta:** Maurizio/banco:
- Leggere gli option bytes con STM32CubeProgrammer, fare mass erase e controllare i 3,3 V.
- Se fallisce ancora, sostituire la GMI.
Maurizio:
- Aggiungere la lettura degli option bytes alla diagnostica stlink_program.
- Interrompere i cicli di flash seriale dopo il primo gmi_blocked (ieri 4 cicli da 15 tentativi).
- **Gia' noto:** GMI 'muta' / NCG senza bootloader (menu 9.5 ST-Link)

<a id="cg-011"></a>

### CG-011 · Dashboard: doppione 24866 sparito; restano centro null, chiave 33326 e i device di banco nel conteggio

- **Area:** dashboard · **Gravita':** low · **Visto:** 2026-11-04 → 2026-11-11
- **Macchine:** 23718, 24338, 28418, 33326, 37008
- **Prove:** - L'avviso offline del vecchio device 24866 (b7233887) e' chiuso dal 10/11 14:02 UTC; nell'elenco c'e' una sola 24866.
- 33326: nuovo device_key_mismatch il 10/11 alle 16:42, stato 'mismatch'.
- Centro null per 23718, 24338, 28418, 33326 e 37008.
- Conteggio flotta 28: 21 macchine reali, 3 con MHD provvisorio (11223344, 11223355, 11155520) e 4 Pi senza MHD (vedi CG-018).
- **Ipotesi:** Il doppione e' stato rimosso o archiviato. Il conteggio e' gonfiato dalle macchine in preparazione.
- **Proposta:** Dashboard/Maurizio:
- Escludere da conteggio e avvisi i device senza MHD o marcati 'banco'.
- Ri-registrare la chiave della 33326.
- Assegnare il centro (o 'banco') alle 5 macchine.
- **Gia' noto:** Profilo display auto / golden SD (hostname clonati, chiave fleet rigenerata)

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

### CG-016 · Contatori errori seriali lato GMI: 29598 ripete ne ~100 nelle prime 3 h; altri azzerati dal flash

- **Area:** hardware · **Gravita':** low · **Visto:** 2026-11-06 → 2026-11-11
- **Macchine:** 29598, 37008, 23718, 28418
- **Prove:** 29598: ne=95 con uptime 11030 s, di nuovo circa 3 h dopo l'accensione delle 06:45 (giorni prima 118-163).
I flash 4.20.92 del 10/11 hanno riavviato le GMI e azzerato i contatori:
- 37008: ore 36 (era 229);
- 23718: fe 17, ne 3, ore 33 (era fe 66, ore 70).
28418 offline dal 09/11, ultimo valore fe 24, ne 18, ore 63.
- **Ipotesi:** 29598: rumore sistematico nelle prime ore (cavo A10KIK4A, massa o GMI verde).
Su 37008 e 23718 serve vedere se la crescita riparte dopo l'azzeramento.
- **Proposta:** Campo Aprilia: test linea 8.4 sulla 29598.
Maurizio: inviare i contatori come delta giornaliero.
- **Gia' noto:** Aggiornamento firmware GMI (linea disturbata GMI verdi)

<a id="cg-018"></a>

### CG-018 · Preparazione di macchine nuove al banco (golden + ST-Link): 11223344 (ex CG-87AD39CF), 11223355, 11155520 e 4 Pi senza MHD

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-09 → 2026-11-11
- **Macchine:** 11223344, 11223355, 11155520, CG-4F2F67B8, CG-E398A14E, CG-0C7892A3, 7a9fd21f
- **Prove:** 11223344 (CG-87AD39CF, device 87ad39cf, cavo BG04MUZY):
- provisioning GIT_BRANCH applicato il 10/11 alle 10:28 UTC, ora branch beta;
- SLIM 190->191->192->193->194 e fw 4.20.90->92->93 (19:11);
- app_restart_storm 5 in 6 h;
- 6 transazioni di prova tra le 16:05 e le 16:12.
11223355 (CG-12BD7042):
- first_seen alle 13:16, stlink_program 4.20.92 ok alle 13:22, gmi_init_ok alle 13:27;
- 6 reboot tra le 13:55 e le 09:22, reboot_storm;
- 20 transazioni.
11155520 (CG-5DC2D8FC): first_seen alle 14:56, ST-Link ok alle 15:01, gmi_init_ok alle 15:43, 8 transazioni.
Pi senza MHD, tutti con cavi BG04M*:
- CG-4F2F67B8: offline dalle 08:54;
- CG-E398A14E e CG-0C7892A3: gmi_mute;
- un Pi con GMI 4.09 (vedi CG-019).
7a9fd21f non compare nei dati di oggi.
- **Ipotesi:** Lotto di macchine nuove in preparazione. Gli MHD 11223344, 11223355 e 11155520 sembrano provvisori. Riavvii e restart frequenti sono attivita' di banco, non guasti.
- **Proposta:** Maurizio/campo: assegnare MHD definitivi e centro prima della spedizione e fare il test linea 8.4 su ognuna.
Dashboard: marcarle 'banco' ed escluderle da avvisi e conteggio.
- **Gia' noto:** GMI 'muta' / NCG senza bootloader (menu 9.5 ST-Link); golden SD (CG-<seriale>)

## In osservazione

<a id="cg-012"></a>

### CG-012 · POS non pronto subito dopo l'avvio: 'gia' in corso', Broken pipe, codice 90

- **Area:** pi · **Gravita':** medium · **Visto:** 2026-11-04 → 2026-11-10
- **Macchine:** 24254, 28418, 33957, 24866, 29597
- **Prove:** 10/11: sulla 24254 avviso 'Operazione activate gia' in corso' alle 13:02 locali, 4 minuti dopo il reboot delle 12:58. Nessuna transazione coinvolta.
29597 ieri: 11 transazioni, 10 approvate, nessun errore POS.
Codice 90 solo sulle macchine di banco (vedi CG-006).
- **Ipotesi:** Stessa corsa all'avvio tra activate, lettura cashless_info e pagamento. Oggi non ha toccato clienti.
- **Proposta:** Maurizio: carta disabilitata finche' il POS non e' IDLE e cashless_info non ha finito.
Chiudere se non ricompare con pagamenti nei prossimi giorni.
- **Gia' noto:** POS: get_advanced_config (operazione gia' in corso)

<a id="cg-017"></a>

### CG-017 · 33957 (Carpi): nessun errore carta nelle 24 h, ma una sola vendita

- **Area:** hardware · **Gravita':** low · **Visto:** 2026-11-07 → 2026-11-09
- **Macchine:** 33957
- **Prove:** 10/11:
- 1 transazione, cash alle 11:30;
- nessun tentativo carta, quindi nessun codice 90/31/04;
- aggiornata a 192 (13:21) e fw 4.20.92 (13:25);
- gitlab 502/connect failed alle 14:22, rientrato alle 14:26;
- telemetria fino alle 20:26.
Oggi: reboot alle 09:00, POS IDLE, TID 75645530, rssi -53.
- **Ipotesi:** La rete sembra stabile. Con nessun tentativo carta non si puo' dire se il codice 90 di fine mattina sia sparito.
- **Proposta:** Tenere sotto osservazione ancora 2-3 giorni.
Campo Carpi: chiedere se il calo di vendite e' normale per il sito.

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
