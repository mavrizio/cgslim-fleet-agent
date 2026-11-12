# Registro problemi flotta CGSLIM

Aggiornato dall'agente il 12/11/2026 10:05. Una voce per causa; MHD senza zeri. Generato: non modificare a mano.

## Aperti

<a id="cg-003"></a>

### CG-003 · POS DISCONNECTED dopo timeout get_advanced_config: 24350, 37008 e 33326 all'ottavo giorno, anche con la 199; ora anche 23718 e 6 Pi di banco

- **Area:** pi · **Gravita':** high · **Visto:** 2026-10-31 → 2026-11-12
- **Macchine:** 24350, 37008, 33326, 23718, 11223344, 11155520, 11223355, 1470000, 54124120, 58547455, 24866, 33957, 36842, 24254
- **Prove:** Avviso 'POS in errore su 8 macchine' (Timeout locale get_advanced_config 15 s) aperto dal 10/11.
Oggi alle 09:4x-09:5x, macchine in campo/beta:
- 24350: DISCONNECTED dopo il reboot delle 09:12 e l'aggiornamento a 199 delle 09:17.
- 37008: DISCONNECTED con la 199 (dalle 17:42 di ieri); 10 vendite cash ieri, nessuna carta.
- 33326: DISCONNECTED con la 199.
- 23718: DISCONNECTED senza p95_error; 6 tentativi carta ieri, nessuno approvato.
Pi di banco con p95_error timeout: 11223344, 11155520, 11223355, 1470000, 54124120, 58547455. La 58547455 aveva approvato 2 carte ieri (14:35-15:24).
La 11223344 ha avuto il cambio PI_IP .97->.99 alle 12:50 mentre era sulla 195 (bug noto).
'Connessione persa durante get_advanced_config', tutte rientrate entro 15 min:
- 24866 e 33957 alle 13:47; 33957 anche alle 16:47;
- 4 macchine alle 17:47 (rollout);
- 36842 alle 18:02;
- 11223355 alle 08:47 di oggi;
- 24254 alle 09:17 di oggi.
- **Ipotesi:** Dopo un timeout della lettura cashless_info il pos-engine resta DISCONNECTED senza ritentare. La 199 non cambia il comportamento.
Sulla 11223344 si somma il bug PI_IP della 195, che richiede di spegnere il POS.
I 'Connessione persa' sono transitori legati ai riavvii dell'app.
- **Proposta:** Maurizio:
- Un errore di get_advanced_config non deve bloccare il P95: saltare la lettura e ritentarla con backoff.
- Nascondere la carta a POS DISCONNECTED.
- Log di pos-engine della 24350 dopo le 09:17.
Campo Parma: spegnere e riaccendere il POS della 24350 e provare una carta reale.
Banco: spegnere e riaccendere il POS della 11223344.
Dashboard: escludere i Pi di banco dall'avviso.
- **Gia' noto:** POS: get_advanced_config; IP del Raspberry (bug 195 su POS dopo PI_IP)

<a id="cg-006"></a>

### CG-006 · 36842 senza parametri bancari (TID 00000000, codice 20); TID di prova 97942484 ora su 8 terminali

- **Area:** pos · **Gravita':** high · **Visto:** 2026-10-30 → 2026-11-12
- **Macchine:** 36842, 23718, 24338, 28418, 11223344, 11223355, 1470000, 54124120, 58547455, 58555555, 58888999
- **Prove:** 36842:
- 11/11 19:20: 2 pagamenti carta 'POS non configurato (codice 20)', uniche transazioni nelle 24 h;
- TID 00000000, nessun acquirer, package 01.04.25.03;
- nessuna carta approvata nello storico.
TID 97942484 su 23718, 11223344, 11223355, 1470000, 54124120, 58547455, 58555555 e 58888999. 1470000 e 58888999 non hanno acquirer letti.
58888999 stamattina:
- 7 errori 'codice 20' tra le 09:22 e le 09:31 (uno dopo 'POS riattivato dopo codice 90');
- 7 approvate, l'ultima alle 09:40.
58555555: 3 rifiuti 'codice 37' alle 08:38-08:44, poi approvate.
Altri TID di prova: 24338 97942485, 28418 97942488.
- **Ipotesi:** Senza parametri ogni carta sulla 36842 fallisce.
Sulla 58888999 il terminale sembra perdere la configurazione dopo un codice 90.
Con lo stesso TID attivo su 8 terminali sono probabili errori 48 e rifiuti (caso noto della 24338). Non confermato per il codice 37.
- **Proposta:** Hardware/POS:
- Parametrizzare la 36842 con il TID di produzione.
- Assegnare TID distinti ai terminali di banco prima della spedizione.
Maurizio: nascondere la carta con TID 00000000 o senza acquirer.
- **Gia' noto:** POS: altri errori (errore 48, TID duplicato su 24338)

