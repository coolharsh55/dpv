#!/usr/bin/env bash
emacs --batch --eval "(require 'org)" ~/org/dpv_docgen_overhall.org --funcall org-html-export-to-html
mv ~/org/dpv_docgen_overhall.html ../index.html