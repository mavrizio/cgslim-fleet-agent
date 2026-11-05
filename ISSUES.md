# Registro problemi flotta CGSLIM

Aggiornato dall'agente il 05/11/2026 10:04. Una voce per causa; MHD senza zeri. Generato: non modificare a mano.

## Aperti

### CG-003 · POS DISCONNECTED dopo timeout get_advanced_config: 24350, 24866, 33326, 37008 (anche con 185 e 187)

- **Area:** pi · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-05
- **Macchine:** 24350, 24866, 33326, 37008, 36842, 26087, 29597, 29598, 28418, 28416, 24338, 23718, 32996, 25158, 24254
- **Prove:** Ora DISCONNECTED con 'Timeout locale in attesa di get_advanced_config (15.0s)':
- 24350 (176): 1 vendita cash in 24 h (16:33).
- 24866 (ora 185, fw 4.20.90): 10 vendite cash, nessuna carta.
- 33326 (187): 1 annullata.
- 37008 (185): 4 vendite cash.
36842: stesso errore, ma stato IDLE e connected.
Avviso 'POS in errore su 5 macchine' aperto dalle 05:02 UTC.
'Connessione persa durante get_advanced_config', rientrata entro 15 min:
- 26087 e 29598 (17:02 e 18:02 UTC);
- 28418 (19:17 UTC);
- 28416 (07:47 UTC).
- **Ipotesi:** Problema noto della lettura cashless_info. Su alcuni terminali la lettura va in timeout e il pos-engine resta DISCONNECTED; ne' la 185 ne' la 187 lo risolvono. Le chiusure di connessione sono innocue.
- **Proposta:** Maurizio:
- Un errore di get_advanced_config non deve lasciare il P95 DISCONNECTED: saltare la lettura e ritentarla con backoff.
- Log di pos-engine da 33326 o 37008 (beta/185, raggiungibili).
Campo: prova con carta reale su 24350 e 24866.
- **Gia' noto:** POS: get_advanced_config

### CG-009 · 24254 (Aprilia) si ferma la sera alle ~19:50 (4 volte) e si riavvia in giornata

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-02 → 2026-11-05
- **Macchine:** 24254
- **Prove:** 04/11:
- Rientrata alle 11:02 (reboot, uptime 139, fuori dal timer).
- Riavvii alle 14:39 e 15:33, entrambi con uptime 65: avviso reboot_storm 3 in 6 h.
- Sottotensione ADESSO alle 11:47 e 12:47 UTC.
- Offline dalle 19:50: quarta sera (19:47-19:50).
05/11: riaccesa alle 08:53 (uptime 135), cioe' col timer, a differenza dei giorni scorsi.
Ora: POS IDLE, throttled 0x50000.
- **Ipotesi:** L'alimentazione viene tolta a orario fisso la sera (presa o timer diverso dalle altre Aprilia, che trasmettono fino alle 23). I riavvii con uptime 65 e la sottotensione indicano anche un'alimentazione instabile in giornata.
- **Proposta:** Campo Aprilia:
- Verificare presa e timer a cui e' collegata.
- Sostituire l'alimentatore.
- Recuperare journal e dmesg attorno alle 14:39, alle 15:33 e alle 19:50 del 04/11.

### CG-005 · Sottotensione del Raspberry (alimentatori/cavi): 33326 continua, 23718 fissa, 36842, 24349 e 24254 a episodi

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-05
- **Macchine:** 33326, 23718, 36842, 24349, 24254, 24350, 24338
- **Prove:** Orari degli avvisi in UTC.
Episodi di sottotensione ADESSO:
- 33326: quasi ogni ora dal 04/11 08:47 a stamattina (aperto alle 08:47); 0x50005.
- 23718: 0x50005 aperto dal 03/11 10:47 e ancora attivo alle 08:47.
- 36842: 04/11 14:47, 19:17, 22:32; oggi 08:17. Ora 0x50005.
- 24349: 04/11 12:32, 15:47, 16:32. Ora 0x50005 a 33 min dall'avvio.
- 24254: 04/11 11:47 e 12:47, con riavvii alle 14:39 e 15:33 (uptime 65). Ora 0x50000.
Sottotensione dal boot (0x50000): 24350 e 24338.
- **Ipotesi:** Alimentatori o cavi deboli. Su 24254 i riavvii con uptime breve vicini agli episodi fanno pensare a cali di alimentazione.
- **Proposta:** Hardware/campo, in ordine:
1. 33326.
2. 24254 (anche per CG-009).
3. 23718 (nuova: alimentatore fornito).
4. 36842 e 24349.
5. 24350 e 24338.
- **Gia' noto:** host.throttled 0x50000 (scheda campi); sottotensione sospettata nei flash GMI falliti

