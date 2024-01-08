PUML = plantuml
CONVERTER = rsvg-convert

#PNGS = $(subst .plantuml,.png,$(wildcard *.plantuml))
PNGS = $(subst .svg,.png,$(wildcard *.svg))
SVGS = $(subst .plantuml,.svg,$(wildcard *.plantuml))

all: $(PNGS) $(SVGS)

%.svg : %.plantuml
	$(PUML) -tsvg $<

%.png : %.svg
	$(CONVERTER) $< -o $@

clean:
	rm -f *.svg
	rm -f *.png
