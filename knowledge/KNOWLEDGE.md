# Conoscenza di base sulla flotta CGSLIM

Scheda per l'analista automatico. Fatti tecnici dallo sviluppo, aggiornati al
2026-11-25. Quando un dato del giorno combacia con un problema gia' noto, dillo
e collegalo; non presentarlo come scoperta.

## Il sistema
- **CGSLIM** = cambiamonete/distributore di gettoni e tessere nei centri commerciali.
  Due schede: **GMI** (STM32F407, firmware "GM2-4.20.NN" / file CGT-4.20.NN.bin,
  gestisce hopper ccTalk, accettatori, lettore MDB) e **Raspberry Pi** (software
  py_cgslim4 "SLIM-4.20.NNN": UI touch, logica, POS, telemetria, aggiornamenti).
- Pi e GMI parlano su seriale USB (adattatore FTDI FT232R, /dev/ttyUSB0, 38400).
  Protocollo ASCII a tag di 3 lettere (#SCN schermata, #CRD credito, #HPS stato
  hopper, #VN1/#VN2 vendita, #TRCFLT fault...).
- POS: **Ingenico SELF2000** con firmware custom, protocollo 95 (ECR95) su TCP,
  gestito dal servizio `pos-engine` sul Pi (porta locale 6031). Lettori MDB
  (Ingenico SELF/2000 in "modalita' 2") passano invece dalla GMI.
- Aggiornamenti: `gitpuller` sul Pi segue un branch git (develop, beta2, mod12,
  parma, mod5, mod10 per i totem del tornello...), costruisce la release in /opt/cgslim/current e, se la release
  contiene un HEX nuovo, flasha la GMI via bootloader seriale.
- **fleet-reporter** sul Pi manda lo stato ogni 15 min (subito sugli eventi) al
  DB Supabase `cgslim-fleet`; la dashboard e' cgslim-fleet.vercel.app.

## Identita' e nomi
- **MHD** = ID macchina GMI (8 cifre, nel DB con zeri iniziali: "00024349").
  I tecnici lo dicono senza zeri: 24349. `machine_registry` da' centro e batteria.
- MHD 7788xxxx e 7777xxxx = macchine di sviluppo/test: escluse dall'analisi.
- Le SD vengono clonate: hostname ripetuti, non usarli per identificare.
- **MOD** = modalita' della GMI (5 = acquisto gettoni con carta, 12 = flusso
  guidato tessere/ricariche, 14 = Saltarello, 255 = F_MODE_ERROR nessuna tramoggia).
- **CHL_MODE** (runtime.cashless.chl_mode): 0 nessun cashless, 2 MDB, 3/4 POS P95
  (4 = griglia importi a riposo).

## Orari
I centri commerciali **spengono le macchine la notte**: si riaccendono tra le
05 e le 09 (accensione con timer, GMI e Pi insieme). Un reboot al mattino e'
normale; offline la notte e' normale. Rilevante e' chi NON si riaccende o chi
si riavvia piu' volte in giornata.

## Campi del payload utili
- `host.throttled` (Raspberry): bit 0 (0x1) sottotensione ADESSO, 0x4 throttling
  adesso, 0x10000 sottotensione avvenuta dal boot, 0x40000 throttling avvenuto.
  0x50000 = c'e' stata sottotensione dal boot (alimentatore/cavo debole).
- `runtime.serial_missing`: la porta della GMI e' sparita (vedi sotto).
- `runtime.gmi_blocked`: aggiornamento firmware GMI fallito, macchina fuori
  servizio (errore 98) finche' non viene riavviata.
- `runtime.serial.gmi`: contatori errori lato GMI (fe/ne/pe/ore) e bootloader;
  `runtime.serial.pi_uart`: errori lato Pi (overrun, frame...).
