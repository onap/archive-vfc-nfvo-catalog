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
package org.openo.commontosca.catalog.wrapper;

import static org.junit.Assert.assertEquals;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonPrimitive;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Assert;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openo.commontosca.catalog.CatalogAppConfiguration;
import org.openo.commontosca.catalog.common.Config;
import org.openo.commontosca.catalog.common.HttpServerAddrConfig;
import org.openo.commontosca.catalog.common.HttpServerPathConfig;
import org.openo.commontosca.catalog.common.MsbAddrConfig;
import org.openo.commontosca.catalog.common.ToolUtil;
import org.openo.commontosca.catalog.db.dao.DaoManager;
import org.openo.commontosca.catalog.db.entity.NodeTemplateData;
import org.openo.commontosca.catalog.db.entity.PackageData;
import org.openo.commontosca.catalog.db.entity.ServiceTemplateData;
import org.openo.commontosca.catalog.db.entity.ServiceTemplateMappingData;
import org.openo.commontosca.catalog.db.entity.TemplateData;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.db.resource.PackageManager;
import org.openo.commontosca.catalog.db.resource.TemplateManager;
import org.openo.commontosca.catalog.db.util.H2DbServer;
import org.openo.commontosca.catalog.db.util.HibernateSession;
import org.openo.commontosca.catalog.model.entity.InputParameter;
import org.openo.commontosca.catalog.model.entity.NodeTemplate;
import org.openo.commontosca.catalog.model.entity.OutputParameter;
import org.openo.commontosca.catalog.model.entity.Parameters;
import org.openo.commontosca.catalog.model.entity.QueryRawDataCondition;
import org.openo.commontosca.catalog.model.entity.RelationShip;
import org.openo.commontosca.catalog.model.entity.ServiceTemplate;
import org.openo.commontosca.catalog.model.entity.ServiceTemplateOperation;
import org.openo.commontosca.catalog.model.entity.ServiceTemplateRawData;
import org.openo.commontosca.catalog.model.wrapper.ServiceTemplateWrapper;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;


public class ServiceTemplateWrapperTest {
  private static ServiceTemplateWrapper serviceTemplateWrapper;
  private static TemplateManager templateManager;
  private static PackageManager packageManager;
  
  static {
    CatalogAppConfiguration configuration = new CatalogAppConfiguration();
    Config.setConfigration(configuration);
    Config.getConfigration().setMsbServerAddr("http://127.0.0.1:80");
    
    HttpServerAddrConfig.setHttpServerAddress("http://127.0.0.1:8201");
    HttpServerPathConfig.setHttpServerPath("../tomcat/webapps/ROOT/");
  }
  
  /**
   * startup db session before class.
   */
  @BeforeClass
  public static void setUpBeforeClass() {
    H2DbServer.startUp();
    DaoManager.getInstance().setDaoNull();
    DaoManager.getInstance().setSessionFactory(HibernateSession.init());
    serviceTemplateWrapper = ServiceTemplateWrapper.getInstance();
    templateManager = TemplateManager.getInstance();
    packageManager = PackageManager.getInstance();
    CatalogAppConfiguration configuration = new CatalogAppConfiguration();
    Config.setConfigration(configuration);
    System.out.println("Set up before class");
  }
  
