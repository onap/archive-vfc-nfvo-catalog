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
package org.openo.commontosca.catalog.model.externalservice.container;

import org.openo.commontosca.catalog.model.externalservice.entity.container.ContainerServiceNodeTemplateList;
import org.xml.sax.InputSource;
import org.xml.sax.XMLReader;
import org.xml.sax.helpers.XMLReaderFactory;

import java.io.IOException;
import java.io.InputStream;
import java.lang.annotation.Annotation;
import java.lang.reflect.Type;

import javax.ws.rs.WebApplicationException;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.MultivaluedMap;
import javax.ws.rs.ext.MessageBodyReader;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.Unmarshaller;
import javax.xml.transform.Source;
import javax.xml.transform.sax.SAXSource;

/**
 * The opentosca container service returns data to the node template entity.
 * 
 * @author 10189609
 * 
 */
public class ContainerServiceNodeTemplateProvider implements
    MessageBodyReader<ContainerServiceNodeTemplateList> {

  @Override
  public boolean isReadable(Class<?> type, Type genericType, Annotation[] annotations,
      MediaType mediaType) {
    return ContainerServiceNodeTemplateList.class.isAssignableFrom(type);
  }

  @Override
  public ContainerServiceNodeTemplateList readFrom(Class<ContainerServiceNodeTemplateList> type,
      Type genericType, Annotation[] annotations, MediaType mediaType,
      MultivaluedMap<String, String> httpHeaders, InputStream entityStream) throws IOException,
      WebApplicationException {
    ContainerServiceNodeTemplateList nodetemplatelist = null;

    try {
      JAXBContext jaxbContext = JAXBContext.newInstance(ContainerServiceNodeTemplateList.class);
      Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
      // ignore namespace
      NamespaceFilter inFilter = new NamespaceFilter(null, false);
      XMLReader reader = XMLReaderFactory.createXMLReader();
      inFilter.setParent(reader);
      Source source = new SAXSource(inFilter, new InputSource(entityStream));

      nodetemplatelist = (ContainerServiceNodeTemplateList) unmarshaller.unmarshal(source);
    } catch (Exception e1) {
      e1.printStackTrace();
    }

    return nodetemplatelist;
  }

}
