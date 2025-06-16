import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class CircularQueue {
    private final int maxDim = 10;
    private int[] queue;
    private int testa, coda;
    private int dim;

    private Lock lock;
    private Condition prod_cv, cons_cv;

    public Coda() {
        dim = 0;
        queue = new int[maxDim];
        testa = coda = 0;
        lock = new ReentrantLock();
        prod_cv = lock.newCondition();
        cons_cv = lock.newCondition();
    }

    public void inserisci(int e) throws InterruptedException {
        lock.lock();
        
        try{
            while (dim >= maxDim) {
                prod_cv.await();
            }

            dim++;
            queue[coda] = e;
            coda = (coda + 1) % maxDim;

            System.out.println("Inserito " + e + " in coda!");

            cons_cv.signal();
        }
        finally{
            lock.unlock();
        }
    }

    public int preleva() throws InterruptedException {
        int e;
        lock.lock();
        try{
            while (dim <= 0) {
                cons_cv.await();
            }

            dim--;
            e = queue[testa];
            testa = (testa + 1) % maxDim;

            System.out.println("Prelevato " + e + " dalla coda!");

            prod_cv.signal();
        }
        finally{
            lock.unlock();
        }

        return e;
    }
}