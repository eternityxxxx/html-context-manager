
class HTML:
    def __init__(self, output = None):
        self.output = output
        self.childrens = []

    def __enter__(self):
        return self

    def __add__(self, other):
        self.childrens.append(other)
        return self

    def __exit__(self, *args):
        if self.output is None:
            print("<html>")

            for child in self.childrens:
                print(str(child))

            print("</html>")
        else:
            with open(self.output, "w") as f:
                f.write("<html>\n")

                for child in self.childrens:
                    f.write(str(child) + "\n")

                f.write("</html>\n")

class TopLevelTag:
    def __init__(self, tag):
        self.tag = tag
        self.childrens = []

    def __enter__(self):
        return self

    def __add__(self, other):
        self.childrens.append(other)
        return self

    def __str__(self):
        starting = "\t" + "<{tag}>".format(tag = self.tag)
        internal = ""

        for child in self.childrens:
            internal += "\n" + "\t" + "\t" + str(child)
        ending = "\n" + "\t" + "</{tag}>".format(tag = self.tag)

        return starting + internal + ending

    def __exit__(self, *attrs):
        return self

class Tag:
    def __init__(self, tag, is_single = False, klass = None, **kwargs):
        self.tag = tag
        self.text = ""

        self.is_single = is_single
        self.attributes = {}


        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for key, value in kwargs.items():
            if "_" in key:
                key = key.replace("_", "-")
            self.attributes[key] = value

    def __enter__(self):
        return self

    def __exit__(self, *atrs):
        return self

    def __str__(self):
        attrs = []
        for key, value in self.attributes.items():
            attrs.append('%s="%s"' % (key, value))

        attr_string = " ".join(attrs)

        if self.is_single and self.attributes:
            return "<{tag} {attrs}/>".format(tag = self.tag, attrs = attr_string)
        elif self.is_single and not self.attributes:
            return "<{tag}/>".format(tag = self.tag)
        elif not self.is_single and self.attributes:
            return "<{tag} {attrs}>{text}</{tag}>".format(tag = self.tag, attrs = attr_string, text = self.text)
        else:
            return "<{tag}>{text}</{tag}>".format(tag = self.tag, text = self.text)

with HTML(output="test.html") as doc:
    with TopLevelTag("head") as head:
        with Tag("title") as title:
            title.text = "hello"
            head += title
        doc += head

    with TopLevelTag("body") as body:
        with Tag("h1", klass=("main-text",)) as h1:
            h1.text = "Test"
            body += h1

        with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
            body += div

        with Tag("p") as paragraph:
            paragraph.text = "another test"
            body += paragraph

        with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
            body += img

        doc += body
