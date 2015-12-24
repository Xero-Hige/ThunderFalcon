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
          :p 2
          )

    "logger-bolt" (python-bolt-spec
          options
          {"decrypter-bolt" :shuffle}
          "bolts.logger.Logger"
          [ ]
          :p 2
          )
    }
  ]
)