### CG-006 · TID POS anomali: 36842 con TID 00000000, macchine beta con TID della serie di prova 9794248x

- **Area:** pos · **Gravita':** medium · **Visto:** 2026-10-30 → 2026-11-05
- **Macchine:** 36842, 24338, 23718, 28418, 33326
- **Prove:** 36842:
- TID 00000000, nessun acquirer, package 01.04.25.03, SN 58551425;
- p95_error get_advanced_config ma stato IDLE;
- solo 2 vendite cash nelle 24 h.
TID della serie 9794248x, la stessa del TID di prova noto 97942487:
- 24338: 97942485;
- 23718: 97942484;
- 28418: 97942488.
33326: POS DISCONNECTED, TID non leggibile.
- **Ipotesi:** Il terminale della 36842 non e' parametrizzato: la carta non puo' funzionare. I TID 9794248x sembrano terminali di prova: in produzione sono un rischio di errore 48.
- **Proposta:** Hardware/POS:
- Parametrizzare la 36842 con il TID di produzione.
- Verificare che 24338, 23718 e 28418 abbiano TID di produzione distinti.
- Leggere il TID di 33326 quando il POS torna connesso.
- **Gia' noto:** POS: altri errori (errore 48, TID duplicato su 24338)

### CG-012 · POS: 'Operazione activate gia' in corso' e 'POS non attivo (codice 90)' subito dopo l'avvio

- **Area:** pi · **Gravita':** medium · **Visto:** 2026-11-04 → 2026-11-05
- **Macchine:** 24254, 28418
- **Prove:** 24254 (176), il 04/11 alle 11:04, 2 minuti dopo il reboot delle 11:02:
- 28 transazioni card_p95 con 'Operazione activate gia' in corso';
- 1 '[Errno 32] Broken pipe';
- avviso pos_error 'activate gia' in corso' alle 10:17 UTC.
24254 il 05/11 alle 09:00: 'POS non attivo (codice 90)', poi una carta approvata alle 09:00.
Totale 24254 nelle 24 h: 33 ko, 1 ok, 6 annullate.
28418 il 04/11 alle 10:32: 2 'activate gia' in corso' e 1 codice 90.
- **Ipotesi:** Un pagamento viene avviato mentre il pos-engine sta ancora facendo l'activate dopo l'avvio. 28 errori nello stesso minuto fanno pensare a un ritentativo automatico in loop della UI o del client, non a 28 clienti. Non e' nella scheda di conoscenza.
- **Proposta:** Maurizio:
- Nel client P95 attendere o accodare la richiesta finche' l'activate e' in corso, invece di restituire errore.
- Mostrare 'POS in avvio' e disabilitare la carta finche' il POS non e' IDLE.
- Verificare chi ritenta 28 volte in un minuto.

### CG-007 · Tramogge 0,0,0 e schermata 73 dopo l'avvio su macchine Parma MOD12

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-01 → 2026-11-05
- **Macchine:** 24350, 28417, 32996, 25158, 37008
- **Prove:** 05/11: hopper ['0','0','0'] e screen 73 su:
- 24350 (uptime 2905);
- 28417 (uptime 4698);
- 32996 (uptime 2965).
Sono le stesse tre di ieri. 25158 e 37008 sono a 1,0,0 e screen 71.
Vendite nelle 24 h: 24350 1 cash; 28417 e 32996 nessuna transazione registrata.
- **Ipotesi:** Stato legato al livello della tramoggia 1 o a una schermata specifica. Oggi e' stabile sulle stesse macchine. Il significato di screen 73 non e' nella scheda.
- **Proposta:** Maurizio: chiarire screen 73 e quando la GMI manda #HPS 0,0,0.
Campo Parma: controllare la tramoggia 1 di 24350, 28417 e 32996.

