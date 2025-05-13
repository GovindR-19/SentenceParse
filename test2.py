import web
import nltk
from nltk import pos_tag, word_tokenize, ne_chunk

# Make sure necessary NLTK models are downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

urls = ("/", "Index")
app = web.application(urls, globals())

render_style = """
<style>
    body {
        font-family: sans-serif;
        margin: 20px;
    }

    form {
        margin-bottom: 20px;
    }

    .tree ul {
        padding-top: 10px;
        position: relative;
        display: block;
        transition: all 0.5s;
    }

    .tree li {
        list-style-type: none;
        margin: 0;
        padding: 10px 5px 0 5px;
        position: relative;
    }

    .tree li::before {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        border-left: 1px solid #ccc;
        height: 100%;
        width: 0;
    }

    .tree li::after {
        content: '';
        position: absolute;
        top: 10px;
        left: 50%;
        border-top: 1px solid #ccc;
        width: 50%;
        height: 0;
    }

    .tree li:only-child::before,
    .tree li:only-child::after {
        display: none;
    }

    .tree li:first-child::after {
        border-left: 1px solid #ccc;
        border-radius: 0 0 0 5px;
        width: 50%;
        left: 50%;
    }

    .tree li:last-child::after {
        border-right: 1px solid #ccc;
        border-radius: 0 0 5px 0;
        width: 50%;
        left: 0%;
    }

    .tree li strong {
        display: inline-block;
        background: #2a6ebb;
        color: white;
        padding: 3px 6px;
        border-radius: 5px;
    }

    .tree li em {
        margin-left: 5px;
        color: #555;
    }
</style>
"""

def tree_to_html(tree):
    if hasattr(tree, 'label') and tree.label:
        return f"<li><strong>{tree.label()}</strong><ul>{''.join(tree_to_html(child) for child in tree)}</ul></li>"
    else:
        word, tag = tree
        return f"<li><strong>{word}</strong> <em>{tag}</em></li>"

class Index:
    def GET(self):
        return render_style + """
            <h1>Sentence Parser</h1>
            <form method="POST">
                <textarea name="sentence" rows="4" cols="60" placeholder="Enter a sentence...">To bait fish withal; if it will feed nothing else, it will feed my revenge.</textarea><br>
                <input type="submit" value="Parse">
            </form>
        """

    def POST(self):
        data = web.input()
        text = data.sentence

        tokens = word_tokenize(text)
        tags = pos_tag(tokens)
        tree = ne_chunk(tags)

        html_tree = tree_to_html(tree)
        return render_style + f"""
            <h1>Sentence Parser</h1>
            <form method="POST">
                <textarea name="sentence" rows="4" cols="60">{text}</textarea><br>
                <input type="submit" value="Parse">
            </form>
            <h2>Parsed Tree</h2>
            <div class="tree">
                <ul><li>{html_tree}</li></ul>
            </div>
        """

if __name__ == "__main__":
    app.run()

