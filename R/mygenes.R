prob.duplic = 0.05
prob.mut =  0.05
prob.elim = 0.05
n.cells = 100
n.gen = 100

it.steps = 5
replicas = 3
s.fitness = T
# to get from .env file
#env_name = '4NOn'
n.input = 8
n.output = 8
env.in = rbind(c(1,1,0,0,0,0,0,0),
               c(0,0,1,1,0,0,0,0),
               c(0,0,0,0,1,1,0,0),
               c(0,0,0,0,0,0,1,1))
env.out = rbind(c(1,1,0,0,0,0,0,0),
               c(0,0,1,1,0,0,0,0),
               c(0,0,0,0,1,1,0,0),
               c(0,0,0,0,0,0,1,1))

test = matrix(c(1,1,0,0,0,1,0,0,0),3,3)

duplic = function(x) {
  to.duplic = which(runif(dim(x)[1])<prob.duplic)
  n = length(to.duplic)
  to.add = matrix(NA, n, n)
  x = rbind(x, x[to.duplic,])
  x = cbind(x, c(x[,to.duplic], rep(0,length(to.duplic))))
}

mut = function(x,prob.elim) {
  
}

elim = function(x,prob.elim) {
  
}
