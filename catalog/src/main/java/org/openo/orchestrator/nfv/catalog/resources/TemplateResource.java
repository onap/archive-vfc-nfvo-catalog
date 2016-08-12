/**
 *     Copyright (C) 2016 ZTE, Inc. and others. All rights reserved. (ZTE)
 *
 *     Licensed under the Apache License, Version 2.0 (the "License");
 *     you may not use this file except in compliance with the License.
 *     You may obtain a copy of the License at
 *
 *             http://www.apache.org/licenses/LICENSE-2.0
 *
 *     Unless required by applicable law or agreed to in writing, software
 *     distributed under the License is distributed on an "AS IS" BASIS,
 *     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *     See the License for the specific language governing permissions and
 *     limitations under the License.
 */
package org.openo.orchestrator.nfv.catalog.resources;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import io.swagger.annotations.ApiResponse;
import io.swagger.annotations.ApiResponses;

import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import org.eclipse.jetty.http.HttpStatus;
import org.openo.orchestrator.nfv.catalog.common.CommonErrorResponse;
import org.openo.orchestrator.nfv.catalog.common.ToolUtil;
import org.openo.orchestrator.nfv.catalog.db.exception.CatalogResourceException;
import org.openo.orchestrator.nfv.catalog.model.entity.InputParameter;
import org.openo.orchestrator.nfv.catalog.model.entity.NodeTemplate;
import org.openo.orchestrator.nfv.catalog.model.entity.QueryRawDataCondition;
import org.openo.orchestrator.nfv.catalog.model.entity.ServiceTemplate;
import org.openo.orchestrator.nfv.catalog.model.entity.ServiceTemplateOperation;
import org.openo.orchestrator.nfv.catalog.model.entity.ServiceTemplateRawData;
import org.openo.orchestrator.nfv.catalog.model.parser.ToscaYamlModelParser;
import org.openo.orchestrator.nfv.catalog.model.wrapper.ServiceTemplateWrapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.codahale.metrics.annotation.Timed;

/**
 * @author 10090474
 * 
 */
@Path("/servicetemplates")
@Api(tags = {"Model Resource"})
public class TemplateResource {
    private static final Logger logger = LoggerFactory.getLogger(TemplateResource.class);

    /**
     * @param servicetemplateid
     * @return
     */
    @Path("/{servicetemplateid}")
    @GET
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    @ApiOperation(value = "Query service template by service template id",
            response = ServiceTemplate.class)
    @ApiResponses(value = {
            @ApiResponse(code = HttpStatus.NOT_FOUND_404, message = "microservice not found",
                    response = String.class),
            @ApiResponse(code = HttpStatus.UNSUPPORTED_MEDIA_TYPE_415,
                    message = "Unprocessable MicroServiceInfo Entity ", response = String.class),
            @ApiResponse(code = HttpStatus.INTERNAL_SERVER_ERROR_500,
                    message = "server internal error", response = CommonErrorResponse.class)})
    @Timed
    public Response getServiceTemplateById(
            @ApiParam(value = "service template id") @PathParam("servicetemplateid") String servicetemplateid) {
        try {
            ServiceTemplate st =
                    ServiceTemplateWrapper.getInstance().getServiceTemplateById(servicetemplateid);
            return Response.status(Response.Status.OK).entity(st).build();
        } catch (CatalogResourceException e) {
            logger.error("getServiceTemplateById failed.", e);
            throw RestUtils.newInternalServerErrorException(e);
        }
    }


    /**
     * @param status
     * @param deletionPending
     * @return
     */
    @GET
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    @ApiOperation(value = "Query service template by filter conditions",
            response = ServiceTemplate.class, responseContainer = "List")
    @ApiResponses(value = {
            @ApiResponse(code = HttpStatus.NOT_FOUND_404, message = "microservice not found",
                    response = String.class),
            @ApiResponse(code = HttpStatus.UNSUPPORTED_MEDIA_TYPE_415,
                    message = "Unprocessable MicroServiceInfo Entity ", response = String.class),
            @ApiResponse(code = HttpStatus.INTERNAL_SERVER_ERROR_500,
                    message = "server internal error", response = CommonErrorResponse.class)})
    @Timed
    public Response getServiceTemplates(
            @ApiParam(value = "template status") @QueryParam("status") String status,
            @ApiParam(value = "delay to delete") @QueryParam("deletionPending") boolean deletionPending) {
        try {
            ServiceTemplate[] sts =
                    ServiceTemplateWrapper.getInstance().getServiceTemplates(status,
                            deletionPending);
            return Response.status(Response.Status.OK).entity(sts).build();
        } catch (CatalogResourceException e) {
            logger.error("getServiceTemplates failed.", e);
            throw RestUtils.newInternalServerErrorException(e);
        }

    }

