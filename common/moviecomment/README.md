# Movie comments API

This little FastAPI app exposes one endpoint on port 8000, `/latest-comments?n=n` where `n` is an integer for the number of comments, defaulting to 10, maxed at 50.

It grabs random comments and sentiments from the [large movie review dataset](http://ai.stanford.edu/~amaas/data/sentiment/) and random movie IDs from an extracted list of IDs from [the movies dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?select=movies_metadata.csv), mixes both and returns the following payload (below an example)

```
curl http://127.0.0.1:8000/latest-comments?n=2 | jq
```

```[javascript]
{
  "comments": [
    {
      "movie_id": 20357,
      "comment": "\"Don't waste your time and money on it. It's not quite as bad as \"\"Adrenalin\"\", by the same director but that's not saying much.\",",
      "rating": 4
    },
    {
      "movie_id": 176068,
      "comment": "\"As a Bruce Campbell fan for nearly two decades, I was thrilled to have an opportunity to see his latest film on the big screen with the man himself in attendance. Unfortunately, \"\"Man with the Screaming Brain\"\" was itself a disappointment.<br /><br />Set in Bulgaria--where the Sci-Fi Channel makes its Saturday night original films--\"\"Man with the Screaming Brain\"\" is a curious mix of '50s B-movie horror, body-switching comedy, violent revenge flick, and overdone slapstick with a touch of romantic reconciliation. If that doesn't make sense, well, neither does \"\"Man with the Screaming Brain.\"\" Campbell plays a pharmaceutical company CEO who visits Bulgaria with his estranged wife in an inexplicable attempt to invest in the former Communist country's half-finished subway system. The two fall in with a former KGB agent turned cab driver, and all three ultimately meet their demise at the hands of a vengeful gypsy woman.<br /><br />A local scientist (Stacy Keach) and his goofy assistant (Ted Raimi), who have developed a technique to allow tissue transplants without the possibility of rejection, steal the bodies and place a portion of the cab driver's brain into Campbell's damaged skull. Also, they put his wife's brain into a robotic body they just happen to have at hand.<br /><br />Campbell escapes, and with a hastily-restitched skull and the voice of the cab driver--whose transplanted brain tissue controls the left side of his body--echoing in his head, sets off to find and kill the gypsy. (His robot wife does the same.) <br /><br />But first, there's an attempt to emulate Steve Martin/Lily Tomlin's \"\"All of Me\"\" when Campbell's two personalities battle for dominance over a restaurant dinner. Just as he was playing his own evil hand in \"\"Evil Dead II,\"\" Campbell is adept at making his body appear to be inhabited by more than one mind.<br /><br />At times, \"\"Screaming\"\" comes closest to another Steve Martin film, \"\"The Man with Two Brains,\"\" as it also takes a silly approach to '50s sci-fi clichés. However, it tries too hard for too little result, and that goes double for Ted Raimi's semi-comprehensible Bulgarian oaf, who gets entirely too much screen time. (Nothing against Raimi, it's just that he's better in smaller doses.) <br /><br />In the end, it's neither outrageous (or funny) enough to satisfy as a spoof, nor is it serious enough to enjoy as a B-movie pastiche. I was glad that Campbell had already left the screening by the time it ground to a halt, as I feared having to say, \"\"Gee, Bruce, that was really...something.\"\"<br /><br />Perhaps the best praise I can give it as a film is that at least the images stuck to the emulsion. And it was twice as good as \"\"Alien Apocalypse.\"\"\",",
      "rating": 3
    }
  ]
}
```

## Usage

### Within Docker

- Run `make build` to build the Docker image.
- `docker run --rm -p 8000:8000 lewagon/moviecomment:0.1.0` to run it locally
- `curl http://localhost:8000/latest-comments?n=34` to fetch 34 random comments.

### Locally

- `poetry install`
- Create a data directory `DATASETS_DIR` and download the files [movies](https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/movies/csvs/movie_ids.csv.gz) and [comments](https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/movies/csvs/imdb_comments_dataset.csv.gz)
- Export the environment variable `DATASETS_DIR=<set the value for DATASETS_DIR where you put the files>`
- `poetry run uvicorn moviecomment.api:app`

## Credits

- [The movies dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?select=movies_metadata.csv), license CCO Public domain.
- The [large movie review dataset](http://ai.stanford.edu/~amaas/data/sentiment/). Mandatory citation below:

```
@InProceedings{maas-EtAl:2011:ACL-HLT2011,
  author    = {Maas, Andrew L.  and  Daly, Raymond E.  and  Pham, Peter T.  and  Huang, Dan  and  Ng, Andrew Y.  and  Potts, Christopher},
  title     = {Learning Word Vectors for Sentiment Analysis},
  booktitle = {Proceedings of the 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies},
  month     = {June},
  year      = {2011},
  address   = {Portland, Oregon, USA},
  publisher = {Association for Computational Linguistics},
  pages     = {142--150},
  url       = {http://www.aclweb.org/anthology/P11-1015}
}
```
