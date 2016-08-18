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

import javax.ws.rs.BadRequestException;
import javax.ws.rs.InternalServerErrorException;
import javax.ws.rs.core.Response;

import org.openo.commontosca.catalog.common.CommonErrorResponse;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;


public class RestUtils {
    /**
     * @param e
     * @return
     */
    public static InternalServerErrorException newInternalServerErrorException(
            CatalogResourceException e) {
        return new InternalServerErrorException(Response
                .status(Response.Status.INTERNAL_SERVER_ERROR)
                .entity(new CommonErrorResponse(e.getErrcode() + "", e.getMessage())).build(), e);
    }

    /**
     * @param e
     * @return
     */
    public static BadRequestException newBadRequestException(CatalogBadRequestException e) {
        return new BadRequestException(Response.status(Response.Status.BAD_REQUEST)
                .entity(new CommonErrorResponse(e.getErrcode() + "", e.getMessage())).build(), e);
    }
}