  /**
   * clean database.
   */
  @Before
  public void setUp() throws Exception {
    /*Response packageListResult = packageWrapper.queryPackageListByCond(null,
        null, null, null, null);
    @SuppressWarnings("unchecked")
    ArrayList<PackageMeta> packageList = (ArrayList<PackageMeta>) packageListResult.getEntity();
    for (PackageMeta packageMeta:packageList) {
      String csarId = packageMeta.getCsarId();
      packageWrapper.delPackage(csarId);
    }*/
    ArrayList<ServiceTemplateData> servicetemplates = templateManager.queryServiceTemplate(
        null, null, null);
    if (null != servicetemplates && servicetemplates.size() > 0) {
      for (int i = 0; i < servicetemplates.size(); i++) {
        String serviceTemplateId = servicetemplates.get(i).getServiceTemplateId();
        templateManager.deleteServiceTemplateById(serviceTemplateId);
      }
    }
    //uploadPackage();
    TemplateData templateData = new TemplateData();
    templateData = setTemplateData();
    templateManager.addServiceTemplate(templateData);
    
    ServiceTemplateMappingData templateMappingData = new ServiceTemplateMappingData();
    templateMappingData = setTemplateMappingData();
    templateManager.addServiceTemplateMapping(templateMappingData);
    
    ArrayList<PackageData> packageList = packageManager.queryPackage(null, null, null, null, null);
    if (packageList != null && packageList.size() > 0) {
      for (int i = 0; i < packageList.size(); i++) {
        String packageOid = packageList.get(i).getCsarId();
        packageManager.deletePackage(packageOid);
      }
    }
    PackageData packageData = new PackageData();
    packageData = getPackageData();
    packageManager.addPackage(packageData);
    
    //ArrayList<ServiceTemplateData> serviceTemplates = templateManager
    //.queryServiceTemplate(null, null, null);
    //ArrayList<NodeTemplateData> nodeTemplateDatas = templateManager
    //.queryNodeTemplateBySeriviceTemplateId("serviceTemplateId");
    System.out.println("Set up before");
  }
  
  

  @Test
  public void testGetServiceTemplates() throws CatalogResourceException {
    ServiceTemplate[] expectResult = getExpectServiceTemplates();
    ServiceTemplate[] result1 = serviceTemplateWrapper.getServiceTemplates(null, false);
    assertEquals(expectResult, result1);
    
    ServiceTemplate[] result2 = serviceTemplateWrapper.getServiceTemplates("InUse", false);
    assertEquals(expectResult, result2);
  }
  
  @Test
  public void testGetNestingServiceTemplate() throws CatalogResourceException {
    ServiceTemplate[] expectResult = getExpectServiceTemplates();
    String[] nodeTypeIds = new String[]{"tosca.nodes.nfv.VL"};
    ServiceTemplate[] result = serviceTemplateWrapper.getNestingServiceTemplate(nodeTypeIds);
    assertEquals(expectResult, result);
  }
  
  @Test
  public void testGetNodeTemplatesByType() throws CatalogResourceException {
    NodeTemplate[] expectResult = getExpectNodeTemplates();
    NodeTemplate[] result1 = serviceTemplateWrapper.getNodeTemplates("serviceTemplateId", null);
    assertEquals(1, result1.length);
    result1[0].setId("nodeTemplateId");
    assertEquals(expectResult, result1);
    
    String[] types = {"tosca.nodes.nfv.VL"};
    NodeTemplate[] result2 = serviceTemplateWrapper.getNodeTemplates("serviceTemplateId", types);
    assertEquals(1, result2.length);
    result2[0].setId("nodeTemplateId");
    assertEquals(expectResult, result2);
  }
  
  @Test
  public void testGetNodeTemplateById() throws CatalogResourceException {
    NodeTemplate[] nodeTemplates = serviceTemplateWrapper.getNodeTemplates(
        "serviceTemplateId", null);
    NodeTemplate result = new NodeTemplate();
    if (null != nodeTemplates && nodeTemplates.length > 0) {
      String nodeTemplateId = nodeTemplates[0].getId();
      result = serviceTemplateWrapper.getNodeTemplateById(
          "serviceTemplateId", nodeTemplateId);
      result.setId("nodeTemplateId");
    }
    NodeTemplate expectResult = getExpectNodeTemplate();
    assertEquals(expectResult, result);
  }
  
  @Test
  public void testGetServiceTemplateOperations() throws CatalogResourceException {
    ServiceTemplateOperation[] expectResult = getServiceTemplateOperation();
    ServiceTemplateOperation[] result = serviceTemplateWrapper
        .getTemplateOperations("serviceTemplateId");
    assertEquals(expectResult, result);
  }
  
  @Test
  public void testGetServiceTemplateById() throws CatalogResourceException {
    ServiceTemplate expectResult = getExpectServiceTemplate();
    ServiceTemplate result = serviceTemplateWrapper.getServiceTemplateById("serviceTemplateId");
    assertEquals(expectResult, result);
  }
  
