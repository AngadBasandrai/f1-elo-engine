import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse
import sys

class Driver:
    def __init__(self, name, rating=1400,started=False,retired=False,races=0,points = 0,championshipPoints=0,wins=0,podiums=0,seasons=0,worldChampionships=0,bestRookie=None,breakthrough = None):
        self.name = name
        self.rating = rating
        self.history = []
        self.buffer = self.rating
        self.started = started
        self.retired = retired
        self.races = races
        self.preSeason = 1400
        self.points = points
        self.championshipPoints = championshipPoints
        self.wins = wins
        self.podiums = podiums
        self.seasons = seasons
        self.worldChampionships = 0
        self.worldChampionshipYear = []
        self.bestPerformer = []
        self.bestRookie = bestRookie
        self.breakthrough = breakthrough
        self.title = None
        self.titleVal = 0

    def calculateTitle(self):
        if self.peakRating() >= 1600 and self.worldChampionships >= 2 and self.wins >= 30 and self.podiums >= 50 and len(self.bestPerformer) > 0:
            self.title = 'Grand Master'
            self.titleVal = 4
        elif self.peakRating() >= 1555 and self.worldChampionships >= 1 and (self.wins >= 30 or (self.wins >= 20 and self.podiums >= 50)) and len(self.bestPerformer) > 0:
            self.title = 'Race Master'
            self.titleVal = 3
        elif (self.peakRating() >= 1500 and (self.wins >= 20 or (self.wins >= 10 and self.podiums >= 30))) or self.worldChampionships >= 1:
            self.title = 'Track Master'
            self.titleVal = 2
        elif (self.peakRating() >= 1450 and (self.wins >= 10 or (self.wins > 3 and self.podiums >= 15))) or len(self.bestPerformer) > 0:
            self.title = 'Speed Master'
            self.titleVal = 1
        

    def addHistory(self, history):
        self.history = history
    
    def addBestPerformer(self, year):
        self.bestPerformer.append(year)
    
    def addWorldChampionship(self, year):
        self.worldChampionshipYear.append(year)
    
    def ratingAdjust(self, scored, expected, k = 1):
            if self.races <= 10:
                if scored-expected > 0:
                    self.buffer = self.rating + (scored-(expected)) * 2 * k
                else:
                    self.buffer = self.rating + (scored-(expected)) * k
            else:
                self.buffer = self.rating + (scored-(expected)) * k
            if self.buffer < 1000:
                self.buffer = 1000
    def upload(self):
        if self.retired:
            self.history.append(np.nan)
        elif self.started:
            self.history.append(self.rating)
            self.rating = self.buffer
            self.buffer = self.rating
        else:
            self.history.append(np.nan)

    def effRating(self):
        try:
            return self.buffer if not self.retired else self.history[np.where(~np.isnan(self.history) == True)[0][-1]]
        except:
            return 1400
    def peakRating(self):
        return np.nanmax(self.history+[self.rating]) if self.started else 1400
    def __repr__(self):
        if self.started:
            if not self.title:
                return self.name + ": 1400 -> " + str(int(self.effRating()*10)/10) + "  ("+ str(int((self.effRating()-1400)*10)/10) +")" + "  Peak: " + str(int(self.peakRating() * 10)/10) + "  (" + str(int((self.effRating() - self.peakRating()) * 10)/10) + ")"
            else:
                return self.name + "(" + self.title + "): 1400 -> " + str(int(self.effRating()*10)/10) + "  ("+ str(int((self.effRating()-1400)*10)/10) +")" + "  Peak: " + str(int(self.peakRating() * 10)/10) + "  (" + str(int((self.effRating() - self.peakRating()) * 10)/10) + ")"
        else:
            return self.name + ": hasn't made professional debut"


