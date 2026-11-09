# Registro problemi flotta CGSLIM

Aggiornato dall'agente il 09/11/2026 10:04. Una voce per causa; MHD senza zeri. Generato: non modificare a mano.

## Aperti

<a id="cg-003"></a>

### CG-003 · POS DISCONNECTED dopo timeout get_advanced_config: fisso su 24350, 33326, 37008 da 5 giorni, i reboot non lo sbloccano

- **Area:** pi · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-09
- **Macchine:** 24350, 33326, 37008, 24866, 24349, 25158, 36842, 26087, 29597, 29598, 28418, 28416, 24338, 23718, 32996, 24254
- **Prove:** 09/11 alle 10:00 DISCONNECTED con 'Timeout locale in attesa di get_advanced_config (15.0s)':
- 24350: reboot alle 09:12 e l'errore resta (uptime 2908 s). Ieri 15 transazioni, tutte cash.
- 33326: reboot alle 08:48 e l'errore resta. Nessuna transazione.
- 37008: nessun reboot da circa 103 h, 27 transazioni cash.
Avviso 'POS in errore su 3 macchine' chiuso l'08/11 alle 23:32 UTC e riaperto oggi alle 08:17 UTC.
'Connessione persa durante get_advanced_config: Connessione chiusa dal dispositivo':
- 24338: 08/11 alle 09:47 UTC, chiuso alle 10:02;
- 25158: 09/11 alle 08:32 UTC, chiuso alle 08:47.
Entrambe sono tornate IDLE da sole.
- **Ipotesi:** Quando la lettura cashless_info va in timeout, il pos-engine resta DISCONNECTED senza ritentare. Succede anche dopo un reboot, quindi lo stato del terminale persiste o la prima lettura fallisce sempre su quei terminali.
Con 'Connessione persa' invece il pos-engine si riprende: i due casi sono gestiti in modo diverso.
- **Proposta:** Maurizio:
- Un errore di get_advanced_config non deve bloccare il P95: saltare la lettura e ritentarla con backoff.
- Nascondere la carta a POS DISCONNECTED.
- Confrontare il percorso 'timeout' con quello 'connessione persa', che invece si recupera.
- Log di pos-engine da 24350 dopo le 09:12 o da 37008.
Campo: spegnere e riaccendere il POS della 24350 (non solo il Pi) e provare una carta reale.
- **Gia' noto:** POS: get_advanced_config

<a id="cg-006"></a>

### CG-006 · 36842: terminale non parametrizzato (TID 00000000), i clienti provano la carta e falliscono con codice 20

- **Area:** pos · **Gravita':** high · **Visto:** 2026-10-30 → 2026-11-09
- **Macchine:** 36842, 24338, 23718, 28418, 33326
- **Prove:** 36842 nelle 24 h:
- 13 transazioni: 10 cash approvate, 3 carta P95 tutte 'POS non configurato (codice 20)' alle 20:39 dell'08/11;
- card_activity 0 ok, 3 ko.
Oggi POS IDLE, TID 00000000, nessun acquirer, package 01.04.25.03, SN 58551425.
TID della serie di prova 9794248x invariati: 24338 97942485, 23718 97942484, 28418 97942488.
33326: POS DISCONNECTED, TID non leggibile.
- **Ipotesi:** Senza parametri bancari ogni pagamento carta sulla 36842 fallisce. La carta e' ancora proposta al cliente: non e' disabilitata.
- **Proposta:** Hardware/POS: parametrizzare il terminale della 36842 con il TID di produzione.
Maurizio: nascondere la carta quando il TID e' 00000000 o mancano gli acquirer.
Verificare i TID di prova di 24338, 23718 e 28418.
- **Gia' noto:** POS: altri errori (errore 48, TID duplicato su 24338)

<a id="cg-009"></a>

