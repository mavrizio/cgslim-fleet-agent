# Registro problemi flotta CGSLIM

Aggiornato dall'agente il 08/11/2026 10:03. Una voce per causa; MHD senza zeri. Generato: non modificare a mano.

## Aperti

<a id="cg-003"></a>

### CG-003 · POS DISCONNECTED dopo timeout get_advanced_config: fisso su 24350, 33326, 37008 da 4 giorni

- **Area:** pi · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-08
- **Macchine:** 24350, 33326, 37008, 24866, 24349, 25158, 36842, 26087, 29597, 29598, 28418, 28416, 24338, 23718, 32996, 24254
- **Prove:** 08/11 alle 10:00 DISCONNECTED con 'Timeout locale in attesa di get_advanced_config (15.0s)':
- 24350: riavviata alle 09:11 e l'errore resta. Nelle 24 h 6 transazioni: 4 cash approvate, 2 carta annullate (la carta e' stata proposta col POS DISCONNECTED).
- 33326: nessuna transazione.
- 37008: 16 cash, nessun reboot da 79 h.
Avviso 'POS in errore su 3 macchine' riaperto alle 08:17 UTC.
24866 (Pi nuovo): POS IDLE, 1 carta approvata.
Oggi non ci sono eventi 'Connessione persa durante get_advanced_config'.
- **Ipotesi:** La lettura cashless_info a volte va in timeout e il pos-engine resta DISCONNECTED senza riuscire a ritentare, anche dopo un reboot (24350).
Il caso della 24866 indica che il problema non e' fisso sul terminale.
La carta continua a essere proposta al cliente anche a POS DISCONNECTED.
- **Proposta:** Maurizio:
- Un errore di get_advanced_config non deve bloccare il P95: saltare la lettura e ritentarla con backoff.
- Nascondere la carta quando il POS e' DISCONNECTED.
- Recuperare i log di pos-engine da 24350 (dopo le 09:11) o da 37008.
Campo: prova con carta reale su 24350.
- **Gia' noto:** POS: get_advanced_config

<a id="cg-006"></a>

### CG-006 · 36842: terminale non parametrizzato (TID 00000000), oggi nessun tentativo carta; beta con TID di prova 9794248x

- **Area:** pos · **Gravita':** high · **Visto:** 2026-10-30 → 2026-11-08
- **Macchine:** 36842, 24338, 23718, 28418, 33326
- **Prove:** 36842 nelle 24 h:
- 29 transazioni, tutte cash approvate, nessun tentativo carta;
- card_activity 0 ok, 0 ko; ultimo ko 'POS non configurato (codice 20)' del 06/11.
Oggi POS IDLE, TID 00000000, nessun acquirer, package 01.04.25.03, SN 58551425.
Dai dati non si capisce se la carta e' stata disabilitata o se i clienti non l'hanno usata.
TID della serie di prova 9794248x: 24338 97942485, 23718 97942484, 28418 97942488.
33326: POS DISCONNECTED, TID non leggibile.
- **Ipotesi:** Senza parametri bancari ogni pagamento carta sulla 36842 fallisce con codice 20. Il problema resta, anche se oggi non si e' manifestato.
- **Proposta:** Hardware/POS: parametrizzare il terminale della 36842 con il TID di produzione.
Maurizio:
- Confermare se la carta e' disabilitata sulla 36842.
- Valutare un blocco automatico della carta quando il TID e' 00000000 o manca l'acquirer.
Verificare i TID di 24338, 23718 e 28418.
- **Gia' noto:** POS: altri errori (errore 48, TID duplicato su 24338)

<a id="cg-009"></a>

