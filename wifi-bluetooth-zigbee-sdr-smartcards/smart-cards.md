# Smart Cards

### Enumeration&#x20;

* Place the smart card on the ACR122U smart card reader
* Enumerate the card to see which type it is.

```
pcsc_scan
# output #
Possibly identified card (using /usr/share/pcsc/smartcard_list.txt):
3B 8F 80 01 80 4F 0C A0 00 00 03 06 03 00 01 00 00 00 00 6A
3B 8F 80 01 80 4F 0C A0 00 00 03 06 .. 00 01 00 00 00 00 ..
	Mifare Standard 1K (as per PCSC std part3)
3B 8F 80 01 80 4F 0C A0 00 00 03 06 03 00 01 00 00 00 00 6A
3B 8F 80 01 80 4F 0C A0 00 00 03 06 03 .. .. 00 00 00 00 ..
	RFID - ISO 14443 Type A Part 3 (as per PCSC std part3)
3B 8F 80 01 80 4F 0C A0 00 00 03 06 03 00 01 00 00 00 00 6A
	Philips MIFARE Standard (1 Kbytes EEPROM)
	http://www.nxp.com/#/pip/pip=[pfp=41863]|pp=[t=pfp,i=41863]
	RFID - ISO 14443 Type A - Transport for London Oyster
	ACOS5/1k Mirfare
	RFID - ISO 14443 Type A - NXP Mifare card with 1k EEPROM
	vivotech ViVOcard Contactless Test Card
	Bangkok BTS Sky SmartPass
	Mifare Classic 1K (block 0 re-writeable)

```

* It it detected as a very common card type the Mifare Classic 1k card.
* Note: The command will continue to scan for a new card. You can CTRL+C when satisfied with all your enumeration.

### Mifare Classic Key Recovery

* To attempt to recovery the key, ensure the card is on your reader, and the reader is plugged in

```
mfoc -O myoutput_file.mfd
```

* This command should generate an output file
* Note: This command can take in excess of 20 minutes to run as it is attempting to recovery the keys....be patient, get a coffee, touch grass.
* `mfoc` will attempt to recover the A and the B keys for all blocks.
  * It will first loot to attain one key (like the default key) and use it to recover the other keys&#x20;
  * The time it takes varies greatly between different hotel cards
  * Once the key is recovered, all data will then be extracted
    * This includes key information and authenticated data.
    * All will be included in your `-O` output file.
* Should `mfoc` be successful use `xxd` to view the key contents&#x20;

```
xxd output.mfd
Block 0: 4c00 2200 0000 0000 0000 00c1 0000 0050 # DATA
Block 1: 4c00 2200 0000 0000 0000 00c1 0000 0050 # DATA
Block 2: 0000 0000 0000 0000 0000 0000 0000 0000 # DATA
Block 3: 2b2d 11bb 12ab ff08 8069 ffff ffff ffff # Key A, Access Bits, Key B
```

* Key A is `2b2d 11bb 12ab ff08 8069`&#x20;
* Key B is `ffff ffff ffff`
  * `ffff ffff ffff` is the default key used with Mifare Classic cards so it is very common to see
* If you ever dump a card and its all `ffff`
* The card is blank....
