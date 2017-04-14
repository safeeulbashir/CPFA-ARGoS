library(changepoint)
library(pracma)
args <- commandArgs()
#args
if(args[12]=="1")
{
	detrend="linear"
}else {
	detrend="constant"
	}
mydata=read.table(args[6])
distributionType=as.numeric(args[10])
data<-as.vector(mydata[,1])
cumsum1=cumsum(data)
cumsum1=detrend(cumsum1, detrend)
cumsum=binseg.mean.cusum(cumsum1,Q=as.numeric(args[7]),pen=2)
cps=cumsum['cps']
#cps
cumsum1=cumsum(data)
cumsum1=detrend(cumsum1, detrend)
xCordinate<-list()
yCordinate<-list()
cpsToWrite<-list()
for(i in seq(1,length(cps[[1]]), 2)){
	xCordinate[i]<-cps[[1]][i]	
	yCordinate[i]<-cumsum1[as.numeric(unlist(cps[[1]][i]))]
}
xCordinate<-as.numeric(unlist(xCordinate))
cpsToWrite=sort(xCordinate)
for(i in seq(1,length(xCordinate)))
	cpsToWrite[i]=cpsToWrite[i]*as.numeric(args[8])
#length(cpsToWrite)
yCordinate<-as.numeric(unlist(yCordinate))
argsplit=strsplit(args[6],"[.]")
argsplit2=strsplit(argsplit[[1]][[2]],"[/]")
#For Pheromone Data
#PeromoneLayingTime=read.table("./PheromoneLayTiming.txt")

randomseed=strsplit(argsplit2[[1]][[5]],"[_]")
#################################################
########Writing Changepoints in file#############
#################################################

cpsToWrite=append(cpsToWrite, args[9], 0) # Adding Random Seed number before the change points
filepath=paste(args[11],"ChangePoints.txt",sep="/") #Creating Filename
#if(!file.exists(filepath)){
#	write("RandomSeed\tCP1\tCP2\tCP3\tCP4",file =filepath, append = TRUE)
#}
write(cpsToWrite, file =filepath, append = TRUE, sep = "\t") #Writing changepoints to file
imagename=paste(argsplit2[[1]][[5]],"png",sep=".")
imagename=paste("/",imagename,sep="")
imagename=paste(args[11],imagename,sep="")
png(filename=imagename)
limits=seq(from=0, to=540, by=60)
labels=seq(from=0, to=5400, by=600)
par(ps = 20, cex = 1.0, cex.main = 1)
plot(cumsum1,col="red",lty=1,lwd=2,xaxt='n',type="l",main = paste("Plot For ",argsplit2[[1]][[5]],sep=""), xlab = "Time(s)", ylab = " Detrended Cumulative Sum", cex=1.5)
axis(1, at=limits,labels=labels, cex=1.5)
points(xCordinate,yCordinate,pch=23)
#legend("topright", inset=.05,c("Change Points in Seconds"), fill=terrain.colors(3), horiz=TRUE)
text(xCordinate, yCordinate, xCordinate*as.numeric(args[8]), cex=1.5, pos=4, col="blue",size=10)
dev.off()

