from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse,pickle,socket
import config

class GetHandler(BaseHTTPRequestHandler):

        def root_index(self):
                head= [ 
                        '<!DOCTYPE html>',
                        '<head>',
                        '</head>'
                        ]

                body= [
                        '<body>',
                        '<table style="width:100%">',
			'<tr>',
                        '<td><b><h3><center>Hour</center></h3></b></td>',
                        '<td><b><h3>FileName</h3></b></td>',
                        '</tr>'
                        ]
                for Hours,FileName in reversed(self.FileList):
                                body.append('<tr><td><center>'+Hours+'</center></td>')
                                body.append('<td><a href="'+FileName+'">'+FileName+'</a></td></tr>')

		body.append('</table>')
                fotter=['</body>']


                message_parts=head+body+fotter

                message_parts.append('')
                message = '\r\n'.join(message_parts)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(message)
                return

        def search(self,array,txt):
                for f in array:
                        if f[1]==txt:
                                return 1
                return 0

        def send_img(self,path): 
                try:
                        with open(path) as f:
                                message = f.read()
                                self.send_response(200)
                                self.end_headers()
                                self.wfile.write(message)
                except:
                         self.root_index()


    
        def do_GET(self):

                with open('shown.pck','r') as f:
                        self.FileList=pickle.load(f)
                parsed_path = urlparse.urlparse(self.path)
                if parsed_path.path=="/": 
                        self.root_index()
                if self.search (self.FileList,parsed_path.path):
                        self.send_img(parsed_path.path)






if __name__ == '__main__':
        from BaseHTTPServer import HTTPServer
        server = HTTPServer((socket.gethostname(), 8081), GetHandler)
        print 'Starting server, use <Ctrl-C> to stop'
        server.serve_forever()

