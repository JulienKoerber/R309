public class Test2 {
    public static void main(String[] args) {
        System.out.println("Table de multiplication de 1 à 10 :");
        
        // Afficher l'entête
        System.out.print("    ");
        for (int j = 1; j <= 10; j++) {
            System.out.printf("%4d", j);
        }
        System.out.println("\n-----------------------------------------------");
        
        // Afficher la table
        for (int i = 1; i <= 10; i++) {
            System.out.printf("%2d |", i);
            for (int j = 1; j <= 10; j++) {
                System.out.printf("%4d", i * j);
            }
            System.out.println();
        }
    }
}
