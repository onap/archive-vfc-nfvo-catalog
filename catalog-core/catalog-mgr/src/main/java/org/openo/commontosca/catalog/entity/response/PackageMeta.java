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

package org.openo.commontosca.catalog.entity.response;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import org.openo.commontosca.catalog.entity.EnumOperationalState;
import org.openo.commontosca.catalog.entity.EnumProcessState;
import org.openo.commontosca.catalog.entity.EnumUsageState;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PackageMeta {

  private String csarId;

  private String name;

  private String downloadUri;

  private String size;

  private String version;

  private String provider;

  private String type;

  private String format;

  private boolean deletionPending;

  private String createTime;

  private String modifyTime;

  private EnumOperationalState operationalState;

  private EnumUsageState usageState;

  private String onBoardState;

  private EnumProcessState processState;

}
