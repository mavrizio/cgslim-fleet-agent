# Registro problemi flotta CGSLIM

Aggiornato dall'agente il 16/11/2026 10:04. Una voce per causa; MHD senza zeri. Generato: non modificare a mano.

## Aperti

<a id="cg-003"></a>

### CG-003 · POS DISCONNECTED dopo timeout get_advanced_config: 24350 (3o giorno senza carte), 37008, 23718, 33326; 24866 rientrata col boot

- **Area:** pi · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-16
- **Macchine:** 24350, 37008, 33326, 23718, 24866, 11223344, 11155520, 11223355, 1470000, 54124120, 58547455, 58555555, 58888999, 33957, 36842, 24254, 32996, 24338, 28418, 25254, 21784, 25158
- **Prove:** Online e DISCONNECTED con 'Timeout locale get_advanced_config' (l'avviso conta 3 macchine):
- 24350: ieri 28 transazioni, 21 cash approvate; 7 con carta e 0 riuscite (6 annullate, 1 timeout alle 17:06). Oggi riavvio alle 09:12, ancora DISCONNECTED: il riavvio del Pi non basta.
- 37008: 23 vendite, tutte cash.
- 23718: nessuna transazione.
- 33326: nessuna transazione, due riavvii stamattina (09:45, 09:48).
24866: P95 letto alle 05:41 (boot), ora IDLE. Ieri pero' 7 tentativi con carta e 0 riusciti (2 timeout alle 18:45 e 18:47, 5 annullati); ultima carta approvata il 14/11 alle 12:18. Oggi vendita approvata alle 09:03.
'Connessione persa get_advanced_config' transitoria dopo il recovery seriale: 32996 dalle 09:17 alle 09:32, 25158 dalle 09:32 alle 09:47; ora entrambe IDLE.
- **Ipotesi:** Dopo un timeout della lettura cashless_info il pos-engine resta DISCONNECTED senza ritentare. Sulla 24350 serve probabilmente spegnere il POS: il reboot del Pi non lo sblocca.
La UI continua a offrire la carta, che finisce in annullato o timeout.
- **Proposta:** Maurizio:
- un errore di get_advanced_config non deve bloccare il P95: saltare la lettura e ritentarla con backoff;
- nascondere la carta a POS DISCONNECTED.
Campo Parma: spegnere e riaccendere il POS della 24350 e provare una carta.
Dashboard: escludere i Pi di banco dall'avviso.
- **Gia' noto:** POS: get_advanced_config

<a id="cg-009"></a>

### CG-009 · 24254 (Aprilia): seconda giornata senza vendite, sottotensione continua, oggi non accesa alle 10:00

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-02 → 2026-11-16
- **Macchine:** 24254
- **Prove:** 15/11:
- accesa alle 09:46, ultimo report alle 20:49;
- POS IDLE dopo la 'Connessione persa' delle 09:47;
- sottotensione ADESSO quasi continua dalle 12:47;
- 0 transazioni (non compare nell'elenco vendite), come il 14/11.
16/11: alle 10:00 non e' ancora tornata. Le altre Aprilia si sono accese tra le 05:41 (24866) e le 07:30 (26087).
Ultima carta approvata il 05/11.
- **Ipotesi:** Non confermato:
- alimentazione del Pi insufficiente, con schermo e UI forse inutilizzabili per il cliente;
- linea o timer diversi dalle altre Aprilia.
Due giorni con zero vendite mentre le vicine vendono 22-31 transazioni fanno pensare a una macchina inutilizzabile.
- **Proposta:** Campo Aprilia, oggi:
- verificare se e' accesa e con quale linea o timer;
- sostituire l'alimentatore del Pi;
- controllare schermo e touch e fare una vendita di prova (cash e carta).
Maurizio: journal e dmesg del 15/11.

<a id="cg-012"></a>

### CG-012 · Codice 31: la 33957 (Carpi) ora rifiuta tutte le carte, 0 carte riuscite su 44 dal 15/11

- **Area:** pos · **Gravita':** high · **Visto:** 2026-11-04 → 2026-11-16
- **Macchine:** 24254, 28418, 33957, 24866, 29597, 23718, 58888999, 33089, 25356, 24349
- **Prove:** 33957 (TID 75645530), 15/11:
- 64 transazioni: 20 approvate, tutte cash;
- 44 con carta e 0 approvate:
  - 1 codice 90 alle 14:09;
  - 21 'codice 31' tra le 14:36 e le 18:31, spesso a coppie;
  - 13 'nessuna carta entro il tempo';
  - 9 annullate.
- 16/11 alle 09:25: timeout con 'POS riattivato dopo codice 90'.
card_activity: ok 0, ko 35; ultima carta approvata il 14/11 alle 19:18.
24349 ieri senza codice 31 (22 approvate su 24). Altri rifiuti: codice 04 su 25158 alle 19:02 e su 33090 alle 14:38 (normali).
- **Ipotesi:** Sulla 33957 non e' piu' un tipo di carta non instradato: rifiuta in modo sistematico, dopo un codice 90.
Possibili cause: terminale non piu' abilitato o sessione con l'acquirer persa (serve un'inizializzazione o una chiusura contabile), oppure rete del router degradata (ieri DNS KO sul Pi, CG-020). Non confermato.
- **Proposta:** Campo Carpi, oggi: spegnere e riaccendere il POS, provare una carta e annotare il messaggio sul display del terminale.
Maurizio/Ingenico:
- verifica del TID 75645530 presso l'acquirer e significato del codice 31;
- se si ripete, chiamata di inizializzazione del terminale.
Maurizio: con N rifiuti consecutivi della banca, mostrare 'carta non disponibile, usa contanti' e avvisare in dashboard.
- **Gia' noto:** POS: altri errori

<a id="cg-004"></a>

### CG-004 · Seriale GMI assente all'accensione (FTDI non enumerato), cavi lotto BG03E: 25158 e 32996 anche oggi

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-16
- **Macchine:** 25158, 32996
- **Prove:** 16/11:
- 32996 (BG03ER1N): alle 09:04 reboot (uptime 112), 'could not open port /dev/ttyUSB0', serial_missing not_enumerated (sul bus solo hub, ethernet e ILITEK); alle 09:08 reboot di recovery (uptime 50); alle 09:09 serial_recovery.
- 25158 (BG03ES5F): alle 09:22 reboot (uptime 108), stessa eccezione; alle 09:26 reboot di recovery (uptime 45); alle 09:27 serial_recovery.
Dopo il recovery: breve 'Connessione persa get_advanced_config' (CG-003), poi POS IDLE.
La 25158 e' a 10 mattine su 11.
Vendite 15/11: 25158 50 (38 approvate), 32996 24 (23 approvate).
Cavo non ancora scambiato.
- **Ipotesi:** Lotto FT232R BG03E e/o alimentazione a ritroso dalla GMI. Il recovery funziona e costa circa 5 minuti al mattino.
- **Proposta:** Campo Parma: scambiare il cavo della 25158 con uno AL05 e lasciare la 32996 come controllo.
Pi: nel prossimo rilascio riavvio anticipato (~30-40 s), uhubctl e TX della GMI in high-Z.
- **Gia' noto:** Seriale assente al mattino (serial_missing, not_enumerated)

<a id="cg-005"></a>

### CG-005 · Sottotensione del Raspberry: 24254 quasi continua dalle 12:47 di ieri, 23718 fissa, 24349 a episodi, 24350/24338 dal boot

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-16
- **Macchine:** 24349, 23718, 24254, 24350, 24338
- **Prove:** Avvisi undervoltage_now del 15/11, orari locali:
- 24254: alle 09:47, 11:02, 11:47 e 12:17, poi continuo dalle 12:47 fino allo spegnimento (ultimo report alle 20:49). Ultimo stato 0x50005.
- 24349: alle 10:47 e alle 15:02. Oggi 0x50000 dopo il boot delle 09:17.
Stato attuale:
- 23718: 0x50005 fissa, avviso aperto dal 03/11 (uptime ~69 h);
- 24350: 0x50000 (boot alle 09:12);
- 24338: 0x50000.
Avviso 'sottotensione dal boot su 3 macchine'.
- **Ipotesi:** Alimentatori o cavi deboli. La 24254 peggiora: ieri praticamente tutto il pomeriggio in sottotensione, probabilmente legato al fermo vendite (CG-009).
- **Proposta:** Hardware/campo, in ordine:
1. 24254, insieme a CG-009;
2. 24349;
3. 23718;
4. 24350 e 24338.
Sostituire alimentatore e cavo del Pi.
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

### CG-020 · Telemetria assente per ore con DNS KO: 33957 e 21784 ieri, 28416 muta per tutta la domenica con 2 sole transazioni

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-11 → 2026-11-16
- **Macchine:** 24350, 33957, 21784, 24349, 28416
- **Prove:** 15/11, orari locali:
- 33957: update_failed 'Could not resolve host' alle 10:06, 13:47 e 16:28. Buchi di telemetria dopo le 11:07, le 13:47 e le 16:28; dall'ultimo nessun report fino al boot delle 09:00 di oggi. Intanto 64 transazioni.
- 21784: buchi dopo le 11:19, 14:36, 15:38, 18:19 e 20:47. Oggi:
  - boot alle 07:55 e report alle 07:57, poi silenzio fino a un secondo boot alle 09:57 (uptime 119);
  - updater in DNS KO dalle 07:59.
- 28416: nessun report dal 14/11 alle 21:49 fino al boot delle 08:44 di oggi. Il 15/11 solo 2 transazioni con carta (10:28 timeout, 10:49 annullata), nessuna approvata, contro 19 il 14/11.
- 37008: DNS KO alle 04:03, rientrato alle 04:04.
24349 e 24350 ieri senza buchi di giorno.
- **Ipotesi:** DNS dell'operatore o del router che cade per ore. Il fleet-reporter tace finche' il DNS non torna.
Su 21784 (oggi) e 24350 (ieri) i doppi avvii fanno pensare a interruzioni di corrente.
28416: non si sa se domenica era spenta, bloccata o solo senza rete; le 2 transazioni dicono che alle 10:28-10:49 era accesa. Non confermato.
- **Proposta:** Maurizio:
- DNS di riserva sul Pi o sul router;
- report anche con DNS KO;
- journal della 28416 del 15/11.
Campo:
- Parma: chiedere se la 28416 domenica era spenta o in errore;
- Carpi: router e SIM della 33957;
- dire dove si trova la 21784 e controllarne l'alimentazione.
- **Gia' noto:** Aggiornamenti bloccati (update_failed, rete/SIM)

<a id="cg-011"></a>

### CG-011 · Dashboard: centro null su 6 macchine, device_key 'missing' su 21784 e 4f2f67b8, Pi di banco nel conteggio

- **Area:** dashboard · **Gravita':** low · **Visto:** 2026-11-04 → 2026-11-16
- **Macchine:** 21784, 23718, 24338, 28418, 33326, 37008
- **Prove:** Centro null: 21784, 23718, 24338, 28418, 33326 e 37008.
device_key_status 'missing': 21784 (online, boot alle 09:57) e il Pi senza MHD 4f2f67b8.
Conteggio flotta 38: comprende 8 Pi di banco e il Pi senza MHD.
- **Ipotesi:** 21784 non ha mai fatto l'enroll della chiave, oppure l'ha persa con una SD clonata. Non confermato.
- **Proposta:** Dashboard/Maurizio:
- re-enroll della chiave della 21784;
- assegnare il centro (o 'banco');
- escludere i device di banco da conteggio e avvisi.
- **Gia' noto:** Profilo display auto / golden SD

<a id="cg-014"></a>

### CG-014 · MOD non documentate: 23718 mod 4, 33180 mod 2 con 1 sola vendita ieri; 28419 tornata mod 12

- **Area:** firmware · **Gravita':** low · **Visto:** 2026-11-05 → 2026-11-16
- **Macchine:** 23718, 33180, 28419
- **Prove:** 23718 (beta, 205, fw 4.20.98): mod 4, schermata 21, tramogge 0,1,1, nessuna vendita.
33180:
- mod 2, schermata 40, tramogge 1,0,0 (ieri 0,0,0);
- chl_mode 0, pos-engine inactive;
- 15/11: 1 sola transazione (cash alle 19:48), contro 18 il 14/11;
- boot oggi alle 08:47.
Le altre Tiburtino ieri hanno fatto tra 3 e 27 vendite.
28419: ora mod 12, schermata 70, tramogge 1,1,0.
- **Ipotesi:** 23718: macchina di prova.
33180 configurata solo contante. Il calo a 1 vendita insieme alle tramogge 0/1,0,0 fa pensare a tramogge vuote o non presenti. Non confermato.
Il mod 2 della 28419 era transitorio o una lettura sbagliata.
- **Proposta:** Campo Tiburtino: controllare e rifornire le tramogge della 33180; confermare che deve essere solo contante.
Maurizio: documentare le MOD 1, 2 e 4.

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

### CG-016 · Errori seriali: 29598 ne 104 nelle prime 3 h; contatori in crescita su 28418, 23718 e 37008

- **Area:** hardware · **Gravita':** low · **Visto:** 2026-11-06 → 2026-11-16
- **Macchine:** 29598, 33326, 11223355, 58547455, 58555555, 37008, 23718, 28418
- **Prove:** - 29598: ne=104 con uptime 11013 s (boot alle 06:45), stesso schema; ieri gmi_hostlink locked/unlocked alle 19:25-19:26 (CG-022).
- 28418: fe 110, ne 25, ore 93 (ieri fe 73, ne 14, ore 56), uptime ~5,8 giorni, test linea del 20/10 KO.
- 23718: fe 71, ne 17, ore 109 (ieri fe 46, ne 12, ore 65).
- 37008: ore 186 (ieri 148), uptime ~11,3 giorni.
- 33326: contatori GMI ora assenti (GMI a 4.20.31, CG-024).
- Banco fermo dal 13/11: valori invariati.
- **Ipotesi:** 29598: rumore sistematico nelle prime ore (cavo A10KIK4A, massa o GMI verde).
Su 28418 e 23718 i frame error crescono di 25-37 al giorno: linea rumorosa.
- **Proposta:** Campo Aprilia: test linea 8.4 sulla 29598.
Laboratorio: test linea su 28418 e 23718.
Maurizio: inviare i contatori come delta giornaliero.
- **Gia' noto:** Aggiornamento firmware GMI (linea disturbata GMI verdi)

<a id="cg-018"></a>

### CG-018 · Preparazione macchine al banco: banco spento dal 13/11, 21784 offline dalle 20:53 di ieri

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-09 → 2026-11-15
- **Macchine:** 11223344, 11223355, 11155520, 1470000, 54124120, 58547455, 58555555, 58888999, 21784, CG-4F2F67B8
- **Prove:** Banco offline dal 13/11:
- 11223344, 11155520, 11223355, 1470000, 58547455, 58555555 e 58888999 dalle 15:18-15:26;
- 54124120 dalle 13:20, con updater 'Couldn't connect'.
21784 (centro null, mod5):
- 14/11: boot verso le 09:19, update_failed DNS e poi recovered alle 10:06; report a singhiozzo (pause dopo le 15:07, 19:03 e 20:06);
- 13 transazioni tra le 12:18 e le 18:51, 10 approvate (1 carta 'esito recuperato con H');
- offline dalle 20:53, non tornata alle 10:00.
Pi senza MHD 4f2f67b8 offline dall'11/11 08:54.
- **Ipotesi:** Banco spento per il fine settimana. 21784: rete instabile (vedi CG-020); non e' noto dove si trovi.
- **Proposta:** Maurizio/campo:
- MHD definitivi, centro e TID distinti prima della spedizione;
- test linea 8.4 su tutte;
- dire dove si trova la 21784.
Dashboard: marcare 'banco'.
- **Gia' noto:** GMI 'muta' / NCG senza bootloader (menu 9.5 ST-Link); golden SD (CG-<seriale>)

<a id="cg-024"></a>

### CG-024 · 33326 (lab): GMI da 4.20.98 a NCG 4.09 e poi 4.20.31, con loop RDY

- **Area:** firmware · **Gravita':** low · **Visto:** 2026-11-16 → 2026-11-16
- **Macchine:** 33326
- **Prove:** 16/11:
- 09:45: reboot (uptime 35), gmi_mute NCG4.09 no_bootloader (probes 0, stlink null);
- 09:46: fw_change 4.20.98 -> 4.09;
- 09:48: secondo reboot (uptime 35), di nuovo gmi_mute;
- 09:52: gmi_back;
- 09:53: fw_change 4.09 -> 4.20.31 ed eccezione 'RILEVATO LOOP BOOTLOADER (RDY)'.
Ora: SLIM-4.20.205 beta, fw 4.20.31, mod 5, schermata 20, contatori GMI null, POS DISCONNECTED (CG-003).
Nessun gmi_flash_failed.
- **Ipotesi:** Probabile intervento al banco: GMI sostituita con una scheda NCG o riprogrammata a mano. Non e' un guasto dell'aggiornamento. Non confermato.
La release 205 contiene la 4.20.98: non e' chiaro se il gitpuller riflashera' la GMI, visto che la release non e' cambiata.
- **Proposta:** Maurizio:
- chiedere al laboratorio cosa e' stato fatto alle 09:45;
- verificare che il Pi riporti la GMI alla 4.20.98 quando il fw non coincide con quello della release (altrimenti flash da menu 9.x);
- se il loop RDY si ripete senza intervento, riaprire CG-001.
- **Gia' noto:** Aggiornamento firmware GMI che fallisce (loop RDY); GMI 'muta' / NCG senza bootloader

## In osservazione

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
