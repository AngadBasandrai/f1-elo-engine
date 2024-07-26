import matplotlib.pyplot as plt
import numpy as np

class Driver:
    def __init__(self, name, rating=1500):
        self.name = name
        self.rating = rating
        self.history = []
        self.buffer = self.rating
        self.started = False
        self.retired = False
        self.k = 1
    
    def ratingAdjust(self, scored, expected):
        if scored >= expected*18/25:
            self.buffer = self.rating + self.k * (scored-(expected*18/25))
        else:
            self.buffer = self.rating + self.k * (scored-(expected*22/25))
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
        return self.buffer if not self.retired else self.history[np.where(~np.isnan(self.history) == True)[0][-1]]
    def peakRating(self):
        return np.nanmax(self.history+[self.rating]) if self.started else 1500
    def __repr__(self):
        if self.started:
            return self.name + ": 1500 -> " + str(int(self.effRating()*10)/10) + "  ("+ str(int((self.effRating()-1500)*10)/10) +")" + "  Peak: " + str(int(self.peakRating() * 10)/10) + "  (" + str(int((self.effRating() - self.peakRating()) * 10)/10) + ")"
        else:
            return self.name + ": hasn't made professional debut"

points = [25,18,15,12,10,8,6,4,2,1,-1,-2,-4,-6,-8,-10,-12,-15,-18,-25,-32,-39]

drivers = []
f = open('drivers.txt')
lines = f.readlines()
for d in lines:
    drivers.append(Driver(d[:-1]))
f.close()

f = open('data')
lines = f.readlines()
for n in range(len(lines)):
    s = lines[n].split(',')
    if s[0] == "--":
        for i in range(len(drivers)):
            try:
                rank = s.index(drivers[i].name)
                drivers[i].buffer = drivers[i].rating + (drivers[i].k*(11-rank))
            except:
                continue
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
        for i in range(len(drivers)):
            try:
                opp = 0
                n = 0
                ratings = []
                for j in range(len(drivers)):
                    if j != i:
                        try:
                            check = s.index(drivers[j].name)
                            opp += drivers[j].rating
                            ratings.append(drivers[j].rating)
                            n += 1
                        except:
                            continue
                opp /= n
                ratings.sort(reverse=True)
                expected = len(ratings)+1
                score = points[s.index(drivers[i].name)]
                for l in range(len(ratings)):
                    if ratings[l] <= drivers[i].rating:
                        expected = l
                        break
                drivers[i].started = True
                drivers[i].ratingAdjust(score, points[expected])
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
for driver in drivers:
    z = driver.history
    if driver.started:
        if not driver.retired:
            z.append(driver.rating)
        ax.plot(z, label = driver.name)

plt.xlabel('races')
plt.ylabel('elo')
ax.set_yticks(np.arange(int(np.nanmin(drivers[-1].history))-20, int(high)+20, 20))
x = np.arange(0,214,1)
xlabels = ['14','','','','','','','','','','','','','','','','','','','','15','','','','','','','','','','','','','','','','','','','','16','','','','','','','','','','','','','','','','','','','','','17','','','','','','','','','','','','','','','','','','','','','18','','','','','','','','','','','','','','','','','','','','','','19','','','','','','','','','','','','','','','','','','','','','','20','','','','','','','','','','','','','','','','','','21','','','','','','','','','','','','','','','','','','','','','','','22','','','','','','','','','','','','','','','','','','','','','','','23','','','','','','','','','','','','','','','','','','','','','','','24']
ax.set_xticks(x)
ax.set_xticklabels(xlabels)
plt.legend(loc="lower right",bbox_to_anchor=(1.1, 0), fontsize="7")
#plt.tight_layout()
ax = plt.gca()
for tick in ax.get_yticks():
    ax.axhline(y=tick, color='gray', linestyle='--', linewidth=0.7)
ax.axhline(y=1600, color='black', linestyle = '--', linewidth=1.7)
ax.axhline(y=1500, color='black', linestyle = 'dotted', linewidth=3.7)
ax.axhline(y=1400, color='black', linestyle = '--', linewidth=1.7)
for tick, label in zip(x, xlabels):
    if len(label) > 0:
        ax.axvline(x=tick, color='gray', linestyle='-', linewidth=1)
plt.show()

f.close()