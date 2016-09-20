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
package org.openo.commontosca.catalog.model.parser.yaml.aria;

import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import org.openo.commontosca.catalog.common.ToolUtil;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.db.resource.TemplateManager;
import org.openo.commontosca.catalog.entity.response.CsarFileUriResponse;
import org.openo.commontosca.catalog.model.common.TemplateDataHelper;
import org.openo.commontosca.catalog.model.entity.EnumDataType;
import org.openo.commontosca.catalog.model.entity.InputParameter;
import org.openo.commontosca.catalog.model.entity.NodeTemplate;
import org.openo.commontosca.catalog.model.entity.OutputParameter;
import org.openo.commontosca.catalog.model.entity.RelationShip;
import org.openo.commontosca.catalog.model.entity.ServiceTemplate;
import org.openo.commontosca.catalog.model.entity.SubstitutionMapping;
import org.openo.commontosca.catalog.model.parser.AbstractModelParser;
import org.openo.commontosca.catalog.model.parser.yaml.aria.entity.AriaParserResult;
import org.openo.commontosca.catalog.model.parser.yaml.aria.entity.AriaParserResult.Input;
import org.openo.commontosca.catalog.model.parser.yaml.aria.entity.AriaParserResult.Node;
import org.openo.commontosca.catalog.model.parser.yaml.aria.entity.AriaParserResult.Node.Relationship;
import org.openo.commontosca.catalog.model.parser.yaml.aria.entity.AriaParserResult.Output;
import org.openo.commontosca.catalog.model.parser.yaml.aria.entity.AriaParserResult.Substitution.Mapping;
import org.openo.commontosca.catalog.model.parser.yaml.aria.service.AriaParserServiceConsumer;

/**
 * @author 10090474
 *
 */
public class AriaModelParser extends AbstractModelParser {

  /* (non-Javadoc)
   * @see org.openo.commontosca.catalog.model.parser.AbstractModelParser#parse(java.lang.String, java.lang.String)
   */
  @Override
  public String parse(String packageId, String fileLocation) throws CatalogResourceException {
    AriaParserResult result = getAriaParserResult(fileLocation);
    
    // service template
    CsarFileUriResponse stDownloadUri = buildServiceTemplateDownloadUri(packageId, fileLocation);
    ServiceTemplate st = parseServiceTemplate(result, packageId, stDownloadUri.getDownloadUri());
    // node templates
    List<NodeTemplate> ntList = parseNodeTemplates(packageId, st.getServiceTemplateId(), result);
    st.setType(getTemplateType(getSubstitutionType(result), ntList).toString());
    // save to db
    TemplateManager.getInstance().addServiceTemplate(
        TemplateDataHelper.convert2TemplateData(st, ToolUtil.toJson(result), ntList));
    
    // substitution
    SubstitutionMapping stm = parseSubstitutionMapping(st.getServiceTemplateId(), result);
    if (stm != null) {
      TemplateManager.getInstance()
          .addServiceTemplateMapping(TemplateDataHelper.convert2TemplateMappingData(stm));
    }
    
    return st.getServiceTemplateId();
  }
  

  /**
   * @param serviceTemplateId
   * @param result
   * @return
   */
  private SubstitutionMapping parseSubstitutionMapping(String serviceTemplateId,
      AriaParserResult result) {
    String type = getSubstitutionType(result);
    if (ToolUtil.isTrimedEmptyString(type)) {
      return null;
    }
    
    org.openo.commontosca.catalog.model.parser.yaml.aria.entity.AriaParserResult.Substitution stm =
        result.getSubstitution();
    return new SubstitutionMapping(
        serviceTemplateId,
        type,
        parseSubstitutionRequirements(stm.getRequirement()),
        parseSubstitutionCapabilities(stm.getCapabilities()));
  }


  /**
   * @param capabilities
   * @return
   */
  private Map<String, String[]> parseSubstitutionCapabilities(Mapping[] capabilities) {
    return parseMappings(capabilities);
  }


  private Map<String, String[]> parseMappings(Mapping[] mappings) {
    Map<String, String[]> ret = new HashMap<>();
    if (mappings != null) {
      for (Mapping mapping : mappings) {
        ret.put(mapping.getMapped_name(), new String[]{mapping.getNode_id(), mapping.getName()});
      }
    }

    return ret;
  }

  /**
   * @param requirement
   * @return
   */
  private Map<String, String[]> parseSubstitutionRequirements(Mapping[] requirement) {
    return parseMappings(requirement);
  }

  /**
   * @param result
   * @return
   */
  private String getSubstitutionType(AriaParserResult result) {
    if (result.getSubstitution() == null) {
      return null;
    }
    return result.getSubstitution().getNode_type_name();
  }


