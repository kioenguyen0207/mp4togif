from distutils.command.build_scripts import first_line_re
from flask import Flask, request, jsonify, send_file
from flask_restful import Api, Resource, reqparse
import werkzeug
import os
import glob
from moviepy.editor import *
# from pygifsicle import optimize

FILE_PATH = "temp"

def converter(filename, start, end, scale):
    if(type(start)==str or type(end)==str or type(scale)==str):
        start=float(start)
        end=float(end)
        scale=float(scale)
    if start == -1 or end == -1:
        clip = (VideoFileClip(filename)
            .resize(scale))
    else:
        clip = (VideoFileClip(filename)
        .subclip(start, end)
        .resize(scale))
    clip.write_gif(filename[:-4]+".gif")
    # optimize(filename[:-4]+".gif")


class convert(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', required=True)
            parser.add_argument('start_at', required=True)
            parser.add_argument('end_at', required=True)
            parser.add_argument('scale', required=True)
            args = parser.parse_args()
            uploaded_file = args['file']
            # temp = os.path.join(FILE_PATH, uploaded_file.filename)
            temp = os.path.join(FILE_PATH, "temp.mp4")
            uploaded_file.save(temp)
            converter(temp, args['start_at'], args['end_at'], args['scale'])
            return send_file(temp[0:-4]+".gif")
        except Exception as ex:
            return jsonify({"msg": ex})