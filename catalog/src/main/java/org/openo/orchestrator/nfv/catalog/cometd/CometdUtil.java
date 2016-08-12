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
/**
* Copyright (C) 2016 ZTE, Inc. and others. All rights reserved. (ZTE)
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/
package org.openo.orchestrator.nfv.catalog.cometd;

import java.io.IOException;
import java.util.Map;

import org.cometd.bayeux.server.BayeuxServer;

import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * @author 10189609
 *
 */
public class CometdUtil {
    private static BayeuxServer bayeuxServer;

    public static BayeuxServer getBayeuxServer() {
        return bayeuxServer;
    }

    public static void setBayeuxServer(BayeuxServer bayeuxServer) {
        CometdUtil.bayeuxServer = bayeuxServer;
    }
    
    public static String convertBean2Json(Object object) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        return mapper.writeValueAsString(object);
    }
    
    @SuppressWarnings("rawtypes")
    public static Map convertJson2Map(String json) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        return mapper.readValue(json, Map.class);
    }
}
