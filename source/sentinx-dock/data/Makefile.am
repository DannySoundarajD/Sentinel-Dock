NULL =

SUBDIRS = \
	icons \
	themes \
	$(NULL)

if ENABLE_APPORT
SUBDIRS += apport
endif

EXTRA_DIST = \
	sentinx-dock-default-icon.svg \
	sentinx-dock.appdata.xml.in \
	net.launchpad.plank.gschema.xml.in \
	sentinx-dock.desktop.in \
	plank.gresource.xml \
	poof.svg \
	ui/preferences.ui \
	$(NULL)

CLEANFILES = \
	sentinx-dock.appdata.xml \
	sentinx-dock.desktop \
	$(gsettings_SCHEMAS) \
	gschemas.compiled \
	net.launchpad.plank.gschema.valid \
	$(NULL)

applicationsdir = $(datadir)/applications
applications_DATA = sentinx-dock.desktop

appdatadir = $(datadir)/metainfo
appdata_DATA = plank.appdata.xml

gsettings_SCHEMAS = net.launchpad.plank.gschema.xml

%.gschema.xml: %.gschema.xml.in Makefile
	$(AM_V_GEN) sed -e 's|@GETTEXT_PACKAGE[@]|$(GETTEXT_PACKAGE)|g' \
	$< > $@ || rm $@

@GSETTINGS_RULES@

gschemas.compiled: Makefile $(gsettings_SCHEMAS:.xml=.valid)
	$(AM_V_GEN) $(GLIB_COMPILE_SCHEMAS) --targetdir=$(builddir) $(builddir)

all-local: gschemas.compiled

%.desktop: %.desktop.in
	$(AM_V_GEN)$(MSGFMT) --desktop --keyword= --keyword=Name \
		--keyword=GenericName --keyword=Comment --keyword=Keywords \
		--template $< -d $(top_srcdir)/po -o $@

%.appdata.xml: %.appdata.xml.in
	$(AM_V_GEN)$(MSGFMT) --xml --template $< -d $(top_srcdir)/po -o $@
