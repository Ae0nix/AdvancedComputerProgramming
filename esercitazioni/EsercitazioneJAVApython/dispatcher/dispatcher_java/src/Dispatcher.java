import java.util.Hashtable;
import javax.jms.*;
import javax.naming.*;

public class Dispatcher {
    


    public static void main(String[] args) {
        Hashtable<String, String> prop = new Hashtable<String, String> ();
        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");

        prop.put( "queue.request", "request");
        prop.put( "queue.response", "response");

        
        try {
            Context jndiContext = new InitialContext(prop);

            QueueConnectionFactory queueConnectionFactory = (QueueConnectionFactory) jndiContext.lookup("QueueConnectionFactory");

            Queue requestQueue = (Queue) jndiContext.lookup("request");

            try {
                QueueConnection requestQueueConnection = queueConnectionFactory.createQueueConnection();
                requestQueueConnection.start();

                QueueSession requestQueueSession = requestQueueConnection.createQueueSession(false, Session.AUTO_ACKNOWLEDGE);


                QueueReceiver receiver = requestQueueSession.createReceiver(requestQueue);
                TextMessage message;
                do{
                    System.out.println("In attesa di messaggi!");
                    message = (TextMessage) receiver.receive();
                    System.out.println("Messaggio ricevuto: " + message.getText());
                }while(message.getText().compareTo("fine") != 0);




            } catch (JMSException e) {
                e.printStackTrace();
            }



        } catch (NamingException e) {
            e.printStackTrace();
        }

        
    }
}
