import json
import math
from crypt import methods
from urllib.parse import parse_qs

from odoo import http
from odoo.http import request


def valid_response(data, status, pagenation_info):
    response_body={
        'message': "successfully",
        "data": data
    }
    if pagenation_info:
        response_body['pagenation_info']=pagenation_info
    return request.make_json_response(response_body, status=status)

def invalid_response(error, status):
    response_body={
        'message': "failed",
        "error": error
    }
    return request.make_json_response(response_body, status=status)
class PropertyApi(http.Controller):
    @http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        print(self)
        args=request.httprequest.data.decode()
        print(args)

        vals=json.loads(args)
        print(vals)
        if not vals.get('name'):
            return request.make_json_response({
                'message': 'name is required'
            }, status=400)


        try:
            res = request.env['property'].sudo().create(vals)
            if res:
                return request.make_json_response({
                    'message': 'the prop has been made successfully'
                    }, status=200)
        except Exception as error:
            return request.make_json_response({
                    'message': error
                    }, status=400)


    @http.route("/v1/property/json", methods=["POST"], type='json', auth='none', csrf=False)
    def post_property_json(self):
        args=request.httprequest.data.decode()
        vals=json.loads(args)
        res = request.env['property'].sudo().create(vals)
        if res:
            return {
                'message': 'the prop has been made successfully'
            }



    @http.route("/v1/property/<int:property_id>", methods=['PUT'], type='http', auth='none', csrf=False)
    def update_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([("id", "=", property_id)])
            if not property_id:
                return request.make_json_response({
                    "message": "Id does not match",
                }, status=400)
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            property_id.write(vals)
            return request.make_json_response({
                "message": "Property has been updated",
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "message": error
            }, status=400)

    @http.route("/v1/property/<int:property_id>", methods=['GET'], type='http', auth='none', csrf=False)
    def get_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([("id", "=", property_id)])
            if not property_id:
                return request.make_json_response({
                    "message": "Id does not match",
                }, status=400)

            return valid_response({
                "message": "Property items:",
                "name": property_id.name,
                "id": property_id.id,
            }, status=200)
        except Exception as error:
            return invalid_response({
                "message": error
            }, status=400)
    @http.route("/v1/property/<int:property_id>", methods=['DELETE'], type='http', auth='none', csrf=False)
    def delete_property(self, property_id):
        property_id=request.env['property'].sudo().search([('id', '=', property_id)])
        try:
            if not property_id:
                return request.make_json_response({
                    "message":"id does not match",
                }, status=400)
            property_id.unlink()
            return request.make_json_response({
                "message":"prop deleted",
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "message": error,
            }, status=400)

    @http.route("/v1/properties", methods=['GET'], type='http', auth='none', csrf=False)
    def get_properties(self):
        try:
            params= parse_qs(request.httprequest.query_string.decode('utf-8'))
            property_domain=[]
            page = offset = None
            limit = 5
            if params:
                if params.get('limit'):
                    limit = int(params.get('limit')[0])
                if params.get('page'):
                    page= int(params.get('page')[0])
            if page:
                offset=(page*limit)-limit
            if params.get('state'):
                property_domain+=[('state', '=', params.get('state'[0]))]
            property_ids= request.env['property'].sudo().search(property_domain, offset=offset, limit=limit, order="id desc")
            property_count = request.env['property'].sudo().search_count(property_domain)
            if not property_ids:
                return request.make_json_response({
                    "message": "No props",
                }, status=400)

            return valid_response([{
                "message": "Property items:",
                "name": property_id.name,
                "id": property_id.id,
            } for property_id in property_ids],
            pagenation_info ={
                'page': page if page else 1,
                'limit': limit,
                'pages': math.ceil(property_count/limit) if limit else 1,
                'count': property_count,
            }, status=200)
        except Exception as error:
            return invalid_response({
                "message": error
            }, status=400)