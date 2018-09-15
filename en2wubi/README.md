# en2wubi

Translate English to Wubi.

+ First export the following environment variable

    ```bash
    export EN2WUBI_PATH=$HOME/.en2wubi
    ```

+ Setup the data structure

    ```bash
    make setup
    ```

## `convert-text`

This tool would help you convert a Chinese given text to Wubi encoding or vice versa.
All the data is saved in `EN2WUBI_PATH/data`. One example of using this tool is:

```bash
make convert-text IN=cn/cn_poem.cn OUT=py/wb_poem.wb TYPE=ch2wb
```

The above command will take `cn_poem.cn` file and transform to `wb_poem.wb`
from Chinese to Wubi encoding. You can use `wb2ch` as a different conversion
type for translating a given Wubi document to Chinese text.

## Contacts

Yuhuang Hu  
Email: yuhuang.hu@ini.uzh.ch
