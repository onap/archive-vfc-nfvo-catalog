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

package org.openo.commontosca.catalog.cometd;

public class CometdException extends Exception {
  public static int ERROR_CODE_BAYEUX = 0;
  public static int ERROR_CODE_PARAM_ERROR = 1;
  public static int ERROR_CODE_SESSION_ERROR = 2;
  public static int ERROR_CODE_SUBSCRIBE_TIMEOUT = 3;
  private int errorCode = -1;

  public CometdException(Throwable e1) {
    super(e1);
  }

  public CometdException(int code, String message) {
    super(message);
    this.errorCode = code;
  }
}
