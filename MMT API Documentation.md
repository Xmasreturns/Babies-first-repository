#Mahjong Matchmaking Toolkit

Mahjong Matchmaking Toolkit (MMT) is a set of functions for manipulating player data and seating players based on their past game history. This toolkit can be used to retrieve useful subsets of game data from an external database, as well as to seat players according to a variety of matchmaking techniques.

Here are a few things you may want to do that MMT can help with:
* Aggregate data for a subset of players in a play group
* Seat players by minimizing the number of times each person plays against the same opponents over time
* Seat players together with opponents they have not played recently
* Visualize data regarding a subset of players in a play group

#####Note: This library uses the following release versions:
* [Python 2.7.2](https://www.python.org/download/releases/2.7.2/)
* [Numpy 1.9.2](http://www.scipy.org/scipylib/download.html)
* [Pandas 0.16.2](http://pypi.python.org/pypi/pandas/0.16.2/#downloads)

## Navigation
- [1. Data Inputs](#1.-data-inputs)
	- [1.1 Game Data](#1.1-game-data)
	- [1.2 Players](#1.2-players)
- [2. Function Overview](#2.-function-overview)
- [3. Function Details](#3.-function-details)

##1. Data Inputs
####1.1 Game Data
Functions in this package require play data in **`.csv`** format with headers that include **`'GameId'`**, **`'PlayerId'`**, **`'Rank'`**, and **`'Score'`**. Additional requirements are as follows:

* Each column must contain only a single datatype
* Each **`GameId`** value must only correspond to 4 or 5 rows, reflecting the number of people playing in that game.
* All values in the **`PlayerId`** and **`GameId`** columns must be integers, strings, or tuples
* All values in the **`Rank`** and **`Score`** columns must be integers

For example, the following is a pandas [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) object converted from Example_Data.csv. It contains information for 2 games played, one on April 6th and another on April 12th:

    >>> df = pandas.read_csv('Example_Data.csv')
    >>> print df

Round & Date | Rank | Player Name | Score
--- | --- | --- | ---
(4, 2010-04-06) | 2 | DMX | 19
(4, 2010-04-06) | 1 | Tanye West | 26
(4, 2010-04-06) | 4 | Leela J. | -4
(4, 2010-04-06) | 3 | Darby P. | 3
(1, 2010-04-12) | 2 | Tanye West | 12
(1, 2010-04-12) | 3 | Ted Q. | 10
(1, 2010-04-12) | 5 | Darby P. | 5
(1, 2010-04-12) | 1 | DMX | 40
(1, 2010-04-12) | 4 | Leela J. | 9

As you can see, the table is improperly formatted - there is no `GameId` column, and there is no `PlayerId` column. All values are in the allowed datatypes, so getting to the correct format only requires renaming the `Round & Date` and `Player Name` headers to `GameId` and `PlayerId`: 

```
>>> df.rename(columns={'Round & Date': 'GameId', 'Player Name': 'PlayerId'}, inplace=True)
>>> print df
```

GameId | Rank | PlayerId | Score
--- | --- | --- | ---
(4, 2010-04-06) | 2 | DMX | 19
(4, 2010-04-06) | 1 | Tanye West | 26
(4, 2010-04-06) | 4 | Leela J. | -4
(4, 2010-04-06) | 3 | Darby P. | 3
(1, 2010-04-12) | 2 | Tanye West | 12
(1, 2010-04-12) | 3 | Ted Q. | 10
(1, 2010-04-12) | 5 | Darby P. | 5
(1, 2010-04-12) | 1 | DMX | 40
(1, 2010-04-12) | 4 | Leela J. | 9

####1.2 Players
Functions in this package require player inputs as a Python list of each `PlayerId` value to be used. The order of the players does not matter, but they must be of the same datatype as the values in `PlayerId`. For example, all of the following are valid inputs for a group of 9 players:

    >>> players_list = [5, 1, 2, 4, 8, 7, 6, 3, 9]
    >>> players_list = ['John', 'Ted', 'Joy', 'Ted F.', 'Terry', 'Peter Jackson', 'DMX', 'TanYe West', 'Brunhilda']
    >>> players_list = [(1,1),(1,2),(1,3),(1,4),(5,1),(6,1),(7,1),(8,3),(9,4)]

##2. Function Overview

[`get_player_data(input_data, players_list)`](#get_player_data%28input_data,-players_list%29)

* Returns a [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) object containing only the rows of `input_data` with players in `players_list`.

[`get_playerid_games(input_data, PlayerId)`](#get_playerid_games%input_data,-PlayerId%29)

* Returns a [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) object containing only the rows of `input_data` with the player corresponding to `PlayerId`.

[`get_split_tables(table_counts, players_list)`](#get_split_tables%28table_counts,-players_list%29)

* Returns `players_list` split into smaller lists, based on the required table sizes from `table_counts`.

[`get_table_counts(players_list)`](#get_table_counts%28players_list%29)

* Returns a list of integers in the order: total # tables, # of 4 player tables, # of 5 player tables.

[`create_pairings_table(players_list)`](#create_pairings_table%28players_list%29)

* Returns a sorted [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) object with each `PlayerId` in `players_list` as both row and column labels. All values in the DataFrame are set to zero.

[`create_freq_matchups(pairings_df, input_data)`](#create_freq_matchups%28pairings_df,-input_data%29)

* Returns a sorted [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) object with each `PlayerId` in `players_list` as both row and column labels. All values in the DataFrame are calculated as the total number of times players of corresponding indices have played against each other.

[`create_score_matchups(pairings_df, input_data)`](#create_score_matchups%28pairings_df,-input_data%29)

* Returns a sorted [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) object with each `PlayerId` in `players_list` as both row and column labels. All values in the DataFrame are the calculated average score of the player of the corresponding row when having played against the player of the corresponding column.

[`match_by_rating(table_counts, matchups_df)`](#match_by_rating%28table_counts,-matchups_df%29)

* Returns a list of lists. Each inner list represents a table and corresponds to a group of `PlayerId` values.

[`playerstats(input_data, players_list)`](#playerstats%28input_data,-players_list%29)

* Returns a [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) object containing aggregate data for each player in `players_list`.

[`sum_ratings(table_players, matchups_df)`](#sum_ratings%28table_players,-matchups_df%29)

* Returns an integer value equal to the sum of matchmaking ratings for all players at the table.

[`swap_two(entrylist)`](#swap_two%28entrylist%29)

* Returns `entrylist` with two random elements swapped.

##3. Function Details
###`get_player_data(input_data, players_list)`

Returns a [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) object containing only the rows of `input_data` with players in `players_list`.

####Parameters:

>`input_data`: *DataFrame*
* All historical game data from which to retrieve player data. Must contain the headers `GameId`, `PlayerId`, `Rank`, and `Score`. For each of these headers, the respective values should follow the [data input requirements](#1.-Data-Inputs).

>`players_list`: *list*
* All `PlayerId` values to be retrieved from `input_data`. All values must be integers, strings, or tuples, and of the same datatype. (e.g. [1,2,3], ['Ted','Joe','Emma']).

####Returns:

>datatype: *DataFrame*
* Result will be a new DataFrame object having the same columns as `input_data` and excluding all rows not containing `PlayerId` elements of `players_list`.

###`get_playerid_games(input_data, PlayerId)`

Returns a [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) object containing only the rows of `input_data` with the player corresponding to `PlayerId`.

####Parameters:

>`input_data`: *DataFrame*
* All historical game data from which to retrieve player data. Must contain the headers `GameId`, `PlayerId`, `Rank`, and `Score`. For each of these headers, the respective values should follow the [data input requirements](#1.-Data-Inputs).

>`PlayerId`: *int, string, or tuple*
* `PlayerId` value whose rows are to be retrieved from `input_data`. Value must be of the same datatype as those in `PlayerId` column of `input_data`.

####Returns:

>datatype: *DataFrame*
* Result will be a new DataFrame object having the same columns as `input_data` and excluding all rows not containing `PlayerId` elements of `players_list`.

###`get_split_tables(table_counts, players_list)`
    
Returns `players_list` split into smaller lists, based on the required table sizes from `table_counts`.
####Parameters:

>`table_counts`: *list of integers*
* Input must be a list of integers where the first 3 elements are: the total number of tables, the number of 4 player tables, and the number of 5 player tables. Total number of tables must equal the sum of the number of 4 and 5 player tables. See [`get_table_counts()`](#get_table_counts%28players_list%29) for more information.

>`players_list`: *list*
* Contains all players to be split into tables. All values must be integers, strings, or tuples, and of the same datatype. (e.g. [1,2,3], ['Ted','Joe','Emma']).

####Returns:

>datatype: *list of lists*
* Contains a list with the contents of `players_list`, but grouped into lists of length 4 or 5 based on `table_counts`.

####Example: 
    >>> table_counts = [2, 1, 1]
    >>> people = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> get_split_tables(table_counts, people)
    [[1, 2, 3, 4], [5, 6, 7, 8, 9]]

###`get_table_counts(players_list)`
    
Returns a list of integers in the order: total # tables, # of 4 player tables, # of 5 player tables.
####Parameters:

>`players_list`: *list*
* Contains all players to be accounted for in the table seating determination. All values must be integers, strings, or tuples, and of the same datatype. (e.g. [1,2,3], ['Ted','Joe','Emma']).

####Returns:

>datatype: *list of integers*
* Contains, in order, the total number of tables, the number of 4 player tables, and the number of 5 player tables. Will use the lowest possible number of 5 player tables while accounting for all players.

####Example: 
    >>> people = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    >>> get_table_counts(people)
    [3, 2, 1]

###`create_pairings_table(players_list)`
    
Returns a sorted [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) object with each `PlayerId` in `players_list` as both row and column labels. All values in the DataFrame are set to zero.
####Parameters:

>`players_list`: *list*
* All `PlayerId` values to be used as row and column labels. All values must be integers, strings, or tuples, and of the same datatype. (e.g. [1,2,3], ['Ted','Joe','Emma']).

####Returns:

>datatype: *DataFrame*
* Result will be a square DataFrame having all values set to zero. Row and column labels will be symmetric across the diagonal.

####Example: 
    >>> friends = ['Ted','Joe','Mary']
    >>> df = create_pairings_table(friends)
    >>> df

 | Ted | Joe | Mary
-- | -- | -- | --
**Ted** | 0 | 0 | 0
**Joe** | 0 | 0 | 0
**Mary** | 0 | 0 | 0

###`create_freq_matchups(pairings_df, input_data)`

Returns a sorted [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) object with each `PlayerId` in `players_list` as both row and column labels. All values in the DataFrame are calculated as the total number of times players of corresponding indices have played against each other.

####Parameters:
>`pairings_df`: *DataFrame*
* Contains all players to be paired as both row and column labels in a square DataFrame. All values in the DataFrame must be zero to return a DataFrame with the correct sums.

>`input_data`: *DataFrame*
* All historical game data to be used as a basis for frequency calculation. Must contain the headers `GameId` and `PlayerId`. For each of these headers, the respective values should contain only a single datatype and be uniquely identifiable.

####Returns:

>datatype: *DataFrame*
* Column and row indices will be sorted in ascending order. Values on the diagonal are equal to the number of games played by the player with that row and column label. Values are symmetric across the diagonal.

###`create_score_matchups(pairings_df, input_data)`

Returns a sorted [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) object with each `PlayerId` in `players_list` as both row and column labels. All values in the DataFrame are the calculated average score of the player of the corresponding row when having played against the player of the corresponding column.

####Parameters:
>`pairings_df`: *DataFrame*
* Contains all players to be paired as both row and column labels in a square DataFrame. All values in the DataFrame must be zero to return a DataFrame with the correct sums.

>`input_data`: *DataFrame*
* All historical game data to be used as a basis for frequency calculation. Must contain the headers `GameId` and `PlayerId`. For each of these headers, the respective values should contain only a single datatype and be uniquely identifiable.

####Returns:

>datatype: *DataFrame*
* Column and row indices will be sorted in ascending order. Values on the diagonal are equal to the average score of the player with that row and column label. Values will **not** be symmetric across the diagonal. All values in the DataFrame are the average score of the player of the corresponding row when having played against the player of the corresponding column.

###`match_by_rating(table_counts, matchups_df)`

Returns a list of lists. Each inner list represents a table and corresponds to a group of `PlayerId` values.

####Parameters:

>`table_counts`: *list of integers*
* Input must be a list of integers where the first 3 elements are: the total number of tables, the number of 4 player tables, and the number of 5 player tables. Total number of tables must equal the sum of the number of 4 and 5 player tables.

>`matchups_df`: *DataFrame*
* Contains matchmaking rating values for each row-column pair corresponding to the players with those labels. Matchmaking rating should result in the players best matched to each other having the lowest values. All player labels in this DataFrame will be placed at exactly one table.

####Returns:

>datatype: *list of lists*
* Each tuple represents a table of players and corresponds to a group of `PlayerId` values.
* For example, the output `[[1, 13, 22, 40], [6, 10, 41, 72, 79]]` denotes 2 tables.
 * Table 1: [`PlayerId = 1, PlayerId = 13, PlayerId = 22, PlayerId = 40`].
 * Table 2: [`PlayerId = 6, PlayerId = 10, PlayerId = 41, PlayerId = 72, PlayerId = 79`].


###`playerstats(input_data, players_list)`

Returns a [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) object containing aggregate data for each player in `players_list`.

####Parameters:

>`input_data`: *DataFrame*
* All historical game data for which to generate aggregate data. Must contain the headers `GameId`, `PlayerId`, `Rank`, and `Score`. For each of these headers, the respective values should follow the [data input requirements](#1.-Data-Inputs).

>`players_list`: *list*
* `PlayerId` values in `input_data` for which to generate aggregate data. All values must be integers, strings, or tuples, and of the same datatype. (e.g. [1,2,3], ['Ted','Joe','Emma']).

####Returns:

>datatype: *DataFrame*
* Each tuple represents a table of players and corresponds to a group of `PlayerId` values.
* For example, the output `[[1, 13, 22, 40], [6, 10, 41, 72, 79]]` denotes 2 tables.
 * Table 1: [`PlayerId = 1, PlayerId = 13, PlayerId = 22, PlayerId = 40`].
 * Table 2: [`PlayerId = 6, PlayerId = 10, PlayerId = 41, PlayerId = 72, PlayerId = 79`].


###`sum_ratings(table_players, matchups_df)`
    
Returns an integer value equal to the sum of matchmaking ratings for all players at the table
####Parameters:

>`table_players:` *list*
* Contains all players to be accounted for in the table aggregate matchmaking determination. All values must be integers, strings, or tuples, and of the same datatype. (e.g. [1,2,3], ['Ted','Joe','Emma']).

>`matchups_df`: *DataFrame*
* Must contain all players in `table_players` as labels in both the rows and columns. Should contain matchmaking ratings for each player-player pairing in a square matrix that is symmetric across the diagonal. These rating may be calculated using any method, but should result in the players best matched to each other having the lowest values.

####Returns:

>datatype: *int*
* Sum aggregate of all matchmaking ratings for each player at the table with each other player as their opponent.

###`swap_two(entrylist)`
Returns `entrylist` with two random elements swapped.

####Parameters:

>`entrylist`: *list*
* Contains all elements to be considered for swapping.

####Returns:

>datatype: *list*
* Contains all original elements of `entrylist`, but with two randomly selected elements having exchanged indices.
