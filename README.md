# Scraping for Insurance Corpus v2

## Installation 
Use a [pipenv](https://pipenv.pypa.io/en/latest/) for quick install of requirements enumerated in the Pipfile. 

## Usage
We used this insurance corpus to train several embedding models using [Flair](https://github.com/flairNLP/flair). 
<ul>
<li> Fine-tuning BERT, Stacked and Flair Embedding
<li> Training these same embeddings from scratch
<li> Make a custom STT model using Azure API
</ul>

## Description of the resulting corpus 

### Wikipedia source
We used Wikipedia hands-on API for retrieving text files of a given subject. We limited our keyword based research in Wikipedia's article titles. We also scrapped all the articles contained in categories named after each keyword.

### Twitter Source 
We used a list of starting user accounts, a few main french insurance companies. For each of these companies, we search for tweets containing a list of keywords and stored mentions (users direclty cited in a tweet by a '@'). For each verified mentioned accounts, we operated the same research. 

### Specialized and generalized newspapers


#### <b> Description by source </b>
| Newspaper                 | Keyword research | Restricted to title | Best matches | Premium option | 
|---------------------------|:----------------:|:-------------------:|:------------:|:--------------:|
| Assurland                 |                  |                     |              |                |
| FFA                       |:heavy_check_mark:|                     |:heavy_check_mark:|                |
| L'Agefi                   |:heavy_check_mark:|                     |              |                |
| L'Obs                     |:heavy_check_mark:|                     |              |                |
| L'opinion                 |:heavy_check_mark:|                     |:heavy_check_mark:|                |
| Le Figaro                 |:heavy_check_mark:|                     |:heavy_check_mark:|:heavy_check_mark:| 
| Le Monde                  |:heavy_check_mark:|                     |              |:heavy_check_mark:| 
| Marianne                  |:heavy_check_mark:|                     |              |                |
| Ouest France              |:heavy_check_mark:|                     |              |:heavy_check_mark:| 
| Risques                   |:heavy_check_mark:|                     |              |                |
| Tribune de l'Assurance    |:heavy_check_mark:|                     |              |:heavy_check_mark:| 
| Université de l'Assurance |:heavy_check_mark:|                     |              |                |

#### <b>Dataset structure</b>

| Newspaper                 | Number of scrapped articles | Average sequence length | Maximum sequence length | Minimum sequence length | 
|---------------------------|:---------------------------:|:-----------------------:|:-----------------------:|:-----------------------:|
| Assurland                 |                             |                         |                         |                         |
| FFA                       |                             |                         |                         |                         |
| L'Agefi                   | 181                         | 497                     | 1413                    | 50                      |
| L'Obs                     | 522                         | 442                     | 17451                   | 2                       |
| L'opinion                 | 636                         | 452                     | 2440                    | 10                      |
| Le Figaro                 | 1698                        | 391                     | 1009                    | 3                       |
| Le Monde                  | 828                         | 347                     | 3038                    | 3                       |
| Marianne                  | 56                          | 668                     | 13494                   | 23                      |
| Ouest France              | 561                         | 250                     | 2170                    | 8                       |
| Risques                   | 252                         | 474                     | 5519                    | 2                       |
| Tribune de l'Assurance    | 5                           | 431                     | 1455                    | 70                      |
| Université de l'Assurance | 42                          | 331                     | 1475                    | 5                       |


<br>
</br>

#### <b>Topics by newspaper</b>


| Newspaper                 | <font size="1"> assurance </font> | <font size="1">assureur</font> | <font size="1">réassurance</font> | <font size="1">réassureur</font> | <font size="1">mutuelle</font> | <font size="1">mutualité</font> | <font size="1">prévoyance</font> | <font size="1">actuariat</font> | <font size="1">actuaire</font> | <font size="1">axa</font> |
|---------------------------|:---------:|:--------:|:-----------:|:----------:|:--------:|:---------:|:----------:|:---------:|:--------:|:---:|
| FFA                       |           |          |             |            |          |           |            |           |          |     |
| L'Agefi                   | 144       | 94       | 52          | 170        | 99       | 57        | 157        | 4         | 15       | 42  |
| L'Obs                     | 3522      | 424      | 0           | 28         | 1193     | 170       | 0          | 0         | 55       | 181 |
| L'opinion                 | 1222      | 1208     | 1097        | 140        | 1253     | 809       | 992        | 91        | 241      | 211 |
| Le Figaro                 | 259       | 52       | 76          | 38         | 58       | 101       | 0          | 32        | 115      | 16  |
| Le Monde                  | 6360      | 0        | 0           | 0          | 778      | 0         | 0          | 0         | 1255     | 1006|
| Marianne                  | 235       | 24       | 0           | 0          | 66       | 19        | 11         | 0         | 0        | 0   |
| Ouest France              | 726       | 0        | 0           | 0          | 0        | 0         | 0          | 0         | 0        | 0   |
| Risques                   | 3239      | 80       | 0           | 0          | 7        | 0         | 0          | 0         | 0        | 2   |
| Tribune de l'Assurance    | 43        | 0        | 0           | 0          | 0        | 0         | 8          | 0         | 0        | 0   |
| Université de l'Assurance | 249       | 6        | 0           | 0          | 0        | 0         | 8          | 0         | 0        | 0   |

