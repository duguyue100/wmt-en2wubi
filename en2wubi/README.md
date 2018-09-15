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
All the data is saved in `EN2WUBI_PATH/data`. To convert the Chinese text to Wubi or the other way around:

```bash
make convert-cn2wb IN=cn/cn_text.cn OUT=wb/wb_text.wb  # CN2WB
make convert-wb2cn IN=wb/wb_text.wb OUT=cn/cn_text.cn  # WB2CN
```

The above command will take `cn_poem.cn` file and transform to `wb_poem.wb`
from Chinese to Wubi encoding. You can use `wb2ch` as a different conversion
type for translating a given Wubi document to Chinese text.

## Contacts

Yuhuang Hu  
Email: yuhuang.hu@ini.uzh.ch
