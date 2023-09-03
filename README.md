<h1> Simple Cache Simulator </h1>
<h3> AOCII - Cache Simulator</h3>
Este projeto consiste em um simulador de cache, desenvolvido em linguagem python para a disciplina de AOCII.
<h2>Features:</h2>
O simulador é capaz de simular caches diretamente mapeadas, totalmente associativas, ou conjunto-associativas
Conta com três políticas de substituição para caches com associatividade, mapeadas da seguinte forma:
R: Random é a política padrão, e, quando chamada, escolhe aleatoriamente entre os blocos do conjunto, remove o que estiver lá armazenado, e então insere o novo dado em seu lugar
F: FIFO, ou First In First Out, implementa uma fila por conjunto, que armazena a ordem em que dados foram inseridos no mesmo. Sempre que há escrita na cache, a posição onde ocorreu a escrita é adicionada à direita da fila. Ao ser chamada, a função de substituição remove da cache a posição que está mais à esquerda, ou seja, armazenada a mais tempo, substitui seu conteúdo, e a reinsere à direita da fila. Desta forma, armazenamos na fila apenas a posição que não é alterada a mais tempo, deixando que o conteúdo da mesma seja armazenado apenas na cache.
L: LRU, ou Least Recently Used, também implementa uma fila, mas esta armazena em sua direita a última posição a ser referenciada, seja por escrita ou por leitura. Sempre que ocorre um acesso à cache, a posição que foi acessada é removida da fila, e reinserida à direita da mesma. A função de substituição é idêntica à FIFO, pois o controle de frequência é feito durante o acesso à cache.

<H2>Uso:</H2>
Da linha de comando, na pasta "cache-simulator", utilizar o seguinte comando:

  python cache_simulator.py <nsets> <bsize> <assoc> <substituição> <flag_saida> arquivo_de_entrada

Sendo:
nsets: Número de conjuntos na cache a ser simulada. Use 1 para totalmente associativa
bsize: Número de bytes por bloco da cache
assoc: Associatividade. Use 1 para diretamente mapeada
substituição: Política de susbstituição, como definida acima. Usar apenas R, L ou F. Qualquer outro valor deve resultar em Random
flag_saida: Flag para selecionar o tipo de output. 0 para pessoas, 1 para o bot do professor
arquivo_de_entrada: caminho para o arquivo de entrada