    /**
     * @param nodeTypeIds
     * @return
     */
    @Path("/nesting")
    @GET
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    @ApiOperation(value = "Query nesting service template of a node type",
            response = ServiceTemplate.class, responseContainer = "List")
    @ApiResponses(value = {
            @ApiResponse(code = HttpStatus.NOT_FOUND_404, message = "microservice not found",
                    response = String.class),
            @ApiResponse(code = HttpStatus.UNSUPPORTED_MEDIA_TYPE_415,
                    message = "Unprocessable MicroServiceInfo Entity ", response = String.class),
            @ApiResponse(code = HttpStatus.INTERNAL_SERVER_ERROR_500,
                    message = "server internal error", response = CommonErrorResponse.class)})
    @Timed
    public Response getNestingServiceTemplate(
            @ApiParam(value = "Node Type Id", required = true) @QueryParam("nodeTypeIds") String nodeTypeIds) {
        try {
            if (ToolUtil.isTrimedEmptyString(nodeTypeIds)) {
                throw new CatalogBadRequestException("nodeTypeIds is null.");
            }
            String[] tmpNodeTypeIds = nodeTypeIds.split(",");
            ServiceTemplate[] sts =
                    ServiceTemplateWrapper.getInstance().getNestingServiceTemplate(
                            ToolUtil.TrimedStringArray(tmpNodeTypeIds));
            return Response.status(Response.Status.OK).entity(sts).build();
        } catch (CatalogResourceException e) {
            logger.error("getNestingServiceTemplate failed.", e);
            throw RestUtils.newInternalServerErrorException(e);
        } catch (CatalogBadRequestException e) {
            logger.error("getNestingServiceTemplate failed.", e);
            throw RestUtils.newBadRequestException(e);
        }
    }

    /**
     * @param nodeTypeId
     * @return
     */
    @Path("/queryingrawdata")
    @POST
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    @ApiOperation(value = "Query raw data of a service template by csar id",
            response = ServiceTemplateRawData.class)
    @ApiResponses(value = {
            @ApiResponse(code = HttpStatus.NOT_FOUND_404, message = "microservice not found",
                    response = String.class),
            @ApiResponse(code = HttpStatus.UNSUPPORTED_MEDIA_TYPE_415,
                    message = "Unprocessable MicroServiceInfo Entity ", response = String.class),
            @ApiResponse(code = HttpStatus.INTERNAL_SERVER_ERROR_500,
                    message = "server internal error", response = CommonErrorResponse.class)})
    @Timed
    public Response getServiceTemplateRawData(
            @ApiParam(value = "Query Service Template Raw Data Condition", required = true) QueryRawDataCondition queryCondition) {
        try {
            ServiceTemplateRawData stRowData =
                    ServiceTemplateWrapper.getInstance().getServiceTemplateRawData(queryCondition);
            return Response.status(Response.Status.OK).entity(stRowData).build();
        } catch (CatalogResourceException e) {
            logger.error("getServiceTemplateRawData failed.", e);
            throw RestUtils.newInternalServerErrorException(e);
        } catch (CatalogBadRequestException e) {
            logger.error("getServiceTemplateRawData failed.", e);
            throw RestUtils.newBadRequestException(e);
        }
    }


    /**
     * @param serviceTemplateId
     * @return
     */
    @Path("/{serviceTemplateId}/operations")
    @GET
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    @ApiOperation(value = "Query operation list of service template",
            response = ServiceTemplateOperation.class, responseContainer = "List")
    @ApiResponses(value = {
            @ApiResponse(code = HttpStatus.NOT_FOUND_404, message = "microservice not found",
                    response = String.class),
            @ApiResponse(code = HttpStatus.UNSUPPORTED_MEDIA_TYPE_415,
                    message = "Unprocessable MicroServiceInfo Entity ", response = String.class),
            @ApiResponse(code = HttpStatus.INTERNAL_SERVER_ERROR_500,
                    message = "server internal error", response = CommonErrorResponse.class)})
    @Timed
    public Response getServiceTemplateOperations(@ApiParam(value = "Service Template Id",
            required = true) @PathParam("serviceTemplateId") String serviceTemplateId) {
        try {
            ServiceTemplateOperation[] operations =
                    ServiceTemplateWrapper.getInstance().getTemplateOperations(serviceTemplateId);
            return Response.status(Response.Status.OK).entity(operations).build();
        } catch (CatalogResourceException e) {
            logger.error("getServiceTemplateOperations failed.", e);
            throw RestUtils.newInternalServerErrorException(e);
        }

    }

