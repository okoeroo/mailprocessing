# Mailprocessing

Handy scripts for mail processing


## extract_pst_to_mbox_files.sh

This script is a wrapper around **readpst**. It will extract the PST file into separate files. The attachments are by name postfixed to the email files. The emails can be postfixed with the **.eml** extentions.

note: mail.py takes the extract_pst_to_mbox_files.sh output as its input in the current configurations.

### Usage:

```bash
mkdir outputdir/

./extract_pst_to_mbox_files.sh mailbox.pst pst-extracted-output-dir/
```


## mail.py

This script indexes all separated email files from the **--input-dir** value. Each email is parsed. Filtering happens by the **--search-field** and the **--search-value**. When these match, the output is written into the **--output-dir**. In this output dir per e-mail a directory is created. The directory name is the **Date** value parsed from the e-mail and concattenated with a random nummerical value. The matching email and each attachment is placed in this per email output directory.


### Usage:
```bash
#!/bin/bash

./mail.py \
    --search-field From \
    --search-value my@example.com \
    --input-dir pst-extracted-output-dir \
    --output-dir selection_output_dir/
```
