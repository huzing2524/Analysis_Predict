# -*- coding: utf-8 -*-
import jwt
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from analysis.retrieve_hzy import main
from analysis.retrieve_jcj import get_factory_id, run


class Analysis(APIView):
    """V2.4.0 分析功能 /api/v2/analysis"""

    def get(self, request):
        result = {}

        token = request.META.get("HTTP_AUTHORIZATION") or None
        # print(request.META.items())
        if token:
            try:
                user_dict = jwt.decode(token, verify=False)
                # print("user_dict=", user_dict)
            except Exception:
                return Response({"msg": "jwt token parse error"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                user_phone = user_dict["username"]
                # print("user_phone=", user_phone)
                factory_id = get_factory_id(user_phone)
                # print("factory_id=", factory_id)
            if factory_id:
                try:
                    # ------市场部------------财务部------------采购部------
                    jcj = run(factory_id)
                    print('jjj', jcj)
                    result.update(jcj)

                    # ------仓库部------------生产部------
                    hzy = main(factory_id)
                    result.update(hzy)

                    print('res', result)

                    return Response(result, status=status.HTTP_200_OK)
                except Exception:
                    return Response({"msg": "Analysis data query occurred exception."},
                                    status=status.HTTP_503_SERVICE_UNAVAILABLE)
            else:
                return Response(result, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"msg": "lack of jwt token"}, status=status.HTTP_401_UNAUTHORIZED)
