from typing import List, Optional
from collections import deque
import copy

class Registro:
    """
    Representa um registro com CPF, nome e data de nascimento.
    """
    def __init__(self, cpf: str, nome: str, data_nasc: str):
        self.cpf = cpf
        self.nome = nome
        self.data_nasc = data_nasc
        self.deletado = False

    def __lt__(self, outro):
        return self.cpf < outro.cpf

    def __eq__(self, outro):
        return self.cpf == outro.cpf

    def __str__(self):
        return f"CPF: {self.cpf}, Nome: {self.nome}, Nascimento: {self.data_nasc}"

class NoABB:
    """
    Representa um nó da ABB, contendo um Registro e a posição na EDL.
    """
    def __init__(self, registro: Registro, posicao: int):
        self.registro = registro
        self.posicao = posicao
        self.esq = None
        self.dir = None

class ABB:
    """
    Implementa a Árvore Binária de Busca com registros.
    """
    def __init__(self, dados: Optional[List[tuple]] = None):
        self.raiz = None
        if dados:
            for posicao, dado in enumerate(dados):
                self.inserir(dado[0], posicao)

    def copiar(self):
        nova_abb = ABB()
        nova_abb.raiz = self._copiar_subarvore(self.raiz)
        return nova_abb

    def _copiar_subarvore(self, no):
        if no is None:
            return None
        novo = NoABB(copy.deepcopy(no.registro), no.posicao)
        novo.esq = self._copiar_subarvore(no.esq)
        novo.dir = self._copiar_subarvore(no.dir)
        return novo

    def inserir(self, registro: Registro, posicao: int):
        """
        Insere um registro na ABB com sua posição na EDL.
        """
        self.raiz = self._inserir_recursivo(self.raiz, registro, posicao)

    def _inserir_recursivo(self, no, registro, posicao):
        if no is None:
            return NoABB(registro, posicao)
        if registro < no.registro:
            no.esq = self._inserir_recursivo(no.esq, registro, posicao)
        elif registro > no.registro:
            no.dir = self._inserir_recursivo(no.dir, registro, posicao)
        return no

    def buscar(self, cpf: str):
        """
        Busca um registro na ABB pelo CPF.
        """
        return self._buscar_recursivo(self.raiz, cpf)

    def _buscar_recursivo(self, no, cpf):
        if no is None:
            return None
        if cpf == no.registro.cpf:
            return no
        if cpf < no.registro.cpf:
            return self._buscar_recursivo(no.esq, cpf)
        else:
            return self._buscar_recursivo(no.dir, cpf)

    def remover(self, cpf: str):
        """
        Remove um registro da ABB com base no CPF.
        """
        self.raiz = self._remover_recursivo(self.raiz, cpf)

    def _remover_recursivo(self, no, cpf):
        if no is None:
            return None
        if cpf < no.registro.cpf:
            no.esq = self._remover_recursivo(no.esq, cpf)
        elif cpf > no.registro.cpf:
            no.dir = self._remover_recursivo(no.dir, cpf)
        else:
            if no.esq is None:
                return no.dir
            elif no.dir is None:
                return no.esq
            sucessor = self._menor_no(no.dir)
            no.registro = sucessor.registro
            no.posicao = sucessor.posicao
            no.dir = self._remover_recursivo(no.dir, sucessor.registro.cpf)
        return no

    def _menor_no(self, no):
        while no.esq is not None:
            no = no.esq
        return no

    def limpar(self):
        """
        Deleta todos os nós da ABB.
        """
        self.raiz = self._limpar_pos_ordem(self.raiz)

    def _limpar_pos_ordem(self, no):
        if no is not None:
            no.esq = self._limpar_pos_ordem(no.esq)
            no.dir = self._limpar_pos_ordem(no.dir)
            del no
        return None

    def percurso_pre_ordem(self):
        """
        Retorna os registros em percurso pré-ordem.
        """
        return self._pre_ordem(self.raiz)

    def _pre_ordem(self, no):
        if no is None:
            return []
        return [no.registro] + self._pre_ordem(no.esq) + self._pre_ordem(no.dir)

    def percurso_in_ordem(self):
        """
        Retorna os registros em percurso in-ordem (ordenado).
        """
        return self._in_ordem(self.raiz)

    def _in_ordem(self, no):
        if no is None:
            return []
        return self._in_ordem(no.esq) + [no.registro] + self._in_ordem(no.dir)

    def percurso_pos_ordem(self):
        """
        Retorna os registros em percurso pós-ordem.
        """
        return self._pos_ordem(self.raiz)

    def _pos_ordem(self, no):
        if no is None:
            return []
        return self._pos_ordem(no.esq) + self._pos_ordem(no.dir) + [no.registro]

    def percurso_largura(self):
        """
        Retorna os registros em percurso por largura (nível).
        """
        if self.raiz is None:
            return []
        fila = deque([self.raiz])
        resultado = []
        while fila:
            no = fila.popleft()
            resultado.append(no.registro)
            if no.esq:
                fila.append(no.esq)
            if no.dir:
                fila.append(no.dir)
        return resultado

# Função para imprimir um registro da EDL via índice armazenado na ABB
def consultar_por_cpf(abb: ABB, edl: List[Registro], cpf: str):
    """
    Busca o CPF na ABB e mostra o registro completo da EDL correspondente.
    """
    no = abb.buscar(cpf)
    if no is None:
        print("Registro não encontrado.")
    else:
        registro = edl[no.posicao]
        if registro.deletado:
            print("Registro apagado.")
        else:
            print("Registro encontrado:")
            print(registro)

# Função para gerar nova EDL ordenada pelo CPF via percurso in-ordem
def gerar_edl_ordenada(abb: ABB, edl: List[Registro]) -> List[Registro]:
    """
    Cria nova EDL ordenada segundo percurso in-ordem da ABB.
    """
    nova_edl = []
    def inserir_ordenado(no):
        if no is not None:
            inserir_ordenado(no.esq)
            nova_edl.append(edl[no.posicao])
            inserir_ordenado(no.dir)
    inserir_ordenado(abb.raiz)
    return nova_edl

# Exemplo de uso (pode modificar à vontade)
if __name__ == "__main__":
    edl = []

    # Inserindo registros
    r1 = Registro("123", "Lucas", "2005-07-10")
    r2 = Registro("456", "Ana", "2002-03-15")
    r3 = Registro("789", "João", "1999-12-01")

    edl.append(r1)
    edl.append(r2)
    edl.append(r3)

    abb = ABB()
    abb.inserir(r1, 0)
    abb.inserir(r2, 1)
    abb.inserir(r3, 2)

    consultar_por_cpf(abb, edl, "456")

    print("\nRegistros ordenados:")
    edl_ordenada = gerar_edl_ordenada(abb, edl)
    for r in edl_ordenada:
        print(r)