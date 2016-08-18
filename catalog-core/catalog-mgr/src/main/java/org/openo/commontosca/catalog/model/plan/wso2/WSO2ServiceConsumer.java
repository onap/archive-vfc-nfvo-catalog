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
package org.openo.commontosca.catalog.model.plan.wso2;

import java.util.Map;

import org.glassfish.jersey.client.ClientConfig;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.model.plan.wso2.entity.DeletePackageResponse;
import org.openo.commontosca.catalog.model.plan.wso2.entity.StartProcessResponse;
import org.openo.commontosca.catalog.model.plan.wso2.entity.DeployPackageResponse;
import org.openo.commontosca.catalog.model.plan.wso2.entity.StartProcessRequest;

import com.eclipsesource.jaxrs.consumer.ConsumerFactory;

/**
 * 
 * @author 10090474
 * 
 */
public class WSO2ServiceConsumer {
    public static final String WSO2_BASE_URL = "http://localhost:9449/";

    /**
     * 
     * @param filePath
     * @return
     * @throws CatalogResourceException
     */
    public static DeployPackageResponse deployPackage(String filePath)
            throws CatalogResourceException {

        // final FormDataMultiPart formData = new FormDataMultiPart();
        // final BodyPart bodyPart = new FormDataBodyPart(fileDetail,
        // uploadedInputStream, MediaType.APPLICATION_OCTET_STREAM_TYPE);
        // formData.bodyPart(bodyPart);
        // formData.setContentDisposition(fileDetail);
        // formData.setMediaType(MediaType.MULTIPART_FORM_DATA_TYPE);
        // final Client client = ClientBuilder.newBuilder()
        // .register(MultiPartFeature.class).build();
        // final WebTarget target = client.target(getPackageURL()).path(
        // "/containerapi/CSARs");
        // final Response response = target.request().post(
        // Entity.entity(formData, formData.getMediaType()));
        // return response;

        return null;
        // try {
        // ClientConfig config = new ClientConfig();
        // IWSO2RestService yamlParseProxy = ConsumerFactory
        // .createConsumer(MSBUtil.getYamlParseBaseUrl(), config,
        // IWSO2RestService.class);
        // String jsonStr = yamlParseProxy.parse(request);
        // return new Gson().fromJson(jsonStr, ParseYamlResult.class);
        // } catch (Exception e) {
        // throw new CatalogResourceException("Call parser api failed.", e);
        // }

    }


    /**
     * @param packageName
     * @return
     * @throws CatalogResourceException
     */
    DeletePackageResponse deletePackage(String packageName)
            throws CatalogResourceException {
        try {
            ClientConfig config = new ClientConfig();
            IWSO2RestService wso2Proxy = ConsumerFactory.createConsumer(
                    WSO2_BASE_URL, config, IWSO2RestService.class);
            DeletePackageResponse response = wso2Proxy
                    .deletePackage(packageName);
            if (response.isSuccess()) {
                return response;
            }
            throw new CatalogResourceException(response.getException());
        } catch (Exception e) {
            throw new CatalogResourceException(
                    "Call Delete Package api failed.", e);
        }
    }


    /**
     * @param processId
     * @param params
     * @return
     * @throws CatalogResourceException
     */
    StartProcessResponse startProcess(String processId,
                                      Map<String, Object> params) throws CatalogResourceException {
        try {
            ClientConfig config = new ClientConfig();
            IWSO2RestService wso2Proxy = ConsumerFactory.createConsumer(
                    WSO2_BASE_URL, config, IWSO2RestService.class);
            StartProcessResponse response = wso2Proxy
                    .startProcess(new StartProcessRequest(processId, params));
            if (response.isSuccess()) {
                return response;
            }
            throw new CatalogResourceException(response.getException());
        } catch (Exception e) {
            throw new CatalogResourceException(
                    "Call Start Process api failed.", e);
        }
    }

}
