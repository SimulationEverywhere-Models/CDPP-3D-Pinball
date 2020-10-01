[top]
components : pinball

[pinball]
type : cell
width : 30
height : 30
delay : transport
defaultDelayTime  : 100
border : nowrapped 
neighbors : pinball(-1,-1) pinball(-1,0) pinball(-1,1) 
neighbors : pinball(0,-1)  pinball(0,0)  pinball(0,1)
neighbors : pinball(1,-1)  pinball(1,0)  pinball(1,1)
initialvalue : 0
initialCellsValue : pinball.val
localtransition : pinball-rule

[pinball-rule]
rule : 9 100 { (0,0) = 9 } 

rule : 1 100 { (0,0) = 0 and (1,1) = 1 }
rule : 4 100 { (0,0) = 0 and (0,-1) = 9 and (1,0) = 1 }
rule : 7 100 { (0,0) = 0 and (-1,0) = 9 and (-1,1) = 9 and (0,1) = 1 }
rule : 5 100 { (0,0) = 1 and (-1,0) = 9 and (0,-1) = 9 }

rule : 2 100 { (0,0) = 0 and (1,0) = 2 }
rule : 5 100 { (0,0) = 0 and (0,-1) = 2 and (-1,-1) = 9 }
rule : 7 100 { (0,0) = 2 and (-1,0) = 9 and (0,1) = 9 }

rule : 3 100 { (1,-1) = 3 and (0,0) = 0 }
rule : 6 100 { (0,0) = 0 and (-1,0) = 9 and (0,-1) = 3 }
rule : 1 100 { (0,0) = 0 and (1,0) = 3 and (0,1) = 9 and (1,1) = 9 }
rule : 7 100 { (0,0) = 3 and (-1,0) = 9 and (0,1) = 9 }

rule : 4 100 { (0,0) = 0 and (0,-1) = 4 }
rule : 7 100 { (0,0) = 0 and (-1,0) = 4 and (-1,1) = 9 }
rule : 1 100 { (0,0) = 4 and (0,1) = 9 and (1,0) = 9 }

rule : 5 100 { (0,0) = 0 and (-1,-1) = 5 }
rule : 8 100 { (0,0) = 0 and (-1,0) = 5 and (0,1) = 9 }
rule : 3 100 { (0,0) = 0 and (0,-1) = 5 and (1,-1) = 9 and (1,0) = 9 }
rule : 1 100 { (0,0) = 5 and (1,0) = 9 and (0,1) = 9 }

rule : 6 100 { (0,0) = 0 and (-1,0) = 6 }
rule : 1 100 { (0,0) = 0 and (0,1) = 6 and (1,1) = 9 }
rule : 3 100 { (0,0) = 6 and (0,-1) = 9 and (1,0) = 9 }

rule : 7 100 { (0,0) = 0 and (-1,1) = 7 }
rule : 1 100 { (0,0) = 0 and (1,0) = 9 and (0,1) = 7 }
rule : 5 100 { (0,0) = 0 and (-1,0) = 7 and (0,-1) = 9 and (-1,-1) = 9 }
rule : 3 100 { (0,0) = 7 and (0,-1) = 9 and (1,0) = 9 }

rule : 8 100 { (0,0) = 0 and (0,1) = 8 }
rule : 3 100 { (0,0) = 0 and (1,-1) = 9 and (1,0) = 8 }
rule : 5 100 { (0,0) = 8 and (0,-1) = 9 and (-1,0) = 9 }

rule : 0 100 { (0,0) = 1 and (-1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit up
rule : 0 100 { (0,0) = 1 and (1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit down
rule : 0 100 { (0,0) = 1 and (0,-1) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit left
rule : 0 100 { (0,0) = 1 and (-1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit right

rule : 0 100 { (0,0) = 2 and (-1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit up
rule : 0 100 { (0,0) = 2 and (1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit down
rule : 0 100 { (0,0) = 2 and (0,-1) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit left
rule : 0 100 { (0,0) = 2 and (-1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit right

rule : 0 100 { (0,0) = 3 and (-1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit up
rule : 0 100 { (0,0) = 3 and (1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit down
rule : 0 100 { (0,0) = 3 and (0,-1) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit left
rule : 0 100 { (0,0) = 3 and (-1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit right

rule : 0 100 { (0,0) = 4 and (-1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit up
rule : 0 100 { (0,0) = 4 and (1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit down
rule : 0 100 { (0,0) = 4 and (0,-1) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit left
rule : 0 100 { (0,0) = 4 and (-1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit right

rule : 0 100 { (0,0) = 5 and (-1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit up
rule : 0 100 { (0,0) = 5 and (1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit down
rule : 0 100 { (0,0) = 5 and (0,-1) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit left
rule : 0 100 { (0,0) = 5 and (-1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit right

rule : 0 100 { (0,0) = 6 and (-1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit up
rule : 0 100 { (0,0) = 6 and (1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit down
rule : 0 100 { (0,0) = 6 and (0,-1) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit left
rule : 0 100 { (0,0) = 6 and (-1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit right

rule : 0 100 { (0,0) = 7 and (-1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit up
rule : 0 100 { (0,0) = 7 and (1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit down
rule : 0 100 { (0,0) = 7 and (0,-1) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit left
rule : 0 100 { (0,0) = 7 and (-1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit right

rule : 0 100 { (0,0) = 8 and (-1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit up
rule : 0 100 { (0,0) = 8 and (1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit down
rule : 0 100 { (0,0) = 8 and (0,-1) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit left
rule : 0 100 { (0,0) = 8 and (-1,0) = 10 and (0,-1) = 9 and (0,1) = 9 } %exit right

rule : 0 100 { t }
