Para inicializar o gerador, abrir a linha de comandos na pasta do script e correr o comando:

python generator.py run_name n_cells n_inter_nodes n_edges it_steps replicas env_set

run_name		nome da simulação/ensaio
n_inter_nodes	número de nós intermédios
n_edges			número de ligações entre nós (inclui ligações com nós de input e output também)
it_steps		passos de interação da avaliação booleana
replicas		número de réplicas
env_set			nome do ambiente em que se está a testar

exemplo:

python generator.py 10_30_2OVn 1000 10 30 5 5 2OVn.env