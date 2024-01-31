import http.server
from pathlib import Path
import traceback
import http.cookies
import os
import urllib
from importlib import reload

SAVED_STATE = {}


def multipart_parse(boundary_info, post_data):
    boundary = boundary_info[boundary_info.find("boundary=") + len("boundary="):].encode() + b""
    parsed_post_list = [val[val.find(b';') + 1:].split(b'\r\n\r\n', 1) for val in post_data.split(boundary) if
                        b"content-disposition" in val.lower()]
    parsed_post_list = [(header.strip().rsplit(b'\r\n', 1)[0].split(b';'),
                         header.strip().rsplit(b'\r\n', 1)[1] if b'\r\n' in header else None,
                         data.rsplit(b'\r\n', 1)[0]) for header, data in parsed_post_list]
    parsed_post_dict = {}
    for headers, additional_headers, data in parsed_post_list:
        header_dict = {}
        if additional_headers is not None:
            additional_headers = additional_headers.split(b':')
            for i in range(len(additional_headers)):
                if i + 1 == len(additional_headers):
                    break
                header_dict[additional_headers[i].lower()] = additional_headers[i + 1]

        for var in headers:
            var_name, var_val = var.split(b'=')
            header_dict[var_name.strip()] = var_val[1:-1]
        if b"name" in header_dict.keys():
            if header_dict[b"name"] not in parsed_post_dict.keys():
                parsed_post_dict[header_dict[b'name']] = []
            parsed_post_dict[header_dict[b'name']].append((header_dict, data))
    return parsed_post_dict


class SendBinary(object):
    def __init__(self, set_content, set_filename):
        self.bin_data = None
        self.set_content = set_content
        self.set_filename = set_filename

    def __call__(self, bin_data, content_type=None, filename=None):
        self.bin_data = bin_data
        if content_type is not None:
            self.set_content(content_type)
        if filename is not None:
            self.set_filename(filename)

    def result(self):
        if self.bin_data is None:
            return (False, b'')
        return (True, self.bin_data)


class SetCookie(object):
    def __init__(self):
        self.cookie_vals = http.cookies.SimpleCookie()

    def __call__(self, name, val, attributes=None):
        self.cookie_vals[name] = val
        if attributes is not None:
            for attr_name in ["expires", "path", "comment", "domain", "max-age", 'secure', 'version', 'httponly',
                              'samesite']:
                if attr_name in attributes.keys():
                    self.cookie_vals[name][attr_name] = attributes[attr_name]

    def result(self):
        return self.cookie_vals


class SetContentType(object):
    def __init__(self):
        self.content_type = 'text/html'

    def __call__(self, content_type):
        self.content_type = content_type

    def result(self):
        return self.content_type


class SetFilename(object):
    def __init__(self):
        self.filename = None

    def __call__(self, filename):
        self.filename = filename

    def result(self):
        return self.filename


class AddHTML(object):
    def __init__(self):
        self._new_html = ""

    def __call__(self, html_to_add):
        self._new_html += html_to_add

    def result(self):
        return self._new_html


CONTENT_MAP = {
    'html': 'text/html',
    'htm': 'text/html',
    'gz': 'application/gzip',
    'gif': 'image/gif',
    'png': 'image/png',
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpeg',
    'ico': 'image/vnd/microsoft.icon',
    'css': 'text/css',
}


def suffix_to_content_type(suffix: str):
    ext = suffix[1:]  # strip off the period
    if ext not in CONTENT_MAP.keys():
        return 'text/html'
    return CONTENT_MAP[ext]


