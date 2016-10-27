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

import org.cometd.annotation.Listener;
import org.cometd.annotation.ServerAnnotationProcessor;
import org.cometd.annotation.Service;
import org.cometd.bayeux.Message;
import org.cometd.bayeux.server.BayeuxServer;
import org.cometd.bayeux.server.ServerChannel;
import org.cometd.bayeux.server.ServerMessage;
import org.cometd.bayeux.server.ServerSession;
import org.cometd.server.BayeuxServerImpl;
import org.cometd.server.authorizer.GrantAuthorizer;
import org.cometd.server.ext.AcknowledgedMessagesExtension;
import org.cometd.server.ext.TimesyncExtension;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import javax.servlet.GenericServlet;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.UnavailableException;
import javax.servlet.http.HttpServletResponse;


public class CometdServlet extends GenericServlet {
  private static final long serialVersionUID = 8807005039926977330L;

  private static final Logger logger = LoggerFactory.getLogger(CometdServlet.class);

  @Override
  public void init() throws ServletException {
    super.init();

    final BayeuxServerImpl bayeux =
        (BayeuxServerImpl) getServletContext().getAttribute(BayeuxServer.ATTRIBUTE);
    if (bayeux == null) {
      throw new UnavailableException("No BayeuxServer!");
    }
    // Create extensions
    bayeux.addExtension(new TimesyncExtension());
    bayeux.addExtension(new AcknowledgedMessagesExtension());

    // Allow anybody to handshake
    bayeux.getChannel(ServerChannel.META_HANDSHAKE).addAuthorizer(GrantAuthorizer.GRANT_PUBLISH);

    ServerAnnotationProcessor processor = new ServerAnnotationProcessor(bayeux);
    processor.process(new CatalogComet());

    CometdUtil.setBayeuxServer(bayeux);
  }

  @Service("catalog")
  public static class CatalogComet {
    @Listener("/meta/subscribe")
    public void catalogSubscribe(ServerSession session, ServerMessage message) {
      logger.info("Catalog Subscribe from " + session + " for "
          + message.get(Message.SUBSCRIPTION_FIELD));
    }

    @Listener("/meta/unsubscribe")
    public void catalogUnsubscribe(ServerSession session, ServerMessage message) {
      logger.info("Catalog Unsubscribe from " + session + " for "
          + message.get(Message.SUBSCRIPTION_FIELD));
    }

    @Listener("/meta/*")
    public void catalogMeta(ServerSession session, ServerMessage message) {
      logger.debug(message.toString());
    }
  }

  @Override
  public void service(ServletRequest servletRequest, ServletResponse servletResponse)
      throws ServletException, IOException {
    ((HttpServletResponse) servletResponse).sendError(503);
  }
}
