import sqlite3 as lite
import random
import Constants
class Gene(object):

	def __init__(self, team_areas, enemy_areas, ballPosition,moveType,extraInformation):
		self.team_areas=team_areas
		self.enemy_areas=enemy_areas
		self.ballPosition=ballPosition
		self.moveType=moveType
		self.extraInformation=extraInformation

	def compare(self,team_area,enemy_area, ballPosition):
		equal=True
		for i in range(len(enemy_area)):
			if not (team_area[i]==self.team_areas[i] or self.team_areas[i]==-1):
				equal=False
			if not (enemy_area[i]==self.enemy_area[i] or self.enemy_area[i]==-1):
				equal=False
		if(ballPosition==self.ballPosition):
			equal=False
		if equal:
			return moveType,extraInformation
		else:
			return -1,-1


class Individual(object):

	def __init__(self,genes=[],id=-1):
		self.genes=genes
		self.id=individual
		self.fitness=0;

	def match_expression(self,team_area,enemy_area,ballPosition):
		for  gene in self.genes:
			moveType, extraInformation= compare(team_area,enemy_area,ballPosition)
			if not (moveType == -1):
				return moveType, extraInformation
		return -1,-1

	def create_random_expression(self):
		team_areas=[]
		enemy_areas=[]
		ballPosition=-1
		moveType=1
		extraInformation=-1
		for i in range(4):
			x=random.randint(0,20)
			if x > 15:
				x=-1
			team_areas.append(x)
		for i in range(4):
			x=random.randint(0,20)
			if x > 15:
				x=-1
			enemy_areas.append(x)

		ballPosition=random.randint(0,20)
		if ballPosition > 15:
			ballPosition=-1

		moveType=random.randint(0,3)
		if moveType==0:
			extraInformation=random.randint(0,3)
		else:
			extraInformation=random.randint(0,15)
		gene =Gene(team_areas,enemy_areas,ballPosition,moveType,extraInformation)
		return gene


	# this creates a new individual by crossover and mutation
	def mix_expressions(self,individual):
		#ensure that only some genes don't remain
		genes=[]
		random.shuffle(self.genes)
		random.shuffle(individual.genes)		
		total_length=0
		choicer=0
		if len(individual.genes) > len(self.genes):
			total_length=len(self.genes)
			choicer=0
		else: 
			total_length=len(individual.genes)
			choicer=1
		for i in range(total_length):
			if random.random() < Constants.MUTATION_RATE:
				genes.append(self.create_random_expression())
			else:
				if random.randint(0,1)==0:
					genes.append(self.genes[i])
				else:
					genes.append(individual.genes[i])

		if choicer==0:
			for j in range(total_length,len(self.genes)-total_length):
				genes.append(self.genes[j])
		else:
			for j in range(total_length,len(individual.genes)-total_length):
				genes.append(individual.genes[j])
		return Individual(genes)


    def goalScored():
    	self.fitness+=10

    def goalScoredAgainst():
    	self.fitness-=5

    def randomMoveMade():
    	self.fitness-=0.1


class  DatabaseAccess(object):
	def __init__(self):      
		self.con = lite.connect('test.db')
		self.mutationPercentage=30
		self.crossoverPercentage=60

	def saveStatistics(self, individual_id, randomMovesTime, fitness,goalsScored,goalsAgainst):
		cur=self.con.cursor()
		executeString="INSERT INTO statistics (individual_id,randomMovesTime, fitness,goalsScored,goalsAgainst) VALUES ("
		executeString+=str(individual_id)+",'"+str(randomMovesTime)+"','"+str(fitness)+"',"+str(goalsScored)+","+str(goalsAgainst)+")"
		cur.execute(executeString)

	def loadGeneticAlgorithms(self,level):
		cur=self.con.cursor()
		cur.execute("SELECT * FROM individual WHERE level="+str(level));
		rows=cur.fetchall()
		individuals=[]
		for row in rows
			individual_id= row[0][0]
			cur.execute("SELECT * FROM genes WHERE individual_id="+str(individual_id));
			generows=cur.fetchall()		
			genes=[]
			for generow in generows:
				enemy_areas=[int(x) for x in generow[3].split(",")]
				team_areas=[int(x) for x in generow[2].split(",")]
				gene=Gene(enemy_areas,team_areas, int(generow[4]) , int(generow[5]) , int(generow[6]))
			genes.append(gene)
			i =Individual(genes)
			individuals.append(i)
		return individuals
	
	def getGeneticAlgorithm(self,id):
		cur=self.con.cursor()
		cur.execute("SELECT * FROM individual WHERE id="+str(id) +"  LIMIT 1");
		row=cur.fetchall()
		individual_id= row[0][0]
		cur.execute("SELECT * FROM genes WHERE individual_id="+str(individual_id));
		rows=cur.fetchall()		
		genes=[]

		for row in rows:
			enemy_areas=[int(x) for x in row[3].split(",")]
			team_areas=[int(x) for x in row[2].split(",")]
			gene=Gene(enemy_areas,team_areas, int(row[4]) , int(row[5]) , int(row[6]))
			genes.append(gene)
		i =Individual(genes)
		return i
		
	def makeNewGeneticAlgorithm(self,individual1,individual2,level):
		#get the new individual
		final_individual=individual1.mix_expressions(individual2)

		#save in the database
		id=self.saveIndividual(level,final_individual)
		individual.id=id
		return final_individual

	def createNewRandomAlgorithm(self,level):
		individual=Individual()
		for i in range(random.randint(0,40)):
			individual.genes.append(individual.create_random_expression())
		id=self.saveIndividual(level,individual)
		individual.id=id
		return individual

	def saveIndividual(self,level,individual):
		cur=self.con.cursor()
		cur.execute("INSERT INTO individual (level) VALUES ("+str(level)+")")
		self.con.commit()
		rows=cur.execute("SELECT MAX(id) FROM individual WHERE level="+str(level))
		row=cur.fetchall()
		id=row[0][0]
		print id

		for gene in individual.genes:
			team_areas= ','.join(map(str, gene.team_areas)) 
			enemy_areas = ','.join(map(str, gene.enemy_areas)) 
			ballPosition= str(gene.ballPosition)
			moveType=str(gene.moveType)
			extraInformation=str(gene.extraInformation)
			executeString="INSERT INTO genes (individual_id,teamAreas,enemyAreas,ballPosition,moveType,extraInformation) VALUES ("
			executeString+=str(id)+",'"+team_areas+"','"+enemy_areas+"',"+ballPosition+","+moveType+","+extraInformation+")"
			cur.execute(executeString)

		self.con.commit()
		return id
		'''
		cur.execute("SELECT * FROM YOUR_TABLE_NAME")
		print all the first cell of all the rows
		for row in cur.fetchall() :
    		print row[0]
    	ID 	individual_id team_areas enemyAreas ballPosition moveType extraInformation
    	INSERT INTO individual (level) VALUES (level)
    	SELECT MAX(id),level FROM individual LIMIT 1 WHERE level=level
    	make id = above
    	for (0,15) //tem
    	moveType, extraInformation=getRandomMoveType()
    	team_areas= getRandomTeamAreas()
    	enemy_areas= getRandomTeamAreas()
    	ballPosition=getRandodmBallPosition()
    	INSERT INTO genes (individual_id,team_areas,enemy_areas,ballPosition,moveType,extraInformation)
    	VALUES (id,team_areas,enemy_areas,ballPosition,moveType,extraInformation)
    	'''