library(changepoint)
library(pracma)
args <- commandArgs()
#args
mydata=read.table(args[6])
distributionType=as.numeric(args[10])
data<-as.vector(mydata[,1])
cumsum1=cumsum(data)
cumsum1=detrend(cumsum1, 'linear')
cumsum=binseg.mean.cusum(cumsum1,Q=as.numeric(args[7]),pen=2)
cps=cumsum['cps']
cumsum1=cumsum(data)
cumsum1=detrend(cumsum1, 'linear')
xCordinate<-list()
yCordinate<-list()
for(i in seq(1,length(cps[[1]]), 2)){
	xCordinate[i]<-cps[[1]][i]	
	yCordinate[i]<-cumsum1[as.numeric(unlist(cps[[1]][i]))]
}
xCordinate<-as.numeric(unlist(xCordinate))
yCordinate<-as.numeric(unlist(yCordinate))
argsplit=strsplit(args[6],"[.]")
argsplit2=strsplit(argsplit[[1]][[2]],"[/]")
#For Pheromone Data
#PeromoneLayingTime=read.table("./PheromoneLayTiming.txt")

randomseed=strsplit(argsplit2[[1]][[5]],"[_]")
#layingTimeInSlidingWindow=SimTimeFromTable/(ticksPerSecond*SlidingWindowMovement)
##LayingTime=PeromoneLayingTime[PeromoneLayingTime[,1]==randomseed[[1]][[2]],2]/(16*as.numeric(args[8]))
#randomseed
########################################
#Colors for Diffrent Types of Pheromones
########################################
colors=c("darkgreen","aquamarine","chartreuse4","chocolate1","blue","cyan3","blueviolet","brown4","darkgoldenrod4","darkorchid3","deeppink4","orangered","sienna","salmon","green4","khaki4")

##################################
#Get the file for Pheromone Lists
##################################
inputFile <- paste(args[9],argsplit2[[1]][[5]],".pheromone",sep="")
con  <- file(inputFile, open = "r")
pheromoneList <- list() #Contails the pheromone lists as for individual Pile
while (length(oneLine <- readLines(con, n = 1, warn = FALSE)) > 0) {
    myVector <- (strsplit(oneLine, " "))
    myVector <- list(as.numeric(myVector[[1]]))
    pheromoneList <- c(pheromoneList,myVector)
  } 
#pheromoneList
imagename=paste(argsplit2[[1]][[5]],"png",sep=".")
imagename=paste("/",imagename,sep="")
imagename=paste(args[11],imagename,sep="")
png(filename=imagename)
limits=seq(from=0, to=540, by=60)
labels=seq(from=0, to=5400, by=600)
plot(cumsum1,col="red",lty=1,lwd=2,xaxt='n',type="l",main = paste("Plot For ",argsplit2[[1]][[5]],sep=""), xlab = "Time(s)", ylab = " Detrended Cumulative Sum", cex=1.5)
axis(1, at=limits,labels=labels, cex=1.5)
points(xCordinate,yCordinate,pch=23)
#legend("topright", inset=.05,c("Change Points in Seconds"), fill=terrain.colors(3), horiz=TRUE)
text(xCordinate, yCordinate, xCordinate*as.numeric(args[8]), cex=1.5, pos=4, col="blue",size=10)
########################################################
#Determine the positions of Pheromones in sliding window
########################################################
colorIndex=1
lowrange=0
upperrange=0
if(distributionType==1){
	lowrange=1
	upperrange=1
}
if(distributionType==4){
	lowrange=2
	upperrange=5
} 
if(distributionType==16){
	lowrange=6
	upperrange=21
}
if(upperrange!=0 && lowrange!=0){
	for(count in lowrange:upperrange)
	{
		tempListXCord<-list()
		tempListYCord<-list()
		valcounter=0
		for(pheromones in pheromoneList[count])
		{ skipper=0
			for(pheromone in pheromones)
			{
				if(skipper>2 && pheromone/(as.numeric(args[8]))>=1)
				{
					tempListXCord[valcounter]=pheromone/(as.numeric(args[8]))
					tempListYCord[valcounter]=cumsum1[pheromone/(as.numeric(args[8]))]
					#print(pheromone/(16*as.numeric(args[8])))
					valcounter=valcounter+1	
				}
				else skipper=skipper+1
				

				
			}
			
		}
		tempListXCord<-unlist(tempListXCord)
		tempListYCord<-unlist(tempListYCord)
		points(tempListXCord,tempListYCord,col=colors[colorIndex])
		colorIndex=colorIndex+1
		#print(length(tempListXCord))
	}
} 
points(LayingTime,cumsum1[LayingTime],pch=21)
text(LayingTime, cumsum1[LayingTime], LayingTime*as.numeric(args[8]), cex=0.6, pos=4, col="green")
dev.off()

