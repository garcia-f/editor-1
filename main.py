from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import subprocess

app = FastAPI()

class Code(BaseModel):
    code: str

@app.post("/run")
async def run_code(code: Code):
    try:
        output = subprocess.check_output(['python', '-c', code.code], stderr=subprocess.STDOUT, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    return {"output": output}

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    filepath = f"uploaded_{file.filename}"
    with open(filepath, "wb") as f:
        f.write(contents)
    return {"filename": filepath}  # Corregido aquí

@app.get("/", response_class=HTMLResponse)
async def main_page():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Editor de Código</title>
        <link rel="stylesheet" href="https://unpkg.com/monaco-editor@latest/min/vs/editor/editor.main.css">
        <style>
            body {
                background-color: #E6E6FA; /* Fondo lila */
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                height: 100vh;
                overflow: hidden;
            }
            .container {
                display: flex;
                height: 100%;
                flex-direction: row;
            }
            .editor, .output {
                flex: 1;
                padding: 10px;
                box-sizing: border-box;
            }
            .editor {
                border-right: 2px solid #ccc;
                display: flex;
                flex-direction: column;
            }
            .editor-buttons {
                margin-bottom: 10px;
            }
            .output {
                border-left: 2px solid #ccc;
                background-color: #f5f5f5;
                overflow-y: auto;
            }
            #editorContainer {
                height: calc(100% - 50px); /* Ajustar para el espacio de los botones */
            }
            button {
                padding: 10px 20px;
                margin: 0 5px;
                border: none;
                border-radius: 4px;
                background-color: #4CAF50;
                color: white;
                cursor: pointer;
                font-size: 14px;
            }
            button:hover {
                background-color: #45a049;
            }
            pre {
                white-space: pre-wrap; /* Mantener el formato del texto */
            }
        </style>
        <script src="https://unpkg.com/monaco-editor@latest/min/vs/loader.js"></script>
    </head>
    <body>
        <div class="container">
            <div class="editor">
                <div class="editor-buttons">
                    <button onclick="runCode()">Ejecutar</button>
                    <button onclick="uploadFile()">Subir Archivo</button>
                </div>
                <div id="editorContainer"></div>
            </div>
            <div class="output">
                <pre id="output"></pre>
            </div>
        </div>

        <script>
            require.config({ paths: { 'vs': 'https://unpkg.com/monaco-editor@latest/min/vs' }});
            require(['vs/editor/editor.main'], function() {
                const editor = monaco.editor.create(document.getElementById('editorContainer'), {
                    value: '',
                    language: 'python',
                    theme: 'vs-light',
                });

                window.runCode = async function() {
                    const code = editor.getValue();
                    const response = await fetch('/run', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({code: code})
                    });
                    const result = await response.json();
                    document.getElementById('output').textContent = result.output;
                }

                window.uploadFile = async function() {
                    const fileInput = document.createElement('input');
                    fileInput.type = 'file';
                    fileInput.onchange = async (event) => {
                        const file = event.target.files[0];
                        const formData = new FormData();
                        formData.append('file', file);
                        const response = await fetch('/uploadfile/', {
                            method: 'POST',
                            body: formData
                        });
                        const result = await response.json();
                        alert('Archivo subido: ' + result.filename);
                        // Opcional: leer y cargar el archivo en el editor
                        const fileContent = await file.text();
                        editor.setValue(fileContent);
                    };
                    fileInput.click();
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)































# from fastapi import FastAPI, HTTPException, UploadFile, File
# from fastapi.responses import HTMLResponse
# from pydantic import BaseModel
# import subprocess

# app = FastAPI()

# class Code(BaseModel):
#     code: str

# @app.post("/run")
# async def run_code(code: Code):
#     try:
#         output = subprocess.check_output(['python', '-c', code.code], stderr=subprocess.STDOUT, universal_newlines=True)
#     except subprocess.CalledProcessError as e:
#         output = e.output
#     return {"output": output}

# @app.post("/uploadfile/")
# async def upload_file(file: UploadFile = File(...)):
#     contents = await file.read()
#     filepath = f"uploaded_{file.filename}"
#     with open(filepath, "wb") as f:
#         f.write(contents)
#     return {"filename": filepath}

# @app.get("/", response_class=HTMLResponse)
# async def main_page():
#     html_content = """
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>Editor de Código</title>
#         <style>
#             body {
#                 background-color: #E6E6FA; /* Fondo lila */
#                 font-family: Arial, sans-serif;
#                 margin: 0;
#                 padding: 0;
#             }
#             .container {
#                 display: flex;
#                 height: 100vh;
#             }
#             .editor, .output {
#                 padding: 20px;
#                 box-sizing: border-box;
#             }
#             .editor {
#                 flex: 1;
#                 border-right: 2px solid #ccc;
#             }
#             .output {
#                 flex: 1;
#                 border-left: 2px solid #ccc;
#                 background-color: #f5f5f5;
#                 overflow-y: auto;
#             }
#             textarea {
#                 width: 100%;
#                 height: 90%;
#                 box-sizing: border-box;
#                 padding: 10px;
#                 font-family: Courier, monospace;
#                 font-size: 14px;
#                 border: 1px solid #ccc;
#                 border-radius: 4px;
#                 resize: none;
#             }
#             button {
#                 padding: 10px 20px;
#                 margin: 10px;
#                 border: none;
#                 border-radius: 4px;
#                 background-color: #4CAF50;
#                 color: white;
#                 cursor: pointer;
#                 font-size: 14px;
#             }
#             button:hover {
#                 background-color: #45a049;
#             }
#             pre {
#                 white-space: pre-wrap; /* Mantener el formato del texto */
#             }
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <div class="editor">
#                 <textarea id="code" placeholder="Escribe tu código Python aquí..."></textarea><br>
#                 <button onclick="runCode()">Ejecutar</button>
#                 <button onclick="uploadFile()">Subir Archivo</button>
#             </div>
#             <div class="output">
#                 <pre id="output"></pre>
#             </div>
#         </div>

#         <script>
#             async function runCode() {
#                 const code = document.getElementById('code').value;
#                 const response = await fetch('/run', {
#                     method: 'POST',
#                     headers: {'Content-Type': 'application/json'},
#                     body: JSON.stringify({code: code})
#                 });
#                 const result = await response.json();
#                 document.getElementById('output').textContent = result.output;
#             }

#             async function uploadFile() {
#                 const fileInput = document.createElement('input');
#                 fileInput.type = 'file';
#                 fileInput.onchange = async (event) => {
#                     const file = event.target.files[0];
#                     const formData = new FormData();
#                     formData.append('file', file);
#                     const response = await fetch('/uploadfile/', {
#                         method: 'POST',
#                         body: formData
#                     });
#                     const result = await response.json();
#                     alert('Archivo subido: ' + result.filename);
#                 };
#                 fileInput.click();
#             }
#         </script>
#     </body>
#     </html>
#     """
#     return HTMLResponse(content=html_content)




























# from fastapi import FastAPI, HTTPException, UploadFile, File
# from fastapi.responses import HTMLResponse
# from pydantic import BaseModel
# import subprocess
# import os

# app = FastAPI()

# class Code(BaseModel):
#     code: str

# @app.post("/run")
# async def run_code(code: Code):
#     try:
#         output = subprocess.check_output(['python', '-c', code.code], stderr=subprocess.STDOUT, universal_newlines=True)
#     except subprocess.CalledProcessError as e:
#         output = e.output
#     return {"output": output}

# @app.post("/uploadfile/")
# async def upload_file(file: UploadFile = File(...)):
#     contents = await file.read()
#     filepath = f"uploaded_{file.filename}"
#     with open(filepath, "wb") as f:
#         f.write(contents)
#     return {"filename": filepath}

# @app.get("/", response_class=HTMLResponse)
# async def main_page():
#     html_content = """
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>Editor de Código</title>
#     </head>
#     <body>
#         <textarea id="code" rows="10" cols="30"></textarea><br>
#         <button onclick="runCode()">Ejecutar</button>
#         <button onclick="uploadFile()">Subir Archivo</button><br>
#         <pre id="output"></pre>

#         <script>
#             async function runCode() {
#                 const code = document.getElementById('code').value;
#                 const response = await fetch('/run', {
#                     method: 'POST',
#                     headers: {'Content-Type': 'application/json'},
#                     body: JSON.stringify({code: code})
#                 });
#                 const result = await response.json();
#                 document.getElementById('output').textContent = result.output;
#             }

#             async function uploadFile() {
#                 const fileInput = document.createElement('input');
#                 fileInput.type = 'file';
#                 fileInput.onchange = async (event) => {
#                     const file = event.target.files[0];
#                     const formData = new FormData();
#                     formData.append('file', file);
#                     const response = await fetch('/uploadfile/', {
#                         method: 'POST',
#                         body: formData
#                     });
#                     const result = await response.json();
#                     alert('Archivo subido: ' + result.filename);
#                 };
#                 fileInput.click();
#             }
#         </script>
#     </body>
#     </html>
#     """
#     return HTMLResponse(content=html_content)
