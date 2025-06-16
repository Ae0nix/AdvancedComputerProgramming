import java.util.Hashtable;

import javax.jms.*;
import javax.naming.*;

public class Magazzino {

    
    public static void main(String[] args) {
        Hashtable<String, String> prop = new Hashtable<String, String> ();
        prop.put( "java.naming.factory.initial","org.apache.activemq.jndi.ActiveMQInitialContextFactory" );
        prop.put( "java.naming.provider.url", "tcp://127.0.0.1:61616" );

        prop.put("queue.request", "request");
        prop.put("queue.response", "response");

        
        try {
            Context jndiContext; jndiContext = new InitialContext(prop);

            QueueConnectionFactory queueConnFactory = (QueueConnectionFactory)jndiContext.lookup("QueueConnectionFactory");
            
            Queue queueRequest = (Queue)jndiContext.lookup("request");
            Queue queueResponse = (Queue)jndiContext.lookup("response");

            try {
                QueueConnection queueConnectionRequest = queueConnFactory.createQueueConnection();
                QueueConnection queueConnectionResponse = queueConnFactory.createQueueConnection();

                QueueSession queueSessionRequest = queueConnectionRequest.createQueueSession(false, Session.AUTO_ACKNOWLEDGE);
                QueueSession queueSessionResponse = queueConnectionResponse.createQueueSession(false, Session.AUTO_ACKNOWLEDGE);
                
                

            } catch (JMSException e) {
                e.printStackTrace();
            }



        } catch (NamingException e) {
            e.printStackTrace();
        }
    
    }
    
}
