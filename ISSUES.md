# Registro problemi flotta CGSLIM

Aggiornato dall'agente il 02/11/2026 10:04. Una voce per causa; MHD senza zeri. Generato: non modificare a mano.

## Aperti

### CG-001 · Aggiornamento firmware GMI fallito: 33326 bloccata (errore 98), loop RDY su 26087 e 29597

- **Area:** firmware · **Gravita':** high · **Visto:** 2026-10-30 → 2026-11-02
- **Macchine:** 33326, 26087, 29597
- **Prove:** 33326 (beta2), report delle 09:57 del 02/11:
- gmi_blocked ancora attivo dal 01/11 09:36: 15 tentativi con CGT-4.20.84.bin, 'Timeout ACK al blocco 7808'.
- Fw riportato 4.20.82, mod 0, screen 29, hopper e contatori GMI null.
- Uptime 251474 s (~70 h): nessun riavvio e nessun intervento.
Il 30/10 il flash di CGT-4.20.83.bin era gia' fallito al blocco 44544.
Sottotensione: undervoltage_now si e' aperto e chiuso piu' di 15 volte dal 01/11 11:31 al 02/11 08:02 (ora locale) ed e' aperto adesso (throttled 0x50005). Pi 3 Model B Rev 1.2.
I loop RDY di 26087 e 29597 del 01/11 sono rientrati: oggi entrambe hanno fw 4.20.84 e funzionano.
- **Ipotesi:** Problema noto del bootloader V2. Il flash fallisce a blocchi diversi (44544, poi 7808) e c'e' una sottotensione intermittente continua. La causa piu' probabile e' l'alimentazione del Pi o un disturbo di linea, non un file corrotto. Il colore della GMI non e' noto.
- **Proposta:** Campo/hardware:
- Sostituire l'alimentatore del Pi di 33326.
- Spegnere e riaccendere GMI e Pi per uscire dall'errore 98.
- Annotare il colore della GMI.
- Se il flash fallisce ancora: flash manuale con ST-Link.
Pi: rimandare il flash della GMI quando il bit 0x1 di throttled e' attivo; registrare throttled e il numero del blocco al momento del Timeout ACK.
- **Gia' noto:** Aggiornamento firmware GMI che fallisce (gmi_flash_failed, gmi_blocked, loop RDY)

### CG-002 · 36842 offline dal 31/10 20:21 e non riaccesa (secondo mattino)

- **Area:** campo · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-02
- **Macchine:** 36842
- **Prove:** Stato attuale:
- Ultimo report 31/10 20:21, offline da 2258 min alle 10:00 del 02/11.
- Le altre 9 Parma oggi si sono riaccese tra le 08:26 (25157) e le 09:23 (25158).
Ultimo payload:
- uptime 140 s;
- throttled 0x50005;
- GMI fe=138 (le altre Parma 3-7);
- SLIM-4.20.172, fw 4.20.83;
- TID POS 00000000;
- p95_error: timeout get_advanced_config.
Nessun intervento risulta fatto.
- **Ipotesi:** Alimentazione insufficiente: c'era sottotensione in corso piu' molti errori di frame lato GMI. In alternativa un guasto di rete o del router. I dati non permettono di distinguere.
- **Proposta:** Campo Parma oggi:
- Verificare se la macchina e' accesa e cosa mostra lo schermo.
- Controllare alimentatore, cavo del Pi e router.
- Recuperare journal e dmesg dal 31/10 20:20.
Al ritorno, verificare l'aggiornamento a SLIM-4.20.176 e fw 4.20.84.

### CG-003 · POS DISCONNECTED dopo timeout get_advanced_config: carte non accettate (7 macchine)

