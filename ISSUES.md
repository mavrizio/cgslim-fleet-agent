# Registro problemi flotta CGSLIM

Aggiornato dall'agente il 17/11/2026 10:04. Una voce per causa; MHD senza zeri. Generato: non modificare a mano.

## Aperti

<a id="cg-003"></a>

### CG-003 · POS DISCONNECTED dopo timeout get_advanced_config: 24350 (4o giorno senza carte), 37008, 23718, 33326

- **Area:** pi · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-17
- **Macchine:** 24350, 37008, 33326, 23718, 24866, 25254, 28416, 33957, 11223344, 11155520, 11223355, 1470000, 54124120, 58547455, 58555555, 58888999, 36842, 24254, 32996, 24338, 28418, 25254, 21784, 25158
- **Prove:** Stato attuale, DISCONNECTED con 'Timeout locale get_advanced_config' (avviso su 4 macchine):
- 24350: boot alle 09:12 di oggi, ancora DISCONNECTED. 16/11: 1 sola transazione, timeout carta alle 11:16; last_ok carta null.
- 37008: 7 vendite cash.
- 23718: nessuna vendita.
- 33326: GMI bloccata (CG-024).
24866: IDLE, 8 vendite cash, nessuna carta.
Transitori rientrati in 15 minuti:
- 33957: 'non riuscito (timeout)' 16/11 alle 12:17;
- 25254: 'Connessione persa' alle 07:47 di oggi;
- 28416: 'Connessione persa' alle 08:47 di oggi.
- **Ipotesi:** Dopo un timeout della lettura cashless_info il pos-engine resta DISCONNECTED senza ritentare. Sulla 24350 il riavvio del Pi non basta: probabilmente il POS va spento. Non confermato.
- **Proposta:** Maurizio:
- un errore di get_advanced_config non deve bloccare il P95: ritentare con backoff;
- nascondere la carta a POS DISCONNECTED.
Campo Parma: spegnere e riaccendere il POS della 24350 e provare una carta.
Dashboard: escludere i Pi di banco dall'avviso.
- **Gia' noto:** POS: get_advanced_config

<a id="cg-009"></a>

### CG-009 · 24254 (Aprilia): terza giornata senza vendite, accesa solo alle 12:35 ieri, oggi spenta alle 10:00

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-02 → 2026-11-17
- **Macchine:** 24254
- **Prove:** 16/11:
- non accesa al mattino; reboot alle 12:37 (uptime 139), quindi accesa verso le 12:35;
- sottotensione ADESSO dalle 13:32 fino all'ultimo report delle 19:55;
- 0 transazioni, come il 14 e il 15/11.
17/11 alle 10:00: offline. Le altre Aprilia si sono accese tra le 05:41 (24866) e le 07:30 (26087).
Ultima carta approvata il 05/11. POS IDLE nell'ultimo report.
- **Ipotesi:** Non confermato:
- linea o timer diversi dalle vicine, oppure accensione manuale;
- alimentazione del Pi insufficiente, che rende la macchina inutilizzabile per il cliente.
- **Proposta:** Campo Aprilia, oggi:
- verificare linea e timer;
- sostituire l'alimentatore del Pi;
- controllare schermo e touch;
- fare una vendita di prova cash e carta.
Maurizio: journal e dmesg del 16/11.

<a id="cg-004"></a>

### CG-004 · Seriale GMI assente all'accensione (FTDI non enumerato), cavi lotto BG03E: 25158 e 32996 anche oggi

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-17
- **Macchine:** 25158, 32996
- **Prove:** 17/11:
- 32996 (BG03ER1N): 09:04 reboot (uptime 113), 'could not open port /dev/ttyUSB0', serial_missing not_enumerated; 09:08 reboot di recovery (uptime 48); 09:09 serial_recovery.
- 25158 (BG03ES5F): 09:23 reboot (uptime 114), stessa eccezione; 09:26 reboot di recovery (uptime 46); 09:27 serial_recovery.
Ora entrambe con POS IDLE.
Vendite 16/11: 25158 7 (6 approvate), 32996 2 (1 approvata).
Cavo non ancora scambiato.
La disconnessione della 33957 a meta' giornata e' un caso diverso (CG-015).
- **Ipotesi:** Lotto FT232R BG03E e/o alimentazione a ritroso dalla GMI. Il recovery funziona e costa circa 5 minuti al mattino.
- **Proposta:** Campo Parma: scambiare il cavo della 25158 con uno AL05, tenendo la 32996 come controllo.
Pi, prossimo rilascio: riavvio anticipato, uhubctl, TX della GMI in high-Z.
- **Gia' noto:** Seriale assente al mattino (serial_missing, not_enumerated)

