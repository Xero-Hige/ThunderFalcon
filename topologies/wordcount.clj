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
    {"tokenizer-bolt" (python-bolt-spec
          options
          {"tweets-spout" :shuffle}
          "bolts.tokenizer.Tokenizer"
          ["words"]
          :p 2
          )

    "logger-bolt" (python-bolt-spec
          options
          {"tokenizer-bolt" :shuffle}
          "bolts.logger.Logger"
          [ ]
          :p 2
          )
    }
  ]
)
