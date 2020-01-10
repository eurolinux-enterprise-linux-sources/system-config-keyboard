# License: GPL
# Copyright Red Hat Inc. 2001 - 2008
# Copyright Lubomir Rintel <lkundrak@v3.sk> 2008, 2009

PKGNAME=system-config-keyboard
VERSION=1.3.1

DESTDIR?=$(INSTROOT)
PREFIX=/usr
SYSCONFDIR=/etc
DATADIR=$(PREFIX)/share
BINDIR=$(PREFIX)/bin
SBINDIR=$(PREFIX)/sbin
MANDIR=$(DATADIR)/man

PKGDATADIR=$(DATADIR)/$(PKGNAME)
PKGIMAGESDIR=$(PKGDATADIR)/pixmaps
PAMD_DIR=$(SYSCONFDIR)/pam.d
SECURITY_DIR=$(SYSCONFDIR)/security/console.apps

PYTHON=python
PYTHON_SITELIB=$(shell $(PYTHON) -c 'from distutils.sysconfig import get_python_lib; print get_python_lib()')
PYTHON_MODULE=$(shell echo $(PKGNAME) |sed 's/-/_/g')

all: gettext

gettext:
	cd po && for i in *.po; do msgfmt $$i -o $$(echo $$i |sed s/.po/.mo/) || exit 1; done

install: ${PKGNAME}.desktop
	mkdir -p $(DESTDIR)$(BINDIR)
	mkdir -p $(DESTDIR)$(SBINDIR)
	mkdir -p $(DESTDIR)$(PKGDATADIR)
	mkdir -p $(DESTDIR)$(PAMD_DIR)
	mkdir -p $(DESTDIR)$(SECURITY_DIR)
	mkdir -p $(DESTDIR)$(PKGDATADIR)/pixmaps
	mkdir -p $(DESTDIR)/usr/share/applications
	mkdir -p $(DESTDIR)/usr/share/firstboot
	mkdir -p $(DESTDIR)/usr/share/firstboot/modules
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/48x48/apps
	mkdir -p $(DESTDIR)$(PYTHON_SITELIB)/$(PYTHON_MODULE)
	install -m 644 src/*.py $(DESTDIR)$(PKGDATADIR)
	install -m 755 src/${PKGNAME} $(DESTDIR)$(SBINDIR)/$(PKGNAME)
	install -m 644 lib/*.py $(DESTDIR)$(PYTHON_SITELIB)/$(PYTHON_MODULE)
	install -m 644 pixmaps/*.png $(DESTDIR)$(PKGDATADIR)/pixmaps
	install -m 644 pixmaps/${PKGNAME}.png $(DESTDIR)/usr/share/icons/hicolor/48x48/apps
	install -m 644 ${PKGNAME}.pam $(DESTDIR)$(PAMD_DIR)/${PKGNAME}
	install -m 644 ${PKGNAME}.console $(DESTDIR)$(SECURITY_DIR)/${PKGNAME}
	install -m 644 ${PKGNAME}.desktop $(DESTDIR)/usr/share/applications/${PKGNAME}.desktop
	ln -sf consolehelper $(DESTDIR)/$(BINDIR)/${PKGNAME}
	ln -sf $(PKGDATADIR)/keyboard_gui.py $(DESTDIR)/usr/share/firstboot/modules/keyboard.py 
	cd po && for i in *.mo; do mkdir -p $(DESTDIR)/usr/share/locale/$$(echo $$i |sed s/.mo//)/LC_MESSAGES/; install -m 644 $$i $(DESTDIR)/usr/share/locale/$$(echo $$i |sed s/.mo//)/LC_MESSAGES/system-config-keyboard.mo || exit 1; done

dist:
	rm -rf $(PKGNAME)-$(VERSION)
	svn export $$(svn info |awk '/^URL:/ {print $$2}') $(PKGNAME)-$(VERSION)
	tar czf $(PKGNAME)-$(VERSION).tar.gz ${PKGNAME}-$(VERSION)

tag:
	svn copy -m "Tagged $(PKGNAME)-$(VERSION)" 	\
		$$(svn info |awk '/^URL:/ {print $$2}')	\
		$$(svn info |awk '/^Repository Root:/ {print $$3}')/tags/$(PKGNAME)-$(VERSION)

clean:
	@rm -fv *~
	@rm -fv src/*.pyc
	@rm -f ${PKGNAME}.desktop

%.desktop: %.desktop.in
	@intltool-merge -d -u po/ $< $@
