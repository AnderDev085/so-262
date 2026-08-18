public class Factory
{
	public static void main(String args[]) {
        System.out.println("Aluno: Anderson de Oliveira Leite");
		Buffer server = new BoundedBuffer();

      		// now create the producer and consumer threads
      		Thread producerThread = new Thread(new Producer(server));
      		Thread consumerThread = new Thread(new Consumer(server));
      
      		producerThread.start();
      		consumerThread.start();               
	}
}