    /**
     * @param serviceTemplateId
     * @param operationName
     * @return
     */
    @Path("/{serviceTemplateId}/operations/{operationName}/parameters")
    @GET
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    @ApiOperation(value = "Query input parameters of a specified operation",
            response = InputParameter.class, responseContainer = "List")
    @ApiResponses(value = {
            @ApiResponse(code = HttpStatus.NOT_FOUND_404, message = "microservice not found",
                    response = String.class),
            @ApiResponse(code = HttpStatus.UNSUPPORTED_MEDIA_TYPE_415,
                    message = "Unprocessable MicroServiceInfo Entity ", response = String.class),
            @ApiResponse(code = HttpStatus.INTERNAL_SERVER_ERROR_500,
                    message = "server internal error", response = CommonErrorResponse.class)})
    @Timed
    public Response getParametersByOperationName(
            @ApiParam(value = "Service Template Id", required = true) @PathParam("serviceTemplateId") String serviceTemplateId,
            @ApiParam(value = "Operation Name", required = true) @PathParam("operationName") String operationName) {
        try {
            InputParameter[] inputs =
                    ServiceTemplateWrapper.getInstance().getParametersByOperationName(
                            serviceTemplateId, operationName);
            return Response.status(Response.Status.OK).entity(inputs).build();
        } catch (CatalogResourceException e) {
            logger.error("getParametersByOperationId failed.", e);
            throw RestUtils.newInternalServerErrorException(e);
        }

    }

    /**
     * @param servicetemplateid
     * @return
     */
    @Path("/{servicetemplateid}/parameters")
    @GET
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    @ApiOperation(value = "Query input parameters of service template",
            response = InputParameter.class, responseContainer = "List")
    @ApiResponses(value = {
            @ApiResponse(code = HttpStatus.NOT_FOUND_404, message = "microservice not found",
                    response = String.class),
            @ApiResponse(code = HttpStatus.UNSUPPORTED_MEDIA_TYPE_415,
                    message = "Unprocessable MicroServiceInfo Entity ", response = String.class),
            @ApiResponse(code = HttpStatus.INTERNAL_SERVER_ERROR_500,
                    message = "server internal error", response = CommonErrorResponse.class)})
    @Timed
    public Response getServiceTemplateParameters(@ApiParam(value = "service template id",
            required = true) @PathParam("servicetemplateid") String servicetemplateid) {
        try {
            InputParameter[] inputs =
                    ServiceTemplateWrapper.getInstance().getServiceTemplateParameters(
                            servicetemplateid);
            return Response.status(Response.Status.OK).entity(inputs).build();
        } catch (CatalogResourceException e) {
            logger.error("getServiceTemplateParameters failed.", e);
            throw RestUtils.newInternalServerErrorException(e);
        }

    }

    /**
     * @param serviceTemplateId
     * @param types
     * @return
     */
    @Path("/{serviceTemplateId}/nodetemplates")
    @GET
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    @ApiOperation(value = "Query node template list of a specified service template",
            response = NodeTemplate.class, responseContainer = "List")
    @ApiResponses(value = {
            @ApiResponse(code = HttpStatus.NOT_FOUND_404, message = "microservice not found",
                    response = String.class),
            @ApiResponse(code = HttpStatus.UNSUPPORTED_MEDIA_TYPE_415,
                    message = "Unprocessable MicroServiceInfo Entity ", response = String.class),
            @ApiResponse(code = HttpStatus.INTERNAL_SERVER_ERROR_500,
                    message = "server internal error", response = CommonErrorResponse.class)})
    @Timed
    public Response getNodeTemplatesByType(
            @ApiParam(value = "Service Template Id", required = true) @PathParam("serviceTemplateId") String serviceTemplateId,
            @ApiParam(value = "The type of node template") @QueryParam("types") String types) {
        try {
            String[] tmpTypes = getSplitedTypes(types);
            NodeTemplate[] nts =
                    ServiceTemplateWrapper.getInstance().getNodeTemplates(serviceTemplateId,
                            ToolUtil.TrimedStringArray(tmpTypes));
            return Response.status(Response.Status.OK).entity(nts).build();
        } catch (CatalogResourceException e) {
            logger.error("getNodeTemplateList failed.", e);
            throw RestUtils.newInternalServerErrorException(e);
        }

    }


