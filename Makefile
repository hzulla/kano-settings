APPNAME=kano-settings

MSGLANGS=$(notdir $(wildcard po/*po))
MSGOBJS=$(addprefix locale/,$(MSGLANGS:.po=/LC_MESSAGES/$(APPNAME).mo))

gettext: $(MSGOBJS)

locale/%/LC_MESSAGES/$(APPNAME).mo: po/%.po
	mkdir -p $(dir $@)
	msgfmt -c -o $@ po/$*.po
