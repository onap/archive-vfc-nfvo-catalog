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

import javax.ws.rs.Consumes;
import javax.ws.rs.DELETE;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;

import org.glassfish.jersey.media.multipart.FormDataMultiPart;
import org.openo.commontosca.catalog.model.plan.wso2.entity.DeletePackageResponse;
import org.openo.commontosca.catalog.model.plan.wso2.entity.DeployPackageResponse;
import org.openo.commontosca.catalog.model.plan.wso2.entity.StartProcessResponse;
import org.openo.commontosca.catalog.model.plan.wso2.entity.StartProcessRequest;

/**
 * 
 * @author 10090474
 * 
 */
@Path("/openoapi/wso2bpel/v1")
public interface IWSO2RestService {
    /**
     * @param request
     * @return
     * @throws Exception
     */
    @Path("/package")
	@POST
    @Consumes(MediaType.APPLICATION_JSON)
	@Produces(MediaType.APPLICATION_JSON)
    DeployPackageResponse deployPackage(FormDataMultiPart request) throws Exception;

    @Path("/package/{packageName}")
    @DELETE
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    DeletePackageResponse deletePackage(
            @PathParam("packageName") String packageName) throws Exception;

    @Path("process/instance")
    @POST
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    StartProcessResponse startProcess(StartProcessRequest request)
            throws Exception;
}
