import web
from parser import getChunks
from vis import build_visjs_data

urls = ("/", "Index")
app = web.application(urls, globals())

form_html = ''' <h2>Sentence Parser</h2>
            <form method="POST">
                <textarea name="sentence" rows="4"></textarea><br>
                <input type="submit" value="Parse">
            </form>'''

style = '''<style>
                ul {
                    list-style-type: none;
                    padding-left: 20px;
                }

                li {
                    margin: 4px 0;
                    font-family: sans-serif;
                    font-size: 14px;
                }
            /* li::before {
                    content: "• ";
                    color: #3498db;  /* blue bullet */
                } */
                li > ul {
                    margin-left: 15px;
                    border-left: 2px solid #ccc;
                    padding-left: 10px;
                }

                li > ul > li {
                    color: #2c3e50;
                }

            /* li > ul > li::before {
                    content: "↳ ";
                    color: #95a5a6;  /* gray pointer */
                } */

                body {
                    padding: 20px;
                }
            </style>
'''

link = ''' <link href="https://unpkg.com/vis-network/styles/vis-network.min.css" rel="stylesheet" type="text/css" />
            <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        '''

def getResult(result):
    output = '''<div id="syntaxTree" style="width: 100%; height: 500px; border: 1px solid lightgray;">'''
    output += "<ul>"
    for label, token in result:
        output += f"<li>{label}<ul>"
        for word, tags in token:
            output+= f"<li>{tags}</li> <ul><li>{word}"
            output += "</li></ul></ul>"
    output += "</ul></div>"
    return output

class Index:
    def GET(self):
        web.header('Content-type', 'text/html')
        return form_html
    
    def POST(self):
        web.header('Content-type', 'text/html')
        try:
            data = web.input()
            sentence = data.get('sentence', '').strip()
            result = getChunks(sentence)

            # Build the JSON data for vis.js
            vis_json = build_visjs_data(result)

            # Optionally, you can use the getResult function for the text-based tree view
            htmlOutput = getResult(result)

            # Return the combined HTML with the vis.js visualization
            return style + link + form_html  + '''
                <div id="network" style="width: 100%; height: 500px; border: 1px solid lightgray;"></div>
                <script type="text/javascript">
                    var data = ''' + vis_json + ''';

                    var container = document.getElementById('network');
                    var options = {
                        nodes: {
                            shape: 'box',
                            color: '#97C2FC',
                            font: { color: '#343434' }
                        },
                        layout: {
                            hierarchical: {
                                direction: 'UD',
                                sortMethod: 'directed'
                            }
                        },
                        edges: {
                            arrows: { to: { enabled: false } }
                        }
                    };

                    var network = new vis.Network(container, data, options);
                </script>
            '''
        except Exception as e:
            return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    app.run()
