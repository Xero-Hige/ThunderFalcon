(ns wordcount
  (:use     [streamparse.specs])
  (:gen-class))

(defn project [options]
   [
    ;; spout configuration
    {"tweets-spout" (python-spout-spec
          options
          "spouts.tweetsFetcher.TweetSpout"
          ["tweet"]
          )
    }
    ;; bolt configuration
    {"filter-bolt" (python-bolt-spec
          options
          {"tweets-spout" :shuffle}
          "bolts.tweetFilter.Filter"
          ["tweetDict"]
          :p 3
          )

    "splitter-bolt" (python-bolt-spec
          options
          {"filter-bolt" :shuffle}
          "bolts.splitter.Splitter"
          ["tweetValuesDict"]
          :p 2
          )

    "jsonGenerator-bolt" (python-bolt-spec
          options
          {"splitter-bolt" :shuffle}
          "bolts.geoJsonGenerator.Generator"
          ["geoJsontweet"]
          :p 2
          )

    "jsonLogger-bolt" (python-bolt-spec
          options
          {"jsonGenerator-bolt" :shuffle}
          "bolts.geoJsonLogger.Logger"
          [ ]
          :p 1
          )
    }
  ]
)