    private String[] getSplitedTypes(String types) {
        if (ToolUtil.isTrimedEmptyString(types)) {
            return new String[0];
        }

        return types.split(",");
    }

    /**
     * @param serviceTemplateId
     * @param nodeTemplateId
     * @return
     */
    @Path("/{serviceTemplateId}/nodetemplates/{nodeTemplateId}")
    @GET
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    @ApiOperation(value = "Query node template by node template id", response = NodeTemplate.class)
    @ApiResponses(value = {
            @ApiResponse(code = HttpStatus.NOT_FOUND_404, message = "microservice not found",
                    response = String.class),
            @ApiResponse(code = HttpStatus.UNSUPPORTED_MEDIA_TYPE_415,
                    message = "Unprocessable MicroServiceInfo Entity ", response = String.class),
            @ApiResponse(code = HttpStatus.INTERNAL_SERVER_ERROR_500,
                    message = "server internal error", response = CommonErrorResponse.class)})
    @Timed
    public Response getNodeTemplateById(
            @ApiParam(value = "Service Template Id", required = true) @PathParam("serviceTemplateId") String serviceTemplateId,
            @ApiParam(value = "Node Template Id", required = true) @PathParam("nodeTemplateId") String nodeTemplateId) {
        try {
            NodeTemplate nt =
                    ServiceTemplateWrapper.getInstance().getNodeTemplateById(serviceTemplateId,
                            nodeTemplateId);
            return Response.status(Response.Status.OK).entity(nt).build();
        } catch (CatalogResourceException e) {
            logger.error("getNodeTemplateById failed.", e);
            throw RestUtils.newInternalServerErrorException(e);
        }

    }

    // /**
    // * @param servicetemplateid
    // * @return
    // */
    // @Path("/{servicetemplateid}/nfvtemplate")
    // @POST
    // @Consumes(MediaType.APPLICATION_JSON)
    // @Produces(MediaType.APPLICATION_JSON)
    // @ApiOperation(value =
    // "Query node template detail of a specified service template", response =
    // NfvTemplate.class)
    // @ApiResponses(value = {
    // @ApiResponse(code = HttpStatus.NOT_FOUND_404, message =
    // "microservice not found", response = String.class),
    // @ApiResponse(code = HttpStatus.UNSUPPORTED_MEDIA_TYPE_415, message =
    // "Unprocessable MicroServiceInfo Entity ", response = String.class),
    // @ApiResponse(code = HttpStatus.INTERNAL_SERVER_ERROR_500, message =
    // "server internal error", response = CommonErrorResponse.class) })
    // @Timed
    // public Response getNfvTemplate(
    // @ApiParam(value = "service template id", required = true)
    // @PathParam("servicetemplateid") String servicetemplateid) {
    // try {
    // NfvTemplate nfvTemplate = ServiceTemplateWrapper.getInstance()
    // .getNfvTemplate(servicetemplateid);
    // return Response.status(Response.Status.OK).entity(nfvTemplate)
    // .build();
    // } catch (CatalogResourceException e) {
    // logger.error("getNfvTemplate failed.", e);
    // throw RestUtils.newInternalServerErrorException(e);
    // }
    //
    // }

    /**
     * 
     * @return
     */
    @Path("/test")
    @GET
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    @ApiOperation(value = "test", response = String.class, responseContainer = "List")
    @ApiResponses(value = {
            @ApiResponse(code = HttpStatus.NOT_FOUND_404, message = "microservice not found",
                    response = String.class),
            @ApiResponse(code = HttpStatus.UNSUPPORTED_MEDIA_TYPE_415,
                    message = "Unprocessable MicroServiceInfo Entity ", response = String.class),
            @ApiResponse(code = HttpStatus.INTERNAL_SERVER_ERROR_500,
                    message = "server internal error", response = CommonErrorResponse.class)})
    @Timed
    public Response test() {
        try {
            ToscaYamlModelParser parser = new ToscaYamlModelParser();
            parser.parse("pk11111", "C:\\Users\\10090474\\Desktop\\3\\NS_core\\NS_core.zip");
            String[] strs = {"111", "222", null, null, "555"};
            Response.status(Response.Status.OK).entity(strs).build();
            throw new CatalogResourceException("test failed.");
        } catch (CatalogResourceException e) {
            logger.error("test failed.", e);
            throw RestUtils.newInternalServerErrorException(e);
        }
    }


}
