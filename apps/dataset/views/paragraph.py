# coding=utf-8
"""
    @project: maxkb
    @Author：虎
    @file： paragraph_serializers.py
    @date：2023/10/16 15:51
    @desc:
"""
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.views import Request

from common.auth import TokenAuth, has_permissions
from common.constants.permission_constants import Permission, Group, Operate, CompareConstants
from common.log.log import log
from common.response import result
from common.util.common import query_params_to_single_dict
from dataset.serializers.common_serializers import BatchSerializer
from dataset.serializers.paragraph_serializers import ParagraphSerializers
from django.utils.translation import gettext_lazy as _


class Paragraph(APIView):
    authentication_classes = [TokenAuth]

    @action(methods=['GET'], detail=False)
    @swagger_auto_schema(operation_summary=_('Paragraph list'),
                         operation_id=_('Paragraph list'),
                         manual_parameters=ParagraphSerializers.Query.get_request_params_api(),
                         responses=result.get_api_array_response(ParagraphSerializers.Query.get_response_body_api()),
                         tags=[_('Knowledge Base/Documentation/Paragraph')]
                         )
    @has_permissions(
        lambda r, k: Permission(group=Group.DATASET, operate=Operate.USE,
                                dynamic_tag=k.get('dataset_id')))
    @log(menu=_('Knowledge Base/Documentation/Paragraph'), operate=_('Paragraph list'))
    def get(self, request: Request, dataset_id: str, document_id: str):
        q = ParagraphSerializers.Query(
            data={**query_params_to_single_dict(request.query_params), 'dataset_id': dataset_id,
                  'document_id': document_id})
        q.is_valid(raise_exception=True)
        return result.success(q.list())

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(operation_summary=_('Create Paragraph'),
                         operation_id=_('Create Paragraph'),
                         manual_parameters=ParagraphSerializers.Create.get_request_params_api(),
                         request_body=ParagraphSerializers.Create.get_request_body_api(),
                         responses=result.get_api_response(ParagraphSerializers.Query.get_response_body_api()),
                         tags=[_('Knowledge Base/Documentation/Paragraph')])
    @has_permissions(
        lambda r, k: Permission(group=Group.DATASET, operate=Operate.MANAGE,
                                dynamic_tag=k.get('dataset_id')))
    @log(menu=_('Knowledge Base/Documentation/Paragraph'), operate=_('Create Paragraph'))
    def post(self, request: Request, dataset_id: str, document_id: str):
        return result.success(
            ParagraphSerializers.Create(data={'dataset_id': dataset_id, 'document_id': document_id}).save(request.data))

    class Problem(APIView):
        authentication_classes = [TokenAuth]

        @action(methods=['POST'], detail=False)
        @swagger_auto_schema(operation_summary=_('Add associated questions'),
                             operation_id=_('Add associated questions'),
                             manual_parameters=ParagraphSerializers.Problem.get_request_params_api(),
                             request_body=ParagraphSerializers.Problem.get_request_body_api(),
                             responses=result.get_api_response(ParagraphSerializers.Problem.get_response_body_api()),
                             tags=[_('Knowledge Base/Documentation/Paragraph')])
        @has_permissions(
            lambda r, k: Permission(group=Group.DATASET, operate=Operate.MANAGE,
                                    dynamic_tag=k.get('dataset_id')))
        @log(menu=_('Knowledge Base/Documentation/Paragraph'), operate=_('Add associated questions'))
        def post(self, request: Request, dataset_id: str, document_id: str, paragraph_id: str):
            return result.success(ParagraphSerializers.Problem(
                data={"dataset_id": dataset_id, 'document_id': document_id, 'paragraph_id': paragraph_id}).save(
                request.data, with_valid=True))

        @action(methods=['GET'], detail=False)
        @swagger_auto_schema(operation_summary=_('Get a list of paragraph questions'),
                             operation_id=_('Get a list of paragraph questions'),
                             manual_parameters=ParagraphSerializers.Problem.get_request_params_api(),
                             responses=result.get_api_array_response(
                                 ParagraphSerializers.Problem.get_response_body_api()),
                             tags=[_('Knowledge Base/Documentation/Paragraph')])
        @has_permissions(
            lambda r, k: Permission(group=Group.DATASET, operate=Operate.USE,
                                    dynamic_tag=k.get('dataset_id')))
        @log(menu=_('Knowledge Base/Documentation/Paragraph'), operate=_('Get a list of paragraph questions'))
        def get(self, request: Request, dataset_id: str, document_id: str, paragraph_id: str):
            return result.success(ParagraphSerializers.Problem(
                data={"dataset_id": dataset_id, 'document_id': document_id, 'paragraph_id': paragraph_id}).list(
                with_valid=True))

        class UnAssociation(APIView):
            authentication_classes = [TokenAuth]

            @action(methods=['PUT'], detail=False)
            @swagger_auto_schema(operation_summary=_('Disassociation issue'),
                                 operation_id=_('Disassociation issue'),
                                 manual_parameters=ParagraphSerializers.Association.get_request_params_api(),
                                 responses=result.get_default_response(),
                                 tags=[_('Knowledge Base/Documentation/Paragraph')])
            @has_permissions(
                lambda r, k: Permission(group=Group.DATASET, operate=Operate.MANAGE,
                                        dynamic_tag=k.get('dataset_id')))
            @log(menu=_('Knowledge Base/Documentation/Paragraph'), operate=_('Disassociation issue'))
            def put(self, request: Request, dataset_id: str, document_id: str, paragraph_id: str, problem_id: str):
                return result.success(ParagraphSerializers.Association(
                    data={'dataset_id': dataset_id, 'document_id': document_id, 'paragraph_id': paragraph_id,
                          'problem_id': problem_id}).un_association())

        class Association(APIView):
            authentication_classes = [TokenAuth]

            @action(methods=['PUT'], detail=False)
            @swagger_auto_schema(operation_summary=_('Related questions'),
                                 operation_id=_('Related questions'),
                                 manual_parameters=ParagraphSerializers.Association.get_request_params_api(),
                                 responses=result.get_default_response(),
                                 tags=[_('Knowledge Base/Documentation/Paragraph')])
            @has_permissions(
                lambda r, k: Permission(group=Group.DATASET, operate=Operate.MANAGE,
                                        dynamic_tag=k.get('dataset_id')))
            @log(menu=_('Knowledge Base/Documentation/Paragraph'), operate=_('Related questions'))
            def put(self, request: Request, dataset_id: str, document_id: str, paragraph_id: str, problem_id: str):
                return result.success(ParagraphSerializers.Association(
                    data={'dataset_id': dataset_id, 'document_id': document_id, 'paragraph_id': paragraph_id,
                          'problem_id': problem_id}).association())

    class Operate(APIView):
        authentication_classes = [TokenAuth]

        @action(methods=['UPDATE'], detail=False)
        @swagger_auto_schema(operation_summary=_('Modify paragraph data'),
                             operation_id=_('Modify paragraph data'),
                             manual_parameters=ParagraphSerializers.Operate.get_request_params_api(),
                             request_body=ParagraphSerializers.Operate.get_request_body_api(),
                             responses=result.get_api_response(ParagraphSerializers.Operate.get_response_body_api())
            , tags=[_('Knowledge Base/Documentation/Paragraph')])
        @has_permissions(
            lambda r, k: Permission(group=Group.DATASET, operate=Operate.MANAGE,
                                    dynamic_tag=k.get('dataset_id')))
        @log(menu=_('Knowledge Base/Documentation/Paragraph'), operate=_('Modify paragraph data'))
        def put(self, request: Request, dataset_id: str, document_id: str, paragraph_id: str):
            o = ParagraphSerializers.Operate(
                data={"paragraph_id": paragraph_id, 'dataset_id': dataset_id, 'document_id': document_id})
            o.is_valid(raise_exception=True)
            return result.success(o.edit(request.data))

        @action(methods=['UPDATE'], detail=False)
        @swagger_auto_schema(operation_summary=_('Get paragraph details'),
                             operation_id=_('Get paragraph details'),
                             manual_parameters=ParagraphSerializers.Operate.get_request_params_api(),
                             responses=result.get_api_response(ParagraphSerializers.Operate.get_response_body_api()),
                             tags=[_('Knowledge Base/Documentation/Paragraph')])
        @has_permissions(
            lambda r, k: Permission(group=Group.DATASET, operate=Operate.USE,
                                    dynamic_tag=k.get('dataset_id')))
        @log(menu=_('Knowledge Base/Documentation/Paragraph'), operate=_('Get paragraph details'))
        def get(self, request: Request, dataset_id: str, document_id: str, paragraph_id: str):
            o = ParagraphSerializers.Operate(
                data={"dataset_id": dataset_id, 'document_id': document_id, "paragraph_id": paragraph_id})
            o.is_valid(raise_exception=True)
            return result.success(o.one())

        @action(methods=['DELETE'], detail=False)
        @swagger_auto_schema(operation_summary=_('Delete paragraph'),
                             operation_id=_('Delete paragraph'),
                             manual_parameters=ParagraphSerializers.Operate.get_request_params_api(),
                             responses=result.get_default_response(),
                             tags=[_('Knowledge Base/Documentation/Paragraph')])
        @has_permissions(
            lambda r, k: Permission(group=Group.DATASET, operate=Operate.MANAGE,
                                    dynamic_tag=k.get('dataset_id')))
        @log(menu=_('Knowledge Base/Documentation/Paragraph'), operate=_('Delete paragraph'))
        def delete(self, request: Request, dataset_id: str, document_id: str, paragraph_id: str):
            o = ParagraphSerializers.Operate(
                data={"dataset_id": dataset_id, 'document_id': document_id, "paragraph_id": paragraph_id})
            o.is_valid(raise_exception=True)
            return result.success(o.delete())

    class Batch(APIView):
        authentication_classes = [TokenAuth]

        @action(methods=['DELETE'], detail=False)
        @swagger_auto_schema(operation_summary=_('Delete paragraphs in batches'),
                             operation_id=_('Delete paragraphs in batches'),
                             request_body=
                             BatchSerializer.get_request_body_api(),
                             manual_parameters=ParagraphSerializers.Create.get_request_params_api(),
                             responses=result.get_default_response(),
                             tags=[_('Knowledge Base/Documentation/Paragraph')])
        @has_permissions(
            lambda r, k: Permission(group=Group.DATASET, operate=Operate.MANAGE,
                                    dynamic_tag=k.get('dataset_id')))
        @log(menu=_('Knowledge Base/Documentation/Paragraph'), operate=_('Delete paragraphs in batches'))
        def delete(self, request: Request, dataset_id: str, document_id: str):
            return result.success(ParagraphSerializers.Batch(
                data={"dataset_id": dataset_id, 'document_id': document_id}).batch_delete(request.data))

    class BatchMigrate(APIView):
        authentication_classes = [TokenAuth]

        @action(methods=['PUT'], detail=False)
        @swagger_auto_schema(operation_summary=_('Migrate paragraphs in batches'),
                             operation_id=_('Migrate paragraphs in batches'),
                             manual_parameters=ParagraphSerializers.Migrate.get_request_params_api(),
                             request_body=ParagraphSerializers.Migrate.get_request_body_api(),
                             responses=result.get_default_response(),
                             tags=[_('Knowledge Base/Documentation/Paragraph')]
                             )
        @has_permissions(
            lambda r, k: Permission(group=Group.DATASET, operate=Operate.MANAGE,
                                    dynamic_tag=k.get('dataset_id')),
            lambda r, k: Permission(group=Group.DATASET, operate=Operate.MANAGE,
                                    dynamic_tag=k.get('target_dataset_id')),
            compare=CompareConstants.AND
        )
        @log(menu=_('Knowledge Base/Documentation/Paragraph'), operate=_('Migrate paragraphs in batches'))
        def put(self, request: Request, dataset_id: str, target_dataset_id: str, document_id: str, target_document_id):
            return result.success(
                ParagraphSerializers.Migrate(
                    data={'dataset_id': dataset_id, 'target_dataset_id': target_dataset_id,
                          'document_id': document_id,
                          'target_document_id': target_document_id,
                          'paragraph_id_list': request.data}).migrate())

    class Page(APIView):
        authentication_classes = [TokenAuth]

        @action(methods=['GET'], detail=False)
        @swagger_auto_schema(operation_summary=_('Get paragraph list by pagination'),
                             operation_id=_('Get paragraph list by pagination'),
                             manual_parameters=result.get_page_request_params(
                                 ParagraphSerializers.Query.get_request_params_api()),
                             responses=result.get_page_api_response(ParagraphSerializers.Query.get_response_body_api()),
                             tags=[_('Knowledge Base/Documentation/Paragraph')])
        @has_permissions(
            lambda r, k: Permission(group=Group.DATASET, operate=Operate.USE,
                                    dynamic_tag=k.get('dataset_id')))
        @log(menu=_('Knowledge Base/Documentation/Paragraph'), operate=_('Get paragraph list by pagination'))
        def get(self, request: Request, dataset_id: str, document_id: str, current_page, page_size):
            d = ParagraphSerializers.Query(
                data={**query_params_to_single_dict(request.query_params), 'dataset_id': dataset_id,
                      'document_id': document_id})
            d.is_valid(raise_exception=True)
            return result.success(d.page(current_page, page_size))

    class BatchGenerateRelated(APIView):
        authentication_classes = [TokenAuth]

        @action(methods=['PUT'], detail=False)
        @has_permissions(
            lambda r, k: Permission(group=Group.DATASET, operate=Operate.MANAGE,
                                    dynamic_tag=k.get('dataset_id')))
        @log(menu=_('Knowledge Base/Documentation/Paragraph'), operate=_('Batch generate related'))
        def put(self, request: Request, dataset_id: str, document_id: str):
            return result.success(
                ParagraphSerializers.BatchGenerateRelated(data={'dataset_id': dataset_id, 'document_id': document_id})
                .batch_generate_related(request.data))