def recalculate(points,file_drivers,start_year,file_winners,file_data,file_labels,file_driver_data,k):
    drivers = []
    f = open(file_drivers, 'r')
    lines = f.read().split(',')
    for d in lines:
        drivers.append(Driver(d))
    f.close()

    y = start_year
    xlabels = [str(y)[-2:]]
    ny = True
    f = open(file_data,'r')
    z = open(file_winners, 'w')
    lines = f.readlines()
    for n in range(len(lines)):
        s = lines[n].split(',')
        p = []
        if s[0] == "--":
            maxDiff = [None,-sys.maxsize-1]
            minDiff = ["-",-sys.maxsize-1]
            newMaxDiff = [None,0]
            breakthroughMaxDiff = [None,0]
            for i in range(len(drivers)):
                drivers[i].calculateTitle()
                try:
                    if s.index(drivers[i].name):
                        drivers[i].seasons += 1
                        p.append([drivers[i], drivers[i].effRating()])
                        if drivers[i].effRating() - drivers[i].preSeason > maxDiff[1]:
                            maxDiff = [drivers[i], drivers[i].effRating() - drivers[i].preSeason]
                        if drivers[i].preSeason - drivers[i].effRating() > minDiff[1]:
                            minDiff = [drivers[i].name, drivers[i].preSeason - drivers[i].effRating()]
                        if drivers[i].effRating() - drivers[i].preSeason > newMaxDiff[1] and drivers[i].seasons == 1 and drivers[i].races >= 5:
                            newMaxDiff = [drivers[i], drivers[i].effRating() - drivers[i].preSeason]
                        if drivers[i].effRating() - drivers[i].preSeason > breakthroughMaxDiff[1] and drivers[i].seasons <= 4 and drivers[i].worldChampionships == 0 and drivers[i].races >= 5:
                            breakthroughMaxDiff = [drivers[i], drivers[i].effRating() - drivers[i].preSeason]
                        drivers[i].preSeason = drivers[i].effRating()
                except:
                    continue
            maxDiff[0].addBestPerformer(y)
            p = sorted(p,key = lambda x: x[1], reverse=True)
            z.write(str(y) + ": ")
            for j in p:
                if j[0].title:
                    z.write(f"{j[0].name}({j[0].title}): {j[1]}")
                else:
                    z.write(f"{j[0].name}: {j[1]}")
            z.write("\n")
            diff = p[0][1] - p[1][1]
            z.write("Lead of championship: " + str(diff) + ",\t")
            diffFromLast = p[0][1] - p[-1][1]
            z.write("Gap between first and last: " + str(diffFromLast) + ",\t")
            avgOppRating = 0
            for i in p:
                avgOppRating += i[1]
            avgOppRating -= p[0][1]
            avgOppRating /= len(p)-1
            diffFromAvg = p[0][1] - avgOppRating
            z.write("Gap between first and average rating(not including champion): " + str(diffFromAvg) + ",\t")
            z.write("Average Rating(not including champion): " + str(avgOppRating) + "\t")
            z.write(f"Best Performer: {maxDiff[0].name}, gained {maxDiff[1]} rating\t")
            if minDiff[1] < 0:
                z.write(f"Worst Performer: {minDiff[0]}, gained {-minDiff[1]} rating\t")
            else:
                z.write(f"Worst Performer: {minDiff[0]}, lost {minDiff[1]} rating\t")
            try:
                newMaxDiff[0].bestRookie = y
                if newMaxDiff[1] > 0:
                    z.write(f"Best Rookie: {newMaxDiff[0].name}, gained {newMaxDiff[1]} rating\t")
                else:
                    z.write(f"Best Rookie: {newMaxDiff[0].name}, lost {-newMaxDiff[1]} rating\t")
            except:
                z.write("No Rookies this season\t")
            try:
                breakthroughMaxDiff[0].breakthrough = y
                z.write(f"Breakthrough Of The Year: {breakthroughMaxDiff[0].name}, gained {breakthroughMaxDiff[1]} rating\n\n")
            except:
                z.write("No Breakthrough this season\n\n")
            p[0][0].worldChampionships += 1
            p[0][0].addWorldChampionship(y)
            y += 1
            xlabels.append((str(y)[-2:]))
            for driver in drivers:
                driver.upload()
        elif s[0] == "~":
            for i in range(len(drivers)):
                try:
                    if s.index(drivers[i].name):
                        print(drivers[i].name + " has retired")
                        drivers[i].upload()
                        drivers[i].retired = True
                except:
                    continue
        else:
            if ny:
                ny = False
            xlabels.append('')
            for i in range(len(drivers)):
                try:
                    ratings = []
                    for j in range(len(drivers)):
                        if j != i:
                            try:
                                check = s.index(drivers[j].name)
                                ratings.append(drivers[j].rating)
                                n += 1
                            except:
                                continue
                    ratings.sort(reverse=True)
                    oppAvg = sum(ratings)/len(ratings)
                    for q in range(len(ratings)):
                        if ratings[q] <= drivers[i].rating:
                            break
                    expected = (((1/(1+(10**((oppAvg - drivers[i].rating)/200))))*2)-1)*points[0]
                    score = points[s.index(drivers[i].name)]
                    drivers[i].started = True
                    drivers[i].races += 1
                    drivers[i].ratingAdjust(score, expected,k)
                    drivers[i].points += score
                    if score > 0:
                        drivers[i].championshipPoints += score
                    if score >= points[2]:
                        drivers[i].podiums += 1
                    if score >= points[0]:
                        drivers[i].wins += 1
                except:
                    continue
            for driver in drivers:
                driver.upload()

    drivers = sorted(drivers, key=lambda x: x.peakRating(), reverse=True)
    for driver in drivers:
        print(driver)
    high = np.nanmax(drivers[0].history)
    drivers = sorted(drivers, key=lambda x: x.effRating(), reverse=True)
    fig, ax = plt.subplots()
    z.close()
    _title = []
    _names = []
    _ratingsList = []
    _ratings = []
    _started = []
    _retired = []
    _races = []
    _seasons = []
    _points = []
    _ppr = []
    _champpoints = []
    _champppr = []
    _wins = []
    _winspr = []
    _podiums = []
    _podiumspr = []
    _wdc = []
    _wdcs = []
    _bestPerformer = []
    _bestRookie = []
    _breakthrough = []
    _peak = []
    _titleVal = []
    for driver in drivers:
        z = driver.history
        if driver.started:
            if not driver.retired:
                z.append(driver.rating)
            ax.plot(z, label = driver.name)
        _title.append(driver.title)
        _names.append(driver.name)
        _ratingsList.append(z)
        _ratings.append(driver.effRating())
        _started.append(driver.started)
        _retired.append(driver.retired)
        _races.append(driver.races)
        _seasons.append(driver.seasons)
        _points.append(driver.points)
        _ppr.append(driver.points/driver.races)
        _champpoints.append(driver.championshipPoints)
        _champppr.append(driver.championshipPoints/driver.races)
        _wins.append(driver.wins)
        _winspr.append(driver.wins/driver.races)
        _podiums.append(driver.podiums)
        _podiumspr.append(driver.podiums/driver.races)
        _wdc.append(driver.worldChampionships)
        _wdcs.append(driver.worldChampionshipYear)
        _bestPerformer.append(driver.bestPerformer)
        _bestRookie.append(driver.bestRookie)
        _breakthrough.append(driver.breakthrough)
        _peak.append(driver.peakRating())
        _titleVal.append(driver.titleVal)
    data = {
        'Title':_title,
        'Name':_names,
        'Rating History':_ratingsList,
        'Rating':_ratings,
        'Started':_started,
        'Retired':_retired,
        'Races':_races,
        'Seasons':_seasons,
        'Points':_points,
        'Points Per Race':_ppr,
        'Championship Points':_champpoints,
        'Championship Points Per Race':_champppr,
        'Wins':_wins,
        'Wins Per Race':_winspr,
        'Podiums':_podiums,
        'Podiums Per Race':_podiumspr,
        'World Championships':_wdc,
        'World Championship Years':_wdcs,
        'Best Performer':_bestPerformer,
        'Best Rookie':_bestRookie,
        'Breakthrough':_breakthrough,
        'Peak':_peak,
        '_':_titleVal,
    }

    df = pd.DataFrame(data)
    df.to_csv(file_driver_data,index=False)

    xlabelsfile = open(file_labels, 'w')
    xlabelsfile.write(str(xlabels))
    xlabelsfile.close()

    plt.xlabel('races')
    plt.ylabel('elo')
    ax.set_yticks(np.arange(int(np.nanmin(drivers[-1].history)), int(high), 50))
    x = np.arange(0,len(xlabels),1)
    ax.set_xticks(x)
    ax.set_xticklabels(xlabels)
    plt.legend(loc="lower right",bbox_to_anchor=(1.1, -0.1), fontsize="5")
    ax = plt.gca()
    for tick in ax.get_yticks():
        ax.axhline(y=tick, color='gray', linestyle='--', linewidth=0.7)
    for tick, label in zip(x, xlabels):
        if len(label) > 0:
            ax.axvline(x=tick, color='gray', linestyle='-', linewidth=1)

    ax.axhline(y=1500, color='black', linestyle='-', linewidth=2)
    ax.axhline(y=1400, color='black', linestyle='-', linewidth=2)
    ax.axhline(y=1300, color='black', linestyle='-', linewidth=2)

    plt.show()

    f.close()