  @Test
  public void testGetServiceTemplateParameters() throws CatalogResourceException {
    Parameters expectResult = getParameters();
    Parameters result = serviceTemplateWrapper.getServiceTemplateParameters("serviceTemplateId");
    assertEquals(expectResult, result);
  }
  
  @Test
  public void testGetParametersByOperationName() throws CatalogResourceException {
    InputParameter[] expectResult = getServiceTemplateInputs();
    InputParameter[] result = serviceTemplateWrapper.getParametersByOperationName(
        "serviceTemplateId", "init");
    assertEquals(expectResult, result);
  }

  @Test
  public void testGetServiceTemplateRawData() throws Exception {
    ServiceTemplateRawData expectResult = new ServiceTemplateRawData();
    expectResult.setRawData("rawData");
    QueryRawDataCondition queryCondition = new QueryRawDataCondition();
    queryCondition.setCsarId("123456");
    ServiceTemplateRawData result = serviceTemplateWrapper
        .getServiceTemplateRawData(queryCondition);
    assertEquals(expectResult, result);
  }
  
  /**
   * delete data after test.
   */
  @After
  public void tearDown() throws Exception {
    packageManager.deletePackage("123456");
    templateManager.deleteServiceTemplateById("serviceTemplateId");
    templateManager.deleteServiceTemplateMapping(null, "serviceTemplateId");
    System.out.println("Tear down");
  }
  
