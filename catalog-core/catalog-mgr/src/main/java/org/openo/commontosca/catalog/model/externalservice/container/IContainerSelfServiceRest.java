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

package org.openo.commontosca.catalog.model.externalservice.container;

import org.openo.commontosca.catalog.model.externalservice.entity.container.ContainerSelfService;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;


/**
 * The opentosca container interface for self service.
 * 
 * @author 10189609
 * 
 */
@Path("/containerapi/CSARs/{csarid}/Content/SELFSERVICE-Metadata")
public interface IContainerSelfServiceRest {
  @GET
  @Path("/data.xml")
  @Produces({"application/octet-stream"})
  ContainerSelfService getContainerSelfService(@PathParam("csarid") String csarId);

  @GET
  @Path("/data.xml")
  @Produces({"application/octet-stream"})
  String getContainerSelfServiceXml(@PathParam("csarid") String csarId);

  @GET
  @Path("/{inputmessageurl}")
  @Produces({"application/octet-stream"})
  String getContainerSelfServiceOptionInputMessage(@PathParam("csarid") String csarId,
      @PathParam("inputmessageurl") String inputmessageUrl);
}
