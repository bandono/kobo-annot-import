With [Kobo e-Reader](https://en.wikipedia.org/wiki/Kobo_eReader) we can highlight [EPUB](https://en.wikipedia.org/wiki/EPUB) book as annotation that will be kept in the reader storage as XML files.

This Python script uses combination of `find`,`rsync`, and `grep` to extract the annotations and save them as individual [Markdown](https://en.wikipedia.org/wiki/Markdown) file using the annotation text (in my case as sort of title) for naming.

I'm using Mac OSX so, plugging my [Kobo Clara HD](https://gl.kobobooks.com/products/kobo-clara-hd) will mount it to `/Volumes/KOBOeReader`. I use one line where:

1. I change dir to the e-Reader (`cd`)
2. `find` annotation files
3. Compare those files whether they are newer or the same with the ones kept on my laptop
4. Copy only newer files to my laptop (`rsync`)
5. Pipe the list of these newer files for processing the XML into individual markdown files


```cd /Volumes/KOBOeReader && find ./ -name "*.annot" -type f -print0 2>/dev/null | rsync -av --files-from=- --from0 --no-relative /Volumes/KOBOeReader <directory where I keep my XML files on my laptop> | grep annot | /<pyenv-version>/python kobo-annot-import.py```

In the Python script I still initiate folder for XML and markdown files.


```
# Define annotation folder
annot_folder = '' # replace with annotation local folder
# Define result folder root
folder_name = 'result' # replace with target folder
```

It will check whether same markdown with the name `Some-Annotation-Text-as-Title-example.md` exists and prevent from overwriting it, assuming the one on the laptop has already been modified. It will then append to `Some-Annotation-Text-as-Title-example (1).md` if content doesn't match newer annotation.


This is a *work in progress*. Always backup properly if not sure on result.