### CG-009 · 24254 (Aprilia): si ferma la sera (ieri alle 20:49) e da 24 h non vende

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-02 → 2026-11-08
- **Macchine:** 24254
- **Prove:** 07/11:
- reboot alle 10:02 (uptime 139, fuori dal timer), con app_restart e gmi_hostlink locked/unlocked;
- ultimo report alle 20:49: settima sera di fila con arresto, ma piu' tardi delle precedenti (19:44-19:54).
08/11:
- reboot alle 08:54 (uptime 139), dentro la finestra del timer; online alle 10:00 con uptime 3814 s.
Vendite:
- nessuna transazione nelle 24 h (in transactions_24h la macchina non c'e');
- ultima carta approvata il 05/11 mattina, ultimo ko il 06/11 alle 16:02.
Oggi POS IDLE, hopper 1,1,0, throttled 0x50000.
- **Ipotesi:** L'alimentazione viene tolta la sera a un orario diverso dalle altre Aprilia (presa o timer).
La sottotensione dal boot indica un alimentatore debole.
Le zero vendite in circa 11 h di accensione ieri sono sospette: macchina non usabile dai clienti, oppure semplice assenza di clienti. Dai dati non si distingue.
- **Proposta:** Campo Aprilia:
- Verificare presa e timer.
- Sostituire l'alimentatore.
- Fare una vendita di prova cash e carta.
- Recuperare journal e dmesg attorno alle 20:49 del 07/11.

<a id="cg-017"></a>

### CG-017 · 33957 (Carpi): carte rifiutate in serie 'codice 31' durante circa 22 h senza telemetria

- **Area:** hardware · **Gravita':** high · **Visto:** 2026-11-07 → 2026-11-08
- **Macchine:** 33957
- **Prove:** Telemetria:
- ultimo report 07/11 11:02;
- avviso offline aperto alle 10:47 UTC, chiuso l'08/11 alle 08:02 UTC, dopo il reboot delle 09:00 (uptime 132).
Transazioni 07/11-08/11, arrivate in differita:
- 61 in tutto: 42 cash approvate, 19 carta P95;
- delle 19 carta: 16 'rifiutata dalla banca (codice 31)' tra le 14:15 e le 18:14 (raffiche di 3-4 nello stesso minuto alle 16:37 e 16:47), 1 'POS non attivo (codice 90)' alle 14:15, 2 annullate.
card_activity: 0 ok, 17 ko. Ultima carta approvata il 06/11 sera (ts 1793988747).
Oggi:
- POS IDLE, TID 75645530, acquirer presenti;
- linea seriale DISTURBATA dal test del 05/11;
- l'MDB SELF/2000 e il P95 riportano lo stesso SN 54802830.
- **Ipotesi:** La finestra dei rifiuti cade dentro la finestra senza telemetria. E' probabile che fosse caduta la connettivita' (router/SIM) e che il POS non raggiungesse l'host bancario.
In alternativa, problema di parametrizzazione o acquirer del TID nuovo, di un terminale appena installato.
Non e' confermato: mancano i log di rete.
- **Proposta:** Campo Carpi:
- Verificare router/SIM e alimentazione del router.
- Fare un pagamento carta di prova oggi.
Maurizio:
- Journal di fleet-reporter e log di pos-engine del 07/11 tra le 11:00 e le 18:30.
- Valutare di disattivare la carta quando la rete e' giu'.
Se il codice 31 si ripete con la rete ok: segnalare TID 75645530 al gestore del terminale.

<a id="cg-004"></a>

### CG-004 · Seriale GMI assente all'accensione (FTDI non enumerato), cavi lotto BG03E

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-08
- **Macchine:** 25158, 32996
- **Prove:** 08/11, il problema si ripresenta su entrambe le macchine dopo due mattini puliti (05/11, 07/11).
32996 (BG03ER1N):
- 09:03: serial_missing not_enumerated (uptime 113), con eccezione 'could not open port /dev/ttyUSB0';
- 09:07: reboot di recovery (uptime 42);
- 09:08: serial_recovery, gmi_hostlink sbloccato.
25158 (BG03ES5F):
- 09:22: serial_missing (uptime 108), con eccezione;
- 09:26: reboot (uptime 43);
- 09:27: serial_recovery.
Nella diagnosi USB non c'e' nessun FTDI: solo hub, ethernet e touch ILITEK.
In tutti e due i casi basta un recovery. Il cavo della 25158 non e' ancora stato scambiato.
- **Ipotesi:** Problema noto del lotto FT232R BG03E e/o dell'alimentazione a ritroso dalla GMI. Resta limitato alle due macchine con cavo BG03E: le altre Parma si sono accese pulite.
- **Proposta:** Campo Parma: scambiare il cavo della 25158 con uno AL05 e lasciare 32996 come controllo.
Pi: riavvio anticipato (~30-40 s), uhubctl e TX della GMI in high-Z nel prossimo rilascio.
- **Gia' noto:** Seriale assente al mattino (serial_missing, not_enumerated)

