from dataclasses import asdict
from markupsafe import escape
from flask import Flask, jsonify, request, abort


import request_esg
import response_esg
import mapper
import uploaddocument
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    return 'Hello, World!'

# Upload ESG for given entity and retrieve all ESG benchmark documents
@app.route('/api/esg/benchmark/upload/<entityName>', methods=['POST'])
def esg_entity_name(entityName):
    file = request.files['documentUpload']
    if not file or file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'File uploaded is not a PDF'}), 400

    uploaddocument.upload_document(file.stream, entityName)

    response_upload = response_esg.UploadRequest()
    response_upload = mapper.map_upload_request(None, entityName)

    return jsonify(asdict(response_upload)), 200

# Fetch specific ESG indicator for given entity
@app.route('/api/esg/benchmark/upload/<entityName>/<esgType>/<esgIndicator>', methods=['POST'])
def esg_upload(entityName, esgType, esgIndicator):
    file = request.files['documentUpload']
    if not file or file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'File uploaded is not a PDF'}), 400

    uploaddocument.upload_document(file.stream, entityName)

    response_upload_type = response_esg.UploadRequestType()
    response_upload_type = mapper.map_upload_request_type(None, entityName)

    return jsonify(asdict(response_upload_type)), 200


# Find status of the benchmarking service
@app.route('/ping', methods=['GET'])
@app.route('/api/esg/benchmark/keepalive', methods=['GET'])
def keep_alive():
    response_keep_alive = response_esg.KeepAliveResponse()
    response_keep_alive.status = 'UP'
    response_keep_alive.message = 'The service is up'

    return jsonify(asdict(response_keep_alive)), 200

# Get PDF URL for given entity name
@app.route('/api/esg/benchmark/pdf-report/<entityName>', methods=['POST'])
def pdf_report(entityName):
    file = request.files['documentUpload']
    if not file or file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'File uploaded is not a PDF'}), 400

    uploaddocument.upload_document(file.stream, entityName)

    response = response_esg.PDFReportResponse()
    response.pdfUrlPath = f"https://storageaimlchallenge.blob.core.windows.net/aimlchallengers/{entityName}.pdf"

    return jsonify(asdict(response)), 200