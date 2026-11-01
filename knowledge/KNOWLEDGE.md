# Conoscenza di base sulla flotta CGSLIM

Scheda per l'analista automatico. Fatti tecnici dallo sviluppo, aggiornati al
2026-11-01. Quando un dato del giorno combacia con un problema gia' noto, dillo
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
  parma, mod5...), costruisce la release in /opt/cgslim/current e, se la release
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

### Menu tecnico sordo dopo errore di erogazione
Fix fw 4.20.84 + SLIM-4.20.176. Errore 101 = erogazione incompleta.

### Riavvii della GMI
Firmware >= 4.20.38 manda #TRCFLT dopo un fault (type 1 HardFault, type 2/3
reset deliberato per errore I2C EEPROM). Senza #TRCFLT e con silenzio lungo =
watchdog (loop bloccante). Il fleet riceve FAULT_REPORT come evento/eccezione.

## Versioni (2026-11-01)
- Firmware GMI piu' recente rilasciato: 4.20.84. Pi: SLIM-4.20.176 su develop/beta.
- I branch delle macchine in campo (mod12, parma, beta2, mod5) ricevono il codice
  nuovo solo quando lo sviluppatore fa il merge: una macchina "indietro" su un
  branch non aggiornato e' normale. E' anomala se il suo repo (git_commit) e'
  avanti ma la release (app_version) no per piu' di un giorno.

## Chi fa cosa (per assegnare i problemi)
- **firmware**: GMI (STM32), bootloader, protocollo seriale lato GMI.
- **pi**: py_cgslim4 (main.py, pos-engine, gitpuller, fleet-reporter, serial_recovery).
- **dashboard**: cgslim-fleet (Supabase/Vercel).
- **hardware**: cavi, alimentatori, schede, POS fisico, router/SIM.
- **campo**: azioni dei tecnici sul posto (riavvio, cambio cavo, verifica).
