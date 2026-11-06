# Registro problemi flotta CGSLIM

Aggiornato dall'agente il 06/11/2026 10:04. Una voce per causa; MHD senza zeri. Generato: non modificare a mano.

## Aperti

### CG-003 · POS DISCONNECTED dopo timeout get_advanced_config: 24350, 24866, 33326, 37008 (anche con 187 e 189)

- **Area:** pi · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-06
- **Macchine:** 24350, 24866, 33326, 37008, 24349, 25158, 36842, 26087, 29597, 29598, 28418, 28416, 24338, 23718, 32996, 24254
- **Prove:** Ora DISCONNECTED con 'Timeout locale in attesa di get_advanced_config (15.0s)':
- 24350 (187): 1 vendita cash alle 16:19;
- 24866 (187): 6 cash, nessuna carta; anche col Pi nuovo delle 09:48;
- 33326 (189): nessuna transazione;
- 37008 (187): 12 cash, nessuna carta.
Avviso 'POS in errore su 3 macchine' aperto dalle 05:02 UTC.
36842 dopo il cambio Pi: IDLE e senza p95_error.
'Connessione persa durante get_advanced_config', rientrate entro 15 min (UTC):
- 24349 alle 12:47 e 15:02;
- 25158 alle 15:32;
- 36842 alle 16:17;
- 26087 alle 16:32 e 20:47;
- 29597 alle 17:02.
- **Ipotesi:** Su alcuni terminali la lettura cashless_info va sempre in timeout e il pos-engine resta DISCONNECTED. Le release 187 e 189 non cambiano il comportamento.
Su 24866 il problema resta col Pi nuovo: sembra legato al terminale e non al Pi.
- **Proposta:** Maurizio:
- Un errore di get_advanced_config non deve bloccare il P95: saltare la lettura e ritentarla con backoff.
- Log di pos-engine da 37008 o 33326.
Campo: prova con carta reale su 24350 e 24866.
- **Gia' noto:** POS: get_advanced_config