<a id="cg-005"></a>

### CG-005 · Sottotensione del Raspberry: 24254 continua, 24349 e 23718 ADESSO, 24350 la sera, 24338 dal boot

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-17
- **Macchine:** 24349, 23718, 24254, 24350, 24338
- **Prove:** 16/11, orari locali:
- 24254: undervoltage_now alle 12:47, poi continuo dalle 13:32 fino allo spegnimento (ultimo report 19:55); ultimo stato 0x50005.
- 24350: undervoltage_now alle 21:47 e alle 22:17 (0xd0005, anche limite termico); oggi 0x50000 dopo il boot delle 09:12.
Oggi:
- 24349: 0x50005, sottotensione ADESSO dopo il boot delle 09:18;
- 23718: 0x50005 fissa, avviso aperto dal 03/11;
- 24338: 0x50000.
- **Ipotesi:** Alimentatori o cavi deboli. Sulla 24254 probabile legame col fermo vendite (CG-009). Non confermato.
- **Proposta:** Hardware/campo, sostituire alimentatore e cavo del Pi in quest'ordine:
1. 24254;
2. 24349;
3. 24350;
4. 23718;
5. 24338.
- **Gia' noto:** host.throttled 0x50000 (scheda campi); sottotensione sospettata nei flash GMI falliti

<a id="cg-006"></a>

### CG-006 · TID di prova 97942484 su 9 terminali (23718, banco e tornello 99999901)

- **Area:** pos · **Gravita':** medium · **Visto:** 2026-10-30 → 2026-11-17
- **Macchine:** 23718, 24338, 28418, 11223344, 11223355, 1470000, 54124120, 58547455, 58555555, 58888999, 99999901
- **Prove:** TID 97942484 su:
- 23718;
- banco: 1470000, 11223344, 11223355, 54124120, 58547455, 58555555, 58888999;
- da oggi 99999901 (terminale 58794916).
1470000 e 58888999 sono senza acquirer letti.
Altri TID di prova: 24338 97942485, 28418 97942488.
99999901 oggi: 2 tentativi con carta e nessuno riuscito, 1 'Broken pipe' (CG-025).
- **Ipotesi:** Con lo stesso TID su piu' terminali sono probabili errori 48 e rifiuti.
- **Proposta:** Hardware/POS: TID distinti per i terminali di banco e per il tornello prima delle prove carta.
Maurizio: nascondere la carta con TID 00000000 o senza acquirer.
- **Gia' noto:** POS: altri errori (errore 48, TID duplicato su 24338)

<a id="cg-014"></a>

### CG-014 · MOD 2 con tramogge 2-3 a zero: 33180 e ora 25356 (0 vendite ieri); 23718 mod 4; 36842 tramoggia 1 a 0

- **Area:** firmware · **Gravita':** medium · **Visto:** 2026-11-05 → 2026-11-17
- **Macchine:** 23718, 33180, 28419, 25356, 36842
- **Prove:** - 25356: oggi mod 2, schermata 71, tramogge 1,0,0. 16/11 nessuna transazione; ultima carta approvata il 15/11 verso le 18:10.
- 33180: mod 2, schermata 40, tramogge 1,0,0, chl_mode 0; 16/11 6 vendite cash tra le 10:25 e le 12:33, poi nessuna.
- 28419: era in mod 2 giorni fa ed e' tornata mod 12 con 1,1,0.
- 23718: mod 4, schermata 21, tramogge 0,1,1.
- 36842: tramogge 0,1,0 e schermata 72 per il secondo giorno; 16/11 6 vendite approvate.
- **Ipotesi:** La mod 2 compare sempre insieme alle tramogge 2 e 3 assenti: forse la GMI ripiega in mod 2 quando trova solo la tramoggia 1. Le tramogge sarebbero vuote, scollegate o non rispondono. Non confermato.
- **Proposta:** Campo Tiburtino: controllare e rifornire le tramogge 2 e 3 di 25356 e 33180.
Campo Parma: tramoggia 1 della 36842.
Maurizio: documentare quando la GMI passa a mod 1, 2 o 4.