<a id="cg-007"></a>

### CG-007 · 36842 senza vendite (tramogge 0,1,0, schermata 72); 32996 ha venduto di nuovo

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-01 → 2026-11-12
- **Macchine:** 36842, 32996, 23718
- **Prove:** 12/11 alle 09:5x:
- 36842: tramogge 0,1,0, schermata 72; nelle 24 h solo 2 carte fallite (codice 20, 19:20).
- 32996: tramogge 1,1,0, schermata 70; 1 vendita cash alle 10:52 di ieri.
Altre Parma nelle 24 h: 24349 8, 25158 7, 24350 3, 28416 3, 25157 1, 28417 0, 28419 0, 32995 0.
23718: mod 1, schermata 45, tramogge 0,0,1; 6 tentativi carta senza approvazioni, nessuna vendita cash.
- **Ipotesi:** La 32996 vende, anche se poco: forse e' solo poco frequentata.
Sulla 36842 la tramoggia 1 non risulta presente e la carta non e' configurata (CG-006): di fatto non puo' vendere.
Non confermato.
- **Proposta:** Campo Parma:
- 36842: display, menu tecnico e tramoggia 1; vendita cash di prova.
Maurizio: chiarire il significato delle schermate 72 e 45 e se la GMI ripete #HPS dopo l'avvio.

<a id="cg-009"></a>

### CG-009 · 24254 (Aprilia): stamattina accesa in orario, ma ieri accensione alle 12:50 e arresto alle 19:46; nessuna vendita

- **Area:** campo · **Gravita':** high · **Visto:** 2026-11-02 → 2026-11-12
- **Macchine:** 24254
- **Prove:** 11/11:
- 12:52: reboot (uptime 140), quindi accesa verso le 12:50;
- 12:55: un tentativo carta in timeout (nessuna carta), unica transazione;
- 17:43 e 17:46: aggiornata a 199 e fw 4.20.93 senza problemi;
- sottotensione 8 volte nel pomeriggio;
- 19:46: ultimo report, undicesima sera di fila con arresto anticipato (le altre Aprilia tra le 23:25 e le 23:47).
12/11:
- 09:16: reboot (uptime 138), prima accensione mattutina in orario;
- 09:17: 'Connessione persa get_advanced_config' rientrata;
- 09:47: sottotensione ADESSO, poi POS IDLE.
Ultima carta approvata il 05/11.
- **Ipotesi:** Alimentazione debole o interrotta: sottotensione a ogni accensione e spegnimento serale anticipato. Possibile presa o timer diversi dalle altre Aprilia.
L'accensione regolare di oggi potrebbe indicare un intervento sul timer. Non confermato.
- **Proposta:** Campo Aprilia, oggi:
- Verificare presa e timer serale.
- Sostituire l'alimentatore del Pi.
- Fare una vendita di prova cash e carta.
Maurizio: journal e dmesg dell'11/11 attorno alle 19:46.

<a id="cg-004"></a>

