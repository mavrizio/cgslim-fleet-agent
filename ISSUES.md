# Registro problemi flotta CGSLIM

Aggiornato dall'agente il 01/11/2026 11:44. Una voce per causa; MHD senza zeri. Generato: non modificare a mano.

## Aperti

### CG-001 · Aggiornamento firmware GMI fallito: 33326 bloccata (errore 98), loop RDY su 26087 e 29597

- **Area:** firmware · **Gravita':** high · **Visto:** 2026-10-30 → 2026-11-01
- **Macchine:** 33326, 26087, 29597
- **Prove:** 33326 (beta2, centro non registrato): gmi_blocked dal 01/11 09:36, 15 tentativi con CGT-4.20.84.bin, 'Timeout ACK al blocco 7808. STM32 non ha risposto.' Gia' dal 30/10 14:55 il flash di CGT-4.20.83.bin era fallito (15 tentativi, blocco 44544; evento ricevuto il 31/10 18:40). 01/11 09:24: eccezione 'RILEVATO LOOP BOOTLOADER (RDY)' (buffer YRDYRDY) e app_down. Payload attuale: mod 0, screen 29, hopper null, contatori GMI null, fw riportato 4.20.82 (non aggiornato). Pi 3 Model B Rev 1.2, throttled 0x50000; l'alert delle 11:31 indica 0x50005 (sottotensione adesso). Uptime 171176 s: non viene spenta la notte. Loop RDY anche su 26087 (10:31, fw 4.20.84 ok alle 10:36) e su 29597 (10:55, fw 4.20.84 ok alle 10:57), rientrati senza intervento.
- **Ipotesi:** Problema noto del bootloader V2. Su 33326 il flash fallisce da due giorni a blocchi diversi (44544, poi 7808): questo fa pensare a disturbi di linea o di alimentazione piu' che a un file corrotto. La sottotensione del Pi durante il flash e' un sospetto concreto. Non si sa se la GMI sia verde (col modem): i contatori GMI non sono disponibili. Su 26087 e 29597 la GMI e' rimasta nel bootloader durante l'aggiornamento ed e' stata recuperata dal flash successivo.
- **Proposta:** Campo: spegnere e riaccendere GMI e Pi su 33326 per uscire dall'errore 98, cambiare o misurare l'alimentatore del Pi e annotare il colore della GMI. Se fallisce ancora, flash manuale con ST-Link. Pi/firmware: registrare throttled e il blocco al momento del Timeout ACK; valutare di rimandare il flash se il bit 0x1 (sottotensione in corso) e' attivo.
- **Gia' noto:** Aggiornamento firmware GMI che fallisce (gmi_flash_failed, gmi_blocked, loop RDY)

### CG-002 · 36842 offline dal 31/10 20:21 e non riaccesa al mattino

- **Area:** campo · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-01
- **Macchine:** 36842
- **Prove:** Ultimo report 31/10 20:21, offline da 918 min alle 11:40. Riavvio alle 20:20 (uptime 71 s) a centro aperto: le altre Parma vendono fino alle 21:53 (32995) e alle 23:38 (25158). Le altre 9 Parma si sono riaccese stamattina tra le 08:26 e le 09:22. Ultimo payload: throttled 0x50005 (sottotensione in corso), GMI fe=138 (le altre Parma 0-3), app SLIM-4.20.172, fw 4.20.83, git bdfc6d4. Non ha ricevuto .173 ne' .176. POS con TID 00000000 e p95_error timeout get_advanced_config. 12 vendite cash il 31/10, l'ultima alle 19:08.
- **Ipotesi:** Alimentazione insufficiente: sottotensione in corso piu' errori di frame lato GMI. Puo' aver causato il riavvio delle 20:20 e poi il blocco o lo spegnimento. In alternativa un problema di rete o router. I dati non permettono di distinguere.
- **Proposta:** Campo Parma oggi: verificare se e' accesa e cosa mostra lo schermo; controllare alimentatore e cavo del Pi e il router; recuperare journal e dmesg dal 31/10 20:20. Dopo il ritorno, controllare che si aggiorni a SLIM-4.20.176 e fw 4.20.84.