<a id="cg-005"></a>

### CG-005 · Sottotensione del Raspberry: 23718 fissa, 24349 a episodi tutto il giorno; 33326 pulita da 2 giorni

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-08
- **Macchine:** 23718, 24349, 33326, 24254, 24350, 24338
- **Prove:** Orari degli avvisi in UTC.
- 23718: 0x50005 ancora ADESSO, avviso aperto dal 03/11 10:47, ultimo alle 08:47 di oggi.
- 24349, episodi ADESSO il 07/11: 12:02-12:17, 14:47-15:47, 17:47-18:17, 20:02, 20:47, 22:17-22:32. Oggi 0x50000 dopo il reboot delle 09:18.
- 33326: 0x0 con uptime 130163 s (~36 h), nessun avviso dal 06/11 09:02.
- Sottotensione dal boot (0x50000) oggi: 24254, 24338, 24349, 24350.
- **Ipotesi:** Alimentatori o cavi deboli. Su 33326 il problema sembra sparito dal reboot del 06/11.
- **Proposta:** Hardware/campo, in ordine:
1. 23718 (fissa da 5 giorni).
2. 24349.
3. 24254 (vedi CG-009).
4. 24350 e 24338.
Su 33326: se domani e' ancora a 0x0, togliere la macchina dalla voce.
- **Gia' noto:** host.throttled 0x50000 (scheda campi); sottotensione sospettata nei flash GMI falliti

<a id="cg-012"></a>

### CG-012 · POS non pronto subito dopo l'avvio: 'gia' in corso', Broken pipe, codice 90 (raffica su 24866)

- **Area:** pi · **Gravita':** medium · **Visto:** 2026-11-04 → 2026-11-06
- **Macchine:** 24254, 28418, 33957, 24866
- **Prove:** 24866, il 06/11 attorno al reboot delle 14:00:
- Broken pipe alle 13:58 e alle 14:03;
- 17 'Operazione get_advanced_config gia' in corso' (8 alle 14:00, 8 alle 14:02, 1 alle 14:03);
- 'POS non attivo (codice 90)' alle 14:03 e alle 14:04.
In tutto 21 errori in 6 minuti con clienti che riprovavano.
33957: codice 90 il 06/11 alle 10:08.
Storico:
- 24254, 04/11: 28 'activate gia' in corso';
- 24254, 05/11 alle 09:00: codice 90;
- 28418, 04/11.
- **Ipotesi:** Dopo l'avvio i pagamenti partono mentre il POS si sta attivando o mentre e' in corso la lettura cashless_info. L'attesa max di 8 s non basta e la carta resta proponibile al cliente.
- **Proposta:** Maurizio:
- Disabilitare la carta finche' il POS non e' IDLE e la lettura cashless_info non e' terminata.
- Oppure rimandare la lettura se un pagamento e' in coda.
- Nel client P95 attendere l'activate invece di restituire errore.
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

<a id="cg-011"></a>

### CG-011 · Dashboard: centro null, chiave non corrispondente su 33326, device duplicato 24866 dopo cambio Pi

- **Area:** dashboard · **Gravita':** low · **Visto:** 2026-11-04 → 2026-11-08
- **Macchine:** 23718, 24338, 28418, 33326, 37008, 24866, 36842
- **Prove:** Centro ancora null per 23718, 24338, 28418, 33326 e 37008.
33326:
- nuovo device_key_mismatch il 07/11 alle 16:13;
- device_key_status 'mismatch';
- avviso aperto dal 03/11.
24866 compare ancora due volte:
- b7233887: offline da 2967 min, ultimo report 06/11 08:32;
- device nuovo: online.
Il conteggio resta 22 invece di 21.
- **Ipotesi:** I cambi di Pi/SD creano un nuovo device che la dashboard non unisce al vecchio con lo stesso MHD. Su 33326 la chiave resta non corrispondente.
- **Proposta:** Dashboard/Maurizio:
- Archiviare b7233887, oppure unire per MHD tenendo il device piu' recente.
- Ri-registrare la chiave di 33326.
- Completare il centro delle 5 macchine.
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