### CG-004 · Seriale GMI assente all'accensione (FTDI non enumerato), cavi lotto BG03E: di nuovo la 25158

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-12
- **Macchine:** 25158, 32996
- **Prove:** 12/11, 25158 (BG03ES5F):
- 09:22: reboot (uptime 108), eccezione 'could not open port /dev/ttyUSB0' e serial_missing not_enumerated (USB: solo hub, ethernet e ILITEK);
- 09:26: reboot di recovery (uptime 45);
- 09:27: serial_recovery.
La 25158 e' a 6 mattine su 7 (06, 08, 09, 10, 11 e 12/11). 7 vendite cash nelle 24 h, l'ultima alle 09:36.
32996 (BG03ER1N) pulita: reboot alle 09:04, nessun serial_missing.
Serial_missing anche sul banco (58888999 alle 16:27, solo STLink sul bus, serial_back dopo 10 s): caso di banco durante la programmazione.
Cavo della 25158 non ancora scambiato.
- **Ipotesi:** Lotto FT232R BG03E e/o alimentazione a ritroso dalla GMI. Il recovery funziona e costa circa 5 minuti.
- **Proposta:** Campo Parma: scambiare il cavo della 25158 con uno AL05 e lasciare la 32996 come controllo.
Pi: nel prossimo rilascio riavvio anticipato (~30-40 s), uhubctl e TX della GMI in high-Z.
- **Gia' noto:** Seriale assente al mattino (serial_missing, not_enumerated)

<a id="cg-005"></a>

### CG-005 · Sottotensione del Raspberry: 24349 e 24254 a episodi tutto il giorno e anche adesso, 23718 fissa

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-01 → 2026-11-12
- **Macchine:** 24349, 23718, 24254, 24350, 24338, 11223355
- **Prove:** Avvisi undervoltage_now dell'11/11, orari locali:
- 24349: circa 13 episodi (10:02, 10:32, 11:17, 12:47, 13:47, 17:02-17:32, 18:02-18:47, 19:47, 20:17-21:47, 22:17, 22:47, 23:17-00:17). Oggi di nuovo alle 09:32, a 15 minuti dal boot delle 09:17.
- 24254: 8 episodi tra le 13:02 e le 20:17. Oggi alle 09:47, a 30 minuti dal boot.
- 23718: 0x50005 fissa, avviso aperto dal 03/11.
- 24338 e 24350: 0x50000.
- 11223355 (banco): 0x50000 a piu' riprese ieri, ora 0x0 dopo il reboot delle 08:41.
- **Ipotesi:** Alimentatori o cavi deboli. Su 24349 e 24254 la sottotensione arriva subito dopo l'accensione e si ripete per tutto il giorno.
- **Proposta:** Hardware/campo, in ordine:
1. 24254 (insieme a CG-009).
2. 24349.
3. 23718.
4. 24350 e 24338.
- **Gia' noto:** host.throttled 0x50000 (scheda campi); sottotensione sospettata nei flash GMI falliti

<a id="cg-014"></a>

### CG-014 · MOD inattesa su branch mod5: 24866 mod 12, 23718 mod 1 senza vendite

- **Area:** firmware · **Gravita':** medium · **Visto:** 2026-11-05 → 2026-11-12
- **Macchine:** 24866, 23718
- **Prove:** 24866 (branch mod5):
- mod 12, schermata 70, tramogge 1,1,0;
- 2 vendite cash ieri;
- ultimo report ieri alle 20:24, prima delle altre Aprilia (23:25-23:47); riaccesa alle 05:41.
23718 (branch mod5):
- oggi mod 1, schermata 45, tramogge 0,0,1 (ieri 0,0,0 e schermata 46);
- 6 tentativi carta, nessuna vendita;
- uptime 155724 s.
- **Ipotesi:** Su 24866 la MOD e' stata probabilmente impostata dal tecnico.
23718 sembra una macchina di prova o non configurata. Mod 1 non e' nella scheda.
- **Proposta:** Maurizio: chiarire quali MOD sono attese per 24866 e 23718.
Campo:
- Aprilia: confermare la MOD della 24866.
- 23718: dire se e' in servizio.

<a id="cg-020"></a>

### CG-020 · 24350 (Parma) senza telemetria dalle 10:51 di ieri alle 09:12 di oggi; aggiornamento a 199 arrivato in ritardo

