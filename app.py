
form_html = ''' <h1>Sentence Parser</h1>
            <form method="POST">
                <textarea id="text_box" name="sentence" rows="4"></textarea><br>
                <br>
                <input  id="button" type="submit" value="Parse">
            </form>'''

style = '''
                <style>
                ul 
                {
                    list-style-type: none;
                    padding-left: 20px;
                }

                li 
                {
                    margin: 4px 0;
                    font-family: sans-serif;
                    font-size: 14px;
                }

                li > ul {
                    margin-left: 15px;
                    border-left: 2px solid #ccc;
                    padding-left: 10px;
                }

                li > ul > li {
                    color: #2c3e50;
                }


                body {
                    display: flex;
                    align-items: center;
                    flex-direction: column;
                    padding: 20px;
                }

                #text_box
                {
                    font-size: 1.5rem;
                    width: 500px;
                    height: 250px;
                    border: 1px solid black;
                    border-radius: 5px;
                }
                
                #button
                {
                    width: 100px;
                    heigh: 100px;
                    font-size: 16px;
                }
                </style>
'''

link = ''' <link href="https://unpkg.com/vis-network/styles/vis-network.min.css" rel="stylesheet" type="text/css" />
            <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        '''










import web
from parser import getChunks
from vis import vis_tree

urls = ( "/", "Index")
app = web.application(urls, globals())




## Building the UL LI tag tree for vis.py
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
        return style + link + form_html
    
    def POST(self):
        web.header('Content-type', 'text/html')
        try:
            ## Capturing the input from user 
            data = web.input()
            sentence = data.get('sentence', '').strip()
            result = getChunks(sentence)

            ## Preparing the JSON data for vis.js
            vis_json = vis_tree(result)

            # Optional ouptut to console
            htmlOutput = getResult(result)

            # Return the combined HTML with the vis.js visualization
            return style + link + form_html  + '''
                <div id="network" style="width: 80%; height: 500px; border: 1px solid lightgray;"></div>
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
