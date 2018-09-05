# Stand-off annotation for deferred TMX
### Implementation of Stand-off annotation for deferred TMX ([Forcada, Esplà-Gomis and Pérez-Ortiz, EAMT 2016](http://www.dlsi.ua.es/~mlf/docum/forcada16j.pdf))

Try it with [Bitextor](https://github.com/bitextor/bitextor)! Use parameter `--deferred` (in `standoff` branch, not in `master` yet). Fully working with [Wiki sample](https://github.com/bitextor/bitextor/wiki/Sample-of-a-bitext)

## Scripts usage

`deferred-document.py`: 3.1 Deferred bitext crawl

- stdin: Bitextor crawl format

`html_content(base_64)  url`

- stdout: deferred Bitextor crawl 

`html_plain_text(base_64)  url  timestamp  MD5_sum  document_standoff_annotation`

--------

`deferred-sentences.py`: 3.2 Deferred translation memory crawl

- Argument input: path of deferred Bitextor crawl file (output of deferred document script)
- stdin: Bitextor DOCALG file

`url1  url2  clean_text1_in_base64  clean_text2_in_base64  [...]`

- stdout: Bitextor DOCALG file with stand-off annotations (can be converted to TMX using Bitextor's `bitextor-buildTMX` using 'deferredseg1' and 'deferredseg2' columns in `--columns`):

`url1  url2  clean_text1_in_base64  clean_text2_in_base64  [...]  standoff_text1  standoff_text2`

--------

`reconstructor-deferred-sentences.py`: reconstructs tab separated deferred sentences (not TMX yet)

- Argument input: Bitextor crawl format

`html_content(base_64)  url`
- stdin: Bitextor DOCALG file with stand-off annotations (only tab separated format supported)

`url1  url2  standoff_text1  standoff_text2  [...]  `
- stdout: Bitextor DOCALG file reconstructed

`url1  url2  clean_text1_in_base64  clean_text2_in_base64  [...]`