### CG-009 · 24254 (Aprilia): si ferma la sera (ieri alle 20:59) e stamattina non e' ripartita; zero vendite

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-02 → 2026-11-09
- **Macchine:** 24254
- **Prove:** 08/11:
- sottotensione ADESSO alle 18:02 e alle 20:32 (ora locale);
- ultimo report alle 20:59 (uptime 43596 s, cioe' accesa dal reboot delle 08:54): ottava sera di fila con arresto.
09/11: alle 10:00 offline da 780 min. Le altre Aprilia si sono riaccese alle 05:40 (24866), 06:45 (29598), 06:53 (29597) e 07:30 (26087).
Vendite:
- nessuna transazione nelle 24 h (la macchina non e' in transactions_24h);
- ultima carta approvata il 05/11.
Ultimo stato: POS IDLE, hopper 1,1,0, screen 70, throttled 0x50000.
- **Ipotesi:** Alimentazione debole o tolta: sottotensione nelle ore prima dell'arresto, poi spegnimento. L'alimentatore che cede a caldo e la presa/timer diversa dalle altre Aprilia sono entrambe possibili.
Le zero vendite per piu' giorni fanno pensare a una macchina non usabile dai clienti.
- **Proposta:** Campo Aprilia, oggi:
- Riaccendere la macchina.
- Verificare presa e timer.
- Sostituire l'alimentatore del Pi.
- Fare una vendita di prova cash e carta e controllare cosa mostra lo schermo.
- Recuperare journal e dmesg dell'08/11 attorno alle 20:59.

<a id="cg-017"></a>

### CG-017 · 33957 (Carpi): ogni mattina, ~1,5 h dopo l'accensione, telemetria muta e carte rifiutate (codice 31/90), nessuna carta approvata da 2 giorni

- **Area:** hardware · **Gravita':** high · **Visto:** 2026-11-07 → 2026-11-09
- **Macchine:** 33957
- **Prove:** Lo schema si e' ripetuto due giorni di fila.
07/11:
- ultimo report alle 11:02;
- 16 'codice 31' tra le 14:15 e le 18:14.
08/11:
- reboot alle 09:00;
- ultimo report alle 10:32 (avviso offline aperto alle 10:17 UTC, chiuso il 09/11 alle 08:02 UTC);
- transazioni arrivate in differita.
Transazioni 08/11, dalle 10:45 alle 19:45:
- 57 in tutto: 30 cash, tutte approvate, e 27 carta P95, nessuna approvata;
- delle 27 carta: 'POS non attivo (codice 90)' alle 11:14, 4 'rifiutata dalla banca (codice 31)' (11:14, 11:30 x2, 11:31), 5 'nessuna carta entro il tempo' (15:06-19:05), 17 annullate.
card_activity: 0 ok, 10 ko, 17 cancelled. Ultima carta approvata il 06/11 sera.
Oggi alle 09:47:
- reboot alle 09:00 (uptime 132);
- POS IDLE, TID 75645530, acquirer presenti, LTE rssi -54;
- l'MDB SELF/2000 e il P95 riportano lo stesso SN 54802830.
- **Ipotesi:** Circa 1,5-2 h dopo l'accensione cade la connettivita' verso Internet (router/SIM/modem): si ferma la telemetria e il POS non raggiunge l'host bancario (codici 90 e 31). Le 17 annullate sono probabilmente clienti che rinunciano dopo i rifiuti.
La ripetizione allo stesso orario fa pensare a un router che si blocca o a un limite della SIM.
Non confermato: mancano i log di rete. Parametrizzazione del TID nuovo resta un'alternativa meno probabile.
- **Proposta:** Campo Carpi oggi:
- Controllare router e SIM: alimentazione, credito/traffico, log, eventuale timer.
- Fare un pagamento carta di prova verso le 11, quando ieri e' iniziato il problema.
Maurizio:
- Log di pos-engine e fleet-reporter dell'08/11 tra le 10:30 e le 12:00 (stato rete, ping, DNS).
- Disattivare la carta quando la rete e' giu'.
Se il codice 31 compare con la rete ok: segnalare il TID 75645530 al gestore del terminale.

<a id="cg-004"></a>

### CG-004 · Seriale GMI assente all'accensione (FTDI non enumerato), cavi lotto BG03E

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-09
- **Macchine:** 25158, 32996
- **Prove:** 09/11, 25158 (BG03ES5F):
- 09:22: serial_missing not_enumerated (uptime 108), eccezione 'could not open port /dev/ttyUSB0';
- 09:26: reboot di recovery (uptime 43);
- 09:27: serial_recovery, gmi_hostlink sbloccato.
Nella diagnosi USB solo hub, ethernet e ILITEK, nessun FTDI.
32996 (BG03ER1N): stamattina accensione pulita alle 09:04 (uptime 119), nessun serial_missing.
Le altre Parma sono pulite. Il cavo della 25158 non e' ancora stato scambiato.
- **Ipotesi:** Problema noto del lotto FT232R BG03E e/o dell'alimentazione a ritroso dalla GMI. E' intermittente: 25158 l'ha avuto 3 mattine su 4 (06, 08, 09/11).
- **Proposta:** Campo Parma: scambiare il cavo della 25158 con uno AL05 e lasciare 32996 come controllo.
Pi: riavvio anticipato (~30-40 s), uhubctl e TX della GMI in high-Z nel prossimo rilascio.
- **Gia' noto:** Seriale assente al mattino (serial_missing, not_enumerated)

<a id="cg-005"></a>

### CG-005 · Sottotensione del Raspberry: 23718 fissa, 24349 e 24254 a episodi; 33326 pulita

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-09
- **Macchine:** 23718, 24349, 24254, 24350, 24338
- **Prove:** Orari degli avvisi in UTC.
- 23718: 0x50005 ancora ADESSO, avviso aperto dal 03/11 10:47, ultimo alle 08:47 di oggi.
- 24349: ADESSO l'08/11 alle 09:47, 10:32, 12:47 e 20:17, ogni volta rientrato in 15-30 min. Oggi 0x50000 dopo il reboot delle 09:18.
- 24254: ADESSO l'08/11 alle 17:02 e 19:32, poco prima dell'arresto serale (vedi CG-009).
- Sottotensione dal boot (0x50000) oggi: 24338, 24349, 24350 e 24254 (ultimo report).
- 33326: 0x0 per il terzo giorno, anche dopo il reboot delle 08:48; tolta dalla voce.
- **Ipotesi:** Alimentatori o cavi deboli. Su 24254 la sottotensione serale potrebbe essere legata agli arresti.
- **Proposta:** Hardware/campo, in ordine:
1. 24254 (insieme a CG-009).
2. 23718 (fissa da 6 giorni).
3. 24349.
4. 24350 e 24338.
- **Gia' noto:** host.throttled 0x50000 (scheda campi); sottotensione sospettata nei flash GMI falliti

<a id="cg-007"></a>

### CG-007 · Tramogge 0,0,0 e schermata 73 su Parma MOD12: tornate su 32996 e 36842 dopo l'accensione

- **Area:** campo · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-09
- **Macchine:** 32996, 36842, 24350, 28417, 23718
- **Prove:** 09/11 alle 09:50-09:56:
- 32996: screen 73, hopper 0,0,0 (reboot alle 09:04);
- 36842: screen 73, hopper 0,0,0 (reboot alle 09:09).
Le altre Parma sono a 1,0,0, screen 71: anche 24350 e 28417.
Ieri tutte e due vendevano: 32996 15 cash, 36842 10 cash + 3 carta fallite. Con 187/4.20.90 lo stato non e' quindi sparito.
Non si sa se la 73 resta fino alla prima vendita o blocca la macchina.
23718 (branch mod5): ancora 0,0,0, screen 46 (vedi CG-014).
- **Ipotesi:** Dopo l'accensione la GMI manda #HPS 0,0,0 se le tramogge non rispondono ancora, e il Pi resta sulla 73. Puo' essere un problema di temporizzazione all'avvio, non un guasto delle tramogge.
Non confermato.
- **Proposta:** Maurizio: chiarire cosa porta alla screen 73 e se la GMI ripete #HPS dopo l'avvio.
Campo Parma: guardare a display 32996 e 36842 e controllare le tramogge dal menu tecnico.
Domani confrontare con lo stato a fine giornata (vendite su queste due).

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

- **Area:** dashboard · **Gravita':** low · **Visto:** 2026-11-04 → 2026-11-09
- **Macchine:** 23718, 24338, 28418, 33326, 37008, 24866
- **Prove:** Centro ancora null per 23718, 24338, 28418, 33326 e 37008.
23718, 24338, 28418 e 33326 si sono riavviate insieme l'08/11 alle 10:38 (uptime 115-143 s): probabilmente sono nello stesso posto.
33326:
- nuovo device_key_mismatch l'08/11 alle 16:27;
- device_key_status 'mismatch', avviso aperto dal 03/11.
24866: il vecchio b7233887 e' ancora offline (4407 min, ultimo report 06/11 08:32) e il conteggio resta 22 invece di 21.
- **Ipotesi:** I cambi di Pi/SD creano un nuovo device che la dashboard non unisce al vecchio. Su 33326 la chiave resta non corrispondente.
Le 4 macchine con centro null e riavvio simultaneo sono probabilmente un banco o un sito di prova.
- **Proposta:** Dashboard/Maurizio:
- Archiviare b7233887, oppure unire per MHD tenendo il device piu' recente.
- Ri-registrare la chiave di 33326.
- Assegnare il centro alle 5 macchine, indicando eventualmente 'banco' per quelle di prova.
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

### CG-016 · Contatori errori seriali alti lato GMI: 29598 (ne ~130-160 nelle prime 3 h ogni giorno), 37008 (ore 190), 28418 e 23718

- **Area:** hardware · **Gravita':** low · **Visto:** 2026-11-06 → 2026-11-09
- **Macchine:** 29598, 37008, 28418, 23718
- **Prove:** Contatori lato GMI oggi:
- 29598: ne=135 con uptime 11022 s. Nei giorni prima 163, 118 e 127, sempre a circa 3 h dall'accensione.
- 37008: ore=190 con uptime 371178 s (ieri 146): +44 in 24 h.
- 28418: fe=17, ne=8, ore=47 con uptime 83436 s (contatori azzerati dal reboot dell'08/11 alle 10:38).
- 23718: fe=39, ne=5, ore=34 con uptime 83315 s (reboot alle 10:38).
Nessun gmi_hostlink fuori dagli avvii.
Le Parma sono a fe 3-6, ne 0-2. Valori medi su 26087 (ne 11) e 24866 (fe 10, ne 8).
- **Ipotesi:** Su 29598 c'e' rumore sistematico nelle prime ore dopo l'accensione (cavo A10KIK4A, massa o GMI verde).
Su 37008, 28418 e 23718 gli errori crescono in modo costante col tempo: 28418 e 23718 in circa 23 h accumulano quanto in 36 h prima.
Per ora non impatta le vendite.
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

<a id="cg-012"></a>

### CG-012 · POS non pronto subito dopo l'avvio: 'gia' in corso', Broken pipe, codice 90

- **Area:** pi · **Gravita':** medium · **Visto:** 2026-11-04 → 2026-11-06
- **Macchine:** 24254, 28418, 33957, 24866
- **Prove:** Nelle ultime 24 h:
- nessun 'gia' in corso' ne' Broken pipe su nessuna macchina;
- 24866 dopo il reboot delle 05:40: 15 cash e 1 timeout carta, nessun errore.
L'unico codice 90 e' su 33957 l'08/11 alle 11:14, a circa 2 h dall'avvio e dentro il buco di telemetria: lo attribuisco a CG-017 (rete), non all'avvio.
Storico: 24866 il 06/11 (21 errori in 6 min), 24254 il 04-05/11, 28418 il 04/11.
- **Ipotesi:** Corsa all'avvio tra pagamento, activate e lettura cashless_info. Non si e' ripresentata da tre giorni.
- **Proposta:** Maurizio: tenere comunque la correzione: carta disabilitata finche' il POS non e' IDLE e cashless_info non ha finito, oppure lettura rimandata se c'e' un pagamento in coda.
Chiudere se resta pulito per un'altra settimana.
- **Gia' noto:** POS: get_advanced_config (operazione gia' in corso)

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