- **Area:** pi · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-02
- **Macchine:** 24254, 24866, 26087, 29597, 29598, 24350, 37008, 36842
- **Prove:** Stato del POS alle 09:46-09:58 del 02/11:
- DISCONNECTED con 'Timeout locale in attesa di get_advanced_config (15.0s)': 24350, 24866, 26087, 29597, 29598, 37008.
- Stesso errore nell'ultimo payload di 24254 (offline dalle 20:43) e di 36842.
- Il riavvio di stamattina non l'ha risolto: 24866 05:42, 29598 06:45, 29597 06:52, 26087 07:30, 24350 09:12.
- Su queste macchine il payload non ha mai i dati p95 (TID, package), quindi la lettura non e' mai riuscita.
- 24349 e' tornata IDLE e connessa dopo il riavvio delle 09:18.
Pagamenti carta nelle 24 h sulle macchine DISCONNECTED: 24 tentativi, 0 approvati.
- 29597: 10 (8 cancelled, 2 timeout);
- 37008: 5 (3 cancelled, 2 timeout);
- 29598: 4 (3 cancelled, 1 timeout);
- 26087: 3 (1 cancelled, 2 timeout);
- 24350: 1 cancelled;
- 24254: 1 cancelled.
Sulle macchine connesse: 28417 2 approvati, 25158 1 approvato, 32996 1 cancelled.
- **Ipotesi:** Problema noto della lettura cashless_info (v.171+), con effetto bloccante. Su certi terminali get_advanced_config non risponde mai; dopo il timeout il pos-engine resta DISCONNECTED e i pagamenti carta falliscono. I 'cancelled' e i 'timeout' sono probabilmente tentativi abortiti, non scelte dei clienti: il rapporto 0/24 contro 3/4 lo rende molto probabile. Resta da capire perche' solo questi terminali non rispondono (package o firmware del POS, oppure rete del centro di Aprilia).
- **Proposta:** Maurizio, urgente:
- In core/cashless_info.py, un errore di get_advanced_config non deve chiudere ne' bloccare la connessione P95. Va saltato e ritentato con backoff a POS libero.
- Rilasciare su mod12, parma, mod5 e beta2.
- Prima verificare su 26087 o 29597 con i log di pos-engine: perche' la connessione non si ristabilisce dopo il timeout?
Campo Aprilia: prova con carta reale dopo la hotfix.
- **Gia' noto:** POS: get_advanced_config

### CG-009 · 24254 (Aprilia) offline dal 01/11 20:43, non riaccesa al mattino

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-02 → 2026-11-02
- **Macchine:** 24254
- **Prove:** Ultimo report 01/11 20:43, offline da 796 min alle 10:00.
Le altre Aprilia hanno trasmesso fino alle 23:13-23:51 e si sono riaccese tra le 05:42 (24866) e le 07:30 (26087).
Ultimo payload:
- uptime 39211 s (avvio verso le 09:50 del 01/11);
- throttled 0x50000;
- GMI fe=13 e ore=6, piu' alti delle vicine;
- POS DISCONNECTED;
- LTE rssi -64.
Vendite 01/11: 2 cash approvate, l'ultima alle 18:22.
Anche 24866 risulta senza report dalle 15:52 del 01/11 ma con vendite fino alle 18:10: possibile problema di rete nel centro.
- **Ipotesi:** Simile a 36842: smette di trasmettere la sera prima della chiusura e non si riaccende. Le cause possibili sono alimentazione (sottotensione dal boot), rete o router LTE, oppure blocco del Pi. Dai dati non si distingue.
- **Proposta:** Campo Aprilia:
- Verificare se e' accesa, cosa mostra lo schermo e lo stato di router e alimentatore.
- Recuperare journal e dmesg dal 01/11 20:40.
Se il Pi e' acceso ma non trasmette, controllare fleet-reporter e la connessione LTE.

### CG-004 · Seriale GMI assente all'accensione (FTDI non enumerato), cavi lotto BG03E

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-02
- **Macchine:** 25158, 32996
- **Prove:** 02/11, 32996 (cavo BG03ER1N):
- avvio 09:03 (uptime 113 s), serial_missing not_enumerated ed eccezione 'could not open port /dev/ttyUSB0';
- sul bus solo gli hub 0424:2514, la LAN 0424:7800 e il touch ILITEK;
- reboot di recupero alle 09:07 (uptime 59), serial_recovery registrato alle 09:08.
02/11, 25158 (cavo BG03ES5F):
- avvio 09:23 (uptime 114), serial_missing ed eccezione;
- reboot alle 09:26 (uptime 59), serial_recovery alle 09:28.
Entrambe ora sono a posto (contatori GMI e hopper presenti) con 1 recupero su 2.
25158 ha il problema per il secondo giorno di fila. Nessuna altra macchina ce l'ha (cavi AL05, A10, A906, BG04M, AK05, AG0J, AJ03).
- **Ipotesi:** Problema noto: lotto di cavi FT232R BG03E difettoso, e/o chip FTDI alimentato a ritroso dalla GMI. Oggi il lotto e' stato colpito al 100%.
- **Proposta:** Campo Parma: scambiare il cavo della 25158 con uno AL05 e lasciare 32996 come controllo.
Pi: nel prossimo rilascio importante riavvio anticipato (~30-40 s), uhubctl e TX della GMI in high-Z.
- **Gia' noto:** Seriale assente al mattino (serial_missing, not_enumerated)