### CG-009 · 24254 (Aprilia) si ferma la sera alle ~19:50 (5 volte) e si spegne anche in giornata

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-02 → 2026-11-06
- **Macchine:** 24254
- **Prove:** 05/11:
- offline dalle 11:10 (avviso alle 10:47 UTC);
- reboot alle 13:05 (uptime 140, fuori dal timer);
- aggiornata a 187 alle 17:05 e fw 4.20.90 alle 17:09;
- ultimo report alle 19:54: quinta sera consecutiva tra le 19:47 e le 19:54.
06/11: alle 10:00 ancora offline (845 min). Ieri si era riaccesa alle 08:53.
Configurazioni GIT_PULL_INTERVAL_SEC e INTERVAL_UPDATE_CHECK pending dal 05/11 20:33 UTC (macchina gia' offline).
Nelle 24 h: 1 carta approvata alle 15:01, 3 timeout cliente e 1 cash.
- **Ipotesi:** L'alimentazione viene tolta a orario fisso la sera e la macchina viene rialimentata a mano in giornata: presa o timer diversi dalle altre Aprilia. Lo spegnimento delle 11:10 e la sottotensione dal boot indicano anche un'alimentazione instabile.
- **Proposta:** Campo Aprilia, oggi:
- Verificare presa e timer e riaccendere la macchina.
- Sostituire l'alimentatore.
- Recuperare journal e dmesg attorno alle 11:10 e alle 19:54 del 05/11.

### CG-004 · Seriale GMI assente all'accensione (FTDI non enumerato), cavi lotto BG03E: ricapitato su 25158

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-06
- **Macchine:** 25158, 32996
- **Prove:** 06/11 su 25158 (cavo BG03ES5F):
- reboot alle 09:22 (uptime 109);
- exception 'ERRORE CRITICO SERIALE ... /dev/ttyUSB0';
- serial_missing not_enumerated: sul bus solo hub, LAN e touch ILITEK, nessun FTDI;
- reboot alle 09:26 (uptime 41) e serial_recovery alle 09:27, poi in servizio (screen 71).
32996 (BG03ER1N): reboot alle 09:03 senza serial_missing, secondo mattino pulito.
Il 05/11 nessun episodio. Il cavo non e' stato scambiato.
- **Ipotesi:** Problema noto e intermittente del lotto FT232R BG03E e/o dell'alimentazione a ritroso dalla GMI. Il mattino pulito di ieri non indicava una risoluzione.
- **Proposta:** Campo Parma: scambiare il cavo della 25158 con uno AL05 e lasciare 32996 come controllo.
Pi: riavvio anticipato, uhubctl e TX della GMI in high-Z nel prossimo rilascio.
- **Gia' noto:** Seriale assente al mattino (serial_missing, not_enumerated)

### CG-005 · Sottotensione del Raspberry: 23718 fissa, 24349 a episodi tutto il giorno; 36842 risolta col cambio Pi, 33326 0x0 dopo il reboot delle 09:50

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-06
- **Macchine:** 23718, 24349, 33326, 24254, 24350, 24338, 36842
- **Prove:** Orari degli avvisi in UTC.
- 23718: 0x50005 aperto dal 03/11 10:47, ancora attivo alle 08:47. Uptime 251113 s: non si spegne la notte.
- 24349, episodi ADESSO il 05/11: 09:02, 10:17, 11:47, 12:47, 14:17, 15:02, 15:47, 16:17, 17:02, 19:02, 20:02, 20:32, 21:02, 21:32, 22:32. Ora 0x50000.
- 33326: episodi ogni 30-60 min dal 05/11 08:47 al 06/11 08:47 (avviso ancora aperto). Dopo il reboot delle 09:50 locali il payload e' 0x0.
- 36842: episodi alle 09:02, 11:32, 14:02 e 14:32 sul Pi vecchio (a771b94f). Dal Pi nuovo (24e994d9, first_seen 15:30 locali) 0x0.
- Sottotensione dal boot (0x50000): 24254, 24338, 24350 (ieri 0xd0000).
- **Ipotesi:** Alimentatori o cavi deboli. Su 36842 il cambio del Pi (con il suo alimentatore?) ha eliminato la sottotensione.
Su 33326 non si sa se il reboot delle 09:50 sia stato un intervento sull'alimentazione: va confermato nelle prossime ore.
- **Proposta:** Hardware/campo, in ordine:
1. 23718 (fissa da 3 giorni).
2. 24349.
3. 24254 (vedi CG-009).
4. Verificare se su 33326 e' stato cambiato l'alimentatore.
5. 24350 e 24338.
- **Gia' noto:** host.throttled 0x50000 (scheda campi); sottotensione sospettata nei flash GMI falliti

### CG-006 · TID POS anomali: 36842 ancora TID 00000000 anche col Pi nuovo, beta con TID di prova 9794248x

- **Area:** pos · **Gravita':** medium · **Visto:** 2026-10-30 → 2026-11-06
- **Macchine:** 36842, 24338, 23718, 28418, 33326
- **Prove:** 36842, dopo il cambio del Pi del 05/11 15:30:
- POS IDLE e connesso;
- TID 00000000, nessun acquirer, package 01.04.25.03, SN 58551425;
- solo 2 vendite cash, nessuna carta.
TID della serie di prova 9794248x:
- 24338: 97942485;
- 23718: 97942484;
- 28418: 97942488.
33326: POS DISCONNECTED, TID non leggibile.
- **Ipotesi:** Il terminale della 36842 non e' parametrizzato: il cambio del Pi non c'entra. I TID 9794248x sembrano di prova e in produzione rischiano l'errore 48.
- **Proposta:** Hardware/POS:
- Parametrizzare la 36842 con il TID di produzione.
- Verificare i TID di 24338, 23718 e 28418.
- Leggere il TID di 33326 quando il POS torna connesso.
- **Gia' noto:** POS: altri errori (errore 48, TID duplicato su 24338)

### CG-012 · POS: 'activate gia' in corso' e 'POS non attivo (codice 90)' subito dopo l'avvio

- **Area:** pi · **Gravita':** medium · **Visto:** 2026-11-04 → 2026-11-05
- **Macchine:** 24254, 28418, 33957
- **Prove:** Nelle ultime 24 h nessun 'activate gia' in corso'.
33957 il 05/11 alle 11:16: 'POS non attivo (codice 90)'. Era il giorno dell'installazione, circa 25 min dopo il primo avvio e il flash ST-Link. Poi 14 approvate su 17 (5 carta).
24254: solo timeout cliente.
Storico:
- 24254, 04/11 alle 11:04: 28 errori 'activate gia' in corso';
- 24254, 05/11 alle 09:00: codice 90;
- 28418, 04/11 alle 10:32.
- **Ipotesi:** Un pagamento viene avviato mentre il POS non ha finito l'attivazione dopo l'avvio. Oggi si e' presentato una sola volta.
- **Proposta:** Maurizio: nel client P95 attendere l'activate invece di restituire errore. Disabilitare la carta finche' il POS non e' IDLE.

### CG-014 · MOD inattesa su branch mod5: 24866 ora mod 12 col Pi nuovo, 23718 mod 4 senza vendite

- **Area:** firmware · **Gravita':** medium · **Visto:** 2026-11-05 → 2026-11-06
- **Macchine:** 24866, 23718
- **Prove:** 24866 (branch mod5, fw 4.20.90):
- col Pi vecchio era mod 2, screen 40;
- col Pi nuovo (09:48) e' mod 12, screen 71, hopper 1,0,0;
- 6 vendite cash il 05/11 (10:18-18:23).
23718 (branch mod5, 187):
- mod 4, screen 23, hopper 0,0,0;
- nessuna transazione nelle 24 h; ultima carta approvata circa il 03/11;
- uptime 2,9 giorni.
- **Ipotesi:** Su 24866 la MOD cambia con l'intervento sul posto: o la modalita' e' stata reimpostata dal tecnico, o la GMI riporta valori diversi.
Su 23718 mod 4 con hopper 0,0,0 potrebbe spiegare l'assenza di vendite. Il significato di mod 4 non e' nella scheda.
- **Proposta:** Maurizio: chiarire quali MOD sono attese per 24866 e 23718 e se il flash 4.20.90 preserva la MOD.
Campo:
- Aprilia: controllare la modalita' di 24866 dal menu tecnico.
- 23718: verificare che eroghi (tramogge, schermata).

### CG-011 · Dashboard: centro null, chiave non corrispondente e config pending su 33326, device duplicati dopo cambio Pi (24866, 36842)

- **Area:** dashboard · **Gravita':** low · **Visto:** 2026-11-04 → 2026-11-06
- **Macchine:** 23718, 24338, 28418, 33326, 37008, 24866, 36842
- **Prove:** Centro ancora null per 23718, 24338, 28418, 33326 e 37008.
33326 (device 27192bb4):
- device_key mismatch (nuovo evento alle 15:55 del 05/11);
- INTERVAL_UPDATE_CHECK di nuovo pending dal 05/11 20:33 UTC, pur essendo online.
24866 compare due volte:
- device b7233887 (Pi Model B Plus Rev 1.2, ultimo report 08:32, avviso offline);
- device nuovo 'CG-NFC-BETA' (Pi 3 B+, first_seen alle 09:48, device_key_enrolled alle 09:49). Stesso uid GMI e stesso cavo AL05ZNFW.
36842: nuovo device 24e994d9 'CG-NFC-BETA' (first_seen 05/11 15:30), vecchio a771b94f.
Per questo il conteggio flotta e' 22 invece di 21.
- **Ipotesi:** I cambi di Pi/SD creano un nuovo device e la dashboard non unisce quello vecchio con lo stesso MHD. Il conteggio online risulta falsato. Su 33326 la chiave non corrisponde, quindi le configurazioni non vengono accettate.
- **Proposta:** Dashboard/Maurizio:
- Archiviare b7233887 e a771b94f, oppure unire per MHD tenendo il device piu' recente.
- Ri-registrare la chiave di 33326 e capire perche' le config restano pending.
- Completare il centro delle 5 macchine.
- **Gia' noto:** Profilo display auto / golden SD (hostname clonati, chiave fleet rigenerata)

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

### CG-016 · Contatori errori seriali alti lato GMI: 28418 (fe 98, ore 70, test linea KO) e 29598 (ne 127)

- **Area:** hardware · **Gravita':** low · **Visto:** 2026-11-06 → 2026-11-06
- **Macchine:** 28418, 29598, 23718
- **Prove:** Contatori lato GMI:
- 28418: fe=98, ne=29, ore=70 con uptime 779344 s (circa 9 giorni acceso); ultimo test linea KO il 20/10.
- 29598: ne=127 con uptime 11011 s.
- 23718: fe=50, ore=66.
Le altre mod12 hanno fe 2-8 e ne 0-5.
Nessun gmi_hostlink anomalo in giornata su queste macchine: solo quello all'avvio di 29598 alle 06:45 e il riavvio app delle 21:48.
- **Ipotesi:** Linea seriale disturbata (cavo, massa o GMI verde). Su 28418 i contatori possono essersi accumulati nei 9 giorni di accensione continua. Su 29598 tanti ne in 3 h sono anomali.
- **Proposta:** Campo: test linea 8.4 su 29598 e 28418.
Maurizio: valutare l'invio dei contatori come delta giornaliero per poterli confrontare.
- **Gia' noto:** Aggiornamento firmware GMI (linea disturbata GMI verdi)

## In osservazione

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

### CG-010 · 37008: dopo il riavvio notturno del 05/11 02:50 stabile, resta accesa la notte

- **Area:** campo · **Gravita':** medium · **Visto:** 2026-11-03 → 2026-11-05
- **Macchine:** 37008
- **Prove:** Uptime 111667 s: nessun reboot dal 05/11 circa alle 02:50, nessun avviso offline stanotte.
Il 05/11:
- version_change 185->187 alle 16:01, con gmi_hostlink locked/unlocked nello stesso minuto;
- 12 vendite cash tra le 10:11 e le 21:55.
Throttled 0x0. POS DISCONNECTED (CG-003).
- **Ipotesi:** La macchina non e' sotto timer notturno (si alimenta 24 h). Il riavvio delle 02:50 resta senza causa nota, ma non si e' ripetuto.
- **Proposta:** Monitorare. Chiudere se resta stabile fino a lunedi'. Chiedere se il centro (ancora null) tiene la macchina accesa di notte.

### CG-007 · Tramogge 0,0,0 e schermata 73 su Parma MOD12: sparite dopo l'aggiornamento 187/4.20.90

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-01 → 2026-11-05
- **Macchine:** 24350, 28417, 32996, 23718
- **Prove:** Oggi 24350, 28417 e 32996 sono a hopper 1,0,0 e screen 71, come le altre Parma. Ieri tutte e tre sono state aggiornate a 187 e fw 4.20.90 (16:09-16:35).
23718 (mod 4, branch mod5) e' a hopper 0,0,0, screen 23 e non ha transazioni nelle 24 h (vedi CG-014).
- **Ipotesi:** Lo stato 0,0,0/73 era probabilmente legato alla combinazione 176/4.20.84 o a uno stato rimasto dal flash. Con la nuova release non si e' ripresentato.
- **Proposta:** Chiudere se le tre Parma restano a 1,0,0 anche lunedi'.
Maurizio: chiarire comunque il significato di screen 73.

## Risolti

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

### CG-008 · Branch riportato 'parma' ma servizio gitpuller@beta su 3 macchine Aprilia

- **Area:** dashboard · **Gravita':** low · **Visto:** 2026-11-01 → 2026-11-01
- **Macchine:** 26087, 29597, 29598
- **Prove:** Il 02/11 dalle 16:35 e' stato applicato il provisioning GIT_BRANCH. Oggi 26087, 29597 e 29598 riportano branch 'beta', servizio gitpuller@beta, git_commit ea89cae e SLIM-4.20.179. Il branch riportato e il servizio coincidono.
- **Ipotesi:** Disallineamento sistemato dal provisioning del branch.
- **Proposta:** Nessuna azione.

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