### CG-003 · POS DISCONNECTED dopo timeout get_advanced_config (7 macchine, tutta Aprilia)

- **Area:** pi · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-01
- **Macchine:** 24254, 24866, 26087, 29597, 29598, 24350, 37008, 36842, 24349
- **Prove:** 7 macchine online hanno pos.state DISCONNECTED (connected false) e p95_error 'Timeout locale in attesa di get_advanced_config (15.0s)': 24254, 24866, 26087, 29597, 29598 (tutte e 5 di Aprilia), 24350 (Parma) e 37008 (beta2). Lo stesso errore c'e' nell'ultimo payload di 36842 (offline). Le altre 11 online sono IDLE e connesse, con identita' P95 letta. 24349: alert 'Connessione persa durante get_advanced_config: Connessione chiusa dal dispositivo', ma il payload attuale e' IDLE e connesso, con lettura alle 11:28. Il 31/10 i POS di Aprilia rispondevano: 29598 con 3 tentativi carta (timeout 18:02, 2 annullati), 24254 con un timeout del cliente alle 18:41. Oggi nessuna transazione carta su tutta la flotta (domenica mattina).
- **Ipotesi:** Problema noto della lettura cashless_info (v.171+), qui con un effetto piu' grave: dopo il timeout all'avvio il pos-engine resta DISCONNECTED. Se e' cosi', le 7 macchine non accettano carte. Il fatto che tutte le macchine di Aprilia siano colpite fa pensare anche a POS spenti o irraggiungibili nella rete locale del centro. Da verificare.
- **Proposta:** Maurizio: leggere i log di pos-engine su 26087 e 24350 (connessione TCP al 192.168.9.170, chi la chiude, eventuali retry). Se il pos-engine non si riconnette dopo il timeout di get_advanced_config, correggere core/cashless_info.py: retry con backoff, lettura che non abbatte la connessione, nessun blocco dei pagamenti. Campo Aprilia: prova di pagamento con carta su 26087 e controllo che il SELF2000 sia acceso.
- **Gia' noto:** POS: get_advanced_config

### CG-004 · Seriale GMI assente all'accensione (FTDI non enumerato), cavi lotto BG03E

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-01
- **Macchine:** 25158, 32996
- **Prove:** 25158 il 01/11 alle 09:22: serial_missing not_enumerated. Sul bus USB solo gli hub 0424:2514, la LAN 0424:7800 e il touch ILITEK; nessun FTDI e ttys vuoto. Eccezione 'ERRORE CRITICO SERIALE: could not open port /dev/ttyUSB0'. serial_recovery alle 09:24, reboot alle 09:27 (uptime 80 s), poi GMI raggiungibile (fw 4.20.84 alle 09:30). Un solo recupero su 2 disponibili. Cavo BG03ES5F. 32996 (cavo BG03ER1N) oggi regolare: avvio alle 09:04, vende fino alle 11:36.
- **Ipotesi:** Problema noto: lotto di cavi FT232R BG03E difettoso e/o chip FTDI alimentato a ritroso dalla GMI.
- **Proposta:** Campo: fare lo scambio del cavo della 25158 con uno AL05, come previsto, nella visita a Parma. Pi: riavvio anticipato (~30-40 s), uhubctl e TX della GMI in high-Z nel prossimo rilascio importante.
- **Gia' noto:** Seriale assente al mattino (serial_missing, not_enumerated)

