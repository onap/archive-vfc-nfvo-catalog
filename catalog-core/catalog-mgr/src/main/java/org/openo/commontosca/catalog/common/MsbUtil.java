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

package org.openo.commontosca.catalog.common;

/**
 * micro-service bus utility class.
 * 
 */
public class MsbUtil {

  public static String getRocBaseUrl() {
    return Config.getConfigration().getMsbServerAddr() + getRocApiRootDomain();
  }

  private static String getRocApiRootDomain() {
    return "/api/roc/v1";
  }

  public static String getNsocLifecycleBaseUrl() {
    return Config.getConfigration().getMsbServerAddr() + getNsocLifeCycleRootDomain();
  }

  private static String getNsocLifeCycleRootDomain() {
    return "/api/nsoc/v1";
  }

  public static String getVimBaseUrl() {
    return Config.getConfigration().getMsbServerAddr() + getVimRootDomain();
  }

  private static String getVimRootDomain() {
    return "/api/vim/v1";
  }

  public static String getPackageUrl() {
    return Config.getConfigration().getMsbServerAddr() + "/api/nsoc/v1/csar/";
  }

  public static String getYamlParseBaseUrl() {
    return Config.getConfigration().getMsbServerAddr() + "/openoapi/yamlparser/v1";
  }
}
