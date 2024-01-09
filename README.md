"The most common way to perform bidding in armageddon rounds is to write your bid down on a piece of paper and give it to the arbiter without showing it to your opponent.

Then the arbiter will reveal both bids. The player willing to play on less time will get the Black pieces and draw odds."

For this analysis on what each player should bid we will be operating with the following assumptions

1. As you have less time your functional skill (as measured by your Elo score) decreases
2. As your skill decreases your opponent's probability to win increases at the expense of your probability to win and the probability to draw

Both of these assumptions leads us to the concept of the skill modifier curve

### skill modifier curve

Elo, as a measurement, only defines a skill level at that control. There is a previously unmeasured modifier that relates the strength of a player over the course of the game at one time control to a player over the course of a game at another time control. 

This can be visualized as

T(1) * M = T(2)

M is the modifier.

To ground it in an example, if a 1200 Elo player with 5+0 time controls can go even with a 1600 player with 3+0 time controls then the modifier is 1.333

T(3+0) * M = T(5+0)

We denote the larger time on right

### what impacts M
#### player
#### amount of time

Moral is, I don’t know. I think it’s on a per player, per time basis

But by comparing average centipede loss at different time controls we can make a comparison

Then double check this with beserk mode

Asterisk with the fact that you can think on your opponents turns

### make charts for top players

Make an overlayed chart for Players at various time controls. Basically it would just be a chart of your centipede loss adjusted for the player you were playing against in the mid game only. 

Explain the reasoning behind this selection

From this we can get a players M curve

### applying this

Let’s consider a situation where Player A and Player B are going to play chess in Armageddon.  You work to find each players “threshold point”. This is where the M value from Player A is significant enough that it cancels out the advantage that they would get from having draw advantage. 

Pa(15+0) = Pb(15+0)

Pa(win only, 15+0) = Pb(draw or win, T+0)

Now we need to solve for T using our modifier curve. 

First we find the Elo of the player that would be equal given the draw odds. This can be reasonable estimated. 

Then we find the ratio of the Elos and move along the modifier curve until we find T(a>b). We repeat this in the other direction to find T(b>a). 

Both of these are the players “threshold times”. If the player won the bid with this time they would be in a 50/50 chance to win. 

If there is a difference in players threshold times then player should be bidding in the middle of them, understanding that the player with the lower threshold time has the advantage. 



Okay so we have some data and can make some ideas
The issue is that the positions aren't super obvious on directions of if its better or worse

Also with the data we have none of the positions really go beyond move 6 or 7

So I want to add more data? But we can't because we maxed out the local db

Part of me wants to do this on AWS where I can just throw a hella amount of data?
