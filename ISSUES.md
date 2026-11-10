# Registro problemi flotta CGSLIM

Aggiornato dall'agente il 10/11/2026 10:03. Una voce per causa; MHD senza zeri. Generato: non modificare a mano.

## Aperti

<a id="cg-003"></a>

### CG-003 · POS DISCONNECTED dopo timeout get_advanced_config: fisso su 24350 e 37008 da 6 giorni, 33326 DISCONNECTED anche con la 191

- **Area:** pi · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-10
- **Macchine:** 24350, 33326, 37008, 24866, 24349, 25158, 36842, 26087, 29597, 29598, 28418, 28416, 24338, 23718, 32996, 24254
- **Prove:** 10/11 ~10:00:
- 24350: DISCONNECTED con 'Timeout locale in attesa di get_advanced_config (15.0s)' dopo il reboot delle 09:12 (uptime 2906 s). Nessuna transazione nelle 24 h.
- 37008: stesso errore, uptime 457298 s (circa 127 h). Ieri 8 vendite cash.
- 33326: DISCONNECTED senza testo di errore. E' passata a SLIM-4.20.190 il 09/11 alle 19:52 e a 4.20.191 oggi alle 09:55 senza tornare IDLE (l'ultimo report e' di 1 minuto dopo il riavvio). Il suo avviso pos_error e' rimasto aperto dal 09/11 23:32 UTC al 10/11 08:17 UTC.
Avviso 'POS in errore su 3 macchine' riaperto oggi alle 08:17 UTC. Il vecchio device della 24866 (offline dal 06/11) porta ancora un p95_error vecchio: potrebbe essere contato fra le 3.
Nessun caso 'Connessione persa' nelle 24 h.
- **Ipotesi:** Quando la lettura cashless_info va in timeout, il pos-engine resta DISCONNECTED senza ritentare, anche dopo un reboot del Pi. Lo stato del terminale persiste, oppure la prima lettura fallisce sempre su quei terminali.
Il conteggio dell'avviso puo' includere il device fantasma della 24866.
- **Proposta:** Maurizio:
- Un errore di get_advanced_config non deve bloccare il P95: saltare la lettura e ritentarla con backoff.
- Nascondere la carta a POS DISCONNECTED.
- Escludere dall'avviso i device offline.
- Recuperare i log di pos-engine della 24350 dopo le 09:12.
- Controllare 33326 con la 191 tra qualche minuto.
Campo Parma: spegnere e riaccendere il POS della 24350 (non solo il Pi) e provare una carta reale.
- **Gia' noto:** POS: get_advanced_config

<a id="cg-006"></a>

### CG-006 · 36842: terminale non parametrizzato (TID 00000000), la carta resta proposta ai clienti

- **Area:** pos · **Gravita':** high · **Visto:** 2026-10-30 → 2026-11-10
- **Macchine:** 36842, 24338, 23718, 28418, 33326
- **Prove:** 36842 oggi:
- POS IDLE;
- TID 00000000, nessun acquirer;
- package 01.04.25.03, SN 58551425.
Nelle 24 h nessuna transazione, quindi nessun nuovo codice 20. L'ultimo ko e' dell'08/11 alle 20:39 (codice 20) e non c'e' nessuna carta approvata nello storico.
TID di prova 9794248x invariati: 24338 97942485, 23718 97942484, 28418 97942488.
33326: POS DISCONNECTED, TID non leggibile.
- **Ipotesi:** Senza parametri bancari ogni pagamento carta sulla 36842 fallisce. Oggi non ci sono tentativi perche' la macchina non ha venduto nulla (vedi CG-007).
- **Proposta:** Hardware/POS: parametrizzare il terminale della 36842 con il TID di produzione.
Maurizio: nascondere la carta quando il TID e' 00000000 o mancano gli acquirer.
- **Gia' noto:** POS: altri errori (errore 48, TID duplicato su 24338)

<a id="cg-007"></a>

