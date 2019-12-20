#include <iostream>
#include <vector>

using namespace std;

// A utility function that returns maximum of two integers
int max(int a, int b) {
    return (a > b) ? a : b;
}

class Objeto {

public:
    int id, valor, peso;

    Objeto(int id, int peso, int valor) {
        this->id = id;
        this->peso = peso;
        this->valor = valor;
    }
};

class Mochila {

public:
    int valor;
    vector<Objeto> objetos;

    Mochila () {
        this->valor = 0;
    }

    Mochila combinar (Objeto objeto) {
        Mochila mochila;
        mochila.valor = this->valor + objeto.valor;
        mochila.objetos = this->objetos;
        mochila.objetos.push_back(objeto);

        return mochila;
    }

    void displayCompleto () {
        int peso_total = 0;

        for (Objeto objeto : this->objetos) {
            peso_total += objeto.peso;
        }

        cout << "Valor Total: " << this->valor << "\n";
        cout << "Peso Total: " << peso_total << "\n";
        cout << "Quantidade: " << this->objetos.size() << "\n";
        if (!this->objetos.empty()) {
            cout << "Objetos: \n";
            for (Objeto objeto : this->objetos) {
                cout << "\t Objeto " << objeto.id << ": Peso: " << objeto.peso << ", Valor: " << objeto.valor << "\n";
            }
        }

    }

};

Mochila knapSack(int tamanho_da_mochila, vector<Objeto> *objetos) {
    objetos->insert(objetos->begin(), objetos->at(0));

    Mochila K[objetos->size()][++tamanho_da_mochila];


    // Build table K[][] in bottom up manner
    for (int i = 1; i < objetos->size(); i++) {

        for (int j = 1; j < tamanho_da_mochila; j++) {

            if (objetos->at(i - 1).peso <= j) {

                if (objetos->at(i).valor + K[i - 1][j - objetos->at(i).peso].valor > K[i - 1][j].valor) {

                    K[i][j] = K[i - 1][j - objetos->at(i).peso].combinar(objetos->at(i));

                } else {

                    K[i][j] = K[i - 1][j];

                }

            } else {

                K[i][j] = K[i - 1][j];

            }
        }
    }

    return K[objetos->size() - 1][tamanho_da_mochila - 1];
}

int main() {

    int tamanho_da_mochila = 550;

    vector<Objeto> objetos = {
            Objeto(1, 26, 27),
            Objeto(2, 17, 31),
            Objeto(3, 23, 34),
            Objeto(4, 6, 8),
            Objeto(5, 5, 29),
            Objeto(6, 15, 21),
            Objeto(7, 28, 22),
            Objeto(8, 19, 24),
            Objeto(9, 20, 7),
            Objeto(10, 5, 25),
            Objeto(11, 15, 15),
            Objeto(12, 32, 32),
            Objeto(13, 11, 19),
            Objeto(14, 16, 32),
            Objeto(15, 11, 28),
            Objeto(16, 23, 28),
            Objeto(17, 30, 16),
            Objeto(18, 14, 28),
            Objeto(19, 20, 34),
            Objeto(20, 15, 11),
            Objeto(21, 26, 21),
            Objeto(22, 30, 16),
            Objeto(23, 30, 33),
            Objeto(24, 30, 27),
            Objeto(25, 18, 29),
            Objeto(26, 31, 22),
            Objeto(27, 35, 17),
            Objeto(28, 15, 9),
    };

    knapSack(tamanho_da_mochila, &objetos).displayCompleto();

    return 0;
}
