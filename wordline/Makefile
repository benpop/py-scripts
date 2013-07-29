SHELL = /bin/sh
INSTALL = install -p -mode 0744

NAMES = al cl wl
PYSRC = $(NAMES:%=%.py)

# INSTALL_DIR = /usr/local/bin
INSTALL_DIR = $(HOME)/bin

all:
	@echo Type \'make install\' to install:
	@echo '   ' $(PYSRC)
	@echo into INSTALL_DIR:
	@echo '   ' $(INSTALL_DIR)

install: $(PYSRC)
	@for f in $(NAMES) ; do \
		echo $(INSTALL) $$f.py $(INSTALL_DIR)/$$f ; \
		$(INSTALL) $$f.py $(INSTALL_DIR)/$$f ; \
	done
