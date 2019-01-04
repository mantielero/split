# split
Script to extract two pages from one scanned image

## Usage
We can do:
```bash
find ./ -name "img-???.png" -print | xargs -t -l -I %  ./split.py %
```
It will create files like `img-000_0.png` and `img-000_1.png`.