<a id="cg-015"></a>

### CG-015 · 33957 (Carpi): seriale GMI persa a macchina accesa (11:27 e 11:39 di ieri) e nessuna vendita dopo le 12:05; linea DISTURBATA

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-05 → 2026-11-16
- **Macchine:** 33957
- **Prove:** 16/11:
- 11:27: 'Disconnessione hardware seriale'; kernel 'ftdi_sio 1-1.1.3 device disconnected' a uptime ~8900 s.
- 11:28: serial_missing not_enumerated.
- 11:32: reboot (uptime 59).
- 11:33: serial_recovery.
- 11:39: nuova disconnessione; 11:40 serial_missing (FT232R rilevato a 8,4 s dal boot, poi perso).
- 11:41: serial_back dopo 85 s.
- 12:06: reboot (uptime 645) e update_failed DNS rientrato.
Avvisi: 3 riavvii del Pi e 5 dell'app in 6 h.
Transazioni solo tra le 10:49 e le 12:05; poi nessuna, con telemetria fino alle 20:23 (domenica 64).
Cavo A10LF8Y6 (non BG03E). Test linea 05/11 DISTURBATA. Oggi boot alle 09:00, fe=3, POS IDLE.
- **Ipotesi:** Disconnessione USB a caldo: contatto o cavo FTDI difettoso, massa, oppure intervento del tecnico (gli orari coincidono con la prova carta delle 11:56-12:05). Non confermato.
Il pomeriggio senza vendite potrebbe essere traffico del lunedi' o macchina non utilizzabile.
- **Proposta:** Campo Carpi:
- chiedere se ieri c'e' stato un intervento tra le 11:27 e le 12:06;
- controllare il connettore USB e sostituire il cavo FTDI;
- ripetere il test linea 8.4;
- verificare che la macchina accetti vendite.
Maurizio: journal del 16/11 dalle 12:06 alle 20:23.
- **Gia' noto:** Seriale assente al mattino (eccezione 'Disconnessione hardware seriale'); aggiornamento firmware GMI (linea disturbata)

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

### CG-020 · Telemetria assente per ore con DNS KO: 24349 muta dalle 12:19 di ieri mentre vendeva, 21784 a singhiozzo

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-11 → 2026-11-17
- **Macchine:** 24350, 33957, 21784, 24349, 28416
- **Prove:** 24349: nessun report dalle 12:19 del 16/11 al boot delle 09:18 di oggi. Intanto 5 transazioni (11:14-23:24), l'ultima approvata alle 17:49.
21784, 16/11:
- report fermi dopo le 07:57, le 11:03, le 13:25, le 16:31 e le 20:03;
- update_failed 'Could not resolve host' alle 11:03 e oggi alle 09:07;
- 'Couldn't connect' alle 13:19 e alle 15:59;
- riavvii alle 11:03 (uptime 351) e alle 09:07 (uptime 492).
33957: DNS KO alle 12:06, rientrato subito.
28416: ieri telemetria regolare, 5 transazioni (4 approvate).
- **Ipotesi:** DNS dell'operatore o del router che cade per ore. Il fleet-reporter tace, le transazioni arrivano comunque (forse in coda). Non confermato.
- **Proposta:** Maurizio:
- DNS di riserva sul Pi o sul router;
- report anche con DNS KO.
Campo:
- Parma: router e SIM della 24349;
- dire dove si trova la 21784 e controllarne alimentazione e router.
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

### CG-011 · Dashboard: centro null su 7 macchine, device_key 'missing' solo sul Pi 4f2f67b8, banco nel conteggio