### CG-007 · Tramogge 0,0,0 e schermata 73 su 32996 e 36842 a ogni accensione; ieri quasi zero vendite

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-01 → 2026-11-10
- **Macchine:** 32996, 36842, 24350, 28417, 23718
- **Prove:** 10/11 alle 09:54-09:55:
- 32996: schermata 73, tramogge 0,0,0 (reboot alle 09:04 e recovery alle 09:08);
- 36842: schermata 73, tramogge 0,0,0 (reboot alle 09:09).
Le altre Parma sono a 1,0,0, schermata 71.
Vendite del 09/11 (stato gia' presente il 09/11 mattina): 32996 una sola vendita cash (18:39), 36842 nessuna transazione. L'08/11 avevano fatto 15 e 13 transazioni.
Nel resto di Parma, ieri:
- 25158 4, 28416 2, 24349 1;
- 24350, 25157, 28417, 28419 e 32995 0.
C'e' quindi anche un calo generale (lunedi'), che non permette di concludere.
23718 (branch mod5): ancora 0,0,0, schermata 46, 0 transazioni (vedi CG-014).
- **Ipotesi:** Dopo l'accensione la GMI manda #HPS 0,0,0 se le tramogge non rispondono ancora, e il Pi resta sulla 73. Le vendite quasi nulle fanno sospettare che la 73 impedisca la vendita, ma il calo su tutta Parma lascia aperta l'alternativa del poco traffico.
Non confermato.
- **Proposta:** Campo Parma, oggi:
- Guardare a display 32996 e 36842.
- Provare una vendita cash.
- Controllare le tramogge dal menu tecnico.
Maurizio: chiarire cosa porta alla schermata 73 e se la GMI ripete #HPS dopo l'avvio. Valutare un nuovo #HPS? dopo 30-60 s dall'avvio.

<a id="cg-009"></a>

### CG-009 · 24254 (Aprilia): accensione tardiva e arresto serale per la nona sera, zero vendite

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-02 → 2026-11-10
- **Macchine:** 24254
- **Prove:** 09/11:
- Reboot alle 12:01 locali (uptime 137). Le altre Aprilia si accendono tra le 05:40 e le 07:30; l'08/11 si era accesa alle 08:54.
- Sottotensione ADESSO alle 11:02 e alle 16:17 UTC.
- Ultimo report alle 19:48 (uptime 28203 s): nona sera di fila con arresto.
10/11 alle 10:00: offline da 851 min. 24866, 29598, 29597 e 26087 si sono riaccese tra le 05:42 e le 07:30.
Vendite:
- nelle 24 h una sola transazione, carta annullata alle 13:02;
- ultima carta approvata il 05/11.
Ultimo stato: POS IDLE, tramogge 1,1,0, schermata 70, throttled 0x50000.
- **Ipotesi:** Alimentazione debole o interrotta: sottotensione gia' all'accensione e nel pomeriggio, poi spegnimento serale. L'accensione tardiva fa pensare che qualcuno la riaccenda a mano, oppure a una presa/timer diversa dalle altre Aprilia.
Non confermato.
- **Proposta:** Campo Aprilia, oggi:
- Riaccendere la macchina.
- Verificare presa e timer.
- Sostituire l'alimentatore del Pi.
- Fare una vendita di prova cash e carta.
- Recuperare journal e dmesg del 09/11 attorno alle 19:48.

<a id="cg-004"></a>

### CG-004 · Seriale GMI assente all'accensione (FTDI non enumerato), cavi lotto BG03E: oggi su tutte e due

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-10
- **Macchine:** 25158, 32996
- **Prove:** 10/11:
- 32996 (BG03ER1N):
  - 09:04: serial_missing not_enumerated (uptime 113) con eccezione 'could not open port /dev/ttyUSB0';
  - 09:08: reboot di recovery (uptime 41);
  - 09:09: serial_recovery.
- 25158 (BG03ES5F):
  - 09:22: serial_missing (uptime 108);
  - 09:26: reboot (uptime 43);
  - 09:27: serial_recovery.
In entrambe la diagnosi USB mostra solo hub, ethernet e ILITEK, nessun FTDI.
25158: 4 mattine su 5 (06, 08, 09 e 10/11). 32996: 08/11 e 10/11.
Le altre Parma (cavi AL05, A10, AG0, AJ0, BG04M) sono pulite. Il cavo della 25158 non risulta ancora scambiato (seriale BG03ES5F).
- **Ipotesi:** Problema noto del lotto FT232R BG03E e/o dell'alimentazione a ritroso dalla GMI. Il recovery funziona, ma ogni volta costa circa 5 minuti di macchina ferma.
- **Proposta:** Campo Parma: scambiare il cavo della 25158 con uno AL05 e lasciare la 32996 come controllo.
Pi: nel prossimo rilascio riavvio anticipato (~30-40 s), uhubctl e TX della GMI in high-Z.
- **Gia' noto:** Seriale assente al mattino (serial_missing, not_enumerated)

<a id="cg-005"></a>

### CG-005 · Sottotensione del Raspberry: 23718 fissa, 24349 e 24254 a episodi

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-10
- **Macchine:** 23718, 24349, 24254, 24350, 24338
- **Prove:** Orari degli avvisi in UTC.
- 23718: 0x50005, sottotensione ADESSO ancora presente. Avviso aperto dal 03/11 10:47, ultimo il 10/11 alle 08:47.
- 24349: sottotensione ADESSO il 09/11 alle 15:17, 18:02, 21:32, 22:17 e 22:47. Ogni episodio e' rientrato entro 15 min. Oggi 0x50000 dopo il reboot delle 09:17 locali.
- 24254: sottotensione ADESSO il 09/11 alle 11:02 (subito dopo l'accensione) e alle 16:17. Ultimo report 0x50000.
- 24338 e 24350: 0x50000, sottotensione avvenuta dal boot.
- Tutte le altre: 0x0. 37008 ha 0x80000 (solo limite termico).
- **Ipotesi:** Alimentatori o cavi deboli. Su 24254 la sottotensione accompagna gli arresti serali (CG-009).
- **Proposta:** Hardware/campo, in ordine:
1. 24254 (insieme a CG-009).
2. 23718 (fissa da 7 giorni).
3. 24349 (5 episodi in 8 h).
4. 24350 e 24338.
- **Gia' noto:** host.throttled 0x50000 (scheda campi); sottotensione sospettata nei flash GMI falliti

<a id="cg-012"></a>

### CG-012 · POS non pronto subito dopo l'avvio: 'gia' in corso', Broken pipe, codice 90; ricomparso su 29597

- **Area:** pi · **Gravita':** medium · **Visto:** 2026-11-04 → 2026-11-09
- **Macchine:** 24254, 28418, 33957, 24866, 29597
- **Prove:** 29597, 09/11:
- reboot alle 14:20 (uptime 59) e alle 14:22 (uptime 60), fuori orario;
- subito dopo 'Operazione get_advanced_config gia' in corso': 3 alle 14:20, 3 alle 14:21, 7 alle 14:23;
- alle 14:29: 1 Broken pipe, 1 'POS non attivo (codice 90)' e 1 timeout.
In tutto 22 transazioni (20 carta): 15 errori, 3 approvate, l'ultima alle 19:32. card_activity: 17 ko, 1 ok.
Storico, stesso schema dopo reboot fuori orario: 24866 il 06/11 (21 errori in 6 min), 24254 il 04-05/11, 28418 il 04/11.
- **Ipotesi:** Corsa all'avvio tra pagamento, activate e lettura cashless_info. Si presenta quando qualcuno usa la carta nei primi minuti dopo un riavvio, probabilmente il tecnico durante un intervento.
- **Proposta:** Maurizio: carta disabilitata finche' il POS non e' IDLE e cashless_info non ha finito, oppure lettura rimandata se c'e' un pagamento in coda.
Campo Aprilia: chiedere chi e' intervenuto sulla 29597 il 09/11 alle 14:20 e perche'.
- **Gia' noto:** POS: get_advanced_config (operazione gia' in corso)

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

<a id="cg-017"></a>

### CG-017 · 33957 (Carpi): carte di nuovo approvate, resta un gruppo di codice 90 a fine mattina

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-07 → 2026-11-09
- **Macchine:** 33957
- **Prove:** 09/11:
- 14 transazioni, 10 carta e 4 cash; 8 approvate, di cui 4 carta (ultima alle 19:40).
- Errori:
  - 4 'POS non attivo (codice 90)' alle 11:42-11:43, circa 2 h 40 min dopo l'accensione delle 09:00;
  - 2 'rifiutata dalla banca (codice 04)' alle 11:44-11:45.
- Nessun codice 31 (il 07/11 erano 16).
- Telemetria attiva fino alle 18:48 (avviso offline alle 18:32 UTC, chiuso il 10/11 alle 08:02 UTC). Nei giorni prima si fermava alle 10:32-11:02.
card_activity: 4 ok, 6 ko.
Oggi: reboot alle 09:00, POS IDLE, TID 75645530, LTE rssi -53.
- **Ipotesi:** La connettivita' e' migliorata: telemetria e carte hanno funzionato quasi tutto il giorno. Il gruppo di codice 90 verso fine mattina fa pensare a un breve calo di rete nella stessa fascia oraria dei giorni precedenti.
Non si sa se sul posto sia stato fatto qualcosa.
- **Proposta:** Campo Carpi: verificare se e' stato toccato router o SIM; se no, controllarli comunque.
Maurizio: log di pos-engine del 09/11 tra le 11:30 e le 11:50.
Declassare se oggi le carte vanno senza codice 90.

<a id="cg-011"></a>

### CG-011 · Dashboard: centro null, chiave non corrispondente su 33326, device duplicato 24866, device nuovi senza MHD

- **Area:** dashboard · **Gravita':** low · **Visto:** 2026-11-04 → 2026-11-10
- **Macchine:** 23718, 24338, 28418, 33326, 37008, 24866
- **Prove:** - Centro ancora null per 23718, 24338, 28418, 33326 e 37008.
- 33326: nuovo device_key_mismatch il 09/11 alle 16:35; device_key_status 'mismatch', avviso aperto dal 03/11.
- 24866: il vecchio device b7233887 e' offline da 5847 min (ultimo report 06/11 08:32) e porta ancora un p95_error vecchio.
- 28418 (stesso gruppo di prova): offline dal 09/11 alle 16:13, un minuto dopo un reboot (uptime 40).
- Il conteggio flotta e' 23: contiene anche il doppione della 24866 e il Pi nuovo senza MHD (CG-018).
- **Ipotesi:** I cambi di Pi/SD creano un nuovo device che la dashboard non unisce al vecchio. I device senza MHD gonfiano il conteggio.
Le macchine con centro null sono probabilmente un banco o un sito di prova.
- **Proposta:** Dashboard/Maurizio:
- Archiviare b7233887, oppure unire per MHD tenendo il device piu' recente.
- Contare a parte i device senza MHD.
- Ri-registrare la chiave di 33326.
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

### CG-016 · Contatori errori seriali alti lato GMI: 29598 (ne ~120-160 nelle prime 3 h), 37008 (ore in crescita), 23718 e 28418

- **Area:** hardware · **Gravita':** low · **Visto:** 2026-11-06 → 2026-11-10
- **Macchine:** 29598, 37008, 28418, 23718
- **Prove:** Contatori lato GMI oggi:
- 29598: ne=118 con uptime 11019 s (giorni prima 135, 163, 118, 127, sempre a circa 3 h dall'accensione).
- 37008: ore=229 con uptime 457298 s (ieri 190): +39 in 24 h.
- 23718: fe=66, ne=11, ore=70 con uptime 169968 s (ieri fe 39, ne 5, ore 34): circa +27 fe e +36 ore in 24 h.
- 28418: fe=24, ne=18, ore=63 nell'ultimo report (09/11 16:13, uptime 110); test linea del 20/10 KO.
Le Parma sono a fe 3-8, ne 0-4.
- **Ipotesi:** 29598: rumore sistematico nelle prime ore dopo l'accensione (cavo A10KIK4A, massa o GMI verde).
37008 e 23718: crescita costante col tempo.
Su 28418 i contatori non ripartono da zero al reboot del Pi: la GMI non si era riavviata.
Nessun impatto visibile sulle vendite.
- **Proposta:** Campo: test linea 8.4 su 29598, poi su 23718, 37008 e 28418.
Maurizio: inviare i contatori come delta giornaliero o col timestamp del primo errore.
- **Gia' noto:** Aggiornamento firmware GMI (linea disturbata GMI verdi)

<a id="cg-018"></a>

### CG-018 · Pi nuovo CG-87AD39CF senza MHD e device 7a9fd21f con GMI 'NCG senza bootloader': installazione in corso?

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-09 → 2026-11-10
- **Macchine:** CG-87AD39CF, 7a9fd21f
- **Prove:** Device 7a9fd21f (non nell'elenco macchine, MHD non noto):
- reboot_storm: 3 riavvii in 6 h (09/11 15:02 UTC) e 4 in 6 h (10/11 08:17 UTC);
- device_key_mismatch il 10/11 alle 08:17 UTC;
- provisioning GIT_BRANCH: annullato alle 18:28 UTC e consegnato alle 19:01 UTC del 09/11.
Eccezioni senza macchina indicata (UTC):
- 'GMI muta' il 09/11 alle 13:47;
- 'GMI con firmware NCG senza bootloader' il 09/11 alle 14:02, 15:02 e 15:17 e il 10/11 dalle 07:47 alle 08:17.
Nuovo device:
- first_seen alle 09:56 locali (hostname CG-87AD39CF), device_key_enrolled alle 09:57;
- SLIM-4.20.190 su branch mod5 (commit 03cad6f, lo stesso delle mod5 a 187);
- mod 0, schermata 55, tramogge null, nessun contatore GMI, chl_mode null, POS DISCONNECTED;
- cavo BG04MUZY, uptime 119.
- **Ipotesi:** Una macchina con GMI NCG vecchia in preparazione, come la 33957 il 05/11, da programmare via ST-Link. Non e' certo che 7a9fd21f e CG-87AD39CF siano la stessa macchina.
La 190 su mod5 viene probabilmente dalla golden.
- **Proposta:** Maurizio/campo: identificare la macchina e il centro, programmare la GMI via ST-Link (menu 9.5), poi test linea 8.4 e assegnazione MHD/centro in dashboard.
Verificare che la release si allinei al branch mod5.
- **Gia' noto:** GMI 'muta' / NCG senza bootloader (menu 9.5 ST-Link); golden SD (CG-<seriale>)

## In osservazione

<a id="cg-001"></a>

### CG-001 · Aggiornamento firmware GMI: rollout 4.20.90 senza fallimenti; 33326 ancora con bootloader V1 debug, 24338 bootloader sconosciuto

- **Area:** firmware · **Gravita':** medium · **Visto:** 2026-10-30 → 2026-11-04
- **Macchine:** 33326, 24338, 24866, 26087, 29597, 29598, 28418
- **Prove:** 05/11: fw_change 4.20.84->4.20.90 riusciti su 13 macchine senza nessun gmi_flash_failed ne' loop RDY:
- 24349 alle 13:40;
- 32996, 24350, 32995, 28416, 25158, 25157, 28417, 28419 tra le 16:12 e le 16:55;
- 24254 alle 17:09;
- 36842 alle 17:17.
Anche 24349 e 36842, che avevano sottotensione nella giornata, hanno flashato correttamente.
33326:
- bootloader ancora 'V1 (build debug)', blc B856A3FC, bll 8248, s1=1, ne=38, ore=66;
- linktest OK alle 09:56 di oggi.
24338: bootloader 'sconosciuto (99536B11, 8392 byte)'.
33957: riprogrammata via ST-Link con V2 (vedi CG-015).
- **Ipotesi:** Il meccanismo di flash seriale e' stabile con la 4.20.90. I bootloader non standard di 33326 e 24338 restano un rischio al prossimo aggiornamento.
- **Proposta:** Maurizio: riportare a V2 di produzione il bootloader di 33326 e 24338 (ST-Link, come fatto su 33957).
Chiudere dopo il prossimo aggiornamento GMI riuscito su 33326 e 24338.
- **Gia' noto:** Aggiornamento firmware GMI che fallisce (gmi_flash_failed, gmi_blocked, loop RDY)

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
