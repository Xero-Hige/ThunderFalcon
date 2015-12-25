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

    "htmlGenerator-bolt" (python-bolt-spec
          options
          {"splitter-bolt" :shuffle}
          "bolts.HTMLgenerator.Generator"
          ["HTMLtweet"]
          :p 2
          )

    "htmlLogger-bolt" (python-bolt-spec
          options
          {"htmlGenerator-bolt" :shuffle}
          "bolts.HTMLlogger.Logger"
          [ ]
          :p 1
          )
    }
  ]
)