- **Area:** dashboard · **Gravita':** low · **Visto:** 2026-11-04 → 2026-11-17
- **Macchine:** 21784, 23718, 24338, 28418, 33326, 37008, 99999901
- **Prove:** Centro null: 21784, 23718, 24338, 28418, 33326, 37008 e il nuovo 99999901.
21784: device_key_status ora 'ok'. Resta 'missing' solo il Pi senza MHD 4f2f67b8.
Conteggio flotta 39: comprende 8 Pi di banco, il Pi senza MHD e il tornello 99999901.
- **Ipotesi:** La chiave della 21784 e' stata re-enrollata. Il resto e' configurazione mancante.
- **Proposta:** Dashboard/Maurizio:
- assegnare il centro (o 'banco');
- escludere banco e laboratorio da conteggio e avvisi.
- **Gia' noto:** Profilo display auto / golden SD

<a id="cg-016"></a>

### CG-016 · Errori seriali in crescita: 23718, 28418, 37008; 29598 ne ~100 dopo ogni boot

- **Area:** hardware · **Gravita':** low · **Visto:** 2026-11-06 → 2026-11-17
- **Macchine:** 29598, 33326, 11223355, 58547455, 58555555, 37008, 23718, 28418
- **Prove:** Contatori di oggi:
- 23718: fe 111, ne 27, ore 145 (ieri 71, 17, 109).
- 28418: fe 137, ne 36, ore 115 (ieri 110, 25, 93), test linea del 20/10 KO.
- 37008: ore 227 (ieri 186), brk 2.
- 29598: ne 103 a uptime 11023 s (boot alle 06:45), stesso schema di ieri (104); nessun hostlink a meta' giornata.
Banco fermo: valori invariati.
- **Ipotesi:** Linee rumorose su 23718 e 28418 (fe +27..+40 al giorno). Su 29598 il rumore e' concentrato all'avvio.
- **Proposta:** Campo Aprilia: test linea 8.4 sulla 29598.
Laboratorio: test linea su 23718 e 28418.
Maurizio: inviare i contatori come delta giornaliero.
- **Gia' noto:** Aggiornamento firmware GMI (linea disturbata GMI verdi)

<a id="cg-018"></a>