  /**
   * destory db session after class.
   */
  @AfterClass
  public static void tearDownAfterClass() {
    try {
      HibernateSession.destory();
      DaoManager.getInstance().setDaoNull();
      H2DbServer.shutDown();
    } catch (Exception e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
  }

  /*private void uploadPackage() {
    InputStream ins = null;
    
    FormDataContentDisposition fileDetail =
        FormDataContentDisposition.name("fileName").fileName("NanocellGW.csar").build();

    try {
      resourcePath = HibernateSession.class.getResource("/").toURI().getPath();
    } catch (URISyntaxException e1) {
      e1.printStackTrace();
    }
    final String filename = "NanocellGW.csar";
    File packageFile = new File(resourcePath + filename);
    try {
      ins = new FileInputStream(packageFile);
    } catch (FileNotFoundException e2) {
      e2.printStackTrace();
    }
    if (ins != null) {
      try {
        PackageWrapper.getInstance().uploadPackage(ins, fileDetail, null);
      } catch (Exception e3) {
        e3.printStackTrace();
      }
    }
  }*/
  
  private TemplateData setTemplateData() {
    ServiceTemplateData serviceTemplate = new ServiceTemplateData();
    ArrayList<NodeTemplateData> nodeTemplates = new ArrayList<NodeTemplateData>();
    NodeTemplateData nodeTemplate = new NodeTemplateData();
    serviceTemplate = setServiceTemplate();
    nodeTemplate = setNodeTemplate();
    nodeTemplates.add(nodeTemplate);
    TemplateData templateData = new TemplateData();
    templateData.setServiceTemplate(serviceTemplate);
    templateData.setNodeTemplates(nodeTemplates);
    return templateData;
  }

  private NodeTemplateData setNodeTemplate() {
    NodeTemplateData nodeTemplate = new NodeTemplateData();
    nodeTemplate.setName("nodeName");
    nodeTemplate.setNodeTemplateId("nodeTemplateId");
    String properties = "{\"cidr\":\"\",\"gateWay\":\"\",\"dhcp\":\"\"}";
    nodeTemplate.setProperties(properties);
    String relationShips = "[{\"sourceNodeName\":\"endpoint.vlan2\","
        + "\"targetNodeName\":\"VLAN\","
        + "\"sourceNodeId\":\"tosca_nodes_nfv_CP_4\","
        + "\"targetNodeId\":\"tosca_nodes_nfv_VL_1\","
        + "\"type\":\"tosca.relationships.nfv.VirtualLinksTo\"}]";
    nodeTemplate.setRelationShips(relationShips);
    nodeTemplate.setServiceTemplateId("serviceTemplateId");
    nodeTemplate.setType("tosca.nodes.nfv.VL");
    return nodeTemplate;
  }

  private ServiceTemplateData setServiceTemplate() {
    ServiceTemplateData serviceTemplate = new ServiceTemplateData();
    serviceTemplate.setCsarId("123456");
    serviceTemplate.setDownloadUri(MsbAddrConfig.getMsbAddress() 
        + "/files/catalog/NSAR/ZTE/NanocellGW/v1.0/Definitions/segw.yml");
    String inputs = "{\"inputs\":[{\"name\": \"SubscribersPerNfc\","
        + "\"type\": \"STRING\",\"description\": \"\",\"required\": false}],"
        + "\"outputs\":[]}";
    serviceTemplate.setInputs(inputs);
    String operations = "[{\"name\":\"init\",\"description\":\"\","
        + "\"packageName\":\"NanocellGW\",\"processId\":\"\","
        + "\"inputs\":[{\"name\": \"SubscribersPerNfc\","
        + "\"type\": \"STRING\",\"description\": \"\","
        + "\"required\": false}]}]";
    serviceTemplate.setOperations(operations);
    serviceTemplate.setRowData("rawData");
    serviceTemplate.setServiceTemplateId("serviceTemplateId");
    serviceTemplate.setTemplateName("templateName");
    serviceTemplate.setType("NS");
    serviceTemplate.setVendor("ZTE");
    serviceTemplate.setVersion("0.0.1");
    return serviceTemplate;
  }
  
  private ServiceTemplateMappingData setTemplateMappingData() {
    ServiceTemplateMappingData mappingData = new ServiceTemplateMappingData();
    mappingData.setCapabilities("");
    mappingData.setMappingId("mappingId");
    mappingData.setNodeType("tosca.nodes.nfv.VL");
    mappingData.setRequirements("");
    mappingData.setServiceTemplateId("serviceTemplateId");
    return mappingData;
  }
  
  private ServiceTemplate[] getExpectServiceTemplates() {
    ServiceTemplate serviceTemplate = new ServiceTemplate();
    serviceTemplate = getExpectServiceTemplate();
    ServiceTemplate[] serviceTemplates = new ServiceTemplate[1];
    serviceTemplates[0] = serviceTemplate;
    return serviceTemplates;
  }
  
  private ServiceTemplate getExpectServiceTemplate() {
    ServiceTemplate serviceTemplate = new ServiceTemplate();
    serviceTemplate.setCsarid("123456");
    serviceTemplate.setDownloadUri(MsbAddrConfig.getMsbAddress() 
        + "/files/catalog/NSAR/ZTE/NanocellGW/v1.0/Definitions/segw.yml");
    InputParameter[] inputs = getServiceTemplateInputs();
    serviceTemplate.setInputs(inputs);
    ServiceTemplateOperation[] operations = getServiceTemplateOperation();
    serviceTemplate.setOperations(operations);
    OutputParameter[] outputs = getOutputs();
    serviceTemplate.setOutputs(outputs);
    serviceTemplate.setServiceTemplateId("serviceTemplateId");
    serviceTemplate.setTemplateName("templateName");
    serviceTemplate.setType("NS");
    serviceTemplate.setVendor("ZTE");
    serviceTemplate.setVersion("0.0.1");
    return serviceTemplate;
  }

  private OutputParameter[] getOutputs() {
    String outputsStr = "[]";
    OutputParameter[] outputs = ToolUtil.fromJson(outputsStr, OutputParameter[].class);
    return outputs;
  }

  private ServiceTemplateOperation[] getServiceTemplateOperation() {
    String operationsStr = "[{\"name\":\"init\",\"description\":\"\","
        + "\"packageName\":\"NanocellGW\",\"processId\":\"\","
        + "\"inputs\":[{\"name\": \"SubscribersPerNfc\","
        + "\"type\": \"STRING\",\"description\": \"\","
        + "\"required\": false}]}]";
    ServiceTemplateOperation[] operations = ToolUtil.fromJson(operationsStr,
        ServiceTemplateOperation[].class);
    return operations;
  }

  private InputParameter[] getServiceTemplateInputs() {
    String inputsStr = "[{\"name\": \"SubscribersPerNfc\","
        + "\"type\": \"STRING\",\"description\": \"\",\"required\": false}]";
    InputParameter[] inputs = ToolUtil.fromJson(inputsStr, InputParameter[].class);
    return inputs;
  }
  
  private Parameters getParameters() {
    String parametersStr = "{\"inputs\":[{\"name\": \"SubscribersPerNfc\","
        + "\"type\": \"STRING\",\"description\": \"\",\"required\": false}],"
        + "\"outputs\":[]}";
    Parameters parameters = ToolUtil.fromJson(parametersStr, Parameters.class);
    return parameters;
  }
  
  private NodeTemplate[] getExpectNodeTemplates() {
    NodeTemplate nodeTemplate = new NodeTemplate();
    nodeTemplate = getExpectNodeTemplate();
    NodeTemplate[] nodeTemplates = new NodeTemplate[1];
    nodeTemplates[0] = nodeTemplate;
    return nodeTemplates;
  }
  
  private NodeTemplate getExpectNodeTemplate() {
    NodeTemplate nodeTemplate = new NodeTemplate();
    nodeTemplate.setId("nodeTemplateId");
    nodeTemplate.setName("nodeName");
    String propertiesStr = "{\"cidr\":\"\",\"gateWay\":\"\",\"dhcp\":\"\"}";
    Map<String, Object> properties = convert2Property(propertiesStr);
    nodeTemplate.setProperties(properties);
    String relationShipsStr = "[{\"sourceNodeName\":\"endpoint.vlan2\","
        + "\"targetNodeName\":\"VLAN\","
        + "\"sourceNodeId\":\"tosca_nodes_nfv_CP_4\","
        + "\"targetNodeId\":\"tosca_nodes_nfv_VL_1\","
        + "\"type\":\"tosca.relationships.nfv.VirtualLinksTo\"}]";
    List<RelationShip> relationShips = convert2RelationShipList(relationShipsStr);
    nodeTemplate.setRelationShips(relationShips);
    nodeTemplate.setType("tosca.nodes.nfv.VL");
    return nodeTemplate;
  }
  
  private Map<String, Object> convert2Property(String properties) {
    JsonObject jsonObject = new Gson().fromJson(properties, JsonObject.class);
    return parseMapValue(jsonObject);
  }

  private Map<String, Object> parseMapValue(JsonObject jsonObject) {
    Map<String, Object> map = new HashMap<>();

    Iterator<Entry<String, JsonElement>> iterator = jsonObject.entrySet().iterator();
    while (iterator.hasNext()) {
      Entry<String, JsonElement> next = iterator.next();
      if (next.getValue() instanceof JsonPrimitive) {
        map.put(next.getKey(), next.getValue().getAsString());
        continue;
      }

      if (next.getValue() instanceof JsonObject) {
        map.put(next.getKey(), parseMapValue((JsonObject) next.getValue()));
        continue;
      }
    }
    return map;
  }
  
  private List<RelationShip> convert2RelationShipList(String srelationShips) {
    RelationShip[] relationShips = ToolUtil.fromJson(srelationShips, RelationShip[].class);
    return Arrays.asList(relationShips);
  }
  
  private PackageData getPackageData() {
    PackageData packageData = new PackageData();
    packageData.setCsarId("123456");
    packageData.setCreateTime("2016-06-29 03:33:15");
    packageData.setDeletionPending("false");
    packageData.setDownloadUri("/NSAR/ZTE/NanocellGW/v1.0/");
    packageData.setFormat("yml");
    packageData.setModifyTime("2016-06-29 03:33:15");
    packageData.setName("NanocellGW");
    packageData.setOnBoardState("non-onBoarded");
    packageData.setOperationalState("Disabled");
    packageData.setProvider("ZTE");
    packageData.setSize("0.93M");
    packageData.setType("NSAR");
    packageData.setUsageState("InUse");
    packageData.setVersion("V1.0");
    packageData.setProcessState("normal");
    return packageData;
  }
}
