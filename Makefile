PKGNAME := pyram
VERSION := 2.1.0
ARCH := all
SRC := src/pyram.c
BIN := build/pyram
OUTDIR := build/pyram-out
PKGDIR := /tmp/$(PKGNAME)_$(VERSION)
PREFIX := /usr/share/$(PKGNAME)
TEST_SCRIPT := test/testAll.sh
SPEED_SCRIPT := benchmarks/runSpeedTests.sh

CC := gcc
CFLAGS := -O3 -march=native -Wall -Wextra

.PHONY: all help build package clean install install-deb test speed-test speed-test-override speed-test-nooverride

all: package

help:
	@printf "Usage:\n"
	@printf "  make build                  Compile the pyram binary into $(BIN)\n"
	@printf "  make package                Build the Debian package in $(OUTDIR)/\n"
	@printf "  make install                Install the compiled binary to /usr/bin/$(PKGNAME)\n"
	@printf "  make install-deb            Install the Debian package using dpkg\n"
	@printf "  make test                   Run the repository test suite\n"
	@printf "  make speed-test             Run the benchmark speed tests and overwrite benchmark outputs\n"
	@printf "  make speed-test-nooverride  Run the benchmark speed tests without overwriting existing outputs\n"
	@printf "  make clean                  Remove generated build artifacts\n"

build: $(BIN)

$(BIN): $(SRC)
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -o $@ $<
	@chmod 755 $@
	@chmod -R a+rwX build

package: $(BIN)
	@rm -rf $(PKGDIR) $(OUTDIR)
	@mkdir -p $(PKGDIR)/DEBIAN $(PKGDIR)$(PREFIX) $(PKGDIR)/usr/bin
	chmod 0755 $(PKGDIR)/DEBIAN
	cp -r src $(PKGDIR)$(PREFIX)
	cp -r lib $(PKGDIR)$(PREFIX)
	cp $(BIN) $(PKGDIR)/usr/bin/$(PKGNAME)
	strip $(PKGDIR)/usr/bin/$(PKGNAME)
	printf "%s\n%s\n%s\n%s\n%s\n%s\n" \
		"Package: $(PKGNAME)" \
		"Version: $(VERSION)" \
		"Section: base" \
		"Priority: optional" \
		"Architecture: $(ARCH)" \
		"Maintainer: Bruno RNS <brunorns05@outlook.com>" > $(PKGDIR)/DEBIAN/control
	printf "Description: PyRAM package\n" >> $(PKGDIR)/DEBIAN/control
	dpkg-deb --build $(PKGDIR)
	mkdir -p $(OUTDIR)
	mv $(PKGDIR).deb $(OUTDIR)/
	@chmod -R a+rwX $(OUTDIR)
	@chmod -R a+rwX build
	@rm -rf $(PKGDIR) $(PKGDIR).deb

install: build
	test -f lib/pypy.so || (echo "Required runtime archive lib/pypy.so not found. Run 'make build' or restore this file." >&2; false)
	sudo mkdir -p /usr/share/$(PKGNAME)/lib
	sudo install -Dm755 $(BIN) /usr/bin/$(PKGNAME)
	sudo install -Dm644 lib/pypy.so /usr/share/$(PKGNAME)/lib/pypy.so
	sudo chmod -R a+rwX /usr/share/$(PKGNAME)

install-deb: package
	sudo dpkg -i $(OUTDIR)/$(PKGNAME)_$(VERSION).deb

test: build
	sudo bash $(TEST_SCRIPT)

speed-test: speed-test-override

speed-test-override: build
	sudo bash $(SPEED_SCRIPT)

speed-test-nooverride: build
	@TIMESTAMP=$$(date +%Y%m%d_%H%M%S) ; \
	OUTDIR=./benchmarks/tests/$$TIMESTAMP ; \
	DATADIR=./benchmarks/data/$$TIMESTAMP ; \
	mkdir -p "$$OUTDIR" "$$DATADIR" ; \
	sudo bash $(SPEED_SCRIPT) "$$OUTDIR" "$$DATADIR"

clean:
	@rm -rf $(BIN) $(OUTDIR) build/pyram_2.1.0
	@rm -rf test/simpleDjango/*
	touch test/simpleDjango/.keepme
	@rm -rf /tmp/$(PKGNAME)_$(VERSION) /tmp/$(PKGNAME)_$(VERSION).deb || true
