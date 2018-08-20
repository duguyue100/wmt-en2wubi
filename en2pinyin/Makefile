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

test-utils:
	PYTHONPATH=$(PYTHONPATH) python ./en2pinyin/test_script/test_utils.py

test-conversion:
	PYTHONPATH=$(PYTHONPATH) python ./en2pinyin/test_script/test_conversion.py

test-text-gen:
	PYTHONPATH=$(PYTHONPATH) python ./en2pinyin/test_script/test_text_gen.py

test-translation:
	PYTHONPATH=$(PYTHONPATH) python ./en2pinyin/test_script/test_text_trans.py

convert-text:
	PYTHONPATH=$(PYTHONPATH) python ./en2pinyin/test_script/convert_text.py --input-doc $(IN) --output-doc $(OUT) --convert-type $(TYPE)

wubi-dictionary:
	PYTHONPATH=$(PYTHONPATH) python ./en2pinyin/test_script/test_wubi_dict.py

cleanall:
