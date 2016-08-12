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
package org.openo.orchestrator.nfv.catalog.model.externalservice.container;

import java.io.InputStream;
import java.util.List;

import javax.ws.rs.client.Client;
import javax.ws.rs.client.ClientBuilder;
import javax.ws.rs.client.Entity;
import javax.ws.rs.client.WebTarget;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import org.glassfish.jersey.client.ClientConfig;
import org.glassfish.jersey.media.multipart.BodyPart;
import org.glassfish.jersey.media.multipart.FormDataBodyPart;
import org.glassfish.jersey.media.multipart.FormDataContentDisposition;
import org.glassfish.jersey.media.multipart.FormDataMultiPart;
import org.glassfish.jersey.media.multipart.MultiPartFeature;
import org.openo.orchestrator.nfv.catalog.common.Config;
import org.openo.orchestrator.nfv.catalog.common.ToolUtil;
import org.openo.orchestrator.nfv.catalog.model.externalservice.entity.containerEntity.ContainerSelfService;
import org.openo.orchestrator.nfv.catalog.model.externalservice.entity.containerEntity.ContainerSelfServiceOption;
import org.openo.orchestrator.nfv.catalog.model.externalservice.entity.containerEntity.ContainerServiceNodeTemplateList;
import org.openo.orchestrator.nfv.catalog.model.externalservice.entity.containerEntity.ContainerServiceTemplateList;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.eclipsesource.jaxrs.consumer.ConsumerFactory;
import com.google.gson.JsonObject;

/**
 * By rest requesting access container services
 * @author 10189609
 *
 */
public class ContainerServiceConsumer {
	private static final Logger LOG = LoggerFactory.getLogger(ContainerServiceConsumer.class);
	/**
	 * get service template by template id from container service.
	 * @param templateid id
	 * @return template list entity
	 */
    public static ContainerServiceTemplateList getServiceTemplates(
            final String templateid) {
        ClientConfig config = new ClientConfig(
                new ContainerServiceTemplateProvider());
        IContainerTemplateRest containerservicetemplateproxy = ConsumerFactory
                .createConsumer(getBaseURL(), config,
                        IContainerTemplateRest.class);
        return containerservicetemplateproxy
                .getToscaServiceTemplate(templateid);
    }

    /**
     * get operation input param xml from container service
     * @param csarId
     * @param operationId
     * @return xml
     */
    public static String getOperationInputParamXml(final String csarId,
            final String operationId) {
        String inputparamsSoapXml = null;
        ClientConfig config = new ClientConfig()
                .register(new ContainerSelfServiceProvider());
        IContainerSelfServiceRest containerserviceoperationproxy = ConsumerFactory
                .createConsumer(getPackageURL(), config,
                        IContainerSelfServiceRest.class);
        String csarid = ToolUtil.formatCsar(csarId);
        ContainerSelfService containerselfservice = containerserviceoperationproxy
                .getContainerSelfService(csarid);
        if (containerselfservice != null) {
            for (int i = 0; i < containerselfservice.getOptionList().size(); i++) {
                ContainerSelfServiceOption serviceOption = containerselfservice
                        .getOptionList().get(i);
                if (serviceOption != null
                        && operationId.equals(serviceOption.getId())) {
                    inputparamsSoapXml = containerserviceoperationproxy
                            .getContainerSelfServiceOptionInputMessage(
                            		csarid,
                                    serviceOption.getPlanInputMessageUrl());
                    break;
                }
            }
        }
        return inputparamsSoapXml;
    }
    
    /**
     * get operations by csar id.
     * @param csarId
     * @return xml
     */
    public static String getOperations(final String csarId) {
    	ClientConfig config = new ClientConfig()
		        .register(new ContainerSelfServiceProvider());
		IContainerSelfServiceRest containerselfserviceproxy = ConsumerFactory
		        .createConsumer(getPackageURL(), config,
		                IContainerSelfServiceRest.class);
		return containerselfserviceproxy.getContainerSelfServiceXML(ToolUtil.formatCsar(csarId));
    }
	
	public static List<ContainerSelfServiceOption> getOperationList(final String csarId) {
    	ClientConfig config = new ClientConfig()
    			.register(new ContainerSelfServiceProvider());
		IContainerSelfServiceRest containerserviceoperationproxy = ConsumerFactory
		        .createConsumer(getPackageURL(), config,
                IContainerSelfServiceRest.class);
    	String csarid = ToolUtil.formatCsar(csarId);
        ContainerSelfService containerselfservice = containerserviceoperationproxy
                .getContainerSelfService(csarid);      
    	return containerselfservice.getOptionList();
    }

    /**
     * upload csar package to opentosca containerapi service.
     * @param uploadedInputStream stream
     * @param fileDetail
     * @return response
     */
    public static Response uploadServicePackage(
            InputStream uploadedInputStream,
            FormDataContentDisposition fileDetail) {
        final FormDataMultiPart formData = new FormDataMultiPart();
        final BodyPart bodyPart = new FormDataBodyPart(fileDetail,
                uploadedInputStream, MediaType.APPLICATION_OCTET_STREAM_TYPE);
        formData.bodyPart(bodyPart);
        formData.setContentDisposition(fileDetail);
        formData.setMediaType(MediaType.MULTIPART_FORM_DATA_TYPE);
        final Client client = ClientBuilder.newBuilder()
                .register(MultiPartFeature.class).build();
        final WebTarget target = client.target(getPackageURL()).path(
                "/containerapi/CSARs");
        final Response response = target.request().post(
                Entity.entity(formData, formData.getMediaType()));
        return response;
    }

    /**
     * upload csar package by file location.
     * @param fileLocation
     * @param fileDetail
     * @return response
     */
    public static Response uploadServicePackageByLocation(String fileLocation) {
        ClientConfig config = new ClientConfig();
        IContainerExtPackageRest containerservicepackageproxy = ConsumerFactory
                .createConsumer(getBaseURL(), config,
                        IContainerExtPackageRest.class);
        String result = containerservicepackageproxy
                .uploadPackageByToscaService(fileLocation);
        JsonObject json = new JsonObject();
        json.addProperty("result", result);
        return Response.ok(json.toString()).build();
    }

    /**
     * delete a csar package by csar name.
     * @param csarName
     * @return
     */
    public static String delServicePackage(final String csarName) {
        ClientConfig config = new ClientConfig();
        IContainerExtPackageRest containerservicepackageproxy = ConsumerFactory
                .createConsumer(getBaseURL(), config,
                    IContainerExtPackageRest.class);
        LOG.info("url:" + getBaseURL() + " csarName:" + csarName);
        return containerservicepackageproxy.deletePackageById(csarName);
    }
    
    /**
     * get node template list.
     * @param templateId
     * @return
     */
    public static ContainerServiceNodeTemplateList getNodeTemplates(
    		final String templateId) {
    	ClientConfig config = new ClientConfig(new ContainerServiceNodeTemplateProvider());
    	IContainerTemplateRest containertemplateproxy = ConsumerFactory
    			.createConsumer(getBaseURL(), config, IContainerTemplateRest.class);
    	return containertemplateproxy.getToscaServiceNodeTemplates(templateId);
    }

    /**
     * get policy infomation by service template id from vnfd
     * @param serviceTemplateID
     * @return
     */
    public static String getPolicys(String serviceTemplateID) {
        ClientConfig config = new ClientConfig(new StringProvider());
        IContainerPortabilityRest containerPolicyproxy = ConsumerFactory
                .createConsumer(getBaseURL(), config,
                        IContainerPortabilityRest.class);
        return containerPolicyproxy.getToscaPolicys(serviceTemplateID);
    }
    
    /**
     * http://127.0.0.1:1337/containerapi/extension
     * 
     * @return
     */
    private static String getBaseURL() {
        StringBuffer buffer = new StringBuffer();
        buffer.append(Config.getConfigration().getOpentoscaServerAddr() + "/containerapi/extension");
        return buffer.toString();
    }

    /**
     * http://127.0.0.1:1337
     * 
     * @return
     */
    private static String getPackageURL() {
        StringBuffer buffer = new StringBuffer();
        buffer.append(Config.getConfigration().getOpentoscaServerAddr());
        return buffer.toString();
    }
}
