/**
 * Copyright 2016 [ZTE] and others.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.openo.commontosca.catalog.resources;

import com.codahale.metrics.annotation.Timed;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import io.swagger.annotations.ApiResponse;
import io.swagger.annotations.ApiResponses;

import org.eclipse.jetty.http.HttpStatus;
import org.openo.commontosca.catalog.common.CommonErrorResponse;
import org.openo.commontosca.catalog.common.ToolUtil;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.model.entity.InputParameter;
import org.openo.commontosca.catalog.model.entity.NodeTemplate;
import org.openo.commontosca.catalog.model.entity.Parameters;
import org.openo.commontosca.catalog.model.entity.QueryRawDataCondition;
import org.openo.commontosca.catalog.model.entity.ServiceTemplate;
import org.openo.commontosca.catalog.model.entity.ServiceTemplateOperation;
import org.openo.commontosca.catalog.model.entity.ServiceTemplateRawData;
import org.openo.commontosca.catalog.model.parser.ToscaYamlModelParser;
import org.openo.commontosca.catalog.model.service.ModelService;
import org.openo.commontosca.catalog.model.wrapper.ServiceTemplateWrapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

/**
 * model template service.
 * 
 */
@Path("/servicetemplates")
@Api(tags = {"Model Resource"})
public class TemplateResource {

  private static final Logger logger = LoggerFactory.getLogger(TemplateResource.class);

  /**
   * Query service template by service template id.
   * @param servicetemplateid service template id
   * @return Response
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
      @ApiResponse(code = HttpStatus.INTERNAL_SERVER_ERROR_500, message = "server internal error",
          response = CommonErrorResponse.class)})
  @Timed
  public Response getServiceTemplateById(@ApiParam(
      value = "service template id") @PathParam("servicetemplateid") String servicetemplateid) {
    try {
      ServiceTemplate st =
          ServiceTemplateWrapper.getInstance().getServiceTemplateById(servicetemplateid);
      return Response.status(Response.Status.OK).entity(st).build();
    } catch (CatalogResourceException e1) {
      logger.error("getServiceTemplateById failed.", e1);
      throw RestUtils.newInternalServerErrorException(e1);
    }
  }


  /**
   * Query service template by filter conditions.
   * @param status template status
   * @param deletionPending delay to delete
   * @return Response
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
      @ApiResponse(code = HttpStatus.INTERNAL_SERVER_ERROR_500, message = "server internal error",
          response = CommonErrorResponse.class)})
  @Timed
  public Response getServiceTemplates(
      @ApiParam(value = "template status") @QueryParam("status") String status,
      @ApiParam(value = "delay to delete") @QueryParam("deletionPending") boolean deletionPending) {
    try {
      ServiceTemplate[] sts =
          ServiceTemplateWrapper.getInstance().getServiceTemplates(status, deletionPending);
      return Response.status(Response.Status.OK).entity(sts).build();
    } catch (CatalogResourceException e1) {
      logger.error("getServiceTemplates failed.", e1);
      throw RestUtils.newInternalServerErrorException(e1);
    }

  }

  /**
   * Query nesting service template of a node type.
   * @param nodeTypeIds node type ids
   * @return Response
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
      @ApiResponse(code = HttpStatus.INTERNAL_SERVER_ERROR_500, message = "server internal error",
          response = CommonErrorResponse.class)})
  @Timed
  public Response getNestingServiceTemplate(@ApiParam(value = "Node Type Id",
      required = true) @QueryParam("nodeTypeIds") String nodeTypeIds) {
    try {
      if (ToolUtil.isTrimedEmptyString(nodeTypeIds)) {
        throw new CatalogBadRequestException("nodeTypeIds is null.");
      }
      String[] tmpNodeTypeIds = nodeTypeIds.split(",");
      ServiceTemplate[] sts = ServiceTemplateWrapper.getInstance()
          .getNestingServiceTemplate(ToolUtil.trimedStringArray(tmpNodeTypeIds));
      return Response.status(Response.Status.OK).entity(sts).build();
    } catch (CatalogResourceException e1) {
      logger.error("getNestingServiceTemplate failed.", e1);
      throw RestUtils.newInternalServerErrorException(e1);
    } catch (CatalogBadRequestException e2) {
      logger.error("getNestingServiceTemplate failed.", e2);
      throw RestUtils.newBadRequestException(e2);
    }
  }

  /**
   * Query raw data of a service template by csar id.
   * @param queryCondition query condition
   * @return Response
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
      @ApiResponse(code = HttpStatus.INTERNAL_SERVER_ERROR_500, message = "server internal error",
          response = CommonErrorResponse.class)})
  @Timed
  public Response getServiceTemplateRawData(
      @ApiParam(value = "Query Service Template Raw Data Condition",
          required = true) QueryRawDataCondition queryCondition) {
    try {
      ServiceTemplateRawData stRowData =
          ServiceTemplateWrapper.getInstance().getServiceTemplateRawData(queryCondition);
      return Response.status(Response.Status.OK).entity(stRowData).build();
    } catch (CatalogResourceException e1) {
      logger.error("getServiceTemplateRawData failed.", e1);
      throw RestUtils.newInternalServerErrorException(e1);
    } catch (CatalogBadRequestException e2) {
      logger.error("getServiceTemplateRawData failed.", e2);
      throw RestUtils.newBadRequestException(e2);
    }
  }


  /**
   * Query operation list of service template.
   * @param serviceTemplateId service template id
   * @return Response
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
      @ApiResponse(code = HttpStatus.INTERNAL_SERVER_ERROR_500, message = "server internal error",
          response = CommonErrorResponse.class)})
  @Timed
  public Response getServiceTemplateOperations(@ApiParam(value = "Service Template Id",
      required = true) @PathParam("serviceTemplateId") String serviceTemplateId) {
    try {
      ServiceTemplateOperation[] operations =
          ServiceTemplateWrapper.getInstance().getTemplateOperations(serviceTemplateId);
      return Response.status(Response.Status.OK).entity(operations).build();
    } catch (CatalogResourceException e1) {
      logger.error("getServiceTemplateOperations failed.", e1);
      throw RestUtils.newInternalServerErrorException(e1);
    }

  }

  /**
   * Query input parameters of a specified operation.
   * @param serviceTemplateId service template id
   * @param operationName operation name
   * @return Response
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
      @ApiResponse(code = HttpStatus.INTERNAL_SERVER_ERROR_500, message = "server internal error",
          response = CommonErrorResponse.class)})
  @Timed
  public Response getParametersByOperationName(
      @ApiParam(value = "Service Template Id",
          required = true) @PathParam("serviceTemplateId") String serviceTemplateId,
      @ApiParam(value = "Operation Name",
          required = true) @PathParam("operationName") String operationName) {
    try {
      InputParameter[] inputs = ServiceTemplateWrapper.getInstance()
          .getParametersByOperationName(serviceTemplateId, operationName);
      return Response.status(Response.Status.OK).entity(inputs).build();
    } catch (CatalogResourceException e1) {
      logger.error("getParametersByOperationId failed.", e1);
      throw RestUtils.newInternalServerErrorException(e1);
    }

  }

  /**
   * Query input parameters of service template.
   * @param servicetemplateid service template id
   * @return Response
   */
  @Path("/{servicetemplateid}/parameters")
  @GET
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  @ApiOperation(value = "Query input parameters of service template", response = Parameters.class)
  @ApiResponses(value = {
      @ApiResponse(code = HttpStatus.NOT_FOUND_404, message = "microservice not found",
          response = String.class),
      @ApiResponse(code = HttpStatus.UNSUPPORTED_MEDIA_TYPE_415,
          message = "Unprocessable MicroServiceInfo Entity ", response = String.class),
      @ApiResponse(code = HttpStatus.INTERNAL_SERVER_ERROR_500, message = "server internal error",
          response = CommonErrorResponse.class)})
  @Timed
  public Response getServiceTemplateParameters(@ApiParam(value = "service template id",
      required = true) @PathParam("servicetemplateid") String servicetemplateid) {
    try {
      Parameters parameters =
          ServiceTemplateWrapper.getInstance().getServiceTemplateParameters(servicetemplateid);
      return Response.status(Response.Status.OK).entity(parameters).build();
    } catch (CatalogResourceException e1) {
      logger.error("getServiceTemplateParameters failed.", e1);
      throw RestUtils.newInternalServerErrorException(e1);
    }

  }

