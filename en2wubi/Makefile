# This is a Python template Makefile, do modification as you want
#
# Project: 
# Author:
# Email :

HOST = 127.0.0.1
PYTHONPATH="$(shell printenv PYTHONPATH):$(PWD)"

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +

run:

setup:
	PYTHONPATH=$(PYTHONPATH) python ./en2wubi/__init__.py

convert-cn2wb:
	PYTHONPATH=$(PYTHONPATH) python ./en2wubi/scripts/convert_text.py --input-doc $(IN) --output-doc $(OUT) --convert-type ch2wb
	PYTHONPATH=$(PYTHONPATH) python ./en2wubi/scripts/fix-wubi.py $(OUT)

convert-wb2cn:
	PYTHONPATH=$(PYTHONPATH) python ./en2wubi/scripts/fix-cn.py $(IN)
	PYTHONPATH=$(PYTHONPATH) python ./en2wubi/scripts/convert_text.py --input-doc $(IN) --output-doc $(OUT) --convert-type wb2ch

cleanall:
