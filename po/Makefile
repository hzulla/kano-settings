APPNAME=kano-settings

MSGLANGS=$(notdir $(wildcard *po))
MSGOBJS=$(addprefix ../locale/,$(MSGLANGS:.po=/LC_MESSAGES/$(APPNAME).mo))

.PHONY: messages.pot

build: $(MSGOBJS)

update: $(MSGLANGS)

clean:
	rm -rf ../locale

messages.pot:
	xgettext -f PYPOTFILES -L Python --force-po -o messages.pot
	xgettext -f CPOTFILES -L C -k_ -kN_ -j -o messages.pot

%.po: messages.pot
	msgmerge -N -U $*.po messages.pot

../locale/%/LC_MESSAGES/$(APPNAME).mo: %.po
	mkdir -p $(dir $@)
	msgfmt -c -o $@ $*.po
