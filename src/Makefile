# License: GPL
# Copyright Red Hat Inc. 2001 - 2008, 2013
# Copyright Lubomir Rintel <lkundrak@v3.sk> 2008, 2009

PKGNAME=system-config-keyboard
VERSION=1.4.0

DESTDIR?=$(INSTROOT)
PREFIX=/usr
SYSCONFDIR=/etc
DATADIR=$(PREFIX)/share
BINDIR=$(PREFIX)/bin
SBINDIR=$(PREFIX)/sbin
MANDIR=$(DATADIR)/man

PKGDATADIR=$(DATADIR)/$(PKGNAME)
PKGIMAGESDIR=$(PKGDATADIR)/pixmaps
POLKITDIR=$(DATADIR)/polkit-1/actions

POLKITFILE=org.fedoraproject.config.keyboard.policy
PKEXEC=$(BINDIR)/pkexec

PYTHON=python
PYTHON_SITELIB=$(shell $(PYTHON) -c 'from distutils.sysconfig import get_python_lib; print get_python_lib()')
PYTHON_MODULE=$(shell echo $(PKGNAME) |sed 's/-/_/g')

all: ${PKGNAME}.desktop gettext polkit

polkit: $(PKGNAME).sh

$(PKGNAME).sh::
	echo -e "#!/bin/sh\nexec $(PKEXEC) $(SBINDIR)/$(PKGNAME) \"\$$@\"" > "$@"
	chmod 755 "$@"

gettext:
	cd po && for i in *.po; do msgfmt $$i -o $$(echo $$i |sed s/.po/.mo/) || exit 1; done

install: all
	mkdir -p $(DESTDIR)$(BINDIR)
	mkdir -p $(DESTDIR)$(SBINDIR)
	mkdir -p $(DESTDIR)$(PKGDATADIR)
	mkdir -p $(DESTDIR)$(POLKITDIR)
	mkdir -p $(DESTDIR)$(PKGDATADIR)/pixmaps
	mkdir -p $(DESTDIR)$(MANDIR)/man1
	mkdir -p $(DESTDIR)$(MANDIR)/man8
	mkdir -p $(DESTDIR)/usr/share/applications
	mkdir -p $(DESTDIR)/usr/share/firstboot
	mkdir -p $(DESTDIR)/usr/share/firstboot/modules
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/48x48/apps
	mkdir -p $(DESTDIR)$(PYTHON_SITELIB)/$(PYTHON_MODULE)
	install -m 644 src/*.py $(DESTDIR)$(PKGDATADIR)
	install -m 755 src/${PKGNAME} $(DESTDIR)$(SBINDIR)/$(PKGNAME)
	install -m 644 lib/*.py $(DESTDIR)$(PYTHON_SITELIB)/$(PYTHON_MODULE)
	install -m 755 $(PKGNAME).sh $(DESTDIR)$(BINDIR)/$(PKGNAME)
	install -m 644 $(POLKITFILE) $(DESTDIR)$(POLKITDIR)
	install -m 644 pixmaps/*.png $(DESTDIR)$(PKGDATADIR)/pixmaps
	install -m 644 pixmaps/${PKGNAME}.png $(DESTDIR)/usr/share/icons/hicolor/48x48/apps
	install -m 644 $(PKGNAME).man $(DESTDIR)$(MANDIR)/man8/$(PKGNAME).8
	ln -sf ../man8/$(PKGNAME).8 $(DESTDIR)$(MANDIR)/man1/$(PKGNAME).1
	install -m 644 ${PKGNAME}.desktop $(DESTDIR)/usr/share/applications/${PKGNAME}.desktop
	ln -sf $(PKGDATADIR)/keyboard_gui.py $(DESTDIR)/usr/share/firstboot/modules/keyboard.py 
	cd po && for i in *.mo; do mkdir -p $(DESTDIR)/usr/share/locale/$$(echo $$i |sed s/.mo//)/LC_MESSAGES/; install -m 644 $$i $(DESTDIR)/usr/share/locale/$$(echo $$i |sed s/.mo//)/LC_MESSAGES/system-config-keyboard.mo || exit 1; done

dist:
	git archive --format=tar --prefix=$(PKGNAME)-$(VERSION)/ $(PKGNAME)-$(VERSION) | bzip2 -9 > $(PKGNAME)-$(VERSION).tar.bz2

tag:
	git tag $(PKGNAME)-$(VERSION)

clean:
	@rm -fv *~
	@rm -fv src/*.pyc
	@rm -f ${PKGNAME}.desktop

%.desktop: %.desktop.in
	@intltool-merge -d -u po/ $< $@