### CG-011 · machine_registry incompleto (centro null) e chiave macchina non corrispondente su 33326

- **Area:** dashboard · **Gravita':** low · **Visto:** 2026-11-04 → 2026-11-05
- **Macchine:** 23718, 24338, 28418, 33326, 37008
- **Prove:** Centro ancora null per 23718, 24338, 28418, 33326 e 37008.
33326:
- device_key_status mismatch, nuovo evento device_key_mismatch alle 15:49 del 04/11;
- avviso aperto dal 03/11 15:02 UTC;
- INTERVAL_UPDATE_CHECK pending dal 04/11 18:36 UTC.
GIT_BRANCH applicato due volte (15:07 e 18:21 UTC) sul device 00000000be399f51, che non corrisponde a nessun MHD nei dati.
- **Ipotesi:** Registro non aggiornato per le beta e la nuova installazione. La chiave di 33326 e' cambiata con la SD sostituita o con l'intervento di ieri.
- **Proposta:** Dashboard/Maurizio:
- Completare il centro delle 5 macchine.
- Ri-registrare la chiave di 33326.
- Capire perche' su 33326 le configurazioni restano pending.
- Identificare il device 00000000be399f51.

### CG-013 · Beta Aprilia e 37008 passate a mod12 restano su SLIM-4.20.185/fw 4.20.90, con lo stesso commit delle mod12 a 176

- **Area:** pi · **Gravita':** low · **Visto:** 2026-11-05 → 2026-11-05
- **Macchine:** 26087, 29597, 29598, 37008
- **Prove:** GIT_BRANCH applicato il 04/11:
- 26087 alle 17:57 UTC, 29598 alle 18:00, 29597 alle 18:02;
- 37008 alle 18:35.
App_restart alle 17:55-19:03.
Ora le quattro riportano branch mod12, gitpuller@mod12, git_commit 65f8fdf, ma SLIM-4.20.185 e fw 4.20.90. Le altre 11 mod12 hanno lo stesso commit 65f8fdf con SLIM-4.20.176 e fw 4.20.84.
- **Ipotesi:** Dopo il cambio verso un branch piu' vecchio il gitpuller non ricostruisce la release (nessun downgrade). Le macchine girano 185 mentre il repo e' a 176: e' lo stato inverso di quello che la scheda indica come anomalo. Se e' voluto, va bene; altrimenti il prossimo merge su mod12 decidera' la versione.
- **Proposta:** Maurizio: confermare che il comportamento e' voluto. In caso contrario, decidere se forzare il rebuild (con downgrade del fw, attenzione al flash) oppure fare il merge di 185 su mod12. La dashboard dovrebbe segnalare quando app_version non corrisponde al commit.

### CG-014 · MOD inattesa su macchine del branch mod5: 24866 mod 2 dopo il flash 4.20.90, 23718 mod 4

- **Area:** firmware · **Gravita':** low · **Visto:** 2026-11-05 → 2026-11-05
- **Macchine:** 24866, 23718
- **Prove:** 24866:
- branch mod5, fw 4.20.90 dalle 16:55 del 04/11 (prima 4.20.84), SLIM-4.20.185;
- ora mod 2, screen 40, chl_mode 4;
- nel registro del 04/11 era indicata in mod5;
- 10 vendite cash nelle 24 h, l'ultima alle 08:11.
23718: branch mod5, mod 4, screen 22.
- **Ipotesi:** Il cambio di modalita' potrebbe venire dal flash (parametri EEPROM reinterpretati da 4.20.90) oppure da una configurazione voluta. I dati non bastano per dirlo. Le vendite cash continuano.
- **Proposta:** Maurizio: verificare se mod 2 e mod 4 sono attese per queste macchine e se il flash 4.20.90 preserva la MOD.
Campo Aprilia: controllare dal menu tecnico la modalita' di 24866.

## In osservazione

### CG-001 · Aggiornamento firmware GMI fallito: 33326 sbloccata il 04/11 (fw 4.20.90), ma con bootloader V1 debug