  /**
   * Query node template list of a specified service template.
   * @param serviceTemplateId service template id
   * @param types node type
   * @return Response
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
      @ApiResponse(code = HttpStatus.INTERNAL_SERVER_ERROR_500, message = "server internal error",
          response = CommonErrorResponse.class)})
  @Timed
  public Response getNodeTemplatesByType(
      @ApiParam(value = "Service Template Id",
          required = true) @PathParam("serviceTemplateId") String serviceTemplateId,
      @ApiParam(value = "The type of node template") @QueryParam("types") String types) {
    try {
      String[] tmpTypes = getSplitedTypes(types);
      NodeTemplate[] nts = ServiceTemplateWrapper.getInstance().getNodeTemplates(serviceTemplateId,
          ToolUtil.trimedStringArray(tmpTypes));
      return Response.status(Response.Status.OK).entity(nts).build();
    } catch (CatalogResourceException e1) {
      logger.error("getNodeTemplateList failed.", e1);
      throw RestUtils.newInternalServerErrorException(e1);
    }

  }


  private String[] getSplitedTypes(String types) {
    if (ToolUtil.isTrimedEmptyString(types)) {
      return new String[0];
    }

    return types.split(",");
  }

  /**
   * Query node template by node template id.
   * @param serviceTemplateId service template id
   * @param nodeTemplateId node template id
   * @return Response
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
      @ApiResponse(code = HttpStatus.INTERNAL_SERVER_ERROR_500, message = "server internal error",
          response = CommonErrorResponse.class)})
  @Timed
  public Response getNodeTemplateById(
      @ApiParam(value = "Service Template Id",
          required = true) @PathParam("serviceTemplateId") String serviceTemplateId,
      @ApiParam(value = "Node Template Id",
          required = true) @PathParam("nodeTemplateId") String nodeTemplateId) {
    try {
      NodeTemplate nt = ServiceTemplateWrapper.getInstance().getNodeTemplateById(serviceTemplateId,
          nodeTemplateId);
      return Response.status(Response.Status.OK).entity(nt).build();
    } catch (CatalogResourceException e1) {
      logger.error("getNodeTemplateById failed.", e1);
      throw RestUtils.newInternalServerErrorException(e1);
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
   * test function.
   * @return Response
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
      @ApiResponse(code = HttpStatus.INTERNAL_SERVER_ERROR_500, message = "server internal error",
          response = CommonErrorResponse.class)})
  @Timed
  public Response test() {
    try {
      ToscaYamlModelParser parser = new ToscaYamlModelParser();
      parser.parse("pk11111", "C:\\Users\\10090474\\Desktop\\1\\bm\\bm.zip");
      String[] strs = {"111", "222", null, null, "555"};
      Response.status(Response.Status.OK).entity(strs).build();

      ModelService.getInstance().delete("pk11111");
      throw new CatalogResourceException("test failed.");
    } catch (CatalogResourceException e1) {
      logger.error("test failed.", e1);
      throw RestUtils.newInternalServerErrorException(e1);
    } catch (CatalogBadRequestException e2) {
      logger.error("test failed.", e2);
      throw RestUtils.newBadRequestException(e2);
    }
  }


}
