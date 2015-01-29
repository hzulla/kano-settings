APPNAME=kano-settings

MSGLANGS=$(notdir $(wildcard po/*po))
MSGOBJS=$(addprefix locale/,$(MSGLANGS:.po=/LC_MESSAGES/$(APPNAME).mo))

.PHONY: po/messages.pot

po/messages.pot:
	xgettext -f po/PYPOTFILES -L Python -o po/messages.pot
	xgettext -f po/CPOTFILES -L C -k_ -kN_  -j -o po/messages.pot

gettext: $(MSGOBJS)

locale/%/LC_MESSAGES/$(APPNAME).mo: po/%.po
	mkdir -p $(dir $@)
	msgfmt -c -o $@ po/$*.po
