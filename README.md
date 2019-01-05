# Processing scanned documents
Script to extract two pages from one scanned image

## Splitting two pages in one image
We can do:
```bash
find ./ -name "img-???.png" -print | xargs -t -l -I %  ./split.py %
```
It will create files like `img-000_0.png` and `img-000_1.png`.

> `-t`: displays the line being run
> `-l`: executing every single line from `find` as a new command
> `-I %`: it will use `%` for the representation of the parameter coming from `find`

## Deskweing a single page
We will do something like:
```bash
find ./ -name "img-???_?.png" -print | xargs -t -l ./deskew.py
```