### CG-018 · Banco spento dal 13/11, 28418 (lab) offline dalle 03:51, 21784 tornata

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-09 → 2026-11-17
- **Macchine:** 11223344, 11223355, 11155520, 1470000, 54124120, 58547455, 58555555, 58888999, 21784, CG-4F2F67B8, 28418
- **Prove:** Banco offline dal 13/11 dalle 13:20-15:26 (54124120 con updater 'Couldn't connect').
28418 (beta, sempre accesa, uptime ~6,5 giorni): ultimo report alle 03:51 di oggi.
21784 (mod5 su GMI mod 12):
- di nuovo online, boot alle 09:07 (uptime 492);
- 16/11: 13 transazioni, 11 approvate (6 carta);
- telemetria a singhiozzo (CG-020).
Pi 4f2f67b8 offline dall'11/11.
- **Ipotesi:** Banco spento per pausa. 28418: spegnimento o blackout del laboratorio, causa non nota.
- **Proposta:** Laboratorio: dire se 28418 e' stata spenta.
Maurizio/campo:
- MHD, centro e TID distinti prima della spedizione;
- test linea 8.4;
- dire dove si trova la 21784.
- **Gia' noto:** GMI 'muta' / NCG senza bootloader (menu 9.5 ST-Link); golden SD (CG-<seriale>)

<a id="cg-025"></a>

### CG-025 · Tornello di banco 99999901 (MOD10): MHD cambiato da 99998888, 4 riavvii brevi, POS 'Broken pipe' (anche dopo PI_IP)

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-16 → 2026-11-17
- **Macchine:** 99999901
- **Prove:** Device nuovo in flotta:
- mod 10, schermata 160, tramogge 1,0,0;
- branch mod5, SLIM-4.20.200, fw 4.20.93;
- TID 97942484, centro null.
Transazioni del Pi:
- come 99998888: 5 carte tra le 08:35 e le 08:41 (4 annullate, 1 'Broken pipe' alle 08:41);
- come 99999901: 09:07 annullata, 09:20 timeout.
- card_activity cancelled 5, ko 2 combacia: e' lo stesso Pi.
Riavvii con uptime ~50 s alle 08:36, 08:51, 09:00 e 09:24; app_restart alle 08:57 e 09:17. repo_healed stale_lock ieri alle 15:51 e oggi alle 08:52.
PI_IP da .97 a .99 alle 09:17 (applicato); avviso POS 'Broken pipe' alle 09:17 e alle 09:47. Ultimo stato POS IDLE.
- **Ipotesi:** Banco in lavorazione: spegnimenti manuali, che spiegano i lock git rimasti, e cambio di MHD.
Il Broken pipe compare gia' alle 08:41, prima del cambio IP, e la release e' 200 (con il fix della 196): non e' il bug noto della 195. Non confermato.
- **Proposta:** Laboratorio:
- confermare che e' una macchina di prova e marcarla 'banco';
- assegnarle un TID distinto.
Maurizio: se il 'Broken pipe' del pos-engine si ripete senza spegnimenti, controllare il log del pos-engine dopo un cambio PI_IP con la 200.
- **Gia' noto:** MOD10 Tornello; IP del Raspberry (PI_IP)

## In osservazione

<a id="cg-012"></a>

### CG-012 · Codice 31: nessun rifiuto ieri, la 33957 ha approvato una carta alle 12:05

- **Area:** pos · **Gravita':** medium · **Visto:** 2026-11-04 → 2026-11-15
- **Macchine:** 24254, 28418, 33957, 24866, 29597, 23718, 58888999, 33089, 25356, 24349
- **Prove:** 16/11, nessun 'codice 31' in tutta la flotta.
33957 (TID 75645530): 8 transazioni tra le 10:49 e le 12:05, 4 approvate.
- Carta: 5 tentativi, 1 approvata alle 12:05.
- 3 'nessuna carta entro il tempo' alle 11:56, 12:00 e 12:03, piu' 1 annullata.
- card_activity: ok 1, ko 4.
24349: 3 approvate su 5, 1 timeout carta.
Dopo le 12:05 la 33957 non ha piu' transazioni (vedi CG-015).
- **Ipotesi:** La sequenza di tentativi dalle 11:56 alle 12:05 sembra una prova carta del tecnico, forse dopo lo spegnimento del POS. I rifiuti del 15/11 potrebbero essere rientrati. Non confermato.
- **Proposta:** Campo Carpi: confermare se ieri e' stato spento e riacceso il POS.
Maurizio: tenere d'occhio i codici 31 per 2-3 giorni; mostrare 'carta non disponibile' dopo N rifiuti consecutivi.
- **Gia' noto:** POS: altri errori

<a id="cg-022"></a>

### CG-022 · gmi_hostlink locked a macchina accesa: 29598 alle 19:25 di ieri (1 minuto)

- **Area:** pi · **Gravita':** low · **Visto:** 2026-11-12 → 2026-11-15
- **Macchine:** 24349, 25158, 36842, 24338, 28418, 23718, 32996, 25157, 28419, 32995, 29598
- **Prove:** 29598, 15/11: locked alle 19:25, unlocked alle 19:26, senza reboot ne' app_restart. La macchina ha ne=104 nelle prime ore (CG-016).
Gli altri eventi delle 24 h sono coppie locked/unlocked al boot o al recovery.
Caso isolato precedente: 32995 il 13/11 alle 12:42.
- **Ipotesi:** Su 29598 e' compatibile con la seriale instabile (ne alti) piu' che con un blocco del main loop. La protezione ha funzionato.
- **Proposta:** Maurizio: aggiungere all'evento la durata del blocco e l'ultima riga inviata.
Collegare al test linea della 29598 (CG-016).
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

<a id="cg-023"></a>

### CG-023 · 36842 (Parma): niente piu' riavvii a meta' giornata, voce chiusa

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-12 → 2026-11-13
- **Macchine:** 36842
- **Prove:** 14 e 15/11 senza riavvii in giornata. Oggi solo la riaccensione normale alle 09:09 (uptime 135).
15/11: 36 transazioni, 32 approvate (8 con carta), 4 annullate. Throttled 0x0.
Ora tramogge 0,1,0 e schermata 72 (ieri 1,1,0): da tenere d'occhio.
- **Ipotesi:** I riavvii del 12 e del 13/11 erano interventi o interruzioni di corrente.
- **Proposta:** Chiusa. Se la tramoggia 1 resta a 0 nei prossimi giorni, far controllare dal campo.
