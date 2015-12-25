(ns wordcount
  (:use     [streamparse.specs])
  (:gen-class))

(defn wordcount [options]
   [
    ;; spout configuration
    {"tweets-spout" (python-spout-spec
          options
          "spouts.tweetsReader.TweetSpout"
          ["tweet"]
          )
    }
    ;; bolt configuration
    {"decrypter-bolt" (python-bolt-spec
          options
          {"tweets-spout" :shuffle}
          "bolts.jsonDecrypter.JsonDecrypter"
          ["tweetDict"]
          :p 3
          )

    "splitter-bolt" (python-bolt-spec
          options
          {"decrypter-bolt" :shuffle}
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
