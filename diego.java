package AtividadeFinal;

import java.util.*;

class Item {
    String nome;
    int peso;
    int valor;

    public Item(String nome, int peso, int valor) {
        this.nome = nome;
        this.peso = peso;
        this.valor = valor;
    }
}

class ProblemaDaMochila {
    public static void mochila(int capacidade, List<Item> itens) {
        int n = itens.size();
        int[][] max = new int[n + 1][capacidade + 1];

        for (int i = 1; i <= n; i++) {
            Item item = itens.get(i - 1);
            for (int w = 1; w <= capacidade; w++) {
                if (item.peso <= w) {
                    max[i][w] = Math.max(max[i - 1][w], max[i - 1][w - item.peso] + item.valor);
                } else {
                    max[i][w] = max[i - 1][w];
                }

                System.out.println("max[" + i + "][" + w + "] = " + max[i][w]);
            }
        }

        int w = capacidade;
        List<Item> ItensSelec = new ArrayList<>();
        for (int i = n; i > 0 && w > 0; i--) {
            if (max[i][w] != max[i - 1][w]) {
                Item item = itens.get(i - 1);
                ItensSelec.add(item);
                w -= item.peso;
            }
        }

        System.out.println("Itens selecionados:");
        for (Item item : ItensSelec) {
            System.out.println(item.nome + " (Peso: " + item.peso + ", Valor: " + item.valor + ")");
        }
    }

    public static void main(String[] args) {
        List<Item> itens = new ArrayList<>();
        itens.add(new Item("Computador", 3, 2000));
        itens.add(new Item("Fone", 1, 500));
        itens.add(new Item("Camera", 4, 1500));
        itens.add(new Item("Livro", 2, 300));

        int capacidade = 4;
        mochila(capacidade, itens);
    }
}