def load(file_name):
    drivers = []
    df = pd.read_csv(file_name)
    for index, row in df.iterrows():
        driver = Driver(row['Name'], row['Rating'], row['Started'], row['Retired'], row['Races'], row['Points'], row['Championship Points'], row['Wins'], row['Podiums'],row['Seasons'],row['World Championships'],row['Best Rookie'],row['Breakthrough Of The Year'])
        listH = row['Rating History'][1:-1].split(', ')
        listWDC = row['World Championship Years'][1:-1].split(', ')
        listBP = row['Best Performer'][1:-1].split(', ')
        history = []
        for i in listH:
            if i == "nan":
                history.append(np.nan)
            else:
                history.append(float(i))
        driver.addHistory(history)
        for i in listWDC:
            driver.addWorldChampionship(i)
        for i in listBP:
            driver.addBestPerformer(i)
        drivers.append(driver)
    return drivers

def show(file_name_data,file_name_lables):
    drivers = load(file_name_data)
    xlabelsfile = open(file_name_lables, 'r')
    xlabels = xlabelsfile.read()
    xlabelsfile.close()
    
    xlabels = xlabels[1:-1].split(', ')
    for i in range(len(xlabels)):
        xlabels[i] = xlabels[i][1:-1]

    drivers = sorted(drivers, key=lambda x: x.peakRating(), reverse=True)
    for driver in drivers:
        print(driver)
    high = np.nanmax(drivers[0].history)
    drivers = sorted(drivers, key=lambda x: x.effRating(), reverse=True)
    fig, ax = plt.subplots()

    toViewFile = open("toView.csv", "r")
    toView = toViewFile.read().split(',')
    toViewFile.close()
    if len(toView) == 1 and toView[0] == '':
        for driver in drivers:
            z = driver.history
            if driver.started:
                if not driver.retired:
                    z.append(driver.rating)
                ax.plot(z, label = driver.name)
    else:
        for driver in drivers:
            if driver.name in toView:
                z = driver.history
                if driver.started:
                    if not driver.retired:
                        z.append(driver.rating)
                    ax.plot(z, label = driver.name)

    plt.xlabel('races')
    plt.ylabel('elo')
    ax.set_yticks(np.arange(int(np.nanmin(drivers[-1].history)), int(high), 50))
    x = np.arange(0,len(xlabels),1)
    ax.set_xticks(x)
    ax.set_xticklabels(xlabels)
    plt.legend(loc="lower right",bbox_to_anchor=(1.1, -0.1), fontsize="4")
    ax = plt.gca()

    for tick in ax.get_yticks():
        ax.axhline(y=tick, color='gray', linestyle='--', linewidth=0.7)
    for tick, label in zip(x, xlabels):
        if len(label) > 1:
            ax.axvline(x=tick, color='gray', linestyle='-', linewidth=1)

    ax.axhline(y=1500, color='black', linestyle='-', linewidth=2)
    ax.axhline(y=1400, color='black', linestyle='-', linewidth=2)
    ax.axhline(y=1300, color='black', linestyle='-', linewidth=2)

    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recalculate or load the results")
    parser.add_argument("-c", "--calculate", action="store_true", help="Recalculate ratings")
    parser.add_argument("-l", "--load", action="store_true", help="Load previously calculated ratings")
    parser.add_argument("-cs", "--calculate_sprint", action="store_true", help="Recalculate sprint ratings")
    parser.add_argument("-ls", "--load_sprint", action="store_true", help="Load previously calculated sprint ratings")

    args = parser.parse_args()

    if args.load:
        show('driverData.csv')
    if args.load_sprint:
        show('driverDataSprint.csv')
    if args.calculate_sprint:
        recalculate([8,7,6,5,4,3,2,1,0,0,0,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10],'driverssprint.csv',2021,'winnerssprint.txt','datasprint.csv','xlabelssprint.csv','driverDataSprint.csv',5)
    elif args.calculate or not any(vars(args).values()):
        recalculate([25,18,15,12,10,8,6,4,2,1,-1,-2,-4,-6,-8,-10,-12,-15,-18,-25,-26,-27,-28,-29,-30],'drivers.csv',2002,'winners.txt','data.csv','xlabels.csv','driverData.csv',1)