  /**
   * @param packageId
   * @param serviceTemplateId
   * @param result
   * @return
   */
  private List<NodeTemplate> parseNodeTemplates(String packageId, String serviceTemplateId,
      AriaParserResult result) {
    Node[] nodes = result.getNodes();
    if (nodes == null || nodes.length == 0) {
      return null;
    }

    List<NodeTemplate> retList = new ArrayList<>();
    for (Node node : nodes) {
      NodeTemplate ret = new NodeTemplate();
      ret.setId(node.getName());
      ret.setName(node.getName());
      ret.setType(node.getType_name());
      ret.setProperties(node.getPropertyAssignments());
      List<RelationShip> relationShipList =
          parseNodeTemplateRelationShip(node.getRelationships(), node);
      ret.setRelationShips(relationShipList);

      retList.add(ret);
    }

    return retList;
  }


  /**
   * @param relationships
   * @param sourceNode 
   * @return
   */
  private List<RelationShip> parseNodeTemplateRelationShip(Relationship[] relationships, Node sourceNode) {
    List<RelationShip> retList = new ArrayList<>();

    if (relationships == null || relationships.length == 0) {
      return retList;
    }

    for (Relationship relationship : relationships) {
      RelationShip ret = new RelationShip();
      ret.setSourceNodeId(sourceNode.getName());
      ret.setSourceNodeName(sourceNode.getName());
      ret.setTargetNodeId(relationship.getTemplate_name());
      ret.setTargetNodeName(relationship.getTemplate_name());
      ret.setType(relationship.getType_name());
      retList.add(ret);
    }

    return retList;
  }


  /**
   * @param result
   * @param packageId
   * @param downloadUri
   * @return
   */
  private ServiceTemplate parseServiceTemplate(AriaParserResult result, String packageId,
      String downloadUri) {
    ServiceTemplate st = new ServiceTemplate();

    st.setServiceTemplateId(ToolUtil.generateId());
    st.setTemplateName(result.getMetadata().get("template_name"));
    st.setVendor(result.getMetadata().get("template_author"));
    st.setVersion(result.getMetadata().get("template_version"));
    st.setCsarid(packageId);
    st.setDownloadUri(downloadUri);
    st.setInputs(parseInputs(result));
    st.setOutputs(parseOutputs(result));
    return st;
  }


  /**
   * @param result
   * @return
   */
  private InputParameter[] parseInputs(AriaParserResult result) {
    Map<String, Input> inputs = result.getInputs();
    if (inputs == null || inputs.isEmpty()) {
      return new InputParameter[0];
    }
    List<InputParameter> retList = new ArrayList<InputParameter>();
    for (Entry<String, Input> e : inputs.entrySet()) {
      retList.add(
          new InputParameter(
              e.getKey(),
              getEnumDataType(e.getValue().getType_name()),
              e.getValue().getDescription(),
              e.getValue().getValue(),
              false));
    }
    return retList.toArray(new InputParameter[0]);
  }
  
  /**
   * @param type
   * @return
   */
  private EnumDataType getEnumDataType(String type) {
    if (EnumDataType.INTEGER.toString().equalsIgnoreCase(type)) {
      return EnumDataType.INTEGER;
    }

    if (EnumDataType.FLOAT.toString().equalsIgnoreCase(type)) {
      return EnumDataType.FLOAT;
    }

    if (EnumDataType.BOOLEAN.toString().equalsIgnoreCase(type)) {
      return EnumDataType.BOOLEAN;
    }

    return EnumDataType.STRING;
  }


  /**
   * @param result
   * @return
   */
  private OutputParameter[] parseOutputs(AriaParserResult result) {
    Map<String, Output> outputs = result.getOutpus();
    if (outputs == null || outputs.isEmpty()) {
      return new OutputParameter[0];
    }
    
    List<OutputParameter> retList = new ArrayList<OutputParameter>();
    for (Entry<String, Output> e: outputs.entrySet()) {
      retList.add(
          new OutputParameter(
              e.getKey(), e.getValue().getDescription(), e.getValue().getValue()));
    }

    return retList.toArray(new OutputParameter[0]);
  }

  private AriaParserResult getAriaParserResult(String fileLocation) throws CatalogResourceException {
    String destPath = copyTemporaryFile2HttpServer(fileLocation);
    try {
      String url = getUrl(toTempFileLocalPath(fileLocation));
      return AriaParserServiceConsumer.parseCsarPackage(url);
    } finally {
      if (destPath != null && !destPath.isEmpty() && (new File(destPath)).exists()) {
        (new File(destPath)).delete();
      }
    }
  }

}
