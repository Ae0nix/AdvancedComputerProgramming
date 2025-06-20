import java.io.*;
import java.net.*;

public class TCPServer {
    public static void main(String[] args) {
        try {
            // Crea il server socket sulla porta 8080
            ServerSocket serverSocket = new ServerSocket(8080);
            System.out.println("Server avviato sulla porta 8080...");
            
            // Aspetta una connessione dal client
            Socket clientSocket = serverSocket.accept();
            System.out.println("Client connesso!");
            
            // Stream per leggere dal client
            BufferedReader in = new BufferedReader(
                new InputStreamReader(clientSocket.getInputStream())
            );
            
            // Stream per scrivere al client
            PrintWriter out = new PrintWriter(
                clientSocket.getOutputStream(), true
            );
            
            // Legge il messaggio dal client
            String messaggio = in.readLine();
            System.out.println("Messaggio ricevuto: " + messaggio);
            
            // Risponde al client
            out.println("Ciao dal server! Ho ricevuto: " + messaggio);
            
            // Chiude le connessioni
            clientSocket.close();
            serverSocket.close();
            
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}