### CG-005 · Sottotensione del Raspberry su 7 macchine (alimentatori/cavi)

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-01
- **Macchine:** 24254, 24338, 24349, 24350, 26087, 33326, 36842
- **Prove:** throttled 0x50000 (sottotensione avvenuta dal boot) su 24254, 24338, 24349, 24350, 26087 e 33326. 0x50005 (sottotensione in corso) nell'ultimo payload di 36842 (31/10 20:21). L'alert undervoltage_now (0x50005) delle 11:31 e' attribuito al device di 33326, ma il payload attuale di 33326 riporta 0x50000. Tutte le altre macchine sono a 0x0.
- **Ipotesi:** Alimentatori o cavi deboli. Le due macchine piu' gravi di oggi, 33326 (flash fallito) e 36842 (offline), sono anche quelle con sottotensione in corso. L'attribuzione dell'alert potrebbe essere errata lato dashboard.
- **Proposta:** Hardware/campo: sostituire per primi gli alimentatori di 36842 e 33326, poi verificare a giro 24349, 24350, 24254 e 26087. Dashboard: controllare a quale device appartiene l'alert 0x50005.
- **Gia' noto:** host.throttled 0x50000 (scheda campi); sottotensione sospettata nei flash GMI falliti

### CG-006 · TID POS anomali: 36842 senza TID, 24338 e 33326 con TID duplicato

- **Area:** pos · **Gravita':** medium · **Visto:** 2026-10-30 → 2026-11-01
- **Macchine:** 36842, 24338, 33326
- **Prove:** 36842 (Parma, produzione): TID 00000000, package PYP-SELF2000 01.04.25.03 (le altre Parma hanno 01.04.02), SN 58551425; lettura del 31/10 00:21; nessuna transazione carta nelle 24 h. 24338 e 33326 riportano lo stesso TID 97942485 su terminali diversi (SN 58795528 e 53818418). 24338: ultimo errore 48 il 30/10 alle 13:21; il POS di 33326 era attivo e letto il 30/10 alle 14:06.
- **Ipotesi:** Il terminale della 36842 non e' parametrizzato (forse dopo un cambio POS o un aggiornamento del package): la carta non puo' funzionare. Il TID duplicato e' una causa nota di errore 48.
- **Proposta:** Hardware/POS: far parametrizzare la 36842 con il TID di produzione; assegnare TID distinti a 24338 e 33326.
- **Gia' noto:** POS: altri errori (errore 48, TID duplicato su 24338)

### CG-007 · 25158: tramogge 0,0,0, schermata 73 e nessuna vendita dopo l'avvio

- **Area:** campo · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-01
- **Macchine:** 25158
- **Prove:** Payload delle 11:30: hopper ['0','0','0'] (le altre Parma MOD12 hanno ['1','0','0']), screen 73 (le altre 71), idle. Ultima vendita 31/10 alle 23:38; nessuna dopo l'avvio delle 09:22. Le vicine vendono: 24350 ultima alle 10:56, 32996 alle 11:36. Stamattina e' passata dal recupero seriale (CG-004).
- **Ipotesi:** Tramoggia 1 vuota o in errore, oppure stato della GMI non ripristinato dopo il recupero seriale e il flash a 4.20.84. Il significato della schermata 73 non e' nella scheda.
- **Proposta:** Campo Parma: verificare tramoggia e schermata della 25158 nella stessa visita della 36842. Maurizio: chiarire cosa indica screen 73.

### CG-008 · Branch riportato 'parma' ma servizio gitpuller@beta su 3 macchine Aprilia

- **Area:** dashboard · **Gravita':** low · **Visto:** 2026-11-01 → 2026-11-01
- **Macchine:** 26087, 29597, 29598
- **Prove:** 26087, 29597 e 29598 risultano con branch parma, ma il servizio attivo e' gitpuller@beta. git_commit 9bf05a7, diverso da mod12 (65f8fdf) e da beta2 (b189183). Oggi hanno comunque ricevuto SLIM-4.20.176 e fw 4.20.84.
- **Ipotesi:** Lettura del branch errata nel fleet-reporter o nella dashboard, oppure nome dell'istanza gitpuller non coerente con il branch seguito.
- **Proposta:** Su una macchina, verificare il branch reale del repo (git rev-parse --abbrev-ref HEAD) e correggere l'unita' gitpuller oppure il campo riportato.