- **Area:** firmware · **Gravita':** medium · **Visto:** 2026-10-30 → 2026-11-04
- **Macchine:** 33326, 24866, 26087, 29597, 29598, 28418
- **Prove:** Cronologia di 33326 il 04/11 (ora locale):
- 15:49: device_key_mismatch.
- 16:18: loop RDY (buffer \x00\x00RDY) e reboot con uptime 118.
- 16:28: fw_change 4.20.54->4.20.90. Avviso gmi_blocked chiuso alle 15:32 UTC.
- 20:20: passa a SLIM-4.20.187.
Durante il flash l'avviso di sottotensione ADESSO era aperto (14:32-15:32 UTC).
Stato di oggi:
- gmi_blocked null, mod 5, screen 20, hopper 1,1,0.
- Bootloader 'V1 (build debug)', blc B856A3FC, bll 8248; s1=1, ne=13, ore=26. Le altre GMI hanno V2, blc 3970B5D6, bll 4260.
- throttled 0x50005; uptime 63452 s.
24866: loop RDY alle 16:45 e fw 4.20.90 alle 16:55, rientrato da solo.
Nessun gmi_flash_failed nelle 24 h.
- **Ipotesi:** Il riavvio alle 16:18, fuori orario, e il bootloader cambiato in V1 debug fanno pensare a un intervento manuale (ST-Link o scheda GMI diversa). Non si puo' verificare: lo uid GMI di prima non e' nei dati. Il flash e' riuscito con sottotensione in corso: la causa dei fallimenti era probabilmente il bootloader o la GMI precedente piu' che l'alimentazione. Il loop RDY breve durante un flash riuscito e' normale.
- **Proposta:** Maurizio:
- Chiedere chi e' intervenuto su 33326 il 04/11 alle 16:18 e se la GMI e' stata sostituita.
- Riportare il bootloader al V2 di produzione: con V1 debug il prossimo aggiornamento potrebbe comportarsi diversamente.
- Tenere la protezione: niente flash con throttled bit 0x1 e stop ai retry dopo un ciclo fallito.
Campo: cambiare comunque l'alimentatore del Pi.
Chiudere se il prossimo aggiornamento GMI va a buon fine.
- **Gia' noto:** Aggiornamento firmware GMI che fallisce (gmi_flash_failed, gmi_blocked, loop RDY)

### CG-004 · Seriale GMI assente all'accensione (FTDI non enumerato), cavi lotto BG03E

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-04
- **Macchine:** 25158, 32996
- **Prove:** 05/11: nessun serial_missing e nessun serial_recovery.
- 32996: un solo reboot alle 09:04 (uptime 127).
- 25158: un solo reboot alle 09:23 (uptime 131).
Nei giorni precedenti: 25158 01-04/11, 32996 02-04/11.
Cavi ancora BG03ES5F (25158) e BG03ER1N (32996): lo scambio non e' stato fatto.
- **Ipotesi:** Problema noto e intermittente: lotto FT232R BG03E e/o alimentazione a ritroso dalla GMI. Un mattino senza episodi non basta a dire che e' sparito, perche' la causa non e' stata toccata.
- **Proposta:** Campo Parma: scambiare il cavo della 25158 con uno AL05 e lasciare 32996 come controllo.
Pi: riavvio anticipato, uhubctl e TX della GMI in high-Z nel prossimo rilascio.
Riaprire la voce se ricapita.
- **Gia' noto:** Seriale assente al mattino (serial_missing, not_enumerated)

### CG-010 · 37008: offline di notte e riavvio alle 02:50 del 05/11 (dopo l'assenza del 02-03/11)

- **Area:** campo · **Gravita':** medium · **Visto:** 2026-11-03 → 2026-11-05
- **Macchine:** 37008
- **Prove:** Ultimo report il 05/11 alle 00:55, poi offline. Reboot alle 02:50 con uptime 121 e app_restart.
Il 04/11:
- app_restart alle 19:03 e alle 19:35;
- TLK_REMOTE_HOST applicato alle 18:03 UTC e GIT_BRANCH alle 18:35 UTC.
Ora: online, uptime 25450 s, throttled 0x0, 4 vendite cash nelle 24 h, POS DISCONNECTED (CG-003).
- **Ipotesi:** La notte prima non si era spenta: un riavvio alle 02:50 dopo circa 2 h di silenzio fa pensare a un taglio di corrente notturno o a un blocco con riavvio. Causa non nota.
- **Proposta:** Monitorare. Recuperare dal journal la causa del riavvio delle 02:50. Chiudere se resta stabile fino a lunedi'.

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
