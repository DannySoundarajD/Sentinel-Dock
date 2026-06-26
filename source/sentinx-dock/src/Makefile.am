include $(top_srcdir)/Makefile.common

sentinx_dock_VALAFLAGS = \
	$(COVERAGE_VALAFLAGS) \
	$(PLANK_CORE_VALAFLAGS) \
	$(top_builddir)/lib/plank.vapi \
	--vapidir $(top_srcdir)/vapi \
	$(top_srcdir)/vapi/config.vapi \
	-C \
	$(NULL)

BUILT_SOURCES = sentinx_dock_vala.stamp

bin_PROGRAMS = sentinx-dock

sentinx_dock_CFLAGS = \
	$(COVERAGE_CFLAGS) \
	$(PLANK_CORE_CFLAGS) \
	-include config.h \
	-I$(top_builddir)/lib \
	$(NULL)

sentinx_dock_LDADD = \
	$(COVERAGE_LDFLAGS) \
	$(PLANK_CORE_LIBS) \
	$(top_builddir)/lib/libplank.la \
	$(NULL)

sentinx_dock_LDFLAGS = \
	-L$(pkglibdir) \
	$(NULL)

sentinx_dock_VALASOURCES = \
	Main.vala \
	$(NULL)

nodist_sentinx_dock_SOURCES = \
	$(sentinx_dock_VALASOURCES:.vala=.c) \
	$(NULL)

$(sentinx_dock_VALASOURCES:.vala=.c): sentinx_dock_vala.stamp

sentinx_dock_vala.stamp: $(sentinx_dock_VALASOURCES) $(top_builddir)/lib/plank.vapi Makefile
	$(AM_V_VALA)$(VALAC) \
		$(sentinx_dock_VALAFLAGS) \
		$(filter %.vala %.c,$^)
	$(AM_V_at)touch $@

CLEANFILES = \
	sentinx_dock_vala.stamp \
	$(nodist_sentinx_dock_SOURCES) \
	$(NULL)

EXTRA_DIST = \
	$(sentinx_dock_VALASOURCES) \
	$(NULL)

