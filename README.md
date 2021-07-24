**NOTE:** BlogLang is not completed for proper use. I've only made this repo available because @Cutewarriorlover wanted to see it :p

# BlogLang

> A parser for bloglang

## What is BlogLang?

BlogLang, a.k.a. BlogLang, is a markup language syntactically similar to Markdown. It feels like markdown, with the extendibility of reStructuredText.

It is designed for writing blogs, tutorials, and informal articles with ease.

Here's is an example of the current document, up to this point, in BlogLang:

```markdown
# BlogLang

:quote:
    A parser for bloglang

## What is BlogLang?

BlogLang, a.k.a. BlogLang, is a markup language syntactically similar to Markdown. It feels like markdown, with the extendibility of reStructuredText.

It is designed for writing blogs, tutorials, and informal articles with ease.
```

The file extension is `.blog`. It has a less complicated spec than Markdown. You see that `:quote:`, RST-like, thing? It is called a *specdent*. Single line *specdents* are called *specs*.

## Features

 - The normal markdown stuff (headings, italics, etc)
 - Links with built-in syntax for IDs
 - Images with built-in syntax for captions (rich captions todo)
 - Extendible "specs" and "specdents"
