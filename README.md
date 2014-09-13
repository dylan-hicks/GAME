####What is the purpose of the GAME programming language?

GAME is designed to solve problems related to sports statistics as well as sports management.
Today, decisions in the world of sports increasingly need to be backed by data and quantitative
analysis, rather than stemming from purely qualitative assessments. This is important for
athletes, coaches, and managers in improving their individual and team performance in addition
to sports reporters seeking compelling data to back their stories. Thus, a lot of money and many
careers are involved in the practice of data analytics in sports. Accessing, manipulating,
updating, and analyzing data are essential in the pursuit of game­changing information ­­ GAME
allows users to accomplish this objective.

####What do I need to run it?

In order to clone the repository and run the compiler, you will need the following packages:

    python
    python-matplotlib
    python-numpy
    gcc
    git
    make

Note that although this code has been written to be cross-platform, the majority of testing has been in Linux.

####How do I set it up?

Choose what directory you want the compiler in, then run the following commands:

    git clone https://github.com/dylan-hicks/GAME.git
    cd GAME
    make

If you aren't using Linux these commands may be slightly different.

####What is an example of a problem you can solve using GAME?

One pressing question in Basketball is when should a player "take the shot", specifically in the mid-range. 
The following demo program analyzes the relationship between the percentage of mid-range shots and total point scored.

    class NBATeam{
        text Team
        num points
        num in_paint
        num from_threes
    }
    function main(){
        list(NBATeam) teams
        load teams from "demo_programs/nba_teams.json"
        list(num) perc_from_mid
        list(num) total_points
        foreach(NBATeam i in teams){
            num points_from_mid = i.points - i.in_paint - i.from_threes
            perc_from_mid.add(points_from_mid / i.points)
            total_points.add(i.points)
        }
        graph(perc_from_mid, total_points, "blue", "circle", "% Midrange vs. Total")
        bestfit(perc_from_mid, total_points, "green", "solid", "Best fit line")
        axis({0.2, 0.5},{80, 120})
        label("x", "% of Points from Mid-range")
        label("y", "Total points (Avg)")
        label("title", "Relationship between % of points scored from mid and total points")
        display()
    }

You can run this demo program yourself by going to the GAME directory and executing:

    make mid_range

Note: This should open up a new window, if you are remotely using a computer make sure to use the -Y option for ssh.
If you want more examples, try the following commands:

    make avg_aces
    make curry
    make sykes

###How do I write the "Hello, World" program?

Open up a good editor (we recomend Vim) and save the following code as hello.game (in the GAME folder):

    function main(){
        print("Hello, World")
    }

Then compile it using "./gamec -o hello.game", and then you may run it with "python hello.game.py".

###How do I learn more?

We have written a tutorial and a reference manual (in the Docs folder) so that you may learn all of GAME's wonderful features.