- **Area:** hardware · **Gravita':** medium · **Visto:** 2026-11-11 → 2026-11-12
- **Macchine:** 24350
- **Prove:** 11/11:
- 10:36: update_failed 'Could not resolve host: gitlab-dev.dedemapp.com' (healed stale_lock), rientrato subito;
- 10:51: ultimo report; avviso offline dalle 11:32.
Nelle 24 h risultano comunque 3 transazioni (15:13-16:32: 2 cash approvate, 1 carta annullata).
La macchina ha perso il rollout mod12 delle 17:42.
12/11:
- 09:12: reboot (uptime 136);
- 09:17: SLIM-4.20.192->199; 09:20 fw 4.20.92->4.20.93.
Ora rssi -48, LTE, POS DISCONNECTED (CG-003).
- **Ipotesi:** Perdita di rete/DNS sul router o sulla SIM della 24350 per tutta la giornata. Le transazioni sono probabilmente state messe in coda e inviate dopo il riavvio.
La macchina e' rimasta in vendita.
Non confermato.
- **Proposta:** Campo Parma: controllare il router e la SIM della 24350 (log di connessione dell'11/11 dalle 10:50).
Maurizio: verificare se le transazioni di ieri pomeriggio sono arrivate in ritardo (timestamp di inserimento) e se il fleet-reporter ritenta senza rete.
- **Gia' noto:** Aggiornamenti bloccati (update_failed, rete/SIM)

<a id="cg-011"></a>

### CG-011 · Dashboard: chiave 33326 sistemata; restano centro null e i Pi di banco nel conteggio

- **Area:** dashboard · **Gravita':** low · **Visto:** 2026-11-04 → 2026-11-12
- **Macchine:** 23718, 24338, 28418, 33326, 37008
- **Prove:** - 33326: device_key_enrolled l'11/11 alle 14:39, avviso mismatch chiuso, oggi device_key_status 'ok'.
- Centro null per 23718, 24338, 28418, 33326 e 37008.
- Conteggio flotta 31:
  - 21 macchine in campo/beta;
  - 9 Pi di banco con MHD provvisorio o nuovo (11223344, 11223355, 11155520, 1470000, 54124120, 58547455, 58555555, 58888999, 21784);
  - il Pi senza MHD 4f2f67b8 (chiave 'missing').
- PI_IP applicati su 24338 (13:50) e 33326 (14:56) senza un evento pi_ip nel flusso; solo la 11223344 lo ha.
- **Ipotesi:** Il conteggio e' gonfiato dalle macchine in preparazione.
L'evento pi_ip forse manca quando il valore non cambia o non viene inviato. Da verificare.
- **Proposta:** Dashboard/Maurizio:
- Escludere da conteggio e avvisi i device di banco.
- Assegnare il centro (o 'banco') alle 5 macchine.
- Verificare perche' il PI_IP applicato su 24338 e 33326 non ha generato l'evento pi_ip.
- **Gia' noto:** Profilo display auto / golden SD; IP del Raspberry (PI_IP)

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

### CG-016 · Errori seriali: 29598 ne ~100 nelle prime 3 h; fe alti su 33326 e 11223355; errori lato Pi su 58547455 e 58555555

- **Area:** hardware · **Gravita':** low · **Visto:** 2026-11-06 → 2026-11-12
- **Macchine:** 29598, 33326, 11223355, 58547455, 58555555, 37008, 23718, 28418
- **Prove:** - 29598: ne=108 con uptime 11044 s (accensione alle 06:45), stesso schema dei giorni scorsi.
- 33326: fe 220, ore 57 (bootloader V1 debug).
- 11223355: fe 237, ore 22.
- Errori lato Pi (pi_uart):
  - 58547455: brk 132, frame 79;
  - 58555555: brk 162, frame 19.
- 37008: ore 27.
- 23718: fe 30, ore 29.
- 28418 dopo il flash delle 04:11: fe 1, ne 1, ore 5 (test linea del 20/10 KO).
- **Ipotesi:** 29598: rumore sistematico nelle prime ore (cavo A10KIK4A, massa o GMI verde).
Sulle due nuove di banco con brk/frame lato Pi: cavo o massa al banco. Da verificare prima della spedizione.
- **Proposta:** Campo Aprilia: test linea 8.4 sulla 29598.
Banco: test linea 8.4 su 58547455 e 58555555.
Maurizio: inviare i contatori come delta giornaliero.
- **Gia' noto:** Aggiornamento firmware GMI (linea disturbata GMI verdi)

<a id="cg-018"></a>

### CG-018 · Preparazione macchine nuove al banco: 9 Pi con MHD provvisori (11223344, 11223355, 11155520, 1470000, 54124120, 58547455, 58555555, 58888999, 21784) e 1 Pi senza MHD

- **Area:** campo · **Gravita':** low · **Visto:** 2026-11-09 → 2026-11-12
- **Macchine:** 11223344, 11223355, 11155520, 1470000, 54124120, 58547455, 58555555, 58888999, 21784, CG-4F2F67B8, 7a9fd21f
- **Prove:** Pi gia' visti, che ieri hanno avuto l'MHD (gmi_init_ok):
- 54124120 = CG-0C7892A3, alle 13:28;
- 1470000 = CG-E398A14E, alle 15:00 ('01470000');
- 58547455 = a9603f2d, alle 13:00.
Nuovi ieri:
- 21784 (CG-B8D3F091): alle 15:48, MDB SELF/2000, mod 12, su 196; offline dalle 15:56.
- 58555555 (CG-358B5348): alle 15:50, NCG4.09 no_bootloader, fw 4.20.93 alle 15:56.
- 58888999 (CG-30AE6DE1): alle 15:57; gmi_mute e 3 reboot alle 16:07-16:17, ST-Link ok alle 16:22 (3,19 V), gmi_init_ok alle 16:29.
Il cavo BG04MV0G del Pi senza MHD 4f2f67b8 (offline dall'11/11 08:54, SLIM-192) ora e' sulla 58888999.
11223344: 195->196->197->198->199 tra le 12:33 e le 16:23, PI_IP .97->.99 alle 12:50.
11223355: 6 reboot tra le 13:01 e le 16:34, piu' quello delle 08:41.
54124120: report a singhiozzo la notte (01:04, 02:55, 04:59), offline dalle 07:06.
Test linea OK su 11155520 e 11223344 (13:04) e su 54124120 (14:00).
7a9fd21f: PI_IP applicato alle 13:52, ma non compare nei device.
- **Ipotesi:** Lotto di macchine in preparazione. Gli MHD sembrano provvisori o di prova. Riavvii e restart sono attivita' di banco.
Sulla 54124120 la rete LTE del banco e' instabile (rssi -74).
- **Proposta:** Maurizio/campo:
- Assegnare MHD definitivi, centro e TID distinti prima della spedizione (CG-006).
- Test linea 8.4 su tutte.
Dashboard: marcarle 'banco' ed escluderle da avvisi e conteggio.
- **Gia' noto:** GMI 'muta' / NCG senza bootloader (menu 9.5 ST-Link); golden SD (CG-<seriale>)

## In osservazione

<a id="cg-001"></a>

### CG-001 · Aggiornamento firmware GMI: rollout 4.20.93 ok su tutta la flotta, 26087 questa volta senza problemi

- **Area:** firmware · **Gravita':** medium · **Visto:** 2026-10-30 → 2026-11-10
- **Macchine:** 26087, 33326, 24338
- **Prove:** 11/11, fw_change 4.20.92->4.20.93:
- mod12 tra le 17:43 e le 17:53, tutte riuscite. 26087 RDY alle 17:47 e fw ok alle 17:53; 29598 RDY alle 17:47 e ok alle 17:52.
- mod5/beta nel pomeriggio. RDY atteso su 23718 (13:40) e 33957 (13:41), poi ok.
- 24350 alle 09:20 di oggi; 28418 4.20.90->4.20.93 alle 04:11.
Nessun gmi_flash_failed sulle macchine in campo.
26087 oggi: 12 transazioni, 8 approvate.
33326 (V1 debug) e 24338 (bootloader sconosciuto): a 4.20.93.
- **Ipotesi:** La corruzione al byte 26880 del 10/11 sulla 26087 non si e' ripetuta: era un disturbo occasionale della linea. Le eccezioni RDY durante un flash voluto sono rumore.
- **Proposta:** Maurizio: non segnalare come eccezione il RDY durante un flash pianificato.
Campo Aprilia: test linea 8.4 sulla 26087 alla prima occasione.
Chiudere dopo il prossimo rollout pulito.
- **Gia' noto:** Aggiornamento firmware GMI che fallisce (gmi_flash_failed, gmi_blocked, loop RDY)

<a id="cg-012"></a>

### CG-012 · POS non pronto dopo l'avvio o dopo un codice 90: 'gia' in corso', Broken pipe, codice 90

- **Area:** pi · **Gravita':** medium · **Visto:** 2026-11-04 → 2026-11-12
- **Macchine:** 24254, 28418, 33957, 24866, 29597, 23718, 58888999
- **Prove:** Codice 90 nelle 24 h:
- 33957: 2 alle 12:42 di ieri, poi approvate;
- 23718: 2 alle 12:49;
- 58888999: 1 alle 09:22 di oggi, seguito da 'codice 20' (vedi CG-006);
- 58555555: 'POS riattivato dopo codice 90' alle 08:38.
Broken pipe solo sui Pi di banco: 11223355 e 58888999, fino alle 06:32 di oggi.
Nessun 'activate gia' in corso' nelle 24 h.
- **Ipotesi:** Stessa corsa all'avvio tra activate, lettura cashless_info e pagamento. Le macchine in campo ne risentono poco: la 33957 ha approvato le carte successive.
- **Proposta:** Maurizio: carta disabilitata finche' il POS non e' IDLE e cashless_info non ha finito.
Chiudere se in campo non ricompare con pagamenti persi.
- **Gia' noto:** POS: get_advanced_config (operazione gia' in corso)

<a id="cg-019"></a>

### CG-019 · ST-Link fallisce ('unknown state' su probe/erase_app) su 3 GMI nuove, ma la flash seriale poi riesce: ex a9603f2d ora 58547455 a 4.20.93

- **Area:** firmware · **Gravita':** low · **Visto:** 2026-11-10 → 2026-11-11
- **Macchine:** 58547455, 54124120, 1470000
- **Prove:** 58547455 (device a9603f2d, ieri non si cancellava):
- 12:44: 'Disconnessione hardware seriale'; 12:47 gmi_mute;
- 12:55: reboot e RDY loop;
- 12:56: fw_change 4.09->4.20.92; 13:00 gmi_init_ok; 13:41 fw 4.20.93;
- 8 vendite approvate tra le 14:35 e le 15:24.
54124120: ST-Link fallito alle 12:30 (probe) e alle 12:36 (erase_app), stesso messaggio 'target was in unknown state when halt was requested'; gmi_init_ok alle 13:28, ora 4.20.93.
1470000: ST-Link fallito alle 14:37 (probe) e alle 14:39 (erase_app); RDY alle 14:48; gmi_init_ok alle 15:00; ora 4.20.93.
Sulla 58888999 l'ST-Link e' riuscito al primo colpo (16:22).
- **Ipotesi:** Lo script ST-Link fallisce sul halt ma lascia la GMI nel bootloader (o lo scrive in parte), e da li' il flash seriale funziona. Non sembra una flash protetta ne' una GMI guasta.
Non confermato.
- **Proposta:** Maurizio:
- Nella diagnostica stlink_program fare reset-halt (connect under reset) e leggere gli option bytes.
- Se dopo un fallimento la GMI risponde RDY, passare subito al flash seriale invece di ripetere l'ST-Link.
- Interrompere i cicli di flash seriale dopo il primo gmi_blocked.
- **Gia' noto:** GMI 'muta' / NCG senza bootloader (menu 9.5 ST-Link)

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

<a id="cg-017"></a>

### CG-017 · 33957 (Carpi): vendite e carte riprese

- **Area:** hardware · **Gravita':** low · **Visto:** 2026-11-07 → 2026-11-09
- **Macchine:** 33957
- **Prove:** 11/11: 10 transazioni tra le 11:19 e le 20:17, 8 approvate (4 carte). Unici errori: 2 codice 90 alle 12:42 (in CG-012).
Aggiornata a 199 e fw 4.20.93 senza problemi. Oggi reboot alle 09:00, POS IDLE.
- **Ipotesi:** Il calo di vendite era legato al traffico del sito o ai problemi POS gia' rientrati.
- **Proposta:** Chiusa. Linea DISTURBATA in CG-015.
