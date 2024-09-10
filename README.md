<h1 align="center"> &nbsp;&nbsp;F1 Elo Engine</h1>
<br/>

> An ELO calculator for F1 drivers created in python

---
   
## Instructions

#### Directions to Use
```sh
> git clone https://github.com/AngadBasandrai/x86-asm-os.git

> pip install -r requirements.txt

> python main.py
```

<hr/>

## Explanation

### ELO System
$Q = \frac{1}{1 + 10^{{R - \bar{R}}/200}}$ \
$Q = Win$ $Chance$ \
$R = Player$ $Rating$ \
$\bar{R} = Average$ $Opponent$ $Rating$ \
so to adjust for negative points below top 10 finishes \
$E = (2Q - 1) * 25$  \
$E$ = $Expected$ $Points$ 

Then expected score is compared with ponts scored \
$S = Points$ $Scored$ \
$R_n = R + K*(S-E)$ \
$R_n = New$ $Rating$

if the number of races participated in is less than 10 than when a player performs better than expected $K_n = 2*K$ \
if the rating goes above 1300 then $K_n = 0.5*K$

### Data Parsing
It iterates through <a href="https://github.com/AngadBasandrai/f1-elo-engine/blob/main/data.csv">data.csv</a> and for each line performs the above mentioned calculations for each player and points are scored according to the points table defined in <a href="https://github.com/AngadBasandrai/f1-elo-engine/blob/main/main.py">main.py</a> \
Upon encountering a line beginning with '--', it will stores the ratings at that point into <a href="https://github.com/AngadBasandrai/f1-elo-engine/blob/main/winners.txt">winners.txt</a>\
When a line starts with '~', it retires the players who are in that line

At the end it stores all the data into <a href="https://github.com/AngadBasandrai/f1-elo-engine/blob/main/driverData.csv">driverData.csv</a> from where it can be loaded anytime using 
```sh
> python main.py -l
```
or 
```sh
> python main.py --load
```

## Contributors
<table align="center">
	<tr align="center" style="font-weight:bold">
		<td>
		Angad Basandrai
		<p align="center">
			<img src = "https://avatars.githubusercontent.com/u/112087272?v=4" width="150" height="150" alt="Angad Basandrai">
		</p>
			<p align="center">
				<a href = "https://github.com/AngadBasandrai">
					<img src = "http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height = "36" alt="GitHub"/>
				</a>
			</p>
		</td>
	</tr>
</table>

## License
[![License](http://img.shields.io/:license-gpl3-blue.svg?style=flat-square)]([http://badges.mit-license.org](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text))

<p align="center">
	Made with :heart: by <a href="https://github.com/AngadBasandrai" target="_blank">Angad Basandrai</a>
</p>