### CG-005 · Sottotensione del Raspberry (alimentatori/cavi): 33326 continua, 24349 intermittente

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-02
- **Macchine:** 33326, 36842, 24349, 24350, 24338, 24254, 26087
- **Prove:** 33326: sottotensione in corso (0x50005) a intermittenza per tutta la notte, con piu' di 15 aperture dell'alert dalle 11:31 del 01/11; aperto ora.
24349: il 01/11 0xd0005 (sottotensione in corso) alle 17:17, 18:17 e 21:17 ora locale; oggi 0x50000 gia' 33 min dopo l'avvio delle 09:18.
24350: 0x50000 subito dopo l'avvio delle 09:12.
24338: 0x50000 (uptime ~69 h).
24254: 0x50000 nell'ultimo report.
36842: 0x50005 nell'ultimo report.
26087: oggi 0x0 dopo l'avvio delle 07:30 (ieri 0x50000).
Le altre macchine sono a 0x0.
- **Ipotesi:** Alimentatori o cavi deboli. Le due macchine ferme piu' gravi (33326 e 36842) sono quelle con sottotensione in corso. Anche 24254, non riaccesa stamattina, aveva sottotensione dal boot.
- **Proposta:** Hardware/campo:
- Sostituire subito gli alimentatori di 33326 e 36842.
- Poi 24349 (sottotensione attiva in giornata), 24350, 24254 e 24338.
- 26087 tenerla sotto osservazione.
- **Gia' noto:** host.throttled 0x50000 (scheda campi); sottotensione sospettata nei flash GMI falliti

### CG-006 · TID POS anomali: 36842 senza TID, 24338 e 33326 con TID duplicato

- **Area:** pos · **Gravita':** medium · **Visto:** 2026-10-30 → 2026-11-01
- **Macchine:** 36842, 24338, 33326
- **Prove:** 36842 (Parma, produzione): TID 00000000, package PYP-SELF2000 01.04.25.03 (le altre Parma hanno 01.04.02), SN 58551425; lettura del 31/10 00:21; nessuna transazione carta nelle 24 h. 24338 e 33326 riportano lo stesso TID 97942485 su terminali diversi (SN 58795528 e 53818418). 24338: ultimo errore 48 il 30/10 alle 13:21; il POS di 33326 era attivo e letto il 30/10 alle 14:06.
- **Ipotesi:** Il terminale della 36842 non e' parametrizzato (forse dopo un cambio POS o un aggiornamento del package): la carta non puo' funzionare. Il TID duplicato e' una causa nota di errore 48.
- **Proposta:** Hardware/POS: far parametrizzare la 36842 con il TID di produzione; assegnare TID distinti a 24338 e 33326.
- **Gia' noto:** POS: altri errori (errore 48, TID duplicato su 24338)

### CG-007 · Tramogge 0,0,0 e schermata 73 dopo l'avvio (25158, 24350)

- **Area:** campo · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-02
- **Macchine:** 25158, 24350
- **Prove:** 02/11, ore 09:58:
- 25158 e 24350 hanno hopper ['0','0','0'] e screen 73; le altre Parma MOD12 hanno ['1','0','0'] e screen 71.
- 24350 si e' avviata alle 09:12 senza problemi di seriale. 25158 si e' avviata alle 09:23 ed e' passata dal recupero seriale.
Il 01/11 25158 era nello stesso stato, poi ha venduto: 5 vendite dalle 13:20 alle 19:13, 1 con carta approvata alle 13:21.
Stamattina nessuna Parma ha ancora vendite, quindi l'assenza di vendite oggi non e' significativa.
- **Ipotesi:** Non e' legato al recupero seriale, perche' 24350 non l'ha avuto. Puo' essere uno stato della GMI dopo l'avvio che poi si sblocca, oppure la tramoggia 1 vuota e ricaricata in seguito. Il significato di screen 73 non e' nella scheda.
- **Proposta:** Maurizio: chiarire cosa indica screen 73 e quando la GMI manda #HPS 0,0,0.
Campo Parma: controllare tramogge e schermo di 24350 e 25158 durante la visita.

### CG-008 · Branch riportato 'parma' ma servizio gitpuller@beta su 3 macchine Aprilia

- **Area:** dashboard · **Gravita':** low · **Visto:** 2026-11-01 → 2026-11-01
- **Macchine:** 26087, 29597, 29598
- **Prove:** 26087, 29597 e 29598 risultano con branch parma, ma il servizio attivo e' gitpuller@beta. git_commit 9bf05a7, diverso da mod12 (65f8fdf) e da beta2 (b189183). Oggi hanno comunque ricevuto SLIM-4.20.176 e fw 4.20.84.
- **Ipotesi:** Lettura del branch errata nel fleet-reporter o nella dashboard, oppure nome dell'istanza gitpuller non coerente con il branch seguito.
- **Proposta:** Su una macchina, verificare il branch reale del repo (git rev-parse --abbrev-ref HEAD) e correggere l'unita' gitpuller oppure il campo riportato.
