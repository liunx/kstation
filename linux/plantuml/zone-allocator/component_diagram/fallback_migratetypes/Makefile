PUML = plantuml
CONVERTER = rsvg-convert

PNGS = $(subst .plantuml,.png,$(wildcard *.plantuml))

all: $(PNGS)

%.png : %.svg
	$(CONVERTER) $< -o $@

%.svg : %.plantuml
	$(PUML) -tsvg $<

clean:
	rm -f *.svg
	rm -f *.png
