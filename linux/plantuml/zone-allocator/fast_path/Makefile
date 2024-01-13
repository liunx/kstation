PUML = plantuml
CONVERTER = rsvg-convert
DIRS = $(wildcard */)
SRC = $(foreach dir, $(DIRS), $(wildcard $(dir)*.plantuml))
PNGS = $(patsubst %.plantuml,%.png,$(SRC))

all: $(PNGS)

%.png : %.svg
	$(CONVERTER) $< -o $@

%.svg : %.plantuml
	$(PUML) -tsvg $<

clean:
	rm -rf $(PNGS)
