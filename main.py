import matplotlib.pyplot as plt
import numpy as np

class Driver:
    def __init__(self, name, rating=1200):
        self.name = name
        self.rating = rating
        self.history = []
        self.buffer = self.rating
        self.started = False
        self.retired = False
        self.k = 1
    
    def ratingAdjust(self, scored, expected):
            self.buffer = self.rating + self.k * (scored-(expected))
            if self.buffer < 100:   
                self.buffer = 100
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

drivers = []
f = open('drivers.txt')
lines = f.readlines()
for d in lines:
    drivers.append(Driver(d[:-1]))
f.close()

y = 2010
xlabels = [str(y)[-2:]]
ny = True
f = open('data')
z = open('winners.txt', 'w')
lines = f.readlines()
for n in range(len(lines)):
    s = lines[n].split(',')
    p = []
    if s[0] == "--":
        for i in range(len(drivers)):
            try:
                if s.index(drivers[i].name):
                    p.append([drivers[i].name, drivers[i].effRating()])
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
        avgOppRating -= p[0][-1]
        avgOppRating /= len(p)-1
        diffFromAvg = p[0][1] - avgOppRating
        z.write("Gap between first and average rating(not including champion): " + str(diffFromAvg) + ",\t")
        z.write("Average Rating(not including champion): " + str(avgOppRating) + "\n\n")
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
                ex = 0
                for q in range(len(ratings)):
                    if ratings[q] <= drivers[i].rating:
                        ex = q
                        break
                expected = (((1/(1+(10**((oppAvg - drivers[i].rating)/200))))*2)-1)*25
                score = points[s.index(drivers[i].name)]
                drivers[i].started = True
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
for driver in drivers:
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
    if len(label) > 0:
        ax.axvline(x=tick, color='gray', linestyle='-', linewidth=1)
plt.show()

f.close()