### CG-016 · Contatori errori seriali alti lato GMI: 29598 (ne in crescita, 163 in 3 h), 37008 (ore 146), 28418 e 23718

- **Area:** hardware · **Gravita':** low · **Visto:** 2026-11-06 → 2026-11-08
- **Macchine:** 29598, 37008, 28418, 23718
- **Prove:** Contatori lato GMI oggi:
- 29598: ne=163 con uptime 11012 s. Ieri ne=118, il giorno prima 127, sempre a circa 3 h dall'accensione.
- 37008: ore=146 con uptime 284525 s (ieri 108): +38 in 24 h.
- 28418: fe=27, ne=14, ore=76 con uptime 36 h (ieri fe 10, ne 5, ore 19); test linea KO il 20/10.
- 23718: fe=48, ne=8, ore=60 con uptime 36 h (ieri fe 22, ore 24).
Su tutte, nessun gmi_hostlink fuori dagli avvii.
Le mod12 Parma hanno fe 3-6, ne 0-5.
- **Ipotesi:** Su 29598 c'e' rumore sistematico sulla linea, nelle prime ore dopo l'accensione e in aumento (cavo A10KIK4A, massa o GMI verde).
Su 37008, 28418 e 23718 gli errori crescono in modo costante col tempo.
- **Proposta:** Campo: test linea 8.4 su 29598, poi su 28418, 23718 e 37008.
Maurizio: inviare i contatori come delta giornaliero, o con il timestamp del primo errore.
- **Gia' noto:** Aggiornamento firmware GMI (linea disturbata GMI verdi)

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

<a id="cg-010"></a>

### CG-010 · 37008: stabile dal riavvio notturno del 05/11 02:50, resta accesa la notte; throttled 0x80000

- **Area:** campo · **Gravita':** medium · **Visto:** 2026-11-03 → 2026-11-05
- **Macchine:** 37008
- **Prove:** Uptime 284525 s (~79 h): nessun reboot dal 05/11 circa alle 02:50, nessun avviso offline stanotte.
16 vendite cash tra il 07/11 10:48 e l'08/11 09:50.
update_failed DNS alle 04:03, rientrato alle 04:04.
Throttled 0x80000: limite termico soft raggiunto dal boot, nessuna sottotensione. CPU a 50,5 °C, la piu' calda della flotta.
POS DISCONNECTED (CG-003). Centro ancora null.
- **Ipotesi:** La macchina e' alimentata 24 h. Il riavvio delle 02:50 non si e' ripetuto.
Il bit termico potrebbe dipendere dal funzionamento continuo o da un vano poco ventilato.
- **Proposta:** Chiudere se resta stabile fino a domani.
Chiedere dove si trova e se e' voluto che resti accesa di notte.
Controllare la ventilazione se il bit termico si ripresenta.

<a id="cg-007"></a>

### CG-007 · Tramogge 0,0,0 e schermata 73 su Parma MOD12: sparite dopo l'aggiornamento 187/4.20.90

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-01 → 2026-11-05
- **Macchine:** 24350, 28417, 32996, 23718
- **Prove:** Oggi 24350, 28417 e 32996 sono a hopper 1,0,0 e screen 71, come le altre Parma. Ieri tutte e tre sono state aggiornate a 187 e fw 4.20.90 (16:09-16:35).
23718 (mod 4, branch mod5) e' a hopper 0,0,0, screen 23 e non ha transazioni nelle 24 h (vedi CG-014).
- **Ipotesi:** Lo stato 0,0,0/73 era probabilmente legato alla combinazione 176/4.20.84 o a uno stato rimasto dal flash. Con la nuova release non si e' ripresentato.
- **Proposta:** Chiudere se le tre Parma restano a 1,0,0 anche lunedi'.
Maurizio: chiarire comunque il significato di screen 73.

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
