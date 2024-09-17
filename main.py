import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse
import sys

class Driver:
    def __init__(self, name, rating=1400,started=False,retired=False,races=0):
        self.name = name
        self.rating = rating
        self.history = []
        self.buffer = self.rating
        self.started = started
        self.retired = retired
        self.races = races
        self.preSeason = 1400

    def addHistory(self, history):
        self.history = history
    
    def ratingAdjust(self, scored, expected):
            if self.races <= 10:
                if scored-expected > 0:
                    self.buffer = self.rating + (scored-(expected)) * 2
                else:
                    self.buffer = self.rating + (scored-(expected))
            elif self.rating > 1500:
                self.buffer = self.rating + (scored-(expected)) * 0.5
            else:
                self.buffer = self.rating + (scored-(expected))
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
            return 1200
    def peakRating(self):
        return np.nanmax(self.history+[self.rating]) if self.started else 1200
    def __repr__(self):
        if self.started:
            return self.name + ": 1200 -> " + str(int(self.effRating()*10)/10) + "  ("+ str(int((self.effRating()-1200)*10)/10) +")" + "  Peak: " + str(int(self.peakRating() * 10)/10) + "  (" + str(int((self.effRating() - self.peakRating()) * 10)/10) + ")"
        else:
            return self.name + ": hasn't made professional debut"

points = [25,18,15,12,10,8,6,4,2,1,-1,-2,-4,-6,-8,-10,-12,-15,-18,-25,-26,-27,-28,-29,-30]

def recalculate():
    drivers = []
    f = open('drivers.csv', 'r')
    lines = f.read().split(',')
    for d in lines:
        drivers.append(Driver(d))
    f.close()

    y = 2007
    xlabels = [str(y)[-2:]]
    ny = True
    f = open('data.csv')
    z = open('winners.txt', 'w')
    lines = f.readlines()
    for n in range(len(lines)):
        s = lines[n].split(',')
        p = []
        if s[0] == "--":
            maxDiff = ["-",-sys.maxsize-1]
            minDiff = ["-",-sys.maxsize-1]
            for i in range(len(drivers)):
                try:
                    if s.index(drivers[i].name):
                        p.append([drivers[i].name, drivers[i].effRating()])
                        if drivers[i].effRating() - drivers[i].preSeason > maxDiff[1]:
                            maxDiff = [drivers[i].name, drivers[i].effRating() - drivers[i].preSeason]
                        if drivers[i].preSeason - drivers[i].effRating() > minDiff[1]:
                            minDiff = [drivers[i].name, drivers[i].preSeason - drivers[i].effRating()]
                        drivers[i].preSeason = drivers[i].effRating()
                except:
                    continue
            p = sorted(p,key = lambda x: x[1], reverse=True)
            z.write(str(y) + ": ")
            z.write(str(p) + "\n")
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
            z.write(f"Best Performer: {maxDiff[0]}, gained {maxDiff[1]} rating\t")
            if minDiff[1] < 0:
                z.write(f"Worst Performer: {minDiff[0]}, gained {-minDiff[1]} rating\t")
            else:
                z.write(f"Worst Performer: {minDiff[0]}, lost {minDiff[1]} rating\n\n")
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
                    expected = (((1/(1+(10**((oppAvg - drivers[i].rating)/200))))*2)-1)*25
                    score = points[s.index(drivers[i].name)]
                    drivers[i].started = True
                    drivers[i].races += 1
                    drivers[i].ratingAdjust(score, expected)
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
    _names = []
    _ratingsList = []
    _ratings = []
    _started = []
    _retired = []
    _races = []
    for driver in drivers:
        z = driver.history
        if driver.started:
            if not driver.retired:
                z.append(driver.rating)
            ax.plot(z, label = driver.name)
        _names.append(driver.name)
        _ratingsList.append(z)
        _ratings.append(driver.effRating())
        _started.append(driver.started)
        _retired.append(driver.retired)
        _races.append(driver.races)

    data = {
        'Name':_names,
        'Rating History':_ratingsList,
        'Rating':_ratings,
        'Started':_started,
        'Retired':_retired,
        'Races':_races
    }

    df = pd.DataFrame(data)
    df.to_csv('driverData.csv',index=False)

    xlabelsfile = open('xlabels.csv', 'w')
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

def load():
    drivers = []
    df = pd.read_csv('driverData.csv')
    for index, row in df.iterrows():
        driver = Driver(row['Name'], row['Rating'], row['Started'], row['Retired'], row['Races'])
        list = row['Rating History'][1:-1].split(', ')
        history = []
        for i in list:
            if i == "nan":
                history.append(np.nan)
            else:
                history.append(float(i))
        driver.addHistory(history)
        drivers.append(driver)
    return drivers

def show():
    drivers = load()
    xlabelsfile = open('xlabels.csv', 'r')
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
    plt.legend(loc="lower right",bbox_to_anchor=(1.1, -0.1), fontsize="5")
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

    args = parser.parse_args()

    if args.load:
        show()
    elif args.calculate or not any(vars(args).values()):
        recalculate()