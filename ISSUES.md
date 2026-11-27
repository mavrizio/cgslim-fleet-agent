# Registro problemi flotta CGSLIM

Aggiornato dall'agente il 27/11/2026 10:03. Una voce per causa; MHD senza zeri. Generato: non modificare a mano.

## Aperti

<a id="cg-003"></a>

### CG-003 · POS DISCONNECTED: 24350 quattordicesimo giorno senza carte; 37008, 37111 e 37112 col POS irraggiungibile da ore (terminale/rete, non Pi)

- **Area:** pos · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-27
- **Macchine:** 24350, 37008, 37111, 37112, 37119, 36804, 36805, 37114, 37113, 29597, 25254, 28416, 33089, 32996, 33326, 23718, 24338, 24866, 25158, 33957, 54124120, 36842, 24254, 28418, 21784, 29598, 32995, 26087, 99999901, 37108, 37109, 37110, 37115, 37116, 37117, 37118, 77700011
- **Prove:** 24350 (SLIM-199):
- DISCONNECTED con timeout get_advanced_config dopo il boot delle 09:12;
- last_ok carta null;
- 1 carta annullata alle 19:03 del 26/11.
37008 (SLIM-212 dalle 12:00 del 26/11):
- down_s 78592, scollegato circa dalle 12:10 di ieri (contatore ripartito con l'aggiornamento);
- last_error 'No route to host';
- 6 vendite cash tra le 17:47 e le 19:48.
37111 (212): down_s 81395, 'Connection refused'.
37112 (212 dalle 22:46): down_s 37849, 'Connection refused'.
Rientrati in 15 min con 'Connessione chiusa dal dispositivo':
- 25254 alle 07:47;
- 28416 alle 08:47;
- 33089 alle 11:17, durante l'aggiornamento.
29597 oggi IDLE.
33957 IDLE, 9 carte approvate.
Avviso pos_error su 11 macchine: 24350 piu' il banco.
- **Ipotesi:** Con la 208+ un down_s che cresce per ore indica il terminale.
- 37008: 'No route to host' significa POS non raggiungibile in IP (spento, cavo LAN, IP).
- 37111 e 37112: 'Connection refused' significa nessun servizio sulla porta (POS spento o in riavvio).
- 24350 e' su mod12 (199), senza le correzioni della 208.
- **Proposta:** Campo Parma: spegnere e riaccendere il POS della 24350; se resta in timeout, sostituirlo.
Lab:
- 37008: alimentazione, cavo e IP del POS (ping 192.168.9.170);
- 37111 e 37112: verificare che il POS sia collegato e acceso.
Maurizio: merge della 208+ su mod12.
Dashboard: escludere il banco dall'avviso pos_error.
- **Gia' noto:** POS: collegamento col terminale (CG-003, SLIM-4.20.208); POS: get_advanced_config

<a id="cg-005"></a>

### CG-005 · Sottotensione del Raspberry: 24254 e 24349 ferme, 24350 sottotensione ADESSO ieri, 33089 nuova con 0x50000

- **Area:** hardware · **Gravita':** high · **Visto:** 2026-11-01 → 2026-11-27
- **Macchine:** 24349, 24254, 24350, 24338, 26087, 37119, 23718, 36804, 29597, 33089
- **Prove:** 24350: undervoltage_now (0x50005) alle 18:02 del 26/11, rientrato alle 18:17. Oggi 0x50000 dopo il boot delle 09:12.
Oggi 0x50000 anche su:
- 24338 (uptime 771931 s);
- 33089 (boot alle 07:57, nuova);
- 36804 (boot alle 08:52, banco).
26087 e 37119 oggi 0x0.
24254: offline da 2853 min, ultimo report 25/11 alle 10:26 con 0x50005.
24349: offline dal 19/11 (CG-029).
- **Ipotesi:** Alimentatori o cavi del Pi deboli. Sulla 24254 e sulla 24349 la sottotensione ha preceduto lo stop. Non confermato.
- **Proposta:** Hardware/campo, alimentatore e cavo del Pi in quest'ordine:
1. 24254 (urgente);
2. 24349;
3. 24350;
4. 33089;
5. 24338;
6. 36804 (lab).
- **Gia' noto:** host.throttled 0x50000 (scheda campi); sottotensione sospettata nei flash GMI falliti

<a id="cg-009"></a>

### CG-009 · 24254 (Aprilia): seconda mattina spenta, quarto giorno senza vendite

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-02 → 2026-11-27
- **Macchine:** 24254
- **Prove:** Ultimo report il 25/11 alle 10:26 (0x50005, avviso undervoltage_now dalle 10:32).
Oggi alle 10 offline da 2853 min.
Nessuna transazione dal 23/11.
Le altre Aprilia si sono accese tra le 05:41 (24866) e le 07:30 (26087) e vendono.
- **Ipotesi:** Alimentatore o cavo del Pi insufficiente: il Pi parte in sottotensione e si ferma. In alternativa la macchina e' staccata, o il timer o la linea sono diversi. Non confermato.
- **Proposta:** Campo Aprilia, oggi:
1. sostituire alimentatore e cavo del Pi;
2. controllare timer e linea;
3. fare una vendita di prova cash.
- **Gia' noto:** collegata a CG-005

<a id="cg-014"></a>

### CG-014 · Tramoggia monete a 0 (schermata 72) su 24350, 25158 e 32996; 33090 rientrata; 33180 tramogge 0,0,0 in mod 2

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-05 → 2026-11-27
- **Macchine:** 24350, 25158, 32996, 33090, 37008, 33180, 29597, 24866, 25356, 36842, 28419, 23718
- **Prove:** Oggi tramogge 0,1,0 con schermata 72:
- 24350: nessuna vendita, solo 1 carta annullata alle 19:03;
- 25158: 2 vendite approvate su 4, l'ultima alle 16:30;
- 32996: 5 vendite approvate su 7 (4 carte), l'ultima alle 09:58 di oggi.
33090: tramogge 1,1,0 e schermata 70, 8 vendite su 8 (10:45-19:31). Rientrata.
37008: schermata 71 con tramogge 1,0,0 (ieri 73 con 0,0,0); 6 vendite cash.
33180: mod 2, schermata 41, tramogge 0,0,0, chl_mode 0, pos-engine inactive; 2 vendite cash.
- **Ipotesi:** Una 72 che dura giorni e' la tramoggia monete vuota, assente o in errore: la macchina vende tessere ma non da' monete. La 33090 e' stata probabilmente rifornita. Non confermato.
- **Proposta:** Campo Parma, oggi: tramoggia monete (ind. 3) di 24350, 25158 e 32996, poi una vendita di prova.
Campo Tiburtino: tramogge e mod della 33180.
Lab: tramoggia tessere della 37008.
- **Gia' noto:** Schermata 72 'solo tessere' (MOD12); Banda 'LA MACCHINA NON DA' RESTO'

<a id="cg-020"></a>

### CG-020 · Telemetria/rete: 21784 a singhiozzo (9 update_failed ieri, oggi muta dalle 09:24); 32995 accesa tardi alle 09:53

- **Area:** hardware · **Gravita':** high · **Visto:** 2026-11-11 → 2026-11-27
- **Macchine:** 21784, 32995, 24350, 28418, 24349, 37008, 54124120, 37113
- **Prove:** 21784, 26/11:
- update_failed alle 11:46 (DNS e 443), 12:41, 13:04, 13:47 e 18:19 (tre), tutti recovered;
- buchi nei report dopo le 11:46, 13:04, 13:47 e 18:19;
- ultimo report della sera alle 19:55;
- 1 vendita cash alle 17:14.
21784, oggi: reboot alle 09:23 (uptime 150), ultimo report alle 09:24.
32995:
- ultimo report del 26/11 alle 00:21;
- oggi accesa alle 09:53 (uptime 112), piu' tardi delle altre Parma (08:26-09:22);
- nessuna vendita nelle 24 h.
update_failed DNS sporadici anche su 24350 (16:59, 20:08) e 37008 (04:04), rientrati.
- **Ipotesi:** 21784: rete mobile, SIM o router instabile. 32995: accensione tardiva, forse timer o accensione a mano. Non confermato.
- **Proposta:** Hardware: SIM, antenna e router della 21784.
Campo Parma: controllare il timer della 32995.
Maurizio: escludere dall'avviso i fallimenti di massa.
- **Gia' noto:** Aggiornamenti bloccati (update_failed, rete/SIM)

<a id="cg-029"></a>

### CG-029 · 24349 (Parma) offline dalle 14:20 del 19/11, ottava mattina senza riaccensione

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-19 → 2026-11-27
- **Macchine:** 24349
- **Prove:** Ultimo report il 19/11 alle 14:20 (0x50005, dopo una mattina di undervoltage_now).
Oggi alle 10 offline da 11259 min.
Le altre Parma si sono accese tra le 08:26 (25157) e le 09:53 (32995).
- **Ipotesi:** Alimentatore del Pi ceduto, oppure macchina staccata. Non confermato.
- **Proposta:** Campo Parma, oggi:
1. verificare la macchina;
2. sostituire alimentatore e cavo del Pi;
3. riaccenderla;
4. fare una vendita di prova.
Se e' stata spenta a mano, dirlo.
- **Gia' noto:** collegata a CG-005

<a id="cg-030"></a>

### CG-030 · 21784: codice 20 di nuovo su tutte le carte (6 il 26/11), nessuna carta approvata dal 20/11

- **Area:** pos · **Gravita':** high · **Visto:** 2026-11-20 → 2026-11-26
- **Macchine:** 21784
- **Prove:** 26/11: 6 errori 'POS non configurato (codice 20)' tra le 19:10 e le 19:11, 0 carte ok.
L'unica vendita e' cash, alle 17:14.
card_activity: ultima carta approvata il 20/11 verso le 10.
POS IDLE e connesso nell'ultimo report.
Terminale 58127169, TID 75501208, anche MDB init.
- **Ipotesi:** Il terminale ha perso la configurazione dell'acquirer o la ricarica dei parametri, forse con i cali di rete o per il doppio uso MDB/P95. Su questa macchina le carte non funzionano da una settimana. Non confermato.
- **Proposta:** Hardware/POS, oggi: verificare configurazione e acquirer del terminale 58127169 e fare una carta di prova sul posto.
Maurizio: nascondere la carta dopo un codice 20.
- **Gia' noto:** POS: altri errori

<a id="cg-004"></a>

### CG-004 · Seriale GMI assente all'accensione, cavi BG03E: 32996 di nuovo stamattina, 25158 prima mattina pulita dal 18/11

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-27
- **Macchine:** 25158, 32996, 77700011, 37116
- **Prove:** 27/11, 32996 (BG03ER1N):
- 09:04: serial_missing not_enumerated (uptime 108) ed eccezione 'could not open port /dev/ttyUSB0';
- 09:08: reboot (uptime 47);
- 09:09: serial_recovery.
Sul bus USB solo hub, ethernet e ILITEK.
27/11, 25158 (BG03ES5F): accensione alle 09:22 (uptime 113) senza serial_missing. E' la prima mattina pulita dopo 9 consecutive (18-26/11).
37116 (BG03ER0O): di nuovo online, accesa alle 22:16 del 26/11 e alle 08:53 di oggi, senza serial_missing.
77700011 (BG03ER1I): ancora senza contatori GMI (schermata 29, mod 0).
- **Ipotesi:** Lotto FT232R BG03E e/o alimentazione a ritroso dalla GMI. La mattina pulita della 25158 e' un caso singolo e non cambia il quadro. Il recovery a 180 s funziona. Non confermato.
- **Proposta:** Campo Parma: scambiare il cavo della 25158 con uno AL05, tenendo la 32996 come controllo.
Lab:
- sostituire il BG03ER0O della 37116;
- verificare la 77700011.
Pi (prossimo rilascio): riavvio anticipato a 30-40 s, uhubctl, TX della GMI in high-Z.
- **Gia' noto:** Seriale assente al mattino (serial_missing, not_enumerated)

<a id="cg-006"></a>

### CG-006 · TID di prova 97942484 anche sulle nuove 37108-37119

- **Area:** pos · **Gravita':** medium · **Visto:** 2026-10-30 → 2026-11-21
- **Macchine:** 23718, 24338, 28418, 11223344, 11223355, 1470000, 54124120, 58547455, 58555555, 58888999, 99999901, 99900055, 99990008, 36805, 37108, 37110, 37111, 37112, 37114, 37115, 37117, 37118, 37119
- **Prove:** TID 97942484 su:
- 23718, 36805, 54124120, 99999901;
- nuove 37108, 37110, 37111, 37112, 37114, 37115, 37117, 37118 e 37119.
Su 37109 e 37116 il TID non e' leggibile (POS in timeout).
Altri TID di prova: 24338 97942485, 28418 97942488.
Storico sulle nuove: codice 90 (37109, 37111, 37112, 37116, 37118), codice 37 (37115), codice 20 (37114).
- **Ipotesi:** Con lo stesso TID su piu' terminali sono probabili rifiuti ed errori 48/90. Le 371xx sembrano destinate al campo.
- **Proposta:** Hardware/POS: TID distinti per tutte le 371xx prima dell'installazione.
Maurizio: nascondere la carta con TID di prova.
- **Gia' noto:** POS: altri errori (errore 48, TID duplicato su 24338)

<a id="cg-016"></a>

### CG-016 · Errori seriali: 28418 test 8.4 KO e flash 4.20.101 riuscito al secondo tentativo; 29598 ne 149; 99999901 ne 682

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-06 → 2026-11-26
- **Macchine:** 28418, 29598, 37008, 24338, 54124120, 23718, 33326, 24866, 37119, 99999901
- **Prove:** 28418, flash a 4.20.101 del 26/11 (SLIM-212 alle 11:32):
- 11:34: 'RILEVATO LOOP BOOTLOADER (RDY)' e gmi_flash_attempt_failed (attempt 0, addr null, offset null, errore 'Nessuna conferma finale', risposta ACK + byte spuri + RDY);
- 11:36: fw_change 4.20.100 -> 4.20.101;
- nessun gmi_flash_failed.
28418 oggi: fe 13, ne 1, ore 36; test 8.4 KO del 24/11 (verso Pi->GMI).
29598: ne 149 a uptime 11087 s.
99999901 (tornello di banco): fe 31, ne 682, rssi -111.
37008: ore 45, pi_uart brk 5.
24338: ore 38, brk 5.
- **Ipotesi:** Sulla 28418 il disturbo in ricezione sulla GMI ha fatto perdere la conferma finale del flash; il recovery ha ripreso al primo tentativo. Con addr null non si distingue settore da linea. Non confermato.
- **Proposta:** Laboratorio:
- 28418: colore della GMI, 8.4 con un altro cavo, misura del segnale RX;
- 99999901: test 8.4.
Campo Aprilia: test 8.4 sulla 29598.
Maurizio:
- valorizzare addr/offset anche quando il flash si ferma alla conferma finale (es. 'final');
- contatori come delta giornaliero.
- **Gia' noto:** Aggiornamento firmware GMI che fallisce (linea disturbata GMI verdi; gmi_flash_attempt_failed dalla 211)

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

<a id="cg-022"></a>

### CG-022 · gmi_hostlink: con la 211/212 i blocchi durante il flash GMI risultano 'linea' (5 macchine su 7); 29597 senza blocchi da ieri

- **Area:** pi · **Gravita':** medium · **Visto:** 2026-11-12 → 2026-11-26
- **Macchine:** 29597, 36804, 37111, 24338, 37008, 33089, 33957, 28418, 37112, 36842, 29598, 77700011, 37118, 24349, 25158, 23718, 32996, 25157, 28419, 32995, 25356, 99999901, 26087, 25357
- **Prove:** 26/11, blocco nello stesso minuto del fw_change a 4.20.101, cause 'linea', durata 8-10 s:
- 37111 alle 11:21;
- 33089 alle 11:24;
- 37008 alle 12:02;
- 24338 alle 12:08;
- 33957 alle 14:49, con gmi_silence_s 20.
Nello stesso caso 'avvio_gmi' corretto:
- 28418 alle 11:36 (gmi_boot_ago_s 45);
- 37112 alle 22:49 (gmi_boot_ago_s 34).
33957 alle 15:00: avvio_gmi dopo il cambio mod dal menu tecnico. Accensioni di oggi: avvio_app (33089, 37112, 33957).
29597: nessun blocco dal 25/11, solo l'accensione delle 06:53.
- **Ipotesi:** Quando la GMI si riavvia dopo il flash, a volte il primo dato utile arriva prima che gmi_boot_ago_s sia noto, e il classificatore cade su 'linea'. Non e' un disturbo reale. Non confermato.
- **Proposta:** Maurizio: se nei 60 s precedenti c'e' stato un flash o un fw_change, classificare 'flash' o 'avvio_gmi'.
Campo Aprilia: test linea 8.4 sulla 29597, ancora utile.
- **Gia' noto:** Pagamenti bloccati perche' la GMI non sente il Pi (evento gmi_hostlink)

<a id="cg-024"></a>

### CG-024 · 33326 (lab): dopo il cambio SD/GMI del 18/11 in loop RDY con NCG 4.09, offline dalle 10:50

- **Area:** firmware · **Gravita':** medium · **Visto:** 2026-11-16 → 2026-11-18
- **Macchine:** 33326
- **Prove:** 18/11:
- 10:44: reboot (uptime 38), version_change 205->192, gmi_mute NCG4.09 no_bootloader;
- 10:45: fw da 4.20.31 a 4.09, device_key_mismatch;
- 10:49: version_change 192->200, app_down e 'RILEVATO LOOP BOOTLOADER (RDY)' (YRDYRDY...);
- da allora nessun report (alle 10:50).
L'avviso gmi_blocked (errore 98) si e' chiuso alle 10:47.
Ora: branch mod5 (era beta), fw riportato 4.09, schermata 88.
La 24338 ha fatto lo stesso giro alle 11:13 (205->192, fw 4.09), ma alle 11:30 e' tornata a 205 / 4.20.98.
- **Ipotesi:** In laboratorio stanno usando la SD golden e/o un'altra GMI. Sulla 33326 il flash e' rimasto a meta' (RDY), come il 16/11 al blocco 13824. Non confermato.
- **Proposta:** Laboratorio: dire cosa e' stato montato sulla 33326.
ST-Link (9.5) con bootloader V2 e 4.20.93/98, poi riaccenderla.
Maurizio: loggare l'indirizzo del blocco fallito.
- **Gia' noto:** Aggiornamento firmware GMI che fallisce (gmi_flash_failed, gmi_blocked, loop RDY)

<a id="cg-011"></a>

### CG-011 · Dashboard: centro null su 22 macchine (nuove 37108-37119), chiave 'missing' su 21784, 'mismatch' su 33326 e 77700011

- **Area:** dashboard · **Gravita':** low · **Visto:** 2026-11-04 → 2026-11-21
- **Macchine:** 21784, 23718, 24338, 28418, 33326, 37008, 99999901, 36804, 36805, 77700011, 37108, 37109, 37110, 37111, 37112, 37114, 37115, 37116, 37117, 37118, 37119
- **Prove:** Centro null su:
- 21784, 23718, 24338, 28418, 33326, 37008, 99999901, 36804, 36805, 77700011, 54124120;
- le 11 nuove 37108-37119.
device_key_status 'missing' su 21784 e sul Pi senza MHD; 'mismatch' su 33326 e 77700011 (avviso aperto dal 19/11).
Conteggio flotta 47; gli ID di banco precedenti non compaiono piu'.
- **Ipotesi:** Macchine in preparazione senza registro. Probabilmente il banco e' stato rinumerato con gli MHD definitivi.
- **Proposta:** Dashboard/Maurizio:
- assegnare il centro o marcare 'banco' le 371xx, 36804 e 36805;
- escludere banco e lab da conteggio e avvisi;
- ri-registrare la chiave della 21784;
- ripulire i vecchi ID di banco.
- **Gia' noto:** Profilo display auto / golden SD

<a id="cg-018"></a>

### CG-018 · Banco/lab: beta a 212 / 4.20.101 (37111, 37112), 37113 gmi_mute e DNS, 99999901 tre riavvii e di nuovo offline

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-09 → 2026-11-27
- **Macchine:** 37108, 37109, 37110, 37111, 37112, 37113, 37114, 37115, 37116, 37117, 37118, 37119, 36804, 36805, 77700011, 23718, 28418, 33326, 54124120, CG-4F2F67B8, 24338, 37008, 99999901
- **Prove:** 26/11, SLIM-212 e fw 4.20.101 senza gmi_flash_failed:
- 37111: 11:17 e 11:21;
- 37008: 12:00 e 12:02;
- 24338: 12:04 e 12:08;
- 37112 (accesa alle 22:41): 205 -> 212 alle 22:46, fw 4.20.98 -> 4.20.101 alle 22:49.
28418 in CG-016.
37113:
- reboot alle 13:46, 15:35, 21:51 e 05:05;
- alle 15:35 gmi_mute (probes 5, reason mute);
- update_failed DNS/443 ripetuti, tutti recovered;
- WCDMA a -85 dBm.
99999901: reboot alle 12:34, 12:53 e 15:06, 10 vendite cash tra le 12:35 e le 15:16, offline dalle 15:53.
36804: 14 vendite su 15.
Accese la sera o la mattina: 36805, 37114, 37115, 37116, 37119.
33326 e 23718 offline dal 18/11.
- **Ipotesi:** Lavori di laboratorio sulle 371xx e sul tornello. Il gmi_mute della 37113 avviene a un riavvio: GMI non pronta o spenta. Non confermato.
- **Proposta:** Laboratorio:
- 37113: rete/SIM e GMI muta;
- 99999901: alimentazione e riavvii;
- dire la destinazione delle 371xx e delle 36804/36805.
Dashboard: togliere il vecchio ID 54124120.
- **Gia' noto:** golden SD (CG-<seriale>); RDY durante il flash = CG-001

<a id="cg-025"></a>

### CG-025 · Tornello di banco 99999901 (MOD10): 15 vendite su 19, STAN duplicato, schermata 161 a hopper vuoto

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-16 → 2026-11-19
- **Macchine:** 99999901
- **Prove:** 18/11:
- 19 transazioni tra le 10:02 e le 13:26, 15 approvate (14 cash, 5 tentativi carta);
- 10:04: codice 37 con 'POS riattivato dopo codice 90';
- 10:12: timeout con 'esito H scartato: STAN 000002 gia' registrato';
- nessun gate_short_change nelle 24 h.
Oggi: schermata 161 (non da' resto, importo esatto), tramogge 0,0,0, POS IDLE, TID 97942484.
- **Ipotesi:** La schermata 161 e' comportamento voluto con l'hopper vuoto. Il STAN duplicato e' coerente col TID condiviso (CG-006). Non confermato.
- **Proposta:** Laboratorio:
- rifornire l'hopper;
- TID distinto.
Maurizio: non emettere gate_short_change con missing=0; controllare la gestione del STAN duplicato.
- **Gia' noto:** MOD10 Tornello; POS: altri errori

## In osservazione

<a id="cg-032"></a>

### CG-032 · 33957 (Carpi): rientrata il 26/11 alle 14:27 dopo intervento (probabile SD nuova), su beta 212/4.20.101, vende

- **Area:** campo · **Gravita':** medium · **Visto:** 2026-11-23 → 2026-11-26
- **Macchine:** 33957
- **Prove:** 26/11, rientro:
- 14:27: reboot (uptime 43) e version_change 200 -> 192;
- 14:28: device_key_mismatch;
- 14:32: version_change 192 -> 200;
- 14:33: device_key_enrolled;
- GIT_BRANCH applicato alle 14:44;
- 14:46: SLIM-212;
- 14:50: fw da 4.20.93 a 4.20.101, nessun flash fallito.
Menu tecnico dalle 14:50 alle 15:09:
- mod 5 ini;
- tramoggia 1 riempita, fondo 500 €;
- spegnimento notturno alle 22:00.
Vendite: 19 transazioni dalle 15:04 alle 19:02, 18 approvate (9 carte, 10 cash). Ultimo report alle 20:25.
Oggi:
- accensione normale alle 09:00 (uptime 133), nessun serial_missing;
- fe 5, ne 1;
- cavo BG04MVH4;
- stm32 rev 0x101F.
- **Ipotesi:** Il passaggio 192 -> 200 con la chiave registrata di nuovo e' lo stesso schema della golden SD: probabilmente sul posto e' stata cambiata la SD. Le due mattine spente potevano essere un problema del Pi o della SD, non solo dell'alimentazione. Non confermato.
- **Proposta:** Campo Carpi: dire cosa e' stato sostituito il 26/11 (SD? GMI? alimentatore?).
Monitoraggio: chiudere dopo 2-3 accensioni regolari con fe/ne fermi.
- **Gia' noto:** Seriale assente al mattino (variante a meta' giornata da cavo guasto); golden SD

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

<a id="cg-012"></a>

### CG-012 · Codice 31: quattro giorni senza rifiuti, voce chiusa

- **Area:** pos · **Gravita':** low · **Visto:** 2026-11-04 → 2026-11-15
- **Macchine:** 24254, 28418, 33957, 24866, 29597, 23718, 58888999, 33089, 25356, 24349
- **Prove:** 16, 17, 18 e 19/11: nessun 'codice 31' in flotta.
33957: 16 approvate su 17 (7 carte).
Unici errori carta nelle 24 h: codice 90 (16234 alle 18:14, 29597 alle 13:56) e 'nessuna carta entro il tempo'.
- **Ipotesi:** I rifiuti del 15/11 sono rientrati dopo l'intervento POS sulla 33957.
- **Proposta:** Chiusa. Riaprire se ricompare il codice 31.
- **Gia' noto:** POS: altri errori

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

<a id="cg-015"></a>

### CG-015 · 33957 (Carpi): stabile, 27 vendite su 31, voce chiusa

- **Area:** hardware · **Gravita':** low · **Visto:** 2026-11-05 → 2026-11-16
- **Macchine:** 33957
- **Prove:** 20/11: 31 transazioni tra le 10:01 e le 19:55, 27 approvate (8 carte), 4 annullate.
Nessun evento seriale; fe 3, ore 1.
Oggi riaccensione normale alle 09:00 (uptime 125), POS IDLE.
- **Ipotesi:** Lo spegnimento del 19/11 era esterno.
- **Proposta:** Chiusa. Resta consigliato il test linea 8.4: l'ultimo, del 05/11, era DISTURBATA.
- **Gia' noto:** Seriale assente al mattino; aggiornamento firmware GMI (linea disturbata)

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

<a id="cg-026"></a>

### CG-026 · 25254 (Tiburtino): spenta tutto il 18/11, di nuovo in vendita, voce chiusa

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-18 → 2026-11-18
- **Macchine:** 25254
- **Prove:** 19/11: 1 vendita cash approvata alle 20:43, ultimo report alle 21:04.
Oggi: riaccensione normale alle 07:46 (uptime 146), POS IDLE, throttled 0x0, schermata 70, tramogge 1,1,0.
- **Ipotesi:** Spegnimento a monte per un giorno intero il 18/11. Causa non nota.
- **Proposta:** Chiusa. Se il tecnico lo sa, annotare cosa e' successo il 18/11.

<a id="cg-027"></a>

### CG-027 · Nuove macchine: 16234 vende regolarmente; 36804 e 36805 di nuovo online (seguite in CG-018), voce chiusa

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-18 → 2026-11-20
- **Macchine:** 16234, 36804, 36805
- **Prove:** 16234: 15 vendite su 15 (14 cash, 1 carta) tra le 10:29 e le 20:46 del 26/11; accesa oggi alle 07:05.
36804 e 36805 online dal 25/11: 36804 14 vendite su 15; la 36805 si e' riaccesa alle 22:54 e alle 09:03.
- **Ipotesi:** Installazione della 16234 riuscita. 36804 e 36805 restano macchine di banco.
- **Proposta:** Chiusa. 36804/36805 in CG-018 (destinazione), POS in CG-003, TID in CG-006.

<a id="cg-028"></a>

### CG-028 · Aprilia: riavvii simultanei del 20/11 non ripetuti, voce chiusa

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-18 → 2026-11-20
- **Macchine:** 26087, 29597, 29598, 24866
- **Prove:** 21 e 22/11: nessun riavvio in giornata sulle quattro.
Vendite del 22/11:
- 26087: 24 su 26;
- 29597: 23 su 27;
- 29598: 17 su 17;
- 24866: 24 su 30.
Oggi accensioni singole: 24866 alle 05:41, 29598 alle 06:46, 29597 alle 06:53, 26087 alle 07:30.
- **Ipotesi:** Stacchi di alimentazione a monte del 19-20/11, non guasti delle macchine.
- **Proposta:** Chiusa. Riaprire se si ripetono riavvii simultanei in giornata.

<a id="cg-031"></a>

### CG-031 · 33957 (Carpi): carte regolari per il secondo giorno, voce chiusa

- **Area:** pos · **Gravita':** low · **Visto:** 2026-11-21 → 2026-11-22
- **Macchine:** 33957
- **Prove:** 23/11:
- 11 transazioni, 10 approvate (7 carta, 4 cash), 1 annullata;
- card_activity ok 6, ko 0;
- nessun codice 90.
Oggi riaccensione alle 09:00, POS IDLE.
- **Ipotesi:** Il codice 90 del 21/11 era transitorio.
- **Proposta:** Chiusa. Riaprire se ricompare il codice 90. I riavvii del 23/11 sono in CG-032.
- **Gia' noto:** POS: altri errori