class DemoWWWHandler(http.server.BaseHTTPRequestHandler):
    def respond(self, returnBytes: bytes, content_type='text/html', cookie: http.cookies.SimpleCookie = None,
                filename=None):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        if filename is not None:
            self.send_header('Content-Disposition', f'attachment; filename="{filename.decode()}"')
        if cookie is not None and len(cookie) > 0:
            for morsel in cookie.values():
                self.send_header('Set-Cookie', morsel.output(header=""))
        self.end_headers()
        self.wfile.write(returnBytes)

    def respond_error(self, error_msg: str = "file not found", error_code=404):
        self.send_response(404, error_msg)
        self.wfile.write(f"{error_code} - {error_msg}".encode())

    def parse_get(self, file_data, QUERY_STRING, QUERY_VARS, POST_DATA={}):
        self.dynamicStack = []
        set_cookie = SetCookie()
        get_client_addr = lambda: self.client_address
        _COOKIE = {}
        for key, val in http.cookies.SimpleCookie(self.headers.get('Cookie')).items():
            _COOKIE[key] = val.value
        get_cookie = lambda: _COOKIE
        set_content_type = SetContentType()
        set_filename = SetFilename()
        send_binary = SendBinary(set_content_type, set_filename)
        file_data_result = ''
        while (tag_loc := file_data.find('<%')) != -1:
            before = file_data[:tag_loc]
            file_data = file_data[tag_loc + 2:]
            eval_tag = True if file_data[0] == '%' else False
            add_html = AddHTML()

            if eval_tag:
                file_data = file_data[1:]
                end_tag_loc = file_data.find('%%>')
                after = file_data[end_tag_loc + 3:]
                before += str(eval(file_data[:end_tag_loc].strip()))
            else:
                end_tag_loc = file_data.find('%>')
                if end_tag_loc == -1:
                    after = ''
                    exec(file_data.strip())
                else:
                    after = file_data[end_tag_loc + 2:]
                    exec(file_data[:end_tag_loc].strip())

                is_binary, bin_data = send_binary.result()
                if is_binary:
                    return bin_data, set_content_type.result(), set_cookie.result(), set_filename.result()
            file_data_result = "".join((file_data_result, before, add_html.result()))
            file_data = after

        return (
                       file_data_result + file_data).encode(), set_content_type.result(), set_cookie.result(), set_filename.result()

    def parse_post(self, file_data, QUERY_STRING, QUERY_VARS):
        content_type = self.headers.get("content-type")
        post_data = self.rfile.read(int(self.headers.get('content-length')))

        if content_type == "application/x-www-form-urlencoded":
            post_data = urllib.parse.parse_qs(post_data)
        else:
            multipart = "multipart/form-data"
            if content_type[:len(multipart)] == multipart:
                post_data = multipart_parse(content_type[len(multipart):], post_data)
            else:
                raise Exception(
                    "unsupported post content-type, only application/x-www-form-urlencoded and multipart/form-data are supported")
        return self.parse_get(file_data, QUERY_STRING, QUERY_VARS, post_data)

    def do_GET(self):
        self.do_ACTION(self.parse_get)

    def do_POST(self):
        self.do_ACTION(self.parse_post)

    def do_ACTION(self, parse_action):
        global COOKIE
        purl = urllib.parse.urlparse(self.requestline.split()[1])
        QUERY_STRING = purl.query
        QUERY_VARS = urllib.parse.parse_qs(purl.query)
        path_portion = purl.path

        if path_portion == '/':
            resourceLoc = Path('./html/index.html')
        else:
            try:
                resourceLoc = Path(path_portion)
                if resourceLoc.is_absolute():
                    resourceLoc = resourceLoc.relative_to('/')
                resourceLoc = Path('./html') / resourceLoc.resolve().relative_to(os.getcwd())
            except:
                self.respond_error()
                return

        if resourceLoc.exists() == False:
            self.respond_error()
        else:
            try:
                suffix = resourceLoc.suffix
                if suffix in ['.html', '.htm']:
                    bin_response, content_type, cookie, filename = parse_action(open(resourceLoc, 'rb').read().decode(),
                                                                                QUERY_STRING, QUERY_VARS)
                    self.respond(bin_response, content_type, cookie=cookie, filename=filename)
                else:
                    self.respond(open(resourceLoc, 'rb').read(), suffix_to_content_type(suffix))
            except Exception as e:
                print(f"couldn't serve file: {resourceLoc} exception:{e}")
                traceback.print_exc()
                self.respond_error(str(e), 500)


if __name__ == "__main__":
    http.server.HTTPServer(('', 8080), DemoWWWHandler).serve_forever()
