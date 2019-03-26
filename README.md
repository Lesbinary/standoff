# Stand-off annotation for deferred TMX
### Implementation of Stand-off annotation for deferred TMX ([Forcada, Esplà-Gomis and Pérez-Ortiz, EAMT 2016](http://www.dlsi.ua.es/~mlf/docum/forcada16j.pdf))

Try it with [Bitextor](https://github.com/bitextor/bitextor)! Use config option `deferredCrawling=true`.

## Scripts usage

### `deferred-document.py`: 3.1 Deferred bitext crawl

- stdin: Bitextor crawl format

`html_content(base_64)  url`

- stdout: deferred Bitextor crawl 

`html5lib_plain_text(base_64)  url  document_standoff_annotation`

--------

### `deferred-sentences.py`: 3.2 Deferred translation memory crawl

- Argument input: path of deferred Bitextor crawl file (output of deferred document script)
- stdin: Bitextor DOCALG file

`url1  url2  clean_text1  clean_text2  [...]`

- stdout: Bitextor DOCALG file with stand-off annotations (can be converted to TMX using Bitextor's `bitextor-buildTMX` using column names `--columns '[...],deferredseg1,checksum1,deferredseg2,checksum2'`):

`url1  url2  clean_text1  clean_text2  [...]  standoff_text1  checksum1  standoff_text2  checksum2`

--------

### `reconstructor-deferred-sentences.py`: sentence reconstruction

- Argument input: Bitextor crawl format

`html_content(base_64)  url`

#### Using tab separated input:

- stdin: Bitextor DOCALG file with stand-off annotations (only tab separated format supported)

`url1  url2  standoff_text1  standoff_text2  checksum1  checksum2  [...]  `
- stdout: Bitextor DOCALG file reconstructed

`url1  url2  clean_text1  clean_text2  checksum1  checksum2  [...]`
  
#### Using `--tmx` option:

- stdin: TMX with existing `tu/tuv/prop type="deferred-seg"` and `tu/tuv/prop type="source-document`

- stdout: TMX with filled `tu/tuv/seg` tag text


