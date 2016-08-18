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
package org.openo.commontosca.catalog.db.util;

import java.util.UUID;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.gson.Gson;

public class CatalogDbUtil {
    private final static Logger logger = LoggerFactory.getLogger(CatalogDbUtil.class);

    public static String generateId() {
        return UUID.randomUUID().toString();
    }

    public static boolean isNotEmpty(String s) {
        return s != null && !"".equals(s) && s.length() > 0;
    }

    public static String objectToString(Object obj) {
        Gson gson = new Gson();
        if (obj != null)
            return gson.toJson(obj);
        else
            return null;
    }

}
