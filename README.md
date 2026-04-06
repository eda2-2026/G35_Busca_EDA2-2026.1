# La Dolce Cakes 

Bem-vindo à La Dolce Cakes, uma loja virtual criada para a venda de bolos artesanais.

Além das funcionalidades de um e-commerce feitas anteriormente, neste trabalho implementamos uma solução que foca em transformar a experiência de navegação no catálogo de bolos em algo instantâneo. Para isso, combinamos duas estratégias:

1. *Busca por Prefixo via Trie:* Para fornecer sugestões de autocompletar em tempo real.
2. *Busca por Substring (Fallback):* Uma varredura em profundidade (DFS) na árvore para encontrar termos no meio do nome (ex: encontrar "Bolo de *Limão*" ao digitar apenas "limao").

A ideia foi unir teoria e prática, criando uma aplicação funcional com uma busca inteligente que melhora a experiência do usuário.

<br>



## Funcionalidades:

• Página Home;

• Catálogo de bolos: mostra os produtos cadastrados;

• Busca inteligente: sugestões aparecem enquanto o usuário digita;

• Carrinho: adicionar, remover e visualizar itens;

• Área do cliente: cadastro, login e edição de perfil;

• Admin: controle total dos produtos e usuários;<br>

## Estruturas de Dados 
 
 ### 1. Árvore de Prefixo (Trie)
 
  Trie (ou árvore de prefixo) é uma estrutura de dados do tipo árvore multidirecional (ou árvore $m$-ária). Diferente de uma árvore binária, que se limita a dois descendentes por nó, a Trie permite múltiplas ramificações baseadas no alfabeto utilizado (ex: 'a' a 'z'). Cada nó da árvore representa um único caractere de uma palavra.
  
  Raiz: Representa uma string vazia (o ponto de partida).
  Caminho: O percurso da raiz até um nó marcado como "fim de palavra" reconstrói o nome de um bolo.
  Payload: Cada nó final armazena um objeto {id, label}, permitindo recuperar os dados do bolo instantaneamente ao completar um termo.
  
  ### Aplicação no Projeto
  Cada nó da árvore funciona como um guia. Ao digitar "CEN", o algoritmo navega pelos nós 'C' → 'E' → 'N' e retorna todos os descendentes deste caminho (ex: "Cenoura", "Cenourinha"). Isso elimina a necessidade de percorrer todo o banco de dados a cada tecla pressionada, filtrando instantaneamente os resultados que não compartilham o mesmo prefixo.
  
  ### Vantagem  e Desempenho
  Por ser uma estrutura multidirecional, a busca não depende do número total de itens no catálogo ($n$), mas apenas do comprimento do termo digitado ($k$).Busca em Banco Comum (SQL): Geralmente $O(n)$, exigindo varredura completa da tabela.Busca na Trie: $O(k)$. Isso garante que a sugestão de bolos seja instantânea, independentemente do tamanho da base de dados.

## Screenshots
• Esta imagem mostra o usuário digitando "pesse" (sem maiúscula e sem acento). O sistema reage in.stantaneamente, mostrando "Bolo de Pêssego" corretamente formatado.

![1](./app/static/images/Captura%20de%20tela%202026-04-06%20171153.png)

•Esta imagem mostra o usuário digitando "Bolo de c" (com 'c' minúsculo e 'Bolo' maiúsculo). A busca reage instantaneamente, mostrando uma lista de sugestões que completam o prefixo.

![2](./app/static/images/Captura%20de%20tela%202026-04-06%20171108.png)

•Esta imagem mostra o usuário digitando "moran" (com 'm' minúsculo). A busca reage instantaneamente, mostrando uma lista de sugestões relevantes baseadas no termo, mesmo que ele esteja no meio da string.

![3](./app/static/images/Captura%20de%20tela%202026-04-06%20171320.png)


## Tecnologias utilizadas:
• Backend: Python / Django (Conceitos de CRUD, Serialização, POO).

• Frontend: HTML5, CSS3, JavaScript (Fetch API para busca).

• Dados: Estrutura de dados Trie.

• Infraestrutura: Docker & Docker Compose.
<br>

## Como Rodar o Projeto
1. Subir os containers:

``docker-compose up -d --build``

<br>

3. Preparar o banco de dados:

``docker-compose exec web python manage.py migrate``

``docker-compose exec web python manage.py loaddata app/loja/fixtures/bolos.json``

``docker-compose exec web python manage.py createsuperuser``

<br>
5. Gerar a árvore de busca (Trie):

``docker-compose exec web python manage.py build_trie``

<br>
7. Acessar:
http://localhost:8000

<br>

## Vídeo

[Projeto de EDA2 - Sistema de Busca com Trie ](https://youtu.be/lFahU0GUPrY)

## Integrantes da Equipe

|  |Matrícula | Aluno |  
|-- | -- | -- |
|  <div align="center"><img src="https://github.com/GeovannaUmbelino.png" alt="geovanna" width="90"></div>  | 23/2014450  | <span style="color:black;">[Geovanna Umbelino](https://github.com/GeovannaUmbelino)</span>   |
| <div align="center"><img src="https://github.com/Sunamit.png" alt="sunamita" width="90"></div> | 22/1008697  | <span style="color:black;">[Sunamita Vitória](https://github.com/Sunamit)</span>    |



