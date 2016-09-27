/**
 * Copyright 2016 ZTE Corporation.
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

import org.openo.commontosca.catalog.db.exception.ErrorCodeException;

public class CatalogBadRequestException extends ErrorCodeException {
  private static final long serialVersionUID = 5699508780537383310L;


  public CatalogBadRequestException(int errcode) {
    super(errcode, "");
  }


  public CatalogBadRequestException(int errcode, Throwable cause) {
    super(cause, errcode);
  }


  public CatalogBadRequestException(int errcode, String message, Throwable cause) {
    super(cause, errcode, message);
  }


  public CatalogBadRequestException() {
    super(9999999, null);
  }


  public CatalogBadRequestException(String message) {
    super(9999999, message);
  }


  public CatalogBadRequestException(Throwable cause) {
    super(cause, 9999999);
  }


  public CatalogBadRequestException(String message, Throwable cause) {
    super(cause, 9999999, message);
  }


  public CatalogBadRequestException(Throwable source, int errId, String debugMessage,
      String[] arguments) {
    super(source, errId, debugMessage, arguments);
  }

  public CatalogBadRequestException(Throwable source, int category, int code, String debugMessage,
      String[] arguments) {
    super(source, category, code, debugMessage, arguments);
  }

  public int getErrcode() {
    return super.getErrorCode();
  }
}