- `serial.adapter.serial`: seriale del cavo FTDI (importante, vedi lotto BG03E).
- `serial.last_test`: esito del test linea dal menu tecnico 8.4 (verdict OK/KO).
- `app.updater`: ok/failures/error del gitpuller.
- `card_activity`: pagamenti carta ok/ko nelle ultime 24 h.
- `runtime.hopper`: es. ["1","1","0"] stato delle tramogge dall'ultimo #HPS
  (null finche' la GMI non lo manda).

## Problemi noti (non sono scoperte)

### Seriale assente al mattino (serial_missing, not_enumerated)
All'accensione mattutina il chip FTDI a volte non si presenta sul bus USB. Il Pi
(da SLIM-4.20.153) si riavvia da solo dopo 180 s, max 2 volte in 24 h
(`serial_recovery`, `serial_recovery_exhausted`). Colpite soprattutto **25158** e
**32996**, entrambe con cavo FT232R seriale **BG03E*** (BG03ES5F, BG03ER1N); le
altre (AL05*, A906*, A10*, BG04M*) no. Ipotesi: lotto di cavi difettoso e/o chip
alimentato a ritroso dalla GMI (spegnere la GMI lo sblocca). Test proposto:
scambiare il cavo della 25158 con uno AL05. Patch previste al prossimo rilascio
importante: riavvio anticipato (~30-40 s), uhubctl, TX della GMI in high-Z.
Eccezione collegata: "ERRORE CRITICO SERIALE ... could not open port /dev/ttyUSB0"
e "Disconnessione hardware seriale. Termino il processo".

### Aggiornamento firmware GMI che fallisce (gmi_flash_failed, gmi_blocked, loop RDY)
Il bootloader seriale V2 a volte non riceve bene: "Timeout ACK al blocco N".
Cause note: linea seriale disturbata sulle **GMI verdi** (col modem; ipotesi
MAX232 che carica i segnali), le GMI rosse no; byte spurio che sfasa i pacchetti
(risincronizzazione lato Pi aggiunta). Dalla SLIM-4.20.129 il recupero fa max 15
tentativi poi errore 98 (usura flash). "RILEVATO LOOP BOOTLOADER (RDY)" = la GMI
e' rimasta nel bootloader (app non valida) e manda RDY in continuo.
La sottotensione del Pi durante il flash e' un sospetto ragionevole.
Dalla **SLIM-4.20.211** (CG-024) ogni flash fallito manda `gmi_flash_attempt_failed`
(`attempt` 0 = aggiornamento normale, 1..15 = recovery; `addr` = indirizzo in flash dove
si e' fermato, da 0x08008000; `error`), e `gmi_flash_failed` ha `fail_addrs` con
l'indirizzo di ogni tentativo. Stesso indirizzo a ogni tentativo = settore della flash
della GMI; indirizzi diversi = linea seriale disturbata.

### POS: get_advanced_config
Dalla SLIM-4.20.171/172 `core/cashless_info.py` legge get_advanced_config,
get_package_release, get_acquirer_info a POS libero (avvio, riposo) e poi ogni
24 h. Errori "Timeout locale in attesa di 'get_advanced_config'" o "Connessione
persa durante 'get_advanced_config'" = il POS non risponde a quella lettura.
"Operazione 'get_advanced_config' gia' in corso" nelle transazioni = un
pagamento si e' scontrato con la lettura (attesa max 8 s). Problema recente, da
quantificare: quante macchine, se impedisce pagamenti.
La v.172 metteva \u0000 nell'identita' P95 e il fleet scartava i report (fixato
lato server 0009 e lato Pi .173).

### POS: collegamento col terminale (CG-003, SLIM-4.20.208 del 25/11)
Provato al banco col SELF2000 vero. Comportamenti del terminale accertati:
- chiude il TCP da solo 0,1-0,3 s dopo molte risposte: un comando mandato in quella
  finestra si perdeva (era il motivo per cui la riattivazione dopo il **codice 90**
  a volte falliva e il cliente prendeva l'errore);
- dopo un suo riavvio, e dopo la **chiusura di cassa automatica notturna**, riparte
  **disattivato**: il primo pagamento prende il codice 90 ("il primo fallisce, il
  secondo va");
- se la rete cade e il collegamento viene abbandonato a meta', puo' restare in una
  "sessione fantasma": accetta la connessione ma non risponde piu' a nulla, anche per
  ore. Serve **spegnere e riaccendere il POS**. Probabile causa dei POS
  DISCONNECTED che non rientrano (24350, 37008).
Dalla 208 pos-engine: aspetta 0,8 s dopo ogni risposta, rimanda una volta un comando
perso prima della presa in carico, rinnova il collegamento dopo 5 min fermo e dopo un
timeout di get_advanced_config (prima restava una sessione a meta'), **riattiva da solo
il POS** se e' stato irraggiungibile per 20 s o piu'. Nelle transazioni "POS riattivato
dopo codice 90" = la riattivazione e' andata, il pagamento e' ripartito: normale.
Un codice 90 SENZA quella nota con release >= 208 e' da segnalare.
Campi nuovi nel payload (release >= 208): `status.pos.last_error` = motivo
dell'ultima disconnessione (es. "nessuna risposta a 'get_advanced_config'",
"Collegamento interrotto: ...", "Connessione chiusa dal dispositivo." che da sola e'
normale) e `status.pos.down_s` = da quanti secondi e' scollegato (solo se
disconnesso). Un down_s che cresce per ore con release >= 208 = POS da spegnere e
riaccendere (campo/hardware), non piu' un bug del Pi da indagare.
Le macchine senza IP del POS configurato danno sempre DISCONNECTED: non e' un guasto.

### POS: altri errori
Errore 48 = timeout del terminale (anche TID duplicato: successo su 24338 col TID
di prova 97942487). Errore 01 = annullata. "nessuna carta entro il tempo" e
"annullato dal cliente" sono comportamento normale del cliente, non guasti.

### Aggiornamenti bloccati (update_failed)
Errori di `git fetch` verso gitlab-dev.dedemapp.com: di solito rete/SIM,
transitori (update_recovered). Da SLIM-4.20.165 il gitpuller ripara il repo
corrotto da blackout (repo_healed). Preoccupante solo se persiste giorni.

### Schermo fermo su "erogazione" ~90 s (MOD12)
#RUI non rilasciato; fix nel firmware 4.20.69. Se ricapita con fw >= 4.20.69 e' da
segnalare.

### Schermata 72 "solo tessere" (MOD12)
72 = la GMI vende tessere/gettoni ma **non monete**: la tramoggia monete (indirizzo 3,
primo valore di `runtime.hopper`) non e' disponibile (vuota, assente, in errore, monete
non pagate rimaste dall'ultima erogazione) oppure VLM impedisce il cambio monete.
La macchina continua a vendere tessere (contanti/carta), non da' resto in monete.
70 = tutto disponibile, 71 = solo cambio monete, 73 = solo ricarica.
Fino al fw 4.20.99, dopo un **inceppamento sbloccato** dalla tramoggia, la GMI restava
sulla 72 per ~8 s (due giri di controllo) anche con la tramoggia buona: corretto nel
**fw 4.20.100** (25/11), vale per tutte le modalita'. Quindi una 72 breve dopo un
errore di erogazione con fw <= 4.20.99 e' quel difetto; una 72 che dura ore o giorni
(es. CG-014) NON e' quel difetto: tramoggia monete da controllare sul posto.

### Menu tecnico sordo dopo errore di erogazione
Fix fw 4.20.84 + SLIM-4.20.176. Errore 101 = erogazione incompleta.

### Banda "LA MACCHINA NON DA' RESTO" (MOD12, 110/111)
Dal fw 4.20.85 + SLIM-4.20.180 la GMI manda #CHG0 quando non puo' dare resto (hopper
monete ind. 3 assente/sotto livello basso/non risponde, monete non pagate, oppure
ultima erogazione monete fallita, ricordo che sopravvive al riavvio): il Pi mostra la
banda rossa e, pagando la tessera in contanti, accetta solo monete. E' voluto, non un
guasto. #TRC8 CHG payout_fail=1/0 = fallimento registrato/cancellato (si cancella alla
prima erogazione monete riuscita). Un payout_fail=1 che resta per giorni = hopper da
far controllare (campo).

### Pagamenti bloccati perche' la GMI non sente il Pi (evento gmi_hostlink)
Dal fw 4.20.86 + SLIM-4.20.181 il Pi manda #IAH ogni 5 s; dopo 20 s senza righe dal Pi
la GMI chiude banconote, gettoniera e cashless (in tutte le modalita') e li riapre dopo
3 #IAH. Nasce dalla 36842 (CG-002: Pi spento, accettatori aperti). Evento
gmi_hostlink {"locked": true/false} solo al cambio: un locked=true seguito presto da
false = Pi bloccato o seriale persa per qualche secondo, e' la protezione che funziona.
Ripetuto spesso = main loop del Pi bloccato o seriale instabile (vedi fe/serial).
Dalla **SLIM-4.20.211** l'evento dice la causa probabile (CG-022): al blocco
`cause` = `avvio_app` (app appena partita: Pi acceso o app riavviata, normale alle
accensioni), `avvio_gmi` (la GMI e' appena ripartita e parte bloccata: un avvio_gmi a
meta' giornata senza reboot del Pi = la GMI si e' riavviata da sola o ha perso
alimentazione), `pi_fermo` (il Pi non ha scritto alla GMI per >= 15 s: main loop
bloccato), `linea` (il Pi scriveva ma la GMI non lo sentiva: cavo, masse, disturbi).
Campi: `pi_tx_gap_s`, `gmi_silence_s` (silenzio misurato dalla GMI), `gmi_boot_ago_s`,
`last_rx` (ultima riga dalla GMI). Allo sblocco `duration_s`. Prima della 211 l'evento ha
solo `locked`.
Sul display 16x2 della GMI compare "PI MUTO". Dal fw 4.20.87 quel display e' tecnico
(fase GMI, credito, B M C): non e' piu' rivolto al pubblico, non e' un guasto.

### MOD5: pulsante fisico GETTONI e schermata 96
Dal fw 4.20.88 + SLIM-4.20.182 il pulsante fisico GETTONI senza credito apre la 96
"Come vuoi pagare?" (stato della GMI, 25 s, accettatori aperti) invece della griglia
carta 95. Screen 96 nel payload e' normale; con credito sotto il prezzo di un gettone
il pulsante non fa nulla (voluto).

### Riavvii della GMI
Firmware >= 4.20.38 manda #TRCFLT dopo un fault (type 1 HardFault, type 2/3
reset deliberato per errore I2C EEPROM). Senza #TRCFLT e con silenzio lungo =
watchdog (loop bloccante). Il fleet riceve FAULT_REPORT come evento/eccezione.

### Profilo display "auto" (SLIM-4.20.188, golden SD universale)
Le macchine preparate con la golden CG-NFC-GOLD v2 hanno `config.profile = "auto"`:
il Pi sceglie il profilo a ogni avvio (touch USB Elo/Risingstar o monitor Elo,
altrimenti 5.5"). Nel runtime il profilo scelto e' in `profile` con
`profile_auto: true`. "auto" nella configurazione e' normale, non un errore.
Una release < 188 che trova "auto" resta sul 5.5" (log "sconosciuto, ignorato").
Le copie della golden al primo avvio si chiamano `CG-<ultime 8 cifre del seriale CPU>`
e compaiono in dashboard come macchine nuove (chiave fleet rigenerata).

### GMI "muta" / errore 97 sui banchi con emulatore ccTalk
Macchine di laboratorio con due adattatori USB-seriale (GMI + emulatore ccTalk):
prima della SLIM-4.20.189 dopo un riavvio la GMI poteva finire su ttyUSB1 e l'app
apriva l'emulatore -> gmi_mute, errore 97, menu 9.5. Dalla 189 l'app sceglie da
sola l'adattatore giusto (log "Porta seriale GMI: ... uso /dev/ttyUSB1"). Su queste
macchine con release < 189 e' un problema noto del banco, non della GMI.

### Richiesta #CCI ogni 30 s (SLIM-4.20.207-209) e <TCA=> vuoto su TLK
Dalla 207 il Pi chiede alla GMI i dispositivi ccTalk (#CCI, sezione cctalk del fleet).
Per errore, dalla 207 alla 209 la richiesta ripartiva ogni ~30 s invece che solo
all'accensione della GMI e ogni 30 min; ogni tanto si scontrava con gli invii periodici
della GMI e su TLK arrivava una risposta vuota `<TCA=>`. Nessun effetto su soldi e
contatori. Corretto nella **SLIM-4.20.210** (25/11). Con la 210 un #CCI perso viene
richiesto solo dopo 30 min; dalla 211 si riprova dopo 60 s.

### Comandi delle prove al banco
#TAP, #POS_SIM, #KEY (tasto SET/SEL simulato, fw >= 4.20.100) e #SCREENSHOT servono
alle prove al banco (#TAP, #POS_SIM e #KEY solo sulle macchine di sviluppo). Fino alla
209 le loro risposte finivano nel trace TLK (`<TCA=#TAP-OK ...>`, percorsi delle
schermate): dalla 209 restano nel log del Pi. Su una macchina di campo non devono
comparire.

### Menu tecnico 9.2 (SLIM-4.20.189)
"Aggiorna software SLIM" mostra le fasi (scarico, controllo, pacchetto) e l'esito;
un'installazione partita dalla 9.2 e' un version_change voluto dal tecnico.

### MOD10 Tornello (scivolo a pagamento, in sviluppo dal 2026-11-10)
MOD10 non e' piu' "vending con resto": e' il tornello di uno scivolo per bambini (firmware
`vnd_gate.c`, `docs/TORNELLO.md`; Pi `src/modes/tornello/`), rami `tornello`, non ancora in
produzione. Una corsa per pagamento (banconote 5/10 con resto in monete, oppure carta dal
touch), schermi 160..167. Il tornello non si blocca mai: se l'hopper non da' tutto il resto
arriva l'evento `gate_short_change` (dovuto/erogato/mancante in centesimi) e il cliente entra
lo stesso; il non erogato resta credito per 2 minuti (`TRC`) e poi si azzera (riga
"Credito scaduto" nelle transazioni). Livello basso dell'hopper = schermo 161 "non da' resto,
importo esatto": banconote rifiutate, solo monete per l'importo esatto o carta, non e' un guasto. Un `gate_short_change` = hopper da rifornire o inceppato.

### IP del Raspberry (PI_IP, SLIM-4.20.195, corretto nella 196)
I Raspberry hanno IP fisso 192.168.9.97/.98/.99 dietro il router della macchina, e
alcuni sono usciti con l'ultimo numero sbagliato. Dalla 195 il proprietario lo cambia
dalla dashboard (chiave delicata `PI_IP`, campo mascherato: solo l'ultimo numero),
senza riavvio del Pi. Evento `pi_ip` (from -> to) = cambio voluto, non un guasto; un
calo di 2-3 s della rete in quel momento e' normale. `pi_ip_failed` = IP rimasto quello
di prima (indirizzo gia' occupato da un altro apparecchio, router che non risponde col
nuovo: in quel caso torna da solo al vecchio e non riprova per 24 ore): da segnalare al
proprietario, non e' un problema della macchina. Un cambio di `host.ips` senza evento
`pi_ip` invece e' anomalo (SD sostituita o modifica a mano).

## Versioni (2026-11-25)
- **Le versioni vanno confrontate come numeri, non come testo**: dal 25/11 il firmware
  GMI ha tre cifre nell'ultimo numero, **4.20.100 e' piu' nuova di 4.20.99** (come
  SLIM-4.20.210 > SLIM-4.20.99). Nel payload e su TLK compare "NCG4.20.100".
- Firmware GMI piu' recente: **4.20.100** (25/11, tramoggia dopo un inceppamento
  sbloccato, #KEY), su main e nella SLIM-4.20.209/210.
- Pi: **SLIM-4.20.211** su develop e **beta** dal 25/11 sera (208: POS CG-003; 209: GMI
  4.20.100; 210: fix #CCI; 211: gmi_hostlink con causa e durata, punto di rottura del
  flash GMI, nuovo tentativo #CCI dopo 60 s). Prima: 207 su beta dal 24/11 con GMI 4.20.99.
- main (golden), mod5, mod10, mod12: non aggiornati il 24-25/11, il merge lo fa lo
  sviluppatore quando decide. Una macchina su quei canali ferma a una versione
  precedente e' normale.
- I branch delle macchine in campo ricevono il codice nuovo solo quando lo
  sviluppatore fa il merge: una macchina "indietro" su un branch non aggiornato e'
  normale. E' anomala se il suo repo (git_commit) e' avanti ma la release
  (app_version) no per piu' di un giorno.

## Chi fa cosa (per assegnare i problemi)
- **firmware**: GMI (STM32), bootloader, protocollo seriale lato GMI.
- **pi**: py_cgslim4 (main.py, pos-engine, gitpuller, fleet-reporter, serial_recovery).
- **dashboard**: cgslim-fleet (Supabase/Vercel).
- **hardware**: cavi, alimentatori, schede, POS fisico, router/SIM.
- **campo**: azioni dei tecnici sul posto (riavvio, cambio cavo, verifica).
