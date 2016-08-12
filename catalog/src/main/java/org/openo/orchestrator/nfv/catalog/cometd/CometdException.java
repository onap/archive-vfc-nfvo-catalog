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
package org.openo.orchestrator.nfv.catalog.cometd;

/**
 * @author 10189609
 * 
 */
public class CometdException extends Exception {
    private static final long serialVersionUID = 497640895744777904L;

    public static final int ERROR_CODE_BAYEUX = 0;
    public static final int ERROR_CODE_PRARM_ERROR = 1;
    public static final int ERROR_CODE_SESSION_ERROR = 2;
    public static final int ERROR_CODE_SUBSCRIBE_TIMEOUT = 3;

    private int errorCode = -1;

    public CometdException(String message) {
        super(message);
    }

    public CometdException(Throwable e) {
        super(e);
    }

    public CometdException(int code, String message) {
        super(message);
        this.errorCode = code;
    }

    public int getErrorCode() {
        return this.errorCode;
    }

    @Override
    public String toString() {
        String s = getClass().getName();
        String message = getLocalizedMessage();
        message = (message != null) ? (s + ": " + message) : s;
        return "errorcode: " + this.errorCode + ";" + message;
    }
}
