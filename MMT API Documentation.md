# Mahjong Matchmaking Toolkit

**The following release versions are used:**
* [Python 3.4.4](https://www.python.org/downloads/releases/3.4.4/)
* [Numpy 1.11.0](http://www.scipy.org/scipylib/download.html)
* [Pandas 0.18.1](https://pypi.python.org/pypi/pandas)

Mahjong Matchmaking Toolkit (MMT) is designed to help group organizers implement player matchmaking. Using imported historical game data, MMT simplifies the calculation of matchmaking ratings for each player in a group. Additionally, MMT can arrange players based on their personal rating.

For instance, a mahjong group organizer needs to assign players to their tables at a scheduled meetup. However, they want to do this such that each table contains players of roughly equal skill. To do so, they use MMT to calculate each attendee's matchmaking rating. Based on that rating, MMT then groups the players into tables for the organizer.

Sample techniques are included for creating matchmaking ratings based on play frequency and [individual scoring](https://en.wikipedia.org/wiki/Japanese_Mahjong), but other techniques (such as [Elo](https://en.wikipedia.org/wiki/Elo_rating_system)) can be used as well.

**More advanced uses of MMT:**
* Fully automate player matchmaking by connecting to a database
* Create visualizations of an individual's scoring performance over time
* Predict the score of each player at a table based on past performance against each other player

## Navigation
* [1. Data Inputs](#1-data-inputs)
	* [1.1 Game Data](#11-game-data)
	* [1.2 Player Lists](#12-player-lists)
* [2. Function Overview](#2-function-overview)
* [3. Function Details](#3-function-details)

## 1. Data Inputs
#### 1.1 Game Data
Functions in this package require game data in **`.csv`** format. Entry headers must include **`GameId`**, **`PlayerId`**, **`Rank`**, and **`Score`**. Additional requirements are as follows:

* Each column must contain only a single datatype
* Each **`GameId`** value must correspond only to 4 or 5 rows, reflecting the number of people playing in that game.
* All values in the **`PlayerId`** and **`GameId`** columns must be integers, strings, or tuples
* All values in the **`Rank`** and **`Score`** columns must be integers

The following example is a pandas [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) object converted from **`Example_Data.csv`**. It contains properly formatted information for 2 games played - one on April 6th and another on April 12th:

```Python
>>> df = pandas.read_csv('Example_Data.csv')
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

#### 1.2 Player Lists
Whenever a function requires a list of players, use **`PlayerId`** values from the game data. All of the following are valid inputs for a group of 9 players:
```Python
>>> player_list = [5, 1, 2, 4, 8, 7, 6, 3, 9]
>>> player_list = ['John', 'Ted', 'Joy', 'Ted F.', 'Terry', 'Peter Jackson', 'DMX', 'TanYe West', 'Brunhilda']
>>> player_list = [(1,1),(1,2),(1,3),(1,4),(5,1),(6,1),(7,1),(8,3),(9,4)]
```
Note that order **does not** matter.

## 2. Function Overview
[`create_pairings_df(player_list)`](#create_pairings_dfplayer_list)

* Initializes a [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) with a number of rows and columns equal to the number of players in the provided list. Each axis is labeled with the sorted contents of the provided list, and all cell values are set to zero.

[`generate_freq_mmr(pairings_df, input_data)`](#generate_freq_mmrpairings_df-input_data)

* Generates and assigns a matchmaking rating (MMR) value to each cell of a provided [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html). This MMR is based on the total number of times players of corresponding indices have played against each other. Use `create_pairings_df` for initializing the input [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html).

[`generate_score_mmr(pairings_df, input_data)`](#generate_score_mmrpairings_df-input_data)

* Generates and assigns a matchmaking rating (MMR) value to each cell of a provided [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html). This MMR is based on the average score of the player of the corresponding row when having played against the player of the corresponding column. Use `create_pairings_df` for initializing the input [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html).

[`get_player_data(input_data, player_list)`](#get_player_datainput_data-player_list)

* Reduces input data to contain only games including players in the provided list.

[`get_playerid_games(input_data, PlayerId)`](#get_playerid_gamesinput_data-playerid)

* Reduces input data to contain only games including the provided **`PlayerID`**.

[`get_split_tables(table_counts, player_list)`](#get_split_tablestable_counts-player_list)

* Splits the provided list of players into smaller lists, based on the required number of 4 and 5 player tables to seat all players.

[`get_table_counts(player_list)`](#get_table_countsplayer_list)

* Determines the number of 4 and 5 player tables required to seat all players in the provided list of players.

[`match_by_mmr(table_counts, matchups_df)`](#match_by_mmrtable_counts-matchups_df)

* Generates groupings of individuals based on matchmaking ratings provided in a [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html). Group sizes are determined by the required number of 4 and 5 player tables to seat all players.

[`playerstats(input_data, player_list)`](#playerstatsinput_data-player_list)

* Generates a [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) containing aggregate data for each player in the provided list based on their historical game data.

[`sum_table_mmr(table_players, matchups_df)`](#sum_table_mmrtable_players-matchups_df)

* Calculates a matchmaking score based on the sum of matchmaking rating for a given table of players. Matchmaking scores identical in value indicate a perfect match.

[`swap_two(entrylist)`](#swap_twoentrylist)

* Returns **`entrylist`** with two random elements swapped.

## 3. Function Details
### `create_pairings_df(player_list)`
Initializes a [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) with a number of rows and columns equal to the number of players in the provided list. Each axis is labeled with the sorted contents of the provided list, and all cell values are set to zero.

##### Parameters:
>`player_list`: *list*
* All `PlayerId` values to be used as row and column labels. All values must be integers, strings, or tuples, and of the same datatype. (e.g. [1,2,3], ['Ted','Joe','Emma']).

##### Returns:
>datatype: *DataFrame*
* Result will be a square DataFrame having all values set to zero. Row and column labels will be symmetric across the diagonal.

##### Example:
```Python
>>> friends = ['Ted','Joe','Mary']
>>> df = create_pairings_df(friends)
>>> print df
```
 <span></span> | Ted | Joe | Mary
--- | --- | --- | ---
**Ted** | 0 | 0 | 0
**Joe** | 0 | 0 | 0
**Mary** | 0 | 0 | 0

### `generate_freq_mmr(pairings_df, input_data)`
Modifies the contents of a [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) using the total number of times players of corresponding indices have played against each other. Each cell is increased by the number of games played between the corresponding players. When called with an empty [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html), cell values can be used as matchmaking ratings.

##### Parameters:
>`pairings_df`: *DataFrame*
* Contains all players to be paired as both row and column labels in a square DataFrame. All values in the DataFrame must be zero to return a DataFrame with the correct sums.

>`input_data`: *DataFrame*
* All historical game data to be used as a basis for frequency calculation. Must contain the headers `GameId` and `PlayerId`. For each of these headers, the respective values should contain only a single datatype and be uniquely identifiable.

##### Returns:
>datatype: *DataFrame*
* Column and row indices will be sorted in ascending order. Values on the diagonal are equal to the number of games played by the player with that row and column label. Values are symmetric across the diagonal.

### `generate_score_mmr(pairings_df, input_data)`
Modifies the contents of a [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) using the calculated average score of the player of the corresponding row when having played against the player of the corresponding column. When called with an empty [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html), cell values can be used as matchmaking ratings.

##### Parameters:
>`pairings_df`: *DataFrame*
* Contains all players to be paired as both row and column labels in a square DataFrame. All values in the DataFrame must be zero to return a DataFrame with the correct sums.

>`input_data`: *DataFrame*
* All historical game data to be used as a basis for frequency calculation. Must contain the headers `GameId` and `PlayerId`. For each of these headers, the respective values should contain only a single datatype and be uniquely identifiable.

##### Returns:
>datatype: *DataFrame*
* Column and row indices will be sorted in ascending order. Values on the diagonal are equal to the average score of the player with that row and column label. Values will **not** be symmetric across the diagonal. All values in the DataFrame are the average score of the player of the corresponding row when having played against the player of the corresponding column.

### `get_player_data(input_data, player_list)`
Reduces input data to contain only games including players in the provided list.

##### Parameters:
>`input_data`: *DataFrame*
* All historical game data from which to retrieve player data. Must contain the headers `GameId`, `PlayerId`, `Rank`, and `Score`. For each of these headers, the respective values should follow the [data input requirements](#1.-Data-Inputs).

>`player_list`: *list*
* All `PlayerId` values to be retrieved from `input_data`. All values must be integers, strings, or tuples, and of the same datatype. (e.g. [1,2,3], ['Ted','Joe','Emma']).

##### Returns:
>datatype: *DataFrame*
* Result will be a new DataFrame object having the same columns as `input_data` and excluding all rows not containing `PlayerId` elements of `player_list`.

### `get_playerid_games(input_data, PlayerId)`
Reduces input data to contain only games including the provided **`PlayerID`**.

##### Parameters:
>`input_data`: *DataFrame*
* All historical game data from which to retrieve player data. Must contain the headers `GameId`, `PlayerId`, `Rank`, and `Score`. For each of these headers, the respective values should follow the [data input requirements](#1.-Data-Inputs).

>`PlayerId`: *int, string, or tuple*
* `PlayerId` value whose rows are to be retrieved from `input_data`. Value must be of the same datatype as those in `PlayerId` column of `input_data`.

##### Returns:
>datatype: *DataFrame*
* Result will be a new DataFrame object having the same columns as `input_data` and excluding all rows not containing `PlayerId` elements of `player_list`.

### `get_split_tables(table_counts, player_list)`
Splits the provided list of players into smaller lists, based on the required number of 4 and 5 player tables to seat all players.

##### Parameters:
>`table_counts`: *list of integers*
* Input must be a list of integers where the first 3 elements are: the total number of tables, the number of 4 player tables, and the number of 5 player tables. Total number of tables must equal the sum of the number of 4 and 5 player tables. See [`get_table_counts()`](#get_table_counts%28player_list%29) for more information.

>`player_list`: *list*
* Contains all players to be split into tables. All values must be integers, strings, or tuples, and of the same datatype. (e.g. [1,2,3], ['Ted','Joe','Emma']).

##### Returns:
>datatype: *list of lists*
* Contains a list with the contents of `player_list`, but grouped into lists of length 4 or 5 based on `table_counts`.

##### Example:
```Python
>>> table_counts = [2, 1, 1]
>>> people = [1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> get_split_tables(table_counts, people)
[[1, 2, 3, 4], [5, 6, 7, 8, 9]]
```

### `get_table_counts(player_list)`
Determines the number of 4 and 5 player tables required to seat all players in the provided list of players.

##### Parameters:
>`player_list`: *list*
* Contains all players to be accounted for in the table seating determination. All values must be integers, strings, or tuples, and of the same datatype. (e.g. [1,2,3], ['Ted','Joe','Emma']).

##### Returns:
>datatype: *list of integers*
* Contains, in order, the total number of tables, the number of 4 player tables, and the number of 5 player tables. Will use the lowest possible number of 5 player tables while accounting for all players.

##### Example:
```Python
>>> people = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
>>> get_table_counts(people)
[3, 2, 1]
```

### `match_by_mmr(table_counts, matchups_df)`
Generates groupings of individuals based on matchmaking ratings provided in a [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html). Group sizes are determined by the required number of 4 and 5 player tables to seat all players.

##### Parameters:
>`table_counts`: *list of integers*
* Input must be a list of integers where the first 3 elements are: the total number of tables, the number of 4 player tables, and the number of 5 player tables. Total number of tables must equal the sum of the number of 4 and 5 player tables.

>`matchups_df`: *DataFrame*
* Contains matchmaking rating values for each row-column pair corresponding to the players with those labels. Matchmaking rating should result in the players best matched to each other having the lowest values. All player labels in this DataFrame will be placed at exactly one table.

##### Returns:
>datatype: *list of lists*
* Each tuple represents a table of players and corresponds to a group of `PlayerId` values.
* For example, the output `[[1, 13, 22, 40], [6, 10, 41, 72, 79]]` denotes 2 tables.
 * Table 1: [`PlayerId = 1, PlayerId = 13, PlayerId = 22, PlayerId = 40`].
 * Table 2: [`PlayerId = 6, PlayerId = 10, PlayerId = 41, PlayerId = 72, PlayerId = 79`].


### `playerstats(input_data, player_list)`
Generates a [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) containing aggregate data for each player in the provided list based on their historical game data.

##### Parameters:
>`input_data`: *DataFrame*
* All historical game data for which to generate aggregate data. Must contain the headers `GameId`, `PlayerId`, `Rank`, and `Score`. For each of these headers, the respective values should follow the [data input requirements](#1-data-inputs).

>`player_list`: *list*
* `PlayerId` values in `input_data` for which to generate aggregate data. All values must be integers, strings, or tuples, and of the same datatype. (e.g. [1,2,3], ['Ted','Joe','Emma']).

##### Returns:
>datatype: *DataFrame*
* Each tuple represents a table of players and corresponds to a group of `PlayerId` values.
* For example, the output `[[1, 13, 22, 40], [6, 10, 41, 72, 79]]` denotes 2 tables.
 * Table 1: [`PlayerId = 1, PlayerId = 13, PlayerId = 22, PlayerId = 40`].
 * Table 2: [`PlayerId = 6, PlayerId = 10, PlayerId = 41, PlayerId = 72, PlayerId = 79`].


### `sum_table_mmr(table_players, matchups_df)`
Calculates a matchmaking score based on the sum of matchmaking rating for a given table of players. Matchmaking scores identical in value indicate a perfect match.

##### Parameters:
>`table_players:` *list*
* Contains all players to be accounted for in the table aggregate matchmaking determination. All values must be integers, strings, or tuples, and of the same datatype. (e.g. [1,2,3], ['Ted','Joe','Emma']).

>`matchups_df`: *DataFrame*
* Must contain all players in `table_players` as labels in both the rows and columns. Should contain matchmaking ratings for each player-player pairing in a square matrix that is symmetric across the diagonal. These rating may be calculated using any method, but should result in the players best matched to each other having the lowest values.

##### Returns:
>datatype: *int*
* Sum aggregate of all matchmaking ratings for each player at the table with each other player as their opponent.

### `swap_two(entrylist)`
Returns **`entrylist`** with two random elements swapped.

##### Parameters:
>`entrylist`: *list*
* Contains all elements to be considered for swapping.

##### Returns:
>datatype: *list*
* Contains all original elements of `entrylist`, but with two randomly selected elements having exchanged indices.
