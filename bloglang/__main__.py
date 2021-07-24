import rich

from bloglang import parser

if __name__ == "__main__":
    doc = R"""\
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6

*italic*, **bold**, and ***both***. ~~Strikethrough~~ and __underline__ are also supported.

:quote:
    some quote
:quote:
    :quote:
        :quote:
            infinitely nested quotes

[link](https://example.org) with title [not a rickroll](https://www.youtube.com/watch?v=dQw4w9WgXcQ "title").

[Jump!](#jump-to)#jump-from

[hello!](#jump-from)#jump-to


Footnote[^1]
![Image alt text](url/to/image.png "image caption\"")
[^1]: Guaranteed to have a jump-back link
"""
    rich.print(parser.parse